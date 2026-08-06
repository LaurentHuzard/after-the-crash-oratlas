# Scope, vocabulary, and the anti-purée rule

The central methodological hazard is **evidence blending**. “Amphetamine-type stimulants” can
mean illicit amphetamine, dexamphetamine, mixed amphetamine salts, lisdexamfetamine,
methamphetamine, MDMA, or synthetic cathinones depending on the paper and indexing system.
A title containing *amphetamine* may describe a methamphetamine-only cohort. A treatment trial
may measure weeks of use reduction rather than withdrawal. A review may import cocaine data
because it is more abundant.

(claim-c01)=
## C01 · Substance identity must travel with every claim

**Claim.** The umbrella label “amphetamine-type stimulants” combines pharmacologically and
clinically distinct exposures, so evidence claims should be tagged by the substance actually
studied rather than silently generalized across the class.

| Label | Meaning | Permitted use |
|---|---|---|
| `AMPH-direct` | Human non-methamphetamine amphetamine exposure | Primary evidence for amphetamine claims |
| `METH-direct` | Human methamphetamine exposure | Primary evidence for methamphetamine claims; indirect for amphetamine |
| `ATS-pooled` | Amphetamine and methamphetamine pooled or not separable | Class-level evidence with explicit heterogeneity warning |
| `COC-context` | Cocaine evidence | Context only, never silently pooled |
| `GUIDELINE` | Clinical guideline or consensus synthesis | Practice framing with inherited evidence limits |
| `PRECLINICAL` | Animal or mechanistic evidence | Hypothesis generation only |

Major reviews and guidelines use different scopes [@asam2024; @li2023; @shoptaw2009;
@khalili2025; @sharafi2024; @sinclair2026]. The practical rule is simple: the evidence tag
remains attached to the claim all the way through the graph.

(claim-c02)=
## C02 · The trajectory literature is lopsided, but not empty

**Claim.** Within this pilot corpus, human withdrawal-trajectory evidence is dominated by
methamphetamine and mixed-stimulant samples, while direct contemporary evidence for
non-methamphetamine amphetamine withdrawal is sparse and much of the direct literature is
historical, small, or sleep-focused.

The clearest modern repeated-measure trajectory studies located here enrolled
methamphetamine-dependent participants [@mcgregor2005; @zorick2010]. The modern clinical review
is also organized mainly around methamphetamine and cocaine [@li2023]. Yet direct amphetamine
evidence does exist:

- a six-person 1963 physiological study reported prolonged REM-related abnormalities
  [@oswald1963];
- a 1972 study linked withdrawal depression, sleep changes, and MHPG excretion [@watson1972];
- a 1982 hospital study found oversleeping followed by reduced and disturbed sleep through
  day 20 [@gossop1982];
- a 1998 retrospective pilot found that 86% of 50 amphetamine-dependent clients described
  significant withdrawal symptoms [@cantwell1998];
- 1999 studies developed the Amphetamine Withdrawal Questionnaire and tested amineptine
  [@srisurapanont1999a; @srisurapanont1999b].

These studies matter precisely because they prevent “non-meth evidence” from being declared
nonexistent. They do not replace a modern, adequately powered, prospective amphetamine cohort.

## Population and exposure boundaries

The primary population is adults who stop or substantially reduce sustained non-medical use
of amphetamine or methamphetamine. Therapeutic prescription discontinuation is a separate
exposure pathway and should not be merged without dedicated analysis. MDMA and synthetic
cathinones are outside the primary synthesis. Cocaine is contextual because its evidence is
often imported into stimulant-withdrawal guidance.

## Recovery phases used in this pilot

| Phase | Operational window | Interpretation |
|---|---:|---|
| Acute | days 0–7 | Early crash and highest short-term safety burden |
| Extended acute | days 8–14 | Rapid change may continue; attribution remains unstable |
| Early post-acute | weeks 3–4 | Symptoms may persist after the initial crash |
| Late post-acute | weeks 5–12 | Craving, sleep, mood, and functioning become central |
| Longer recovery | months 3–12 | Relapse, quality of life, cognition, relationships, and work should be measured |

These are analytic bins, not biological laws. Study-specific time points remain visible.
