# Methods

## Design

This is a targeted rapid evidence map designed to exercise ORAtlas's claim-first ingestion,
relation graph, disagreement map, and TRUST display. It is **not** a completed systematic
review or meta-analysis.

- Search cutoff: **6 August 2026**
- Primary domain: human amphetamine and methamphetamine withdrawal
- Secondary domain: treatment evidence where outcome distinctions are informative
- Languages screened: English
- Sources: PubMed, PubMed Central, Cochrane, guideline publications, publisher pages, and
  backward citation chasing
- Human duplicate screening: not performed
- Full-text verification: not available for every paywalled source

## Eligibility logic

Included records had to contribute to at least one of:

1. substance definitions and directness;
2. acute or post-acute symptom trajectory;
3. withdrawal measurement;
4. withdrawal-specific treatment;
5. stimulant-use-disorder treatment where outcome separation mattered;
6. psychiatric overlap or functional recovery gaps.

Preclinical studies, MDMA-only studies, and synthetic-cathinone-only studies were not included
in this pilot. Cocaine evidence was retained only as explicit context.

## Substance tags

Every source received one of the declared evidence tags in [Scope and vocabulary](01_scope.md).
A methamphetamine-only source was never counted as direct non-methamphetamine amphetamine
evidence. Historical direct amphetamine studies remained visible even when their methods were
weak by contemporary standards.

## Claim construction

Claims were drafted to be:

- anchorable and independently inspectable;
- qualified enough to preserve source limits;
- falsifiable or revisable;
- explicit about population, exposure, outcome, and method;
- free of individualized treatment recommendations.

## Relation semantics

- `supports`: the source directly supports the qualified claim;
- `partially-supports`: the source supports only part of the claim or a narrower scope;
- `contradicts`: the source provides a materially opposing result;
- `contextualizes`: the source defines scope, uncertainty, or a neighboring outcome;
- `method-source`: the source supplies an instrument or method.

Two disagreement edges are intentionally preserved:

1. Gossop 1982 challenges a simple first-week recovery clock for sleep.
2. Srisurapanont 1999 reports a positive amineptine signal against the broader “no established
   medication” conclusion.

Neither edge is automatically adjudicated as truth or error.

## TRUST assessment

One relation-level TRUST record was generated for each of the 77 relations.
Ratings consider identity, entailment, access, population and exposure relevance, outcome
relevance, methodological and statistical safeguards, replication convergence, and conflict
dependency. All records are:

- `assessorType: agent`
- `reviewStatus: agent-proposed`
- `humanReviewed: false`
- `aggregateScore: null`

The pilot does not convert ordinal judgments into a probability that a source or claim is true.

## Reproducibility

Machine-readable artifacts are listed in `review-manifest.json`. Run:

```bash
python3 scripts/validate_repository.py
```

The validator checks controlled values, IDs, referential integrity, relation/TRUST parity,
anchors, bibliography keys, CSV counts, and internal links.
