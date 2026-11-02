# Script: Why Your Go Benchmarks Are Lying

GoLab 2026. 45-minute slot: 42 minutes presented, 3 minutes Q&A. 54 pages.
Intermediate Go audience.

Deck: `slides/presentation.md`. Each `##` heading below matches the slide
title verbatim, so you can find your place by what is on screen.
`make sync/notes NOTES_TALK=talks/go-benchmarks-lying` copies each entry into
its slide as a presenter note.

## How to use this

**SAY** lines are the words, written to be spoken. You do not need them
verbatim. **DO** lines are delivery cues. Learn the beats first, then the three
questions, then the two stories, then the numbers.

**Throughline:** a benchmark moved that could not have moved.

**No maths on stage.** Say why a check matters. Do not explain how the
statistics work.

## The beats

| Section | The one thing |
| --- | --- |
| Cold open | A red bot comment on code that could not be slower |
| Why Datadog cares | Our code runs in your process |
| 01 A Loose Cable | Careful people miss trivial errors |
| 02 Is It Real Work? | The compiler deletes your work |
| 03 The Regression That Was a Speedup | Noise can point the wrong way |
| 04 It Was the Machine | A control benchmark exposes the machine |
| 05 How We Run It at Datadog | Dedicated hardware, workloads, budgets |
| 06 Detecting Change Over Time | A/B cannot see drift |
| Ledger and close | Write every false alarm down. Three questions, two scales |

## Timing

The budgets are a model, not a measurement. Replace them after the timed read.

Checkpoints: §01 by 3:00 · §02 by 8:00 · §03 by 14:00 · §04 by 21:00 ·
§05 by 26:00 · §06 by 33:30 · ledger by 37:30 · finish by 41:00. If §05 has
not started by 28:00, apply the cut ladder in `outline.md`.

---

## Why Your Go Benchmarks Are Lying

**SAY**

Every benchmark you write is a measurement system. Like any instrument, it
can be precise and still wrong.

Today I give you three questions. They turn a number into a measurement.

**DO**

Do not introduce yourself yet. Advance.

---

## A benchmark bot comment

**SAY**

June this year. dd-trace-go, the Datadog Go tracer. I restructure one file
and push.

The benchmark bot answers: `BenchmarkOTLPProtoSize` is six to nine percent
slower than main. Nothing in my diff goes near OTLP encoding.

So. Would you fix it?

Most of us would. We open a profiler, find something, and push a fix.

**DO**

Ask the question. Wait two seconds. Do not solve it. The answer comes in §03.

---

## Why Datadog cares

**SAY**

Why do I care so much? Before Datadog, I maintained Prometheus
`client_golang` and worked on the Parca profiler. Each of those jobs punished
me for a benchmark I did not question.

At Datadog, our code runs inside your process. Every nanosecond we spend
comes out of your budget. For us, overhead is product correctness.

One public number: profile-guided optimisation took three point four percent
of CPU off one large production service. Staging was too noisy to show it.
The team had to divide CPU by the work done before the change was visible.

We invest in this internally. The effort is called SpeedLab. This talk is the
spillover.

**DO**

Say the SpeedLab name once. Ledger row 30 permits the name and its existence
only. The practice comes in §05. The PGO number is one service, not all of
production. Ledger row 47.

---

## A Loose Cable

**DO**

Section budget 5:00, including the basics slide. Start by 3:00.

---

## September 2011

**SAY**

September 2011. The OPERA experiment fires neutrinos from CERN to a detector
in Italy. The neutrinos arrive early. Faster than light.

If that is true, Einstein is wrong. The team knows it. Their coordinator says:
a result is never a discovery until other people confirm it.

So they publish, and they ask the world to find their mistake.

**DO**

Let the headline stand for a beat before you speak. Ledger row 46 holds the
quote.

---

## "Trivial things we are

**SAY**

And then he says this.

"If there is a problem, it must be a tough, nasty effect, because trivial
things we are clever enough to rule out."

Remember that sentence.

**DO**

Read the quote slowly. Pause after "rule out".

---

## The cause

**SAY**

It was this. A fibre-optic connector, not fully seated, in the GPS timing
chain. Seventy-three nanoseconds of bias.

A trivial thing.

And a second fault pushed the other way and partly hid the first. The bug hid
behind another bug.

**DO**

Let them look at the photo first. Do not put a number on the second fault.
Ledger row 9.

---

## Your cables

**SAY**

These physicists were not careless. They were very careful, and the
instrument was still wrong.

You have `testing.B`, a laptop, and thirty browser tabs. Your cables are the
compiler, the statistics, and the machine.

---

## systematic error survives expert review

**SAY**

Which brings us to the only rule that matters today.

**DO**

Ten seconds. Do not explain the joke.

---

## Three questions

**SAY**

Three questions.

Is the benchmark measuring real work?

Is my sample stable enough?

Is the difference bigger than the noise?

If you cannot answer all three, you do not have a measurement. You have a
number. We ask them on the laptop first, and then in CI.

**DO**

Pause after each question. The audience hears them again in every section.

---

## One command, two habits

**SAY**

A quick reminder of the instrument. One command.

`-count=10`, because one run is one draw, not a measurement. `-benchmem`,
always, because allocations show what the code really did.

We need both in a minute.

**DO**

Thirty seconds. Do not teach the flags.

---

## Is It Real Work?

**DO**

Section budget 6:00. Question 1: real work? Start by 8:00.

---

## The compiler is not neutral

**SAY**

Question one. Real work.

Your benchmark is just code. The compiler reads it, sees that you never use
the result, and removes the work. It is right to do that.

Your loop still runs `b.N` times. It just runs empty.

---

## Dead-code elimination

**SAY**

`makeBuffer` allocates sixty-four bytes. The benchmark calls it and throws
the result away.

Watch what happens.

---

## `make bench-dce`

**SAY**

A quarter of a nanosecond, against eleven. It looks forty times faster.

Now look at the allocations. Zero. `make` cannot skip the allocation. Zero
allocations means the call is gone.

**DO**

Point at the allocations column.

---

## `ns/op` can lie

**SAY**

Time can lie. A very fast function and an empty loop look the same.

An allocation happened, or it did not. `allocs/op` cannot lie.

Always pass `-benchmem`.

**DO**

Land this slowly. It is the most reusable line in the talk.

---

## the compiler deleted your benchmark

**SAY**

Those are the real numbers from two slides ago.

**DO**

Ten seconds.

---

## `b.Loop()` · Go 1.24, fixed in 1.26

**SAY**

The fix is `b.Loop`, from Go 1.24. Setup before the loop is not timed. The
loop body stays alive, so the compiler cannot delete it.

But there is a catch that many people missed. In 1.24 and 1.25, `b.Loop`
kept the body alive by blocking inlining. So your benchmark could allocate
where your production code does not.

Go 1.26 removed that. Upgrade before you compare.

**DO**

Ledger rows 39 and 40. Go 1.26 is the fix, not the regression. Do not say it
backwards.

---

## What `b.Loop` removes

**SAY**

Two rows matter. Setup is not timed, and the body is not deleted.

Write `b.Loop()` literally in the loop condition. If you assign it to a
variable first, you lose the protection.

**DO**

Do not read the table. Point at two rows.

---

## The Regression That Was a Speedup

**DO**

Section budget 7:00. Question 2: stable sample? Start by 14:00. This section
answers the opening question.

---

## Read the benchmark first

**SAY**

Back to the bot comment. Would you fix it?

I did not. First, I read the benchmark. This is the whole timed loop. One
call, `proto.Size`, on a struct built before the timer starts.

It calls none of the code I changed. And on my machine it was stable: under
zero point one percent from run to run.

---

## Same machine, both branches

**SAY**

So I built both branches on the same machine and compared them.

Main: eight hundred eighty-three nanoseconds. My branch: eight hundred forty.

My branch was faster. CI did not get the size wrong. It got the sign wrong.

**DO**

Let this sit. It is the biggest surprise in the talk.

---

## The mechanism

**SAY**

Why? My change moved function addresses in the package. The hot loop moved
relative to cache lines and branch targets.

At this speed, that is worth several percent, in either direction. On a CI
runner that cannot pin its clock, that is enough to flip the verdict.

The fix: no code change. Nothing was wrong.

---

## A known phenomenon

**SAY**

This is well known. Emery Berger's talk, Performance Matters, shows that code
layout alone can swing performance by ten percent. Watch it.

---

## A noisy result can be

**SAY**

So the lesson is not "CI is bad". A noisy result can point the wrong way.

It can block a good change. And it can let a real regression through.

---

## One number is a point sample

**SAY**

Here is how noisy one number is. Same binary, same machine. Thirty-nine
nanoseconds, then twenty-seven.

A forty-three percent swing, and nothing changed.

One run is one point. You need a sample.

---

## `benchstat`

**SAY**

The tool is `benchstat`. Run with `-count`, give it the old and the new
results, and it compares the two samples.

It answers one question: is B different from A, beyond the noise? A tilde
means no. That is a result. Do not rerun until you get the answer you want.

It cannot tell you whether the machine is trustworthy. If an unchanged
benchmark spreads by more than about five percent, fix the machine first.

**DO**

No formulas. Say why, not how.

---

## more samples will not fix a noisy machine

**SAY**

Only one of these buttons works.

**DO**

Ten seconds. The next section is about the other button.

---

## It Was the Machine

**DO**

Section budget 5:00. Question 3: above the noise? Start by 21:00.

---

## A second red number

**SAY**

Second story, three weeks later. OpenTelemetry Go compile-time
instrumentation. I land a dependency fix and run the overhead benchmark on my
laptop.

`multi`: two hundred thirty percent overhead, against a ceiling of one hundred
fifty. `largeidle`: two hundred twelve.

Both fail. It looks like I broke something badly.

---

## `largeidle` shares

**SAY**

But my change touched dependencies in `multi` only. `largeidle` shares none
of them. It cannot have regressed. And it moved as much as `multi`.

When code that did not change gives a different result, the common factor is
the machine. I ran parallel builds all afternoon while I benchmarked.

That is the trick to take home: a control benchmark. Keep one benchmark that
your change cannot touch. If it moves, do not trust the others.

**DO**

The fix was to wait for CI. That job runs only in CI, on a dedicated runner.

---

## The mirror image

**SAY**

Put the two stories side by side.

First: CI said slower, the laptop was right, and the cause was code layout.

Second: the laptop said slower, CI was right, and the cause was machine load.

Neither place is right by default. And the tell was the same both times: a
benchmark moved that could not have moved.

**DO**

This is the throughline. Say the last line slowly.

---

## What does isolation actually buy?

**SAY**

"Run it in a container" is common advice. So we measured what it buys, on
this laptop.

Idle: under five percent spread. Add sixteen background spinners: three
times slower, four times noisier. Pin the benchmark in a container under the
same load: the spread goes back to about the idle level.

**DO**

This is one local run from August. Do not call it a general result. The
platform details are on the slide if someone asks.

---

## 5.25% is not a triumph

**SAY**

Five percent is not a good number. It is the best this laptop can do.

A change smaller than that is invisible here. For a smaller change, you need
a different machine. That is the next section.

**DO**

Do not compare this number with the bare-metal results. They come from a
different benchmark on a different machine. Ledger row 8.

---

## The macOS caveat

**SAY**

One caveat. On macOS, Docker runs in a Linux VM. `--cpuset-cpus` pins a
virtual CPU.

The VM can still move it across physical cores. Nothing in the container can
turn off SMT or pin the clock.

You get isolation from your other processes. You do not get controlled
hardware.

**DO**

Do not soften this.

---

## How We Run It at Datadog

**DO**

Section budget 7:30. Start by 26:00.

---

## What we do at Datadog

**SAY**

So how do we do this at Datadog, where overhead is the product? Four things.

Dedicated hardware, not shared CI runners. An overhead budget for each SDK.
Several workloads for each SDK, not one. And we gate the release, not only
the pull request.

Let me show you why each one is there.

**DO**

Ledger row 23. Say the practice shape only. Give no hardware counts, budget
figures, archetype names, or scale. If someone asks for numbers, say that
they are internal.

---

## Why not just add more runners?

**SAY**

First, the hardware. Shared runners have neighbours, changing clocks, and
shared caches. A real regression can vanish, and a fake one can appear.

So why not add more runners? Read what the Go project says about its
performance builders. Often there is only one physical machine, with a
backlog of work.

More capacity helps correctness. Performance needs the scarce machine.

**DO**

Read the quote aloud. Ledger row 38.

---

## What's the impact of disabling SMT?

**SAY**

What does dedicated hardware buy? These are the experiments behind our
FOSDEM talk. Two CPU-bound tasks, on the same physical core, then on separate
cores.

Spread: twenty-four percent with SMT on. Zero point zero four with it off.
About a hundred times less variance. And twice as fast, because the core is
no longer shared.

---

## What's the impact of disabling DFS?

**SAY**

Now frequency scaling. Turn it off: ten times less variance.

And the mean got slower. Turbo is fast, and inconsistent. A benchmark must be
comparable. It does not need to be fast.

---

## Three sysfs writes

**SAY**

All of that is three writes. Turn off SMT. Pin the governor. Turn off boost.

On bare metal, the spread goes from about twenty-four percent to zero point
zero four.

In a VM, the write can succeed and do nothing. That is worse than an error.

---

## Workload archetypes

**SAY**

Second, the workloads. One workload is not representative. Our FOSDEM talk
describes four archetypes. Idle: background workers. Latency: APIs with many
small requests. Throughput: queues and batch jobs. Enterprise: business apps
with a database.

Remember the second story. `largeidle` is Idle. `multi` is Enterprise.
Different code, same movement, same moment. That is a shared environment,
not a shared cause.

**DO**

Ledger row 20. Do not say which archetypes Datadog runs.

---

## A macro gate is a budget

**SAY**

Third, the budget. A micro gate compares two commits. A macro gate compares
against a budget: a ceiling that you must not cross.

That is a product decision, not a statistics question. How much of the
customer's machine may we take?

**DO**

The example values come from the second story, not from Datadog budgets.

---

## Detecting Change Over Time

**DO**

Section budget 4:00. Question 2, across days. Start by 33:30.

---

## A/B is the wrong model for CI

**SAY**

Fourth, time. `benchstat` compares two samples. CI does not have two samples.
It has a time series: one result per commit, for months, with hardware
changes and dependency updates in between.

If you compare each commit with its parent, you ask the noise question every
time. And you miss slow drift completely.

---

## What regressions look like

**SAY**

This is how we draw a regression on a slide. This is what it looks like in
real data.

A step change is clear in a drawing. In real data, it hides in the noise.

---

## Change-point detection

**SAY**

So ask a different question. Not "is this commit slower than its parent?"
Ask "where did the history shift, and stay shifted?"

That is change-point detection. It finds lasting shifts and ignores one-off
spikes. Apache Otava implements it. Netflix wrote about doing this at scale.

It needs history, so it belongs in a nightly job, not in the PR gate.

**DO**

No statistics. Say what it finds, not how.

---

## Why a baseline, not a pair

**SAY**

The Go team says why, about their own hardware. They never report a number
alone, only relative to a baseline. Because the machine on one day is very
different from the same machine the next day.

If that is true for the Go team, it is true for your CI runner.

**DO**

Read the quote aloud.

---

## Two patterns

**SAY**

So, two patterns. A PR gate: fast and strict. A small set of benchmarks that
regressed before, a same-machine A/B, and a tight threshold.

A nightly suite: complete and slow. Pinned hardware, all controls on, and
change-point detection. Before a release, the budget gate.

CI detects. To explain a result, you still measure on a controlled machine.

---

## Keep a ledger of false positives

**SAY**

The last practice is the cheapest. Remember the first bot comment? The same
benchmark fired again eleven days later, on another pull request.

That time, one comment closed it, because the first investigation was
written down. Without that note, the next person repeats the investigation.
Or worse, they "fix" it.

Write down every false alarm.

**DO**

Budget 1:00. Start by 37:30.

---

## The minimum viable discipline

**SAY**

If you take one slide home, take this one.

Use `b.Loop` and read allocations. Run enough samples and compare with
`benchstat`. Add one control benchmark that your change cannot touch.

That is under an hour of work.

---

## Three questions, two scales

**SAY**

Three questions, two scales.

Real work: `b.Loop` on the laptop. Real workloads and budgets in CI.

Stable sample: ten runs and `benchstat`. Then a time series with change
points.

Above the noise: a control benchmark and a known ceiling. Then bare metal
with SMT and boost off.

A sub-ten-percent micro delta can be layout noise. A shared runner cannot be
fixed with more samples.

**DO**

Say the last two lines slowly.

---

## Take it with you

**SAY**

The talk repo is the QR code. It has the deck, the script, and every captured
result, so you can check my numbers.

The earlier FOSDEM talk is there too, if you want the language-neutral
version.

---

## Questions?

**SAY**

OPERA's coordinator was right. A result is not a discovery until someone
else confirms it. That includes your benchmarks.

Trust a number only after the compiler, the sample, and the machine have each
earned it.

Thank you.

**DO**

Stop. Leave the slide up. Three minutes of Q&A.

---

## Reserve answers

Name the committed result file and the environment. Do not improvise a rerun
on stage. Every number below traces to `claims-ledger.md` or `demo/results/`.

### Numbers to memorise

| Number | What |
| --- | --- |
| **~73 ns** | OPERA connector bias |
| **−3.4%** | CPU on one large Datadog service, from PGO |
| **0.25 vs 11 ns · 0 vs 1 allocs** | DCE demo |
| **883 → 841 ns** | #4891, main vs branch |
| **43%** | swing, same binary |
| **4.75 / 18.88 / 5.25%** | local spread: idle / loaded / pinned, one run |
| **230% / 212% vs 150%** | #643 overhead vs ceiling |
| **~24% → 0.04%** | SMT on → off (~100×), AWS m5.metal |
| **0.38% → 0.04%** | DFS on → off (~10×), AWS m5.metal |

### Things to never say

* Do not put a figure on the OPERA oscillator fault.
* Do not call Docker Desktop on macOS hardware isolation.
* Do not claim statistical significance proves practical importance.
* Do not compare the laptop spread with the bare-metal numbers.
* Do not give Datadog hardware counts, budget figures, archetype names, or
  scale. Ledger row 23 permits the practice shape only.

### Setup

Present from the bespoke HTML if you want the reveals to animate:
`make serve/go-benchmarks-lying` → `localhost:8000/presentation.html`.
The PDF is a correct handout but shows every fragment at once.
