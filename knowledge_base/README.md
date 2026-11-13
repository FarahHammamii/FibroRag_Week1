# knowledge_base/ — plan (nothing ingested yet)

**Week 1 status:** 9 candidate clinical references (C01–C09). No corpus has been built yet; this starts after formal selection.

**Rules for the corpus**

- One manifest line per source: URL, DOI/PMID, title, version, date collected, licence, SHA-256 hash, type, jurisdiction, population, quality, access.
- Metadata and content are stored separately.
- Paywalled or incompatible licences: link only, no copy (for example ACOG). No way around a paywall.
- PMC: check the licence article by article. "Free to read" is not the same as "free to reuse".
- Store only allowed raw text, split into passages with offsets. Raw full texts with unclear rights are git-ignored (`knowledge_base/raw/`).
- Log corrections, retractions and updates.
- No individual patient data. Tunisian group-level studies give context; they do not define a local policy.
- To build: a FR/EN glossary (FIGO terms, outcomes, units, controlled synonyms).
