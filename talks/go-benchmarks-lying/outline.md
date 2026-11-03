# Talk outline: Why Your Go Benchmarks Are Lying

> **Format:** GoLab 2026, room 2, 10:45. 45-minute slot: 42 minutes presented, 3 minutes Q&A. Not recorded. Intermediate Go audience.
> **Deck:** `slides/presentation.md` (86 pages, 3 reveals)
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
Prefer charts and diagrams to numbers.

## Message

Benchmarking is not easy. It needs investment, maths, tooling, and a keen
eye. The value is huge: Datadog does it, and the Go team does it. If you ship
a library, a tool, or a service on a hot path, invest. Now you know what to
do.

## Beat sheet

The times are a model: SAY words at 130 words per minute, plus pauses and
visuals. A timed read must replace them (see `TODO.md`).

| Section | Purpose | Monday action | Target | Cumulative |
| --- | --- | --- | ---: | ---: |
| Why speed matters | Tobi quote. Customer happiness, not CPU. Latency and throughput. Cost of slowness. Before you optimize. Martí | Profile production first | 4:00 | 4:00 |
| Why Datadog cares | Code in your process. PGO −3.4% on one service. SpeedLab | — | 1:30 | 5:30 |
| Cold open | #4891: the PR, the bot comment ("Would you fix it?"), the last bot run (faster), the benchmark that matters (~16 ns). Plant, do not resolve | — | 2:30 | 8:00 |
| **01 A Loose Cable** | OPERA: a result that could not be true. "Trivial things we are clever enough to rule out." The three questions. One basics slide | — | 4:30 | 7:30 |
| **02 Is It Real Work?** | DCE capture, `ns/op` vs `allocs/op`, `b.Loop` and the Go 1.26 fix, the cache trap (Harsanyi) | `b.Loop`, `-benchmem`, Go 1.26 | 4:30 | 12:00 |
| **03 The Regression That Was a Speedup** | Resolve #4891: same-machine A/B was faster. Code layout. One `benchstat` slide | Same-machine A/B before you touch code | 5:00 | 17:00 |
| **04 It Was the Machine** | #643: `largeidle` could not have moved. One local container run. macOS caveat | A control benchmark | 4:30 | 21:30 |
| **05 How We Run It at Datadog** | Dedicated hardware, FOSDEM credit, SMT and DFS charts, prombench, Gregg, workloads, coordinated omission, budgets | Bare metal, SMT and boost off, budget gates | 6:00 | 27:30 |
| **06 Detecting Change Over Time** | A/B cannot see drift. Change points, Netflix, Henrik Ingo. Go team quote, dashboard, SlowBots. Two patterns | Nightly trend plus a small PR gate | 4:30 | 32:00 |
| Ledger | #4891 fires again. Write it down | Write down every false alarm | 1:00 | 33:00 |
| **07 Agents Need Real Benchmarks** | PGO prediction vs production. DODO: production-grounded benchmarks for agents, the per-function results chart. `dodo-cli` | Give your agent production data | 5:00 | 38:00 |
| Close | Benchmarking is not easy. On a hot path, invest. Now you know what to do. Talk repo | Invest | 3:30 | 41:30 |

The rows after the cold open still carry their old targets, so this model now sums to about 46 minutes. The SAY word count says about 32 to 38 minutes. Trust neither: the timed read decides. If it runs long, cut the why slides first: Martí, then latency and throughput. The model is uncertain in both directions. If the timed read is short, use the stretch beats in the script.

**Checkpoints:** §01 by 3:00 · §03 by 12:00 · §05 by 21:30 · §07 by 33:00 ·
finish by 41:30. If §05 has not started by 24:00, apply the cut ladder live.

## Narrative order

The talk opens on why speed matters, then Datadog's stake. The #4891 story
follows: the PR, the bot comment, the last bot run that says faster, and the
benchmark that measured the changed code. The puzzle stays unresolved until
§03. Datadog's stake sits before the story, because "overhead is product
correctness" is the reason the talk exists. OPERA follows as the physics version of the throughline: careful
experts, a number that could not be true, and a trivial cause.

The two incidents are mirror images. In #4891, CI said slower and the laptop
was right. In #643, the laptop said slower and CI was right. The tell is the
same: a benchmark moved that could not have moved. Say that on the mirror-image
slide.

§05 shows the Datadog practice inside ledger row 23: dedicated hardware,
per-SDK overhead budgets, several workloads per SDK, and gating on the
release. The archetype table is the public FOSDEM taxonomy (row 20). It is not
a statement of which archetypes Datadog runs.

§07 is the newest material. Agents optimise whatever the benchmark measures,
so a wrong benchmark now fails faster. DODO grounds the benchmark in
production data (ledger rows 48 and 49). The PGO slide is the bridge: a
benchmark is a prediction, and production is the answer.

The close states the message: benchmarking is not easy, it is worth it,
Datadog and the Go team do it, so invest if you are on a hot path. It ends
on OPERA's coordinator: a result is never a discovery until other people
confirm it.

## Cut ladder

Apply in this order if the timed read runs long:

1. "Noise goes all the way down" (−0:15). Fun, not load-bearing.
2. "A known phenomenon" (−0:20). Say the Berger reference in one sentence on
   "The mechanism".
3. "What's the impact of disabling DFS?" (−0:30). "Three sysfs writes" keeps the
   point.
4. "What regressions look like" (−0:20).
5. "The macOS caveat" (−0:30). Keep one spoken sentence on "5.25% is not a
   triumph".
6. "`dodo-cli` · internal beta" (−0:40). Keep the DODO diagrams.
7. "One command, two habits" (−0:30). Last resort: §02 uses `-benchmem`.

**Never cut without review:** either opening incident, the OPERA quote, the DCE
capture, "What we do at Datadog", the SMT impact data, the false-positive
ledger, the DODO diagrams, "Benchmarking is not easy", the 3×2 recap, or any
of the three memes. The memes cost ten seconds
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
* Go team baseline and SlowBots quotes: rows 34 and 38. Dashboard: row 36.
  Change points: row 21. Gregg: row 24.
* PGO benchmark −5.4% vs production −3.4%: row 47.
* DODO: Datadog blog, June 2026 (row 48). `dodo-cli` features: row 49.
* Added for length: cache trap (row 45), prombench (row 44), coordinated
  omission (rows 13, 22), SlowBots (row 37), Netflix (row 21), Henrik Ingo
  (row 51), FOSDEM credit (row 29).

## Audience resources

* Talk repository: <https://github.com/kakkoyun/golab-26>
* Prior FOSDEM version: <https://youtu.be/8211fNI_nc4>
