# Experimental plan v0.1 (to be frozen before any test)

## Questions and hypotheses

**Review question (PCC):** What evidence and conditions of applicability are reported for uterine fibroids in guidelines and research syntheses, including the Tunisian context, that can support an auditable academic question-answering corpus? The RAG methods are investigated in a separate targeted technical search. See [review protocol](../review/review_protocol.pdf).

**Experimental question:** with the same model, corpus and context budget, what is the added effect of (a) re-ranking by quality/applicability and (b) claim checking with abstention on the reliability of answers to FibroidQA questions, at comparable coverage?

- **H1:** M2 > M1 on Recall@5 of relevant *and* applicable passages.
- **H2:** M3 < M2 on the rate of unsupported claims, at comparable coverage.
- **H3:** M3 separates answerable from unanswerable questions better, without a collapse of coverage on answerable ones.
- **H0:** no difference. Negative effects are possible and will be reported.

## Systems compared

| System | What it is |
|---|---|
| **M0** | LLM alone, same safety prompt, no corpus. Its claims are checked against external gold, not penalised on citations. |
| **M1** | Standard hybrid RAG: BM25 + multilingual embeddings, RRF fusion, structured answer with citations. |
| **M2** | M1 + re-ranking by quality/applicability metadata, same number of passages and budget. |
| **M3** | M2 + claim checking + selective gate (answer / qualify / abstain). |

**Ablations (if time allows):** M1 + gate alone; M2 + checking without gate; BM25 vs dense vs hybrid for retrieval only; a simple refusal rule based on the retrieval score.

**Kept fixed:** corpus and hashes, prompt (except the module tested), model and version, chunking (proposed 350 tokens, overlap 50), k = 5, context budget about 1,750 tokens, temperature, seed if available, max output length, hardware. All tuning on the dev set only, and logged. I also measure latency (p50, p95), API cost if any, and RAM. No GPU purchase and no fine-tuning.

## FibroidQA (a project benchmark, not a validated one)

- **Target:** 80 items (20 dev, 60 test); reduce to 60 if needed and say so.
- **Categories:** classification/imaging, treatment, fertility, context and disagreements, unanswerable or unsafe questions.
- **Each item has:** family ID, language, question, synthetic context, category, expected decision (ANSWER / QUALIFY / ABSTAIN), essential elements, gold claims, IDs and offsets of supporting spans, source version, reason, safety flags.
- Paraphrases of the same question stay in the same split. French first; 10 FR/EN pairs optional.
- Gold answers are written **before** running any system, from the source passages, following a codebook.
- **Without a medical expert**, I report "faithfulness to the documents", not clinical accuracy. If an expert is available, they review 20 hard cases chosen in advance.
- AI may suggest questions but never writes or judges them alone. I annotate the answers blind (shuffled, system names hidden) and watch for length bias.
- I re-code 15% of items later (intra-rater agreement). With a second person: raw agreement + Cohen's kappa.

## Measures

- **Retrieval:** Recall@k = gold passages found in top-k / all gold passages; MRR; nDCG@5 if graded relevance is set in advance.
- **Citations:** precision = claim–passage links that truly support / all links; recall = claims needing support that have a good citation / claims needing support.
- **Claims:** support rate = supported claims / verifiable claims; unsupported rate = (neutral + contradicted + uncited) / verifiable claims. Empty answers are not "perfect": they are penalised through coverage.
- **Answer level:** correct = all essential elements right and no major false claim; completeness = gold elements covered / required.
- **Decisions:** 3×3 confusion matrix (ANSWER / QUALIFY / ABSTAIN), macro F1, abstention precision and recall.
- **Risk and coverage:** coverage = questions with a real answer / all; risk = real answers with at least one major unsupported or contradicted claim. Risk–coverage curves, AURC, risk at a common coverage (50% / 75% if reached).
- **"Major" error** = could change the understanding of a diagnosis, intervention, risk or outcome. Defined before testing.
- **Statistics:** paired bootstrap at question level (by family if paraphrases), 2,000 resamples, fixed seed; exact McNemar for binary results if the sample allows. Effect sizes and intervals first, not many p-values. Small sample, so results are exploratory.

## Gate and error analysis

- **Gate score:** share of essential claims verified, plus blocking rules (a major claim unsupported, missing context, out-of-scope question).
- **Threshold τ** chosen on dev among {0.5, 0.7, 0.9, 1.0}: highest coverage with risk ≤ 10% if reachable; otherwise I report the frontier. Frozen before the test set.
- **QUALIFY** when some parts are verified and limits can be stated; else **ABSTAIN**. Real conflicts are reported with both sources, not hidden.
- **Error types to log:** false support, retrieval miss, outdated source, wrong population, wrong outcome, false refusal, translation error, prompt injection from a document, invented reference. Evidence-order test (candidate technical reference T15; see review/candidate_references.csv).

## Rough schedule (my own plan, not the official briefs)

S2 freeze criteria and screen · S3 corpus, passages and dev questions · S4 baselines M0/M1 · S5 re-ranking M2 · S6 checking and gate M3 · S7 frozen test and analysis · S8 report and reproducibility. If time is short, I cut items or drop the cross-encoder, not the annotation.
