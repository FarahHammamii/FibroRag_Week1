"""Check the recorded pilot run and recompute the counts. No network needed.

What it checks:
1. every raw file still matches its SHA-256 hash (nothing was edited after the run)
2. deduplication of the raw records gives the same unique list
3. the queries in review/search_queries.csv are the exact ones that were run
4. the title-coding table matches the exported records one by one
5. the hit counts in the log match the raw API answers
"""
import csv, json, hashlib, pathlib, collections
from pilot import dedup

ROOT = pathlib.Path(__file__).resolve().parents[2]
RUN = ROOT / "review/pilot_run_local"


def load(name):
    return json.loads((RUN / name).read_text(encoding="utf-8"))


manifest = load("sha256.json")
for name, sha in manifest.items():
    f = RUN / name.replace("\\", "/")  # the run was made on Windows
    assert hashlib.sha256(f.read_bytes()).hexdigest() == sha, name

logs = load("log.json")
raw = load("results_raw_metadata.json")
unique = load("results_dedup.json")
assert dedup(raw) == unique

with (ROOT / "review/search_queries.csv").open(encoding="utf-8-sig") as f:
    queries = {x["id"]: x["equation"] for x in csv.DictReader(f)}
with (ROOT / "review/record_title_coding.csv").open(encoding="utf-8-sig") as f:
    coded = list(csv.DictReader(f))

assert len(raw) == len(coded)
for x, y in zip(raw, coded):
    assert (x["query_id"], x["title"], x["doi"], x["pmid"]) == (y["query_id"], y["title"], y["doi"], y["pmid"])

for entry in logs:
    k = entry["id"]
    assert queries[k] == entry["query"]
    z = load("raw/" + k + ("_count.json" if entry["base"] == "PubMed" else "_0.json"))
    if entry["base"] == "PubMed":
        count = int(z["esearchresult"]["count"])
    elif entry["base"] == "OpenAlex":
        count = int(z["meta"]["count"])
    else:
        count = int(z["hitCount"])
    classes = collections.Counter(x["ai_title_class"] for x in coded if x["query_id"] == k)
    assert count == entry["count"] and sum(classes.values()) == entry["n_export"]
    print(k, count, entry["n_export"], dict(sorted(classes.items())))

print(f"Manifest: {len(manifest)} files OK; queries: {len(logs)}; "
      f"records: {len(raw)}; unique: {len(unique)}; duplicates: {len(raw) - len(unique)}")
