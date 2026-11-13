# FIBRO-RAG — Week 1

**An evidence-aware, selective question-answering assistant on uterine fibroids.**
Individual 8-week project · Farah Hammami · Research Master in Computer Science.

**Status (13/11/2026):** protocol v1.0 written after a real pilot search. No formal review and no AI experiment yet. Research prototype — not a medical device, no clinical advice.

**Research question:** with the same model, corpus and budget, does re-ranking sources by quality/applicability, and checking each claim with the option to refuse, make answers more faithful to the sources at comparable coverage? The contribution is a reproducible adaptation, a small benchmark (FibroidQA) and ablations — not a new algorithm.

## Week 1 deliverables



## Folders

- `scoping/` — scope, use cases, the three options, decisions log.
- `review/` — protocol, pilot search data and analysis, references (see `review/README.md`).
- `code/bibliographic_search/` — search script, check script, tests.
- `knowledge_base/` — rules for the future corpus (nothing ingested yet).
- `assistant/` — planned architecture.
- `evaluation/` — experimental plan and 8 draft test scenarios.
- `figures/` — pilot flow, title sorting chart, architecture.
- `weekly_reports/`, `ai_journal/`.

## Reproduce

Python 3.10+, standard library only.

```bash
# check the saved run (no Internet needed)
python code/bibliographic_search/verify_pilot.py
python -m unittest discover -s code/bibliographic_search -p "test_*.py"

# run the searches again (Internet needed; results will change as databases are updated)
export CONTACT_EMAIL="your@email"        # optional: NCBI_API_KEY, OPENALEX_API_KEY
python code/bibliographic_search/pilot.py --ids MED-v1 MED-v2 MED-v3 MED-v4 MED-v5 \
  TECH-v1 TECH-v2 TECH-v3 TECH-v4 TECH-v5 TECH-v6 TECH-v7 --limit 30 --out review/pilot_run_reproduction
```

Never commit API keys (`.env` is git-ignored).

## Ethics and rights

Public sources and synthetic questions only. No patient data, no diagnosis, no prescription. Licences are respected; texts that cannot be redistributed are not copied. No expert validation at this stage.

Figures can be redrawn with `python code/figures/title_coding_chart.py review/query_analysis.csv figures/title_coding.png` and `dot -Tpng figures/pilot_flow.dot -o figures/pilot_flow.png` (Graphviz).
