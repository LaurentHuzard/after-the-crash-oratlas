#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []

RELATION_TYPES = {
    "supports", "partially-supports", "contradicts", "contextualizes",
    "method-source", "background", "unclear",
}
DIRECTIONS = {"positive", "negative", "mixed", "neutral"}
CLAIM_TYPES = {"empirical", "mechanistic", "methodological", "theoretical", "normative", "summary", "other"}
TRUST_RATINGS = {"very-low", "low", "moderate", "high", "very-high", "not-assessed", "not-applicable"}
TRUST_STATUSES = {"assessed", "not-assessed", "not-applicable"}
TRUST_CRITERIA = {
    "identityIntegrity", "entailment", "sourceAccess", "populationRelevance",
    "interventionExposureRelevance", "outcomeRelevance", "methodologicalSafeguards",
    "statisticalSafeguards", "replicationConvergence", "conflictDependency",
}
SAFE_PATH = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*(/[A-Za-z0-9][A-Za-z0-9._-]*)*$")
DOI = re.compile(r"^10\.\d{4,9}/\S+$")
PMID = re.compile(r"^\d{1,9}$")

def fail(message: str) -> None:
    ERRORS.append(message)

def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
        return {}

def load_jsonl(path: Path) -> list[dict]:
    rows = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception as exc:
        fail(f"{path.relative_to(ROOT)}: cannot read: {exc}")
        return rows
    for number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except Exception as exc:
            fail(f"{path.relative_to(ROOT)}:{number}: invalid JSON: {exc}")
            continue
        if not isinstance(value, dict):
            fail(f"{path.relative_to(ROOT)}:{number}: record must be an object")
            continue
        rows.append(value)
    return rows

manifest = load_json(ROOT / "review-manifest.json")
if manifest.get("schemaVersion") != "1.0.0":
    fail("review-manifest.json: schemaVersion must be 1.0.0")
if manifest.get("review", {}).get("reviewType") != "computational-literature-review":
    fail("review-manifest.json: unexpected reviewType")
artifacts = manifest.get("artifacts", {})
for key in ("claims", "citations", "relations", "trustAssessments", "provenance"):
    value = artifacts.get(key)
    if not isinstance(value, str) or not SAFE_PATH.fullmatch(value):
        fail(f"review-manifest.json: unsafe or missing artifact path: {key}")
    elif not (ROOT / value).is_file():
        fail(f"review-manifest.json: missing artifact file: {value}")

claims = load_jsonl(ROOT / artifacts.get("claims", "knowledge/claims.jsonl"))
citations = load_jsonl(ROOT / artifacts.get("citations", "knowledge/citations.jsonl"))
relations = load_jsonl(ROOT / artifacts.get("relations", "knowledge/claim-evidence-relations.jsonl"))
trust = load_jsonl(ROOT / artifacts.get("trustAssessments", "knowledge/trust-assessments.jsonl"))

def unique_ids(rows: list[dict], label: str) -> set[str]:
    ids = [row.get("id") for row in rows]
    for index, value in enumerate(ids, 1):
        if not isinstance(value, str) or not value:
            fail(f"{label}:{index}: missing id")
    duplicates = [value for value, count in Counter(ids).items() if value and count > 1]
    for value in duplicates:
        fail(f"{label}: duplicate id {value}")
    return {value for value in ids if isinstance(value, str) and value}

claim_ids = unique_ids(claims, "claims")
citation_ids = unique_ids(citations, "citations")

for row in claims:
    if row.get("claimType") not in CLAIM_TYPES:
        fail(f"claim {row.get('id')}: invalid claimType")
    if not row.get("text") or not row.get("anchor"):
        fail(f"claim {row.get('id')}: text and anchor are required")

for row in citations:
    if "doi" in row and not DOI.fullmatch(str(row["doi"])):
        fail(f"citation {row.get('id')}: invalid DOI")
    if "pmid" in row and not PMID.fullmatch(str(row["pmid"])):
        fail(f"citation {row.get('id')}: invalid PMID")
    if not row.get("title"):
        fail(f"citation {row.get('id')}: title is required")

pairs = []
for row in relations:
    pair = (row.get("claimId"), row.get("citationId"))
    pairs.append(pair)
    if pair[0] not in claim_ids:
        fail(f"relation {pair}: unknown claim")
    if pair[1] not in citation_ids:
        fail(f"relation {pair}: unknown citation")
    if row.get("relationType") not in RELATION_TYPES:
        fail(f"relation {pair}: invalid relationType")
    if row.get("supportDirection") not in DIRECTIONS:
        fail(f"relation {pair}: invalid supportDirection")
    if row.get("humanReviewed") is not False:
        fail(f"relation {pair}: pilot relations must be humanReviewed=false")

for pair, count in Counter(pairs).items():
    if count > 1:
        fail(f"duplicate relation pair {pair}")

trust_pairs = []
for row in trust:
    pair = (row.get("claimId"), row.get("citationId"))
    trust_pairs.append(pair)
    if pair not in set(pairs):
        fail(f"TRUST {pair}: no matching relation")
    if row.get("assessorType") != "agent":
        fail(f"TRUST {pair}: assessorType must be agent")
    if row.get("reviewStatus") != "agent-proposed":
        fail(f"TRUST {pair}: reviewStatus must be agent-proposed")
    if row.get("aggregateScore", "missing") is not None:
        fail(f"TRUST {pair}: aggregateScore must be null")
    criteria = row.get("criteria", {})
    if set(criteria) != TRUST_CRITERIA:
        fail(f"TRUST {pair}: criterion keys do not match contract")
    for name, assessment in criteria.items():
        if assessment.get("rating") not in TRUST_RATINGS:
            fail(f"TRUST {pair}/{name}: invalid rating")
        if assessment.get("status") not in TRUST_STATUSES:
            fail(f"TRUST {pair}/{name}: invalid status")

if Counter(pairs) != Counter(trust_pairs):
    fail("Relation/TRUST coverage is not exactly one-to-one")

# MyST anchors and duplicates.
labels: dict[str, str] = {}
for path in sorted((ROOT / "content").glob("*.md")):
    text = path.read_text(encoding="utf-8")
    for match in re.finditer(r"^\(([^)]+)\)=$", text, flags=re.MULTILINE):
        label = match.group(1)
        if label in labels:
            fail(f"duplicate MyST label {label}: {labels[label]} and {path.relative_to(ROOT)}")
        labels[label] = str(path.relative_to(ROOT))

for row in claims:
    anchor = row["anchor"]
    if anchor not in labels:
        fail(f"claim {row['id']}: missing MyST anchor {anchor}")

# Citation keys used in prose and bibliography.
all_markdown = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "content").glob("*.md"))
used_keys = set(re.findall(r"@([A-Za-z0-9_.:-]+)", all_markdown))
bib_text = (ROOT / "content/references.bib").read_text(encoding="utf-8")
bib_keys = set(re.findall(r"@\w+\{([^,]+),", bib_text))
missing_bib = used_keys - bib_keys
unknown_citations = used_keys - citation_ids
unreferenced_citations = citation_ids - bib_keys
if missing_bib:
    fail(f"citation keys used but absent from BibTeX: {sorted(missing_bib)}")
if unknown_citations:
    fail(f"citation keys used but absent from citations.jsonl: {sorted(unknown_citations)}")
if unreferenced_citations:
    fail(f"structured citations absent from BibTeX: {sorted(unreferenced_citations)}")

# Evidence CSV.
with (ROOT / "evidence/evidence-table.csv").open(encoding="utf-8", newline="") as handle:
    csv_rows = list(csv.DictReader(handle))
if len(csv_rows) != len(citations):
    fail(f"evidence CSV has {len(csv_rows)} rows; expected {len(citations)}")
if {row.get("id") for row in csv_rows} != citation_ids:
    fail("evidence CSV IDs do not match structured citation IDs")

# Provenance counts.
provenance = load_json(ROOT / "provenance.json")
expected_counts = {
    "claims": len(claims),
    "citations": len(citations),
    "relations": len(relations),
    "trustAssessments": len(trust),
}
for key, expected in expected_counts.items():
    actual = provenance.get("artifacts", {}).get(key, {}).get("count")
    if actual != expected:
        fail(f"provenance count {key}={actual}; expected {expected}")

# Internal Markdown links. Ignore generated files, VCS metadata, and installed dependencies.
IGNORED_MARKDOWN_DIRS = {".git", ".myst", "_build", "node_modules"}
for path in ROOT.rglob("*.md"):
    relative_parts = path.relative_to(ROOT).parts
    if any(part in IGNORED_MARKDOWN_DIRS for part in relative_parts):
        continue
    text = path.read_text(encoding="utf-8")
    for target in re.findall(r"\]\((?!https?://|mailto:|#)([^)#]+)(?:#[^)]+)?\)", text):
        resolved = (path.parent / target).resolve()
        try:
            resolved.relative_to(ROOT.resolve())
        except ValueError:
            fail(f"{path.relative_to(ROOT)}: link escapes repository: {target}")
            continue
        if not resolved.exists():
            fail(f"{path.relative_to(ROOT)}: broken internal link: {target}")

# Minimal MyST config check without external dependencies.
myst = (ROOT / "myst.yml").read_text(encoding="utf-8")
for required in ("version: 1", "project:", "bibliography:", "toc:", "site:"):
    if required not in myst:
        fail(f"myst.yml: missing {required}")
if "\t" in myst:
    fail("myst.yml: tabs are not permitted")

print(f"Claims: {len(claims)}")
print(f"Citations: {len(citations)}")
print(f"Relations: {len(relations)}")
print(f"TRUST assessments: {len(trust)}")
print(f"BibTeX keys used: {len(used_keys)}")
print(f"Disagreement edges: {sum(1 for row in relations if row['relationType'] == 'contradicts')}")

if ERRORS:
    print("\nVALIDATION FAILED", file=sys.stderr)
    for error in ERRORS:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("VALIDATION PASSED")
