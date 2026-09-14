# Dedup analysis — mock (60) vs guide (76)

Content-overlap scan (Jaccard on content words). **No literal duplicates found** — max overlap was 0.22; pairs share a topic but are distinct scenarios with different specifics and correct answers, so all 136 are kept. `data/duplicates.json` is empty.

Top topical-overlap pairs (review if you disagree; add the mock id to duplicates.json to drop it):

| mock | guide | overlap |
|---|---|---|
| `m10` | `g2` | 0.219 |
| `m44` | `g62` | 0.2 |
| `m2` | `g14` | 0.186 |
| `m41` | `g50` | 0.156 |
| `m9` | `g13` | 0.143 |
| `m38` | `g62` | 0.141 |
| `m12` | `g12` | 0.138 |
| `m35` | `g57` | 0.127 |
| `m4` | `g2` | 0.125 |
| `m6` | `g1` | 0.123 |
| `m42` | `g69` | 0.122 |
| `m31` | `g46` | 0.117 |
