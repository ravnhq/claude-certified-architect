#!/usr/bin/env python3
"""Rebuild the CCAR-P / CCDV-F question banks, and the imported half of the
CCAR-F bank, from the collected CertSafari corpus.

Those two banks are no longer hand-written. Their items come from
.corpus/certsafari/<CODE>.json — the archive scripts/certsafari-collection.md
describes — folded into the schema the exam builders already read, so the page
generator, the validators and the quiz engine are untouched by the switch. This
script is the only writer of ccap/data/questions.json and ccdf/data/questions.json.

What it has to reconcile between the two shapes:

  * CertSafari ships every option as an "A) text" string and keys an item by
    repeating the winning option strings verbatim, so the letter lives inside
    the text. The bank keys by letter instead, so the prefix is stripped and
    letters are reassigned in the order CertSafari presented them. Preserving
    that order is deliberate: the exam engine never shuffles options, so an
    explanation that names "option C" still points at the option it meant.
  * Explanations open with a "Correct." / "Incorrect." verdict that the exam
    page already renders as colour and position, so the words are stripped.
  * A CertSafari stem is one blob; the bank splits scenario from ask because the
    page styles the two differently. See split_stem().
  * Roughly four in five multiple-response stems say "(Select all that apply.)"
    rather than naming a number, which would render under a "Select 3 responses."
    badge the stem never justifies. Those stems get the count appended and a
    `stem_note` recording that the edit was ours, not CertSafari's.
  * The bank keys every item to an official blueprint objective. CertSafari
    states one itself: each captured page snapshot carries a "Subdomain X.Y:
    <title>" label, where X is the domain and Y indexes that domain's objective
    list in objectives.json. That is the authority here — it is CertSafari's own
    classification of its own item, not a guess made downstream. The label's
    title is checked against the objective it resolves to, so a blueprint
    revision that reorders an objective list stops the import instead of
    silently relabelling several hundred items.

Hand-made tags under .corpus/certsafari/tags/ are honoured as a cross-check when
they are present: a tag that contradicts the snapshot is reported and ignored.
The import does not need them and does not wait for them.

Answers are as CertSafari marked them and have not been independently verified.

Usage: python3 utils/import_certsafari.py [ccaf|ccap|ccdf|all] [--tags-dir DIR]

Foundations differs in two ways: its objectives file is blueprint.json (the
official task statements; objectives.json there holds the score-report list the
bank browser groups by), and the output is imported_en.json, merged at load time
with the hand-authored guide and mock items rather than replacing them.
"""
from __future__ import annotations
import argparse, glob, hashlib, json, os, re, sys
from collections import Counter, defaultdict

UTILS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(UTILS_DIR)
CORPUS_DIR = os.path.join(ROOT_DIR, ".corpus", "certsafari")
TAGS_DIR = os.path.join(CORPUS_DIR, "tags")
sys.path.insert(0, UTILS_DIR)

# The exam code names the corpus file and the tag files; the id prefix and the
# validator that gates the result are per track. The validator is imported for
# its stem-count reader, so the count this script appends is read back by the
# exact function that checks it.
TRACKS = {
    "ccaf": {"code": "CCAR-F", "prefix": "f", "validator": "validate_professional_bank",
             "objectives": "blueprint.json", "out": "imported_en.json"},
    "ccap": {"code": "CCAR-P", "prefix": "p", "validator": "validate_professional_bank",
             "objectives": "objectives.json", "out": "questions.json"},
    "ccdf": {"code": "CCDV-F", "prefix": "d", "validator": "validate_developer_bank",
             "objectives": "objectives.json", "out": "questions.json"},
}

# CertSafari's own label for the item, read out of the captured page snapshot.
# It appears once per snapshot, inside the accessibility dump the collector saved.
SUBDOMAIN = re.compile(r"Subdomain\s+(\d+)\.(\d+):\s*([^\"\n]+)")

OPTION_PREFIX = re.compile(r"^[A-Z]\)\s*")
# The verdict is written "Correct." in most records and "Correct" in a few
# hundred; both are followed by the rationale proper.
VERDICT_PREFIX = re.compile(r"^(Correct|Incorrect)\b[.:,]?\s+")
SENTENCE_SPLIT = re.compile(r"(?<=[.?!])\s+")
SELECT_ALL = re.compile(r"\s*\((?:select|choose) all that apply\.?\)\s*$", re.IGNORECASE)

# Eight is what the corpus actually needs (two CCDV-F items run to H) and what
# the validators accept. A ninth option would be a new shape, not a rounding
# error, so it fails here instead of silently producing an unlabelled option.
LETTERS = "ABCDEFGH"


def split_stem(stem: str) -> tuple[str, str]:
    """Split one CertSafari stem into the bank's `situation` / `question` pair.

    Deliberately dumb and deterministic: split on terminal punctuation, glue a
    trailing parenthetical ("(Select all that apply.)") back onto the sentence
    it qualifies, and take the last sentence as the ask. Across all 896 records
    that lands the ask on a sentence ending in "?" or opening with a directive
    for every item but one, which ends in a colon and reads correctly anyway. A
    single-sentence stem has no scenario, so `situation` comes back empty — the
    page omits the block rather than rendering an empty one.
    """
    parts = SENTENCE_SPLIT.split(" ".join(stem.split()))
    if len(parts) > 1 and parts[-1].startswith("("):
        parts[-2:] = [parts[-2] + " " + parts[-1]]
    return " ".join(parts[:-1]), parts[-1]


def state_select_count(question: str, wanted: int, stated_counts) -> tuple[str, str | None]:
    """Make a multiple-response stem state the count the item is keyed to.

    `stated_counts` is the validator's own reader, so a stem left untouched here
    is one the gate already accepts. "(Select all that apply.)" is replaced
    rather than appended to, because a stem carrying both phrasings reads as a
    contradiction.
    """
    if wanted in stated_counts(question):
        return question, None
    return (f"{SELECT_ALL.sub('', question)} (Select {wanted}.)",
            f"CertSafari's stem did not state a count; '(Select {wanted}.)' was "
            f"appended to match the {wanted}-answer key.")


def normalized(text: str) -> str:
    """Compare-ready form: letters and digits only, single-spaced.

    CertSafari abbreviates a long objective title ("Configure Claude tools and
    environments for teams" for one the guide writes with an "(e.g., Claude
    Code)" tail), so the two are compared as prefixes rather than for equality,
    and punctuation differences must not decide the match.
    """
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def classify(rec: dict, objectives: dict) -> tuple[dict | None, list[str]]:
    """Read one record's domain, objective and subdomain id off its snapshot."""
    fp = rec["fingerprint"]
    found = {(int(d), int(i), title.strip()) for d, i, title in SUBDOMAIN.findall(rec["snapshot"])}
    if not found:
        return None, [f"{fp[:12]}: snapshot carries no 'Subdomain X.Y:' label"]
    if len({(d, i) for d, i, _ in found}) > 1:
        return None, [f"{fp[:12]}: snapshot carries conflicting subdomain labels "
                      f"{sorted((d, i) for d, i, _ in found)}"]

    domain, index, title = sorted(found)[0]
    if domain not in objectives:
        return None, [f"{fp[:12]}: subdomain {domain}.{index} names domain {domain}, "
                      f"which is not in the blueprint"]
    if not 1 <= index <= len(objectives[domain]):
        return None, [f"{fp[:12]}: subdomain {domain}.{index} is past the "
                      f"{len(objectives[domain])} objectives domain {domain} has"]

    objective = objectives[domain][index - 1]
    lhs, rhs = normalized(title), normalized(objective)
    if not (rhs.startswith(lhs) or lhs in rhs or rhs in lhs):
        return None, [f"{fp[:12]}: subdomain {domain}.{index} is titled {title!r}, but "
                      f"objective {index} of domain {domain} is {objective!r}"]
    return {"task_id": f"{domain}.{index}", "domain": domain, "objective": objective}, []


def load_tags(code: str, tags_dir: str) -> dict:
    """Merge every hand-made tag file for one exam into {fingerprint: tag}.

    Optional, and only ever a second opinion: the snapshot label is the
    authority. Missing files are normal. Where two files disagree the later one
    by name wins, because the disagreement is reported against the snapshot
    anyway.
    """
    merged = {}
    for path in sorted(glob.glob(os.path.join(tags_dir, f"{code}.*.json"))):
        with open(path, encoding="utf-8") as fh:
            merged.update(json.load(fh))
    return merged


def convert(rec: dict, label: dict, stated_counts) -> tuple[dict | None, list[str]]:
    """Turn one corpus record into one bank item (without its id)."""
    fp = rec["fingerprint"]
    errors = []

    def err(msg):
        errors.append(f"{fp[:12]}: {msg}")

    raw_options, explanations = rec["options"], rec["explanations"]
    if len(explanations) != len(raw_options):
        err(f"{len(raw_options)} options but {len(explanations)} explanations")
        return None, errors
    if not 2 <= len(raw_options) <= len(LETTERS):
        err(f"{len(raw_options)} options is outside the 2-{len(LETTERS)} the bank can letter")
        return None, errors

    key_index = []
    for answer in rec["correct_answers"]:
        if answer not in raw_options:
            err("an answer key entry does not repeat any option verbatim")
            return None, errors
        key_index.append(raw_options.index(answer))
    if len(set(key_index)) != len(key_index) or not key_index:
        err(f"answer key names {len(key_index)} option(s), {len(set(key_index))} of them distinct")
        return None, errors

    options = []
    for i, (raw, explanation) in enumerate(zip(raw_options, explanations)):
        correct = i in key_index
        verdict = VERDICT_PREFIX.match(explanation)
        # The verdict word is the one cross-check the corpus offers on its own
        # option/explanation pairing. Where it is present it must agree with the
        # key, or the two lists are misaligned and every explanation is wrong.
        if verdict and (verdict.group(1).lower() == "correct") != correct:
            err(f"option {LETTERS[i]} is keyed {correct} but its explanation says "
                f"{verdict.group(1)!r}")
        text = OPTION_PREFIX.sub("", raw).strip()
        body = VERDICT_PREFIX.sub("", explanation).strip()
        if not text:
            err(f"option {LETTERS[i]} has no text once the letter prefix is removed")
        if not body:
            err(f"option {LETTERS[i]} has no explanation once the verdict is removed")
        options.append({"letter": LETTERS[i], "text": text,
                        "correct": correct, "explanation": body})

    situation, question = split_stem(rec["question"])
    letters = sorted(LETTERS[i] for i in key_index)
    note = None
    if len(letters) > 1:
        question, note = state_select_count(question, len(letters), stated_counts)

    item = {
        # Filled in by import_track() once the bank is sorted; named here so the
        # written file leads with the id the way the hand-authored bank did.
        "id": "",
        "domain": label["domain"],
        # CertSafari's own subdomain id for the item, kept so a reader can trace
        # the objective back to the label the classification came from.
        "task_id": label["task_id"],
        "objective": label["objective"],
        "situation": situation,
        "question": question,
        "options": options,
        "correct": letters if len(letters) > 1 else letters[0],
        "select": len(letters),
    }
    if note:
        item["stem_note"] = note
    item["source"] = "certsafari"
    item["source_url"] = rec["source"]
    item["fingerprint"] = fp
    return item, errors


def import_track(track_key: str, tags_dir: str) -> int:
    track = TRACKS[track_key]
    code, prefix = track["code"], track["prefix"]
    validator = __import__(track["validator"])
    stated_counts = validator.stated_select_counts

    data_dir = os.path.join(ROOT_DIR, track_key, "data")
    with open(os.path.join(CORPUS_DIR, f"{code}.json"), encoding="utf-8") as fh:
        records = json.load(fh)
    with open(os.path.join(data_dir, track["objectives"]), encoding="utf-8") as fh:
        # Order matters here, unlike everywhere else in the repo: a subdomain
        # label addresses an objective by its position in this list.
        objectives = {int(d): list(v["objectives"])
                      for d, v in json.load(fh)["domains"].items()}

    tags = load_tags(code, tags_dir)
    errors, warnings = [], []

    # A stem repeated with different options is one question CertSafari asks
    # several ways. Marking the group lets the page present them as variants
    # later; a stem that appears once carries no marker at all.
    stems = Counter(" ".join(r["question"].lower().split()) for r in records)

    items = []
    for rec in records:
        fp = rec["fingerprint"]
        label, label_errors = classify(rec, objectives)
        errors.extend(label_errors)
        if label is None:
            continue

        tag = tags.get(fp)
        if tag and (tag.get("domain"), tag.get("objective")) != \
                   (label["domain"], label["objective"]):
            warnings.append(
                f"{fp[:12]}: a tag file says domain {tag.get('domain')} / "
                f"{str(tag.get('objective'))!r}, CertSafari's own subdomain "
                f"{label['task_id']} says {label['objective']!r} — the label wins")

        item, item_errors = convert(rec, label, stated_counts)
        errors.extend(item_errors)
        if item is None:
            continue
        stem = " ".join(rec["question"].lower().split())
        if stems[stem] > 1:
            item["cluster"] = hashlib.sha256(stem.encode("utf-8")).hexdigest()[:8]
        items.append(item)

    if warnings:
        print(f"{track_key}: {len(warnings)} tag disagreement(s):")
        for w in warnings[:20]:
            print(f"  ! {w}")
        if len(warnings) > 20:
            print(f"  ... and {len(warnings) - 20} more")

    if errors:
        print(f"{track_key}: FAILED — {len(errors)} problem(s):")
        for e in errors[:40]:
            print(f"  - {e}")
        if len(errors) > 40:
            print(f"  ... and {len(errors) - 40} more")
        return 1

    # Sorting by fingerprint rather than by corpus order keeps ids stable when
    # the collector appends a newly seen question to the middle of the archive.
    items.sort(key=lambda q: (q["domain"], q["fingerprint"]))
    seq = defaultdict(int)
    for item in items:
        seq[item["domain"]] += 1
        item["id"] = f"{prefix}{item['domain']}-{seq[item['domain']]:03d}"

    out_path = os.path.join(data_dir, track["out"])
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(items, fh, indent=1, ensure_ascii=False)

    multi = sum(1 for q in items if isinstance(q["correct"], list))
    print(f"{track_key}: wrote {len(items)} items to {os.path.relpath(out_path, ROOT_DIR)}")
    print(f"  per domain    {dict(sorted(seq.items()))}")
    print(f"  multi-response{multi:5d} ({multi / len(items) * 100:.1f}%)")
    print(f"  stem rewritten{sum(1 for q in items if 'stem_note' in q):5d} "
          f"(count appended to match the key)")
    print(f"  clustered     {sum(1 for q in items if 'cluster' in q):5d} "
          f"(share a stem with another item)")
    print(f"  subdomains    {len({q['task_id'] for q in items}):5d} of "
          f"{sum(len(v) for v in objectives.values())} carry at least one item")
    if tags:
        print(f"  cross-checked {len(tags):5d} hand-made tags, "
              f"{len(warnings)} disagreed with the snapshot label")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("track", nargs="*", default=["all"], choices=["ccaf", "ccap", "ccdf", "all"])
    parser.add_argument("--tags-dir", default=TAGS_DIR,
                        help="optional <CODE>.*.json tag files to cross-check the "
                             "snapshot labels against")
    args = parser.parse_args()
    tracks = list(TRACKS) if "all" in args.track else args.track
    return max(import_track(t, args.tags_dir) for t in tracks)


if __name__ == "__main__":
    sys.exit(main())
