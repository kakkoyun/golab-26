# Talk outline: Why Your Go Benchmarks Are Lying

> **Format:** GoLab 2026. 45-minute slot: 38 minutes presented, 7 minutes Q&A. Intermediate Go audience.
> **Deck:** `slides/presentation.md` (105 pages, including progressive-reveal steps)
> **Demonstrations:** no live demos; every command and captured result stays in the repository

## Thesis

A benchmark is a measurement system. It can report a precise number while
measuring removed work, an unstable sample, or an uncontrolled machine. Trust a
Go benchmark only after answering three questions:

1. Is the benchmark measuring real work?
2. Is the sample stable enough?
3. Is the difference large relative to the noise?

**The same three questions apply at two scales, and the answers differ.** That
is the structure of the talk.

| | Local + micro | CI + macro |
| --- | --- | --- |
| Real work? | the compiler deletes it | the workload is unrealistic |
| Stable sample? | one run is a point | pairs cannot see drift |
| Above the noise? | your laptop is uncontrolled | the hardware moves |

Microbenchmarks usually fail **representative**. Macrobenchmarks usually fail
**repeatable**. Neither is a substitute for the other, and the talk covers both.

## Timing baseline

GoLab gives the talk a 45-minute slot. The target is 38 minutes presented and
7 minutes of Q&A.

By the model below, the GopherCon UK script held about 53 minutes of spoken material at 129 pages. The GoLab cut removes 24 pages and about 1,400 SAY words. The prose pass removes 330 more. The cut keeps the
basics and both incidents, because GoLab lists the talk as Intermediate. It
removes the mechanism explainers and the advanced side paths.

The times below are a word-count model: SAY words at 130 words per minute, plus
25% for reveals, pauses, and visuals. Three earlier timing estimates in this repository were wrong. A timed read-through must replace this model before
delivery (see `TODO.md`).

## Beat sheet

| Part | Section | Purpose | Target | Cumulative |
| --- | --- | --- | ---: | ---: |
| 1 | **01 Why Benchmark?** | Is it slow, could it go faster, is it worth it. Latency and throughput, cost of slowness, Martí | 3:30 | 3:30 |
| 1 | **02 Why I Care** | How I got here, why Datadog cares | 1:00 | 4:30 |
| 1 | **03 A Loose Cable** | OPERA, the three questions, the two-scales roadmap | 2:30 | 7:00 |
| 1 | **04 Before You Measure** | Representative and repeatable, micro vs macro, start macro | 1:15 | 8:15 |
| 1 | **05 Benchmarking, Quickly** | Write, run, read, profile, read compiler output | 2:30 | 10:45 |
| 2 | **06–10 Local and micro** | Bot-comment plant, DCE, constant folding, timers, `b.Loop`, code layout, statistics, local environment, recap | 12:00 | 22:45 |
| 3 | **11–15 CI and macro** | #643 opener, macro design, SMT and DFS impact, change-point detection, baseline, CI patterns, false-positive ledger, recap | 10:45 | 33:30 |
| 4 | **16 Wire It Up** | Three CLIs, `benchenv`, minimum discipline, 3×2 recap, take-home | 2:30 | 36:00 |

The model total is 36:00 for 3,756 SAY words. The remaining 2 minutes to 38:00 are buffer.

**Rehearsal checkpoints:** §05 by 8:15 · §06 by 10:45 · §11 by 22:45 · §16 by 33:30 · finish by 36:00. If §11 has not started by 25:00, apply the cut ladder live.

## Narrative order

### Why first, then the story

Open on *why benchmark at all* — the user is the metric, not the CPU. Is it
actually slow? Could it go faster? Is it worth optimizing? Then the vocabulary
(latency vs throughput, cost of slowness, Lütke) and a pointer to where the
"what to optimize" half lives (Martí). This front matter is the WHY; it earns
the right to spend fifty minutes on measurement.

Only then the speaker context — *why I care* — as a short beat about
consequences, not credentials. Datadog's stake lands here because the
"overhead is product correctness" line is the sharp version of the WHY.

### The story, then the contract

OPERA is beat three, not the cold open. A careful team, a surprising result, and
two faults that partially masked each other. Pivot to a laptop benchmark only
after the connector reveal. The three questions and the two-scales roadmap stay
welded to OPERA — they are the contract that sets up the arcs and must
immediately precede them.

### Two arcs, two opening incidents

Each arc opens on a real incident, and the two are deliberate mirror images.

- **Arc 1 — dd-trace-go #4891.** CI reported `BenchmarkOTLPProtoSize` 6-9%
  slower. Planted before the compiler section and left unresolved. Resolved in
  §1B once the audience can read a benchmark: the PR was actually faster, and
  code layout had flipped the sign.
- **Arc 2 — otel-go-compile-instrumentation #643.** A local overhead run
  reported `multi` at 230% and `largeidle` at 212% against a 150% ceiling.
  `largeidle` shares no changed dependencies, so it could not have regressed.
  The machine was the variable; CI on a dedicated runner was right.

The tell is identical in both cases: **a benchmark moved that could not have
moved.** Say that explicitly on the mirror-image slide.

### The bridge between arcs

Berger's causal profiling closes arc 1: a component speedup does not imply a
system speedup, because contention and queueing decide how much of a local win
survives. That is the reason arc 2 exists, and it is the transition line into it.

### Close

Return to the three questions as a 3×2 grid, one row per question and one column
per scale. The two lines that must land: a sub-10% micro delta can be layout
noise, and a shared runner cannot be fixed with more samples.

## Cut ladder

The GoLab cut already removed most of the previous ladder. It removed "what a macro gate
needs at scale", "Go runs this on Go", "Seeing the hardware", "How the
keepalive works", the macro traps, and the SMT and DFS mechanism slides. It
also removed the observer effect, escape analysis, `make asm-dce`, inlining,
`StopTimer` with no `StartTimer`, causal profiling, the Linux toolbox,
`perflock`, the existing-tools table, and the `honestbench` and `benchgate`
panels. The script and the ledger still hold that material for a longer slot.

Apply in this order if the timed read-through runs long:

1. "Why SMT breaks benchmarks" and "Why DFS breaks benchmarks" (−1:00). Keep
   the impact data and the three sysfs writes.
2. "Finding what to optimize" (−0:20). The Martí link stays on the closing
   slide.
3. "The two-variable sink" (−0:25). `b.Loop` is the fix the talk recommends.
4. "Constant folding" (−0:15).
5. "Reading compiler output" (−0:30). Last resort, because §07 uses the
   compiler output vocabulary.

**Never cut without review:** either opening incident, the DCE captured
evidence, the local CV experiment, the macOS caveat, the SMT and DFS impact
data, the 3×2 recap, the Datadog rationale, "Why not just add more runners?",
the §05 basics, or **any of the three memes**. The memes cost ten seconds each.
They are the fix for the density complaint from the first delivery.

## Public results and sources to preserve

- OPERA connector bias and the two-fault account: CERN press release and
  Cartlidge, *Science* 335(6072):1027. Claims ledger row 9.
- Google search team latency result: claims ledger row 10.
- Local CV experiment: committed files under `demo/results/`.
- FOSDEM SMT and DFS variance data: claims ledger rows 1-3.
- dd-trace-go #4891: `07-war-stories.md` story 1, sources [S28].
- otel-go-compile-instrumentation #643: `07-war-stories.md` story 2, [S29],
  claims ledger row 18.
- Causal profiling: claims ledger row 19.
- Workload archetypes: claims ledger row 20, from the FOSDEM talk.
- Change-point detection: claims ledger row 21.
- PGO production reduction: <https://www.datadoghq.com/blog/datadog-pgo-go/>.
- Prior FOSDEM version: <https://youtu.be/8211fNI_nc4>.

## Open gate before delivery

Claims ledger **row 23** is `pending`. The "what a macro gate needs at scale"
slide has already been reframed to avoid unpublished statements about Datadog's
internal benchmarking infrastructure. If Kemal wants the Datadog-specific
version back, that row has to move to `verified` first.

## Audience resources

- Talk repository: <https://github.com/kakkoyun/golab-26>
- Benchmark tools and skills: <https://github.com/kakkoyun/benchlab>
- Binaries: `go install github.com/kakkoyun/benchlab/cmd/...@latest`
- Agent Skills: `npx skills add kakkoyun/benchlab --all`
