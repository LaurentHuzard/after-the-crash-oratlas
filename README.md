# After the Crash

**Acute and Protracted Withdrawal Across Amphetamine-Type Stimulants Beyond Methamphetamine**

This repository is a **substance-specific pilot evidence map** built for submission to
[Open Review Atlas](https://oratlas-ftpoygqvua-ew.a.run.app/). It asks a deceptively simple
question: what do we actually know about withdrawal and recovery after sustained amphetamine
use when all stimulant evidence is no longer treated as interchangeable?

## What is inside

- 12 qualified, anchorable claims
- 22 structured citations
- 77 claim–citation relations, including two preserved disagreement edges
- 77 agent-proposed TRUST records, one for every relation
- a MyST article with protocol, search strategy, evidence map, and provenance
- a CSV evidence inventory
- deterministic local validation and a GitHub Pages workflow

The central design rule is strict substance tagging:

1. direct non-methamphetamine amphetamine evidence;
2. direct methamphetamine evidence;
3. pooled amphetamine-type stimulant evidence;
4. cocaine or other-stimulant context;
5. guideline or mechanistic evidence.

## What the pilot already reveals

Direct non-methamphetamine amphetamine evidence exists, but much of the trajectory literature
located in this pilot is historical, small, or concentrated on sleep physiology. The more
contemporary longitudinal literature is largely methamphetamine-specific. The graph therefore
records directness explicitly rather than allowing a methamphetamine result to quietly become
an “amphetamine” fact.

## Current status

`v0.1.0` is an **AI-assisted pilot awaiting human scientific review**. It is intentionally
useful enough to test ORAtlas claim passports, evidence traversal, and disagreement maps, but
it is not a completed systematic review. Every TRUST assessment is marked `agent-proposed`
and every relation is marked `humanReviewed: false`.

## Safety and interpretation

This is a research artifact, not medical advice, diagnosis, or an individualized treatment
plan. Stimulant withdrawal can involve severe depression, suicidality, psychosis, agitation,
or medical complications. Urgent or dangerous symptoms require professional assessment.

## Validate locally

```bash
python3 scripts/validate_repository.py
```

The validator checks the manifest, JSONL syntax and controlled values, referential integrity,
claim anchors, citation keys, CSV counts, one-to-one relation/TRUST coverage, duplicate MyST
labels, and internal repository links.

## Build the MyST site

```bash
npm install -g mystmd
myst build --html
```

## Publish and prepare the ORAtlas submission

```bash
bash scripts/publish_github.sh
```

The script validates the repository, initializes Git if needed, connects the existing public
GitHub repository, pushes `main`, and publishes release `v0.1.0`. See
[`ORATLAS_SUBMISSION.md`](ORATLAS_SUBMISSION.md) for the final browser steps.

## License

Review text and structured evidence are licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Source publications retain their
own copyrights and licenses.
