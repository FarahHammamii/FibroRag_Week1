# assistant/ — planned architecture (not built yet)

![Planned pipeline](../figures/architecture.png)

## Offline (once)

Allowed sources → dedup by DOI/PMID → text extraction with sections → version and correction checks → passages with IDs → metadata (date, design, guideline or not, quality, population, FIGO type, outcome, jurisdiction, licence).

## At question time

1. **Scope check** — out-of-scope or personal medical questions are refused with a reason.
2. **Synonyms** — normalise FR/EN terms (no translation of units or negations).
3. **M1 — hybrid retrieval:** BM25 + dense, fused with RRF: score = Σ 1/(k0 + rank), k0 = 60 to be tested on dev. Top 20 candidates, then top 5 after re-ranking.
4. **M2 — re-ranking inside the top 20** with a fixed, simple rule: drop retracted or clearly non-applicable sources, keep a minimum relevance, prefer sources whose population/outcome match the question, then documented quality (unknown ≠ low), and break ties with the RRF rank. Tested against rank alone; prestige never replaces relevance. A cross-encoder is optional and evaluated separately.
5. **Generation** — JSON with claims, source IDs, dates and limits.
6. **M3 — checking** — IDs and spans checked by code; support judged by an NLI model or a separate judge; human audit on a sample.
7. **Gate** — ANSWER / QUALIFY / ABSTAIN with a threshold tuned on dev and safety rules. Never a diagnosis or a prescription.

## Definitions I use

- **Quality:** documented methodological confidence (design + suitable appraisal tool), not just the date.
- **Relevance:** the content matches the question.
- **Applicability:** population, context, FIGO type, intervention/outcome and jurisdiction match. "Unknown" is not the same as "not applicable".
- **Sufficiency:** the essential elements are covered by matching passages. One source can be enough for a definition, not for a comparison.
- **Unsupported claim:** a checkable statement not entailed by its cited passages, or contradicted by them — even if it is true elsewhere.
- **Good abstention:** evidence is missing for essential elements, or the question is out of scope; the answer says what is missing without inventing.
- **Contradiction:** compare under the same conditions first; then report the disagreement, never merge different outcomes.

## First version (MVP)

20–40 allowed sources (target), RRF, simple re-ranking, support checker, gate, controlled evaluation. Optional: cross-encoder, entropy, graph, more languages. A simple interface comes last.

**Safety:** text inside sources is data, never instructions; any command inside a document is ignored. No patient data collected or sent. No clinical system deployed.
