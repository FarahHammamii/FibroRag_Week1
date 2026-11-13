# Bibliographic search

The pilot uses Python 3.10+ and the standard library. `pilot.py` queries PubMed, Europe PMC and OpenAlex and saves the original responses, metadata, query log and SHA-256 manifest. The original run is under `review/pilot_run_local/`.

From the repository root, verify the existing run without internet:

```bash
python code/bibliographic_search/verify_pilot.py
python -m unittest discover -s code/bibliographic_search -p "test_*.py"
```

To make a new pilot (requires internet):

```bash
python code/bibliographic_search/pilot.py --ids MED-v1 MED-v2 MED-v3 MED-v4 MED-v5 TECH-v1 TECH-v2 TECH-v3 TECH-v4 TECH-v5 TECH-v6 TECH-v7 --limit 30 --out review/pilot_run_new
```

The output directory must not exist. `CONTACT_EMAIL`, `NCBI_API_KEY` and `OPENALEX_API_KEY` can be set as environment variables when needed. Never commit API keys. Results depend on database updates and ranking. The 2026 date filters are intentional for the archived protocol. The verifier targets the archived run and its corresponding title coding, not a new run.

The query register is `review/search_queries.csv`. The old raw outputs are retained unchanged; the derived title-coding and summary CSV headers were standardized. For the title chart, install matplotlib and run:

```bash
python -m pip install matplotlib
python code/figures/title_coding_chart.py review/query_analysis.csv figures/title_coding.png
```
