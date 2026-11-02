# Talk outline: Why Your Go Benchmarks Are Lying

> **Format:** GoLab 2026, room 2, 10:45. 45-minute slot: 42 minutes presented, 3 minutes Q&A. Not recorded. Intermediate Go audience.
> **Deck:** `slides/presentation.md` (54 pages, 3 reveals)
> **Demonstrations:** no live demos. Every command and captured result stays in the repository.

## Throughline

**A benchmark moved that could not have moved.**

At Datadog our code runs inside the customer's process. A false red result
wastes our time. A false green result costs the customer CPU. The talk is the
set of checks we run before we believe a number.

Every section opens on a real incident, asks one of three questions, and ends
on one action the audience can take on Monday:

1. Is the benchmark measuring real work?
2. Is the sample stable enough?
3. Is the difference large relative to the noise?

| | Laptop + micro | CI + macro |
| --- | --- | --- |
| Real work? | the compiler deletes it | one workload is not representative |
| Stable sample? | one run is a point | pairs cannot see drift |
| Above the noise? | the laptop has a ceiling | shared runners move |

**No maths on stage.** Say why a check matters, not how the statistics work.

## Beat sheet

The times are a model: SAY words at 130 words per minute, plus pauses and
visuals. A timed read must replace them (see `TODO.md`).

| Section | Purpose | Monday action | Target | Cumulative |
| --- | --- | --- | ---: | ---: |
| Cold open | #4891 bot comment: "Would you fix it?" Plant, do not resolve | — | 1:30 | 1:30 |
| Why Datadog cares | Code in your process. PGO −3.4% on one service. SpeedLab | — | 1:30 | 3:00 |
| **01 A Loose Cable** | OPERA: a result that could not be true. "Trivial things we are clever enough to rule out." The three questions. One basics slide | — | 5:00 | 8:00 |
| **02 Is It Real Work?** | DCE capture, `ns/op` vs `allocs/op`, `b.Loop` and the Go 1.26 fix | `b.Loop`, `-benchmem`, Go 1.26 | 6:00 | 14:00 |
| **03 The Regression That Was a Speedup** | Resolve #4891: same-machine A/B was faster. Code layout. One `benchstat` slide | Same-machine A/B before you touch code | 7:00 | 21:00 |
| **04 It Was the Machine** | #643: `largeidle` could not have moved. One local container run. macOS caveat | A control benchmark | 5:00 | 26:00 |
| **05 How We Run It at Datadog** | Dedicated hardware, SMT and DFS data, workloads, budgets, release gate | Bare metal, SMT and boost off, budget gates | 7:30 | 33:30 |
| **06 Detecting Change Over Time** | A/B cannot see drift. Change points. Go team baseline quote. Two patterns | Nightly trend plus a small PR gate | 4:00 | 37:30 |
| Ledger and close | False-positive ledger, minimum discipline, 3×2 recap, talk repo | Write down every false alarm | 3:30 | 41:00 |

One minute of buffer to 42:00.

**Checkpoints:** §01 by 3:00 · §03 by 14:00 · §05 by 26:00 · ledger by 37:30 ·
finish by 41:00. If §05 has not started by 28:00, apply the cut ladder live.

## Narrative order

The bot comment opens the talk and stays unresolved until §03. Datadog's stake
comes next, because "overhead is product correctness" is the reason the talk
exists. OPERA follows as the physics version of the throughline: careful
experts, a number that could not be true, and a trivial cause.

The two incidents are mirror images. In #4891, CI said slower and the laptop
was right. In #643, the laptop said slower and CI was right. The tell is the
same: a benchmark moved that could not have moved. Say that on the mirror-image
slide.

§05 shows the Datadog practice inside ledger row 23: dedicated hardware,
per-SDK overhead budgets, several workloads per SDK, and gating on the
release. The archetype table is the public FOSDEM taxonomy (row 20). It is not
a statement of which archetypes Datadog runs.

The close answers the opening: OPERA's coordinator said a result is never a
discovery until other people confirm it. Benchmarks are the same.

## Cut ladder

Apply in this order if the timed read runs long:

1. "A known phenomenon" (−0:20). Say the Berger reference in one sentence on
   "The mechanism".
2. "What's the impact of disabling DFS?" (−0:30). "Three sysfs writes" keeps the
   point.
3. "What regressions look like" (−0:20).
4. "The macOS caveat" (−0:30). Keep one spoken sentence on "5.25% is not a
   triumph".
5. "One command, two habits" (−0:30). Last resort: §02 uses `-benchmem`.

**Never cut without review:** either opening incident, the OPERA quote, the DCE
capture, "What we do at Datadog", the SMT impact data, the false-positive
ledger, the 3×2 recap, or any of the three memes. The memes cost ten seconds
each.

## Public results and sources to preserve

* OPERA: CERN and Cartlidge, *Science* 335(6072):1027 (row 9). Ereditato
  quotes, *The Guardian*, 22 Sep 2011 (row 46).
* PGO −3.4% CPU on one service: Datadog blog, May 2024 (row 47).
* `b.Loop` and the Go 1.26 inlining change: rows 4, 39, 40.
* dd-trace-go #4891: `07-war-stories.md` story 1, rows 26 and 27.
* otel-go-compile-instrumentation #643: `07-war-stories.md` story 2, row 18.
* Local container run: `demo/results/cv-summary.txt`, one run, August 2026 (row 8).
* FOSDEM SMT and DFS data: rows 1-3. Workload archetypes: row 20.
* Datadog practice shape: row 23. SpeedLab name: row 30.
* Go team baseline and SlowBots quotes: rows 34 and 38. Change points: row 21.

## Audience resources

* Talk repository: <https://github.com/kakkoyun/golab-26>
* Prior FOSDEM version: <https://youtu.be/8211fNI_nc4>
