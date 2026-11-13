# Literature review

The protocol and the PRISMA note are the formal Week 1 deliverables. The pilot analysis explains the recorded search and why certain queries are retained. No studies have been formally included yet.

- `search_queries.csv`: exact query versions and decisions; OpenAlex date filter is also set in the search script.
- `pilot_run_local/`: original run logs, raw API responses, raw and deduplicated metadata, and SHA-256 hashes (unchanged).
- `query_analysis.csv` and `record_title_coding.csv`: exploratory AI-assisted title coding and counts; not human screening decisions.
- `possible_duplicate_versions.csv`: similar-title groups requiring manual checking.
- `candidate_references.csv`, `references.bib`, `technical_evidence_matrix.csv`: preliminary literature leads, not final inclusions or validated gold evidence.
- `selection.csv`, `medical_extraction.csv`, `technical_extraction.csv`: templates for the formal review.

The medical review follows a PCC scoping approach. The technical search is targeted rather than exhaustive. See `review_protocol.pdf` and `pilot_search_analysis.pdf` for the details.
