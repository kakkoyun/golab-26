---
marp: true
theme: golab
# fragment-floor: 3. `*` is the ONLY list marker allowed on slides. Every list
# is an intentional Marp reveal; a `-` bullet here is a bug. `make check/fragments`
# guards the count against formatters that rewrite markers.
math: mathjax
html: true
paginate: true
header: "Why Your Go Benchmarks Are Lying · GoLab 2026"
footer: " "
style: |
  .columns { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem; }
  .columns3 { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1rem; }
  .medium { font-size: 1.0em; }
  .small  { font-size: 0.8em; }
  .tiny   { font-size: 0.6em; }
  /* The theme sets `img { display: block }`, so text-align cannot centre an
     image. Block elements need auto margins. */
  .center img { margin-left: auto; margin-right: auto; }
  .hidden { visibility: hidden; }
  .hl-blue   { color: #00ADD8; font-weight: 700; }
  .hl-orange { color: #E8833A; font-weight: 700; }
  .centered-table table { margin-left: auto; margin-right: auto; }
  .comment { display: block; opacity: 0.45; font-size: 0.75em; line-height: 1.5; }
  .checklist { display: grid; grid-template-columns: auto 1fr; gap: 0.6rem 0.5rem; align-items: baseline; font-size: 30px; }
---

<!-- _class: title gopher-sage -->
<!-- _paginate: false -->
<!-- _header: "" -->

##### GoLab · 2026

# Why Your Go Benchmarks Are Lying

And How to Stop Them

### Kemal Akkoyun · Datadog

<!--
SAY

Every benchmark you write is a measurement system. Like any instrument, it
can be precise and still wrong.

Today I give you three questions. They turn a number into a measurement.

DO

Do not introduce yourself yet. Advance.
-->

---

## A benchmark bot comment

<div class="big center">

`BenchmarkOTLPProtoSize`

**6-9% slower than main**

</div>

<br>

<div class="center">

Nothing in the diff touches OTLP encoding.

**Would you fix it?**

</div>

<!--
SAY

June this year. dd-trace-go, the Datadog Go tracer. I restructure one file
and push.

The benchmark bot answers: `BenchmarkOTLPProtoSize` is six to nine percent
slower than main. Nothing in my diff goes near OTLP encoding.

So. Would you fix it?

Most of us would. We open a profiler, find something, and push a fix.

DO

Ask the question. Wait two seconds. Do not solve it. The answer comes in §03.
-->

---

<!-- _class: vcenter -->

## Why Datadog cares

<div class="columns">
<div>

### Our code, your process

Every ns comes out of a
customer's budget.

</div>
<div>

### <span class="hl-blue">−3.4%</span> CPU

on one large service, from PGO alone.

</div>
</div>

<div class="center">

![width:200](../assets/dd_speedlab_logo.png)

<span class="small">Datadog invests in performance testing internally. This talk is the spillover.</span>

</div>

### Overhead is product correctness

<!--
SAY

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

DO

Say the SpeedLab name once. Ledger row 30 permits the name and its existence
only. The practice comes in §05. The PGO number is one service, not all of
production. Ledger row 47.
-->

---

<!-- _class: section -->
<!-- _paginate: false -->

###### 01

# A Loose Cable

<!--
DO

Section budget 5:00, including the basics slide. Start by 3:00.
-->

---

## September 2011

<div class="center">

![width:660](../assets/particles-break-light-speed-headline.png)

</div>

<!--
SAY

September 2011. The OPERA experiment fires neutrinos from CERN to a detector
in Italy. The neutrinos arrive early. Faster than light.

If that is true, Einstein is wrong. The team knows it. Their coordinator says:
a result is never a discovery until other people confirm it.

So they publish, and they ask the world to find their mistake.

DO

Let the headline stand for a beat before you speak. Ledger row 46 holds the
quote.
-->

---

<!-- _class: vcenter -->

## "Trivial things we are

## clever enough to rule out."

<br>

<div class="center">

Antonio Ereditato, OPERA coordinator · *The Guardian*, 22 Sep 2011

</div>

<!--
SAY

And then he says this.

"If there is a problem, it must be a tough, nasty effect, because trivial
things we are clever enough to rule out."

Remember that sentence.

DO

Read the quote slowly. Pause after "rule out".
-->

---

## The cause

<div class="columns">
<div>

### A loose fibre connector

**~73 ns** early bias

A second fault pushed back
and *masked* it

<div class="small">

CERN, 22 Feb 2012 · Cartlidge,
*Science* 335(6072):1027

</div>

</div>
<div class="center">

![width:400](../assets/opera-loose-cable.png)

</div>
</div>

<!--
SAY

It was this. A fibre-optic connector, not fully seated, in the GPS timing
chain. Seventy-three nanoseconds of bias.

A trivial thing.

And a second fault pushed the other way and partly hid the first. The bug hid
behind another bug.

DO

Let them look at the photo first. Do not put a number on the second fault.
Ledger row 9.
-->

---

## Your cables

<div class="big">

compiler · statistics · machine

</div>

<!--
SAY

These physicists were not careless. They were very careful, and the
instrument was still wrong.

You have `testing.B`, a laptop, and thirty browser tabs. Your cables are the
compiler, the statistics, and the machine.
-->

---

<!-- _class: meme -->

![bg contain](../assets/meme-trust-nobody.png)

systematic error survives expert review

<!--
SAY

Which brings us to the only rule that matters today.

DO

Ten seconds. Do not explain the joke.
-->

---

## Three questions

<div class="big">

1. **Real work?**
2. **Stable sample?**
3. **Above the noise?**

</div>

<!--
SAY

Three questions.

Is the benchmark measuring real work?

Is my sample stable enough?

Is the difference bigger than the noise?

If you cannot answer all three, you do not have a measurement. You have a
number. We ask them on the laptop first, and then in CI.

DO

Pause after each question. The audience hears them again in every section.
-->

---

## One command, two habits

```bash
go test -bench=. -benchmem -count=10 ./...
```

###### bloop_bench_test.go

```text
BenchmarkHash_BLoop-16   6834830   356.2 ns/op   0 B/op   0 allocs/op
```

<div class="center big">

`-count=10`: one run is one draw.

`-benchmem`: always show allocations.

</div>

<!--
SAY

A quick reminder of the instrument. One command.

`-count=10`, because one run is one draw, not a measurement. `-benchmem`,
always, because allocations show what the code really did.

We need both in a minute.

DO

Thirty seconds. Do not teach the flags.
-->

---

<!-- _class: section -->
<!-- _paginate: false -->

###### 02

# Is It Real Work?

Question 1: real work?

<!--
DO

Section budget 6:00. Question 1: real work? Start by 8:00.
-->

---

## The compiler is not neutral

It sees the result is unused.

It removes the work, **correctly**.

<br>

<div class="big">

Your loop still runs `b.N` times.

It just runs empty.

</div>

<!--
SAY

Question one. Real work.

Your benchmark is just code. The compiler reads it, sees that you never use
the result, and removes the work. It is right to do that.

Your loop still runs `b.N` times. It just runs empty.
-->

---

## Dead-code elimination

###### dce_bench_test.go

```go
func makeBuffer(n int) []byte {
    return make([]byte, n) // heap-escaping allocation
}

func BenchmarkMakeBuffer_DCE(b *testing.B) {
    for range b.N {
        makeBuffer(64) // result discarded → call removed
    }
}
```

<!--
SAY

`makeBuffer` allocates sixty-four bytes. The benchmark calls it and throws
the result away.

Watch what happens.
-->

---

## `make bench-dce`

###### dce_bench_test.go

```text
DCE       0.2532 ns/op   0 B/op   0 allocs/op
correct  11.14   ns/op  64 B/op   1 allocs/op
```

<div class="center big">

`make([]byte, 64)` cannot skip allocating.

Yet: **0 allocs/op**

</div>

<!--
SAY

A quarter of a nanosecond, against eleven. It looks forty times faster.

Now look at the allocations. Zero. `make` cannot skip the allocation. Zero
allocations means the call is gone.

DO

Point at the allocations column.
-->

---

<!-- _class: vcenter -->

## `ns/op` can lie

## `allocs/op` cannot

<br>

<div class="center">

Always `-benchmem`.

</div>

<!--
SAY

Time can lie. A very fast function and an empty loop look the same.

An allocation happened, or it did not. `allocs/op` cannot lie.

Always pass `-benchmem`.

DO

Land this slowly. It is the most reusable line in the talk.
-->

---

<!-- _class: meme -->

![bg contain](../assets/meme-this-is-fine.png)

the compiler deleted your benchmark

<!--
SAY

Those are the real numbers from two slides ago.

DO

Ten seconds.
-->

---

## `b.Loop()` · Go 1.24, fixed in 1.26

###### bloop_bench_test.go

```go
func BenchmarkHash_BLoop(b *testing.B) {
    data := make([]byte, 1024)   // setup excluded automatically
    copy(data, payload)

    var s [32]byte
    for b.Loop() {
        s = sha256.Sum256(data)
    }
}
```

<div class="center">

Go 1.24 and 1.25 blocked inlining in the loop body.
**Go 1.26 removed that.** Upgrade before you compare.

</div>

<!--
SAY

The fix is `b.Loop`, from Go 1.24. Setup before the loop is not timed. The
loop body stays alive, so the compiler cannot delete it.

But there is a catch that many people missed. In 1.24 and 1.25, `b.Loop`
kept the body alive by blocking inlining. So your benchmark could allocate
where your production code does not.

Go 1.26 removed that. Upgrade before you compare.

DO

Ledger rows 39 and 40. Go 1.26 is the fix, not the regression. Do not say it
backwards.
-->

---

## What `b.Loop` removes

<div class="centered-table">

| | `for range b.N` | `for b.Loop()` |
| --- | --- | --- |
| ResetTimer at start | No | **Yes** |
| StopTimer at end | No | **Yes** |
| Setup re-runs on ramp-up | Yes | **No** |
| DCE prevented | No | **Yes** |

</div>

<div class="center">

Must be written literally as `b.Loop()`.

</div>

<!--
SAY

Two rows matter. Setup is not timed, and the body is not deleted.

Write `b.Loop()` literally in the loop condition. If you assign it to a
variable first, you lose the protection.

DO

Do not read the table. Point at two rows.
-->

---

<!-- _class: section -->
<!-- _paginate: false -->

###### 03

# The Regression That Was a Speedup

Question 2: stable sample?

<!--
DO

Section budget 7:00. Question 2: stable sample? Start by 14:00. This section
answers the opening question.
-->

---

## Read the benchmark first

###### dd-trace-go

```go
// The entire timed loop:
proto.Size(tracesData)
```

<div class="center">

Struct built **before** `ResetTimer`.

Calls **none** of the code the PR touched.

Locally: **<0.1%** run-to-run variance.

</div>

<!--
SAY

Back to the bot comment. Would you fix it?

I did not. First, I read the benchmark. This is the whole timed loop. One
call, `proto.Size`, on a struct built before the timer starts.

It calls none of the code I changed. And on my machine it was stable: under
zero point one percent from run to run.
-->

---

## Same machine, both branches

<div class="centered-table">

| Build | 1 span | 10 spans |
| --- | --- | --- |
| `main` | 883.3 ns | 7115 ns |
| `#4891` | <span class="hl-blue">840.7 ns</span> | <span class="hl-blue">6775 ns</span> |

</div>

<div class="center big">

**The PR was faster.** CI inverted the sign.

</div>

<!--
SAY

So I built both branches on the same machine and compared them.

Main: eight hundred eighty-three nanoseconds. My branch: eight hundred forty.

My branch was faster. CI did not get the size wrong. It got the sign wrong.

DO

Let this sit. It is the biggest surprise in the talk.
-->

---

## The mechanism

<div class="big">

Function addresses moved.

Cache lines and branch targets moved with them.

</div>

<br>

At sub-microsecond scale, alignment is worth several percent, **either direction**.

<div class="center">

**Resolution: no code change.**

</div>

<!--
SAY

Why? My change moved function addresses in the package. The hot loop moved
relative to cache lines and branch targets.

At this speed, that is worth several percent, in either direction. On a CI
runner that cannot pin its clock, that is enough to flip the verdict.

The fix: no code change. Nothing was wrong.
-->

---

## A known phenomenon

<div class="cols">
<div>

[**Performance Matters**](https://www.youtube.com/watch?v=r-TLSBdHe1A)
Emery Berger · Strange Loop 2019

<div class="big">

Code layout alone swings
performance **±10%**.

</div>

</div>
<div class="center">

![width:420](../assets/strangeloop19_emery_berger_performance_matters.png)

</div>
</div>

<!--
SAY

This is well known. Emery Berger's talk, Performance Matters, shows that code
layout alone can swing performance by ten percent. Watch it.
-->

---

<!-- _class: vcenter -->

## A noisy result can be

## **directionally wrong**

<br>

<div class="center">

It blocks good changes and waves regressions through.

</div>

<!--
SAY

So the lesson is not "CI is bad". A noisy result can point the wrong way.

It can block a good change. And it can let a real regression through.
-->

---

## One number is a point sample

###### noisy.txt

```text
BenchmarkMakeBuffer_Correct-16    41877204    39.39 ns/op
...
BenchmarkMakeBuffer_Correct-16    52521198    27.54 ns/op
```

<div class="center big">

Same binary. **43% swing.**

</div>

<!--
SAY

Here is how noisy one number is. Same binary, same machine. Thirty-nine
nanoseconds, then twenty-seven.

A forty-three percent swing, and nothing changed.

One run is one point. You need a sample.
-->

---

## `benchstat`

```bash
go test -bench=. -benchmem -count=10 . | tee new.txt
benchstat old.txt new.txt
```

<div class="center big">

Is B different from A, beyond the noise?

`~` means **no**. That is a result.

</div>

<div class="center">

It cannot tell you whether the **machine** is trustworthy.

</div>

<!--
SAY

The tool is `benchstat`. Run with `-count`, give it the old and the new
results, and it compares the two samples.

It answers one question: is B different from A, beyond the noise? A tilde
means no. That is a result. Do not rerun until you get the answer you want.

It cannot tell you whether the machine is trustworthy. If an unchanged
benchmark spreads by more than about five percent, fix the machine first.

DO

No formulas. Say why, not how.
-->

---

<!-- _class: meme -->

![bg contain](../assets/meme-two-buttons.png)

more samples will not fix a noisy machine

<!--
SAY

Only one of these buttons works.

DO

Ten seconds. The next section is about the other button.
-->

---

<!-- _class: section -->
<!-- _paginate: false -->

###### 04

# It Was the Machine

Question 3: above the noise?

<!--
DO

Section budget 5:00. Question 3: above the noise? Start by 21:00.
-->

---

## A second red number

<div class="centered-table">

| Scenario | Overhead | Ceiling |
| --- | --- | --- |
| `multi` | <span class="hl-blue">**230%**</span> | 150% |
| `largeidle` | <span class="hl-blue">**212%**</span> | 150% |

</div>

<div class="center">

A local run after a dependency fix. It looks like a serious regression.

</div>

<!--
SAY

Second story, three weeks later. OpenTelemetry Go compile-time
instrumentation. I land a dependency fix and run the overhead benchmark on my
laptop.

`multi`: two hundred thirty percent overhead, against a ceiling of one hundred
fifty. `largeidle`: two hundred twelve.

Both fail. It looks like I broke something badly.
-->

---

<!-- _class: vcenter -->

## `largeidle` shares

## **zero** changed dependencies

<br>

<div class="center big">

It cannot have regressed.

The common factor was the **machine**.

</div>

<!--
SAY

But my change touched dependencies in `multi` only. `largeidle` shares none
of them. It cannot have regressed. And it moved as much as `multi`.

When code that did not change gives a different result, the common factor is
the machine. I ran parallel builds all afternoon while I benchmarked.

That is the trick to take home: a control benchmark. Keep one benchmark that
your change cannot touch. If it moves, do not trust the others.

DO

The fix was to wait for CI. That job runs only in CI, on a dedicated runner.
-->

---

## The mirror image

<div class="columns">
<div>

### `#4891`

CI said slower.

The laptop was right.

Cause: **code layout**.

</div>
<div>

### `#643`

The laptop said slower.

CI was right.

Cause: **machine load**.

</div>
</div>

<div class="center big">

Neither environment is authoritative by default.

</div>

<div class="center">

Same tell: **a benchmark moved that could not have moved.**

</div>

<!--
SAY

Put the two stories side by side.

First: CI said slower, the laptop was right, and the cause was code layout.

Second: the laptop said slower, CI was right, and the cause was machine load.

Neither place is right by default. And the tell was the same both times: a
benchmark moved that could not have moved.

DO

This is the throughline. Say the last line slowly.
-->

---

## What does isolation actually buy?

<div class="centered-table">

| Condition | mean ns/op | **spread** |
| --- | --- | --- |
| idle host | 11.46 | **4.75%** |
| + 16 spinners | 34.97 | <span class="hl-blue">**18.88%**</span> |
| pinned container, same load | 16.28 | <span class="hl-orange">**5.25%**</span> |

</div>

<div class="small center">

One local run, August 2026 · Apple M4 Max · container under
Apple Virtualization.framework · `demo/results/cv-summary.txt`

</div>

<!--
SAY

"Run it in a container" is common advice. So we measured what it buys, on
this laptop.

Idle: under five percent spread. Add sixteen background spinners: three
times slower, four times noisier. Pin the benchmark in a container under the
same load: the spread goes back to about the idle level.

DO

This is one local run from August. Do not call it a general result. The
platform details are on the slide if someone asks.
-->

---

<!-- _class: vcenter -->

## 5.25% is not a triumph

## It is a ceiling

<br>

<div class="center">

On this laptop, a change smaller than the spread is invisible.

</div>

<!--
SAY

Five percent is not a good number. It is the best this laptop can do.

A change smaller than that is invisible here. For a smaller change, you need
a different machine. That is the next section.

DO

Do not compare this number with the bare-metal results. They come from a
different benchmark on a different machine. Ledger row 8.
-->

---

## The macOS caveat

* `--cpuset-cpus=0` pins a **vCPU inside a VM**
* The VM can still migrate it across physical cores
* Nothing inside can disable host SMT or pin the clock

<br>

<div class="center">

**Get:** isolation from neighbours. **Don't get:** controlled hardware.

</div>

<!--
SAY

One caveat. On macOS, Docker runs in a Linux VM. `--cpuset-cpus` pins a
virtual CPU.

The VM can still move it across physical cores. Nothing in the container can
turn off SMT or pin the clock.

You get isolation from your other processes. You do not get controlled
hardware.

DO

Do not soften this.
-->

---

<!-- _class: section -->
<!-- _paginate: false -->

###### 05

# How We Run It at Datadog

Question 3, at hardware scale.

<!--
DO

Section budget 7:30. Start by 26:00.
-->

---

## What we do at Datadog

<div class="cols">
<div class="card">

### Dedicated hardware

not shared runners

</div>
<div class="card measure">

### An overhead budget

per SDK

</div>
<div class="card measure">

### Several workloads

per SDK

</div>
<div class="card">

### Gate the release

not only the PR

</div>
</div>

<!--
SAY

So how do we do this at Datadog, where overhead is the product? Four things.

Dedicated hardware, not shared CI runners. An overhead budget for each SDK.
Several workloads for each SDK, not one. And we gate the release, not only
the pull request.

Let me show you why each one is there.

DO

Ledger row 23. Say the practice shape only. Give no hardware counts, budget
figures, archetype names, or scale. If someone asks for numbers, say that
they are internal.
-->

---

## Why not just add more runners?

<div class="center">

Shared runners hide real regressions and invent phantom ones.

</div>

> There is often only one physical machine for some configurations, and often backlogged with work […]

<div class="center">

The Go project, about its **performance** builders.

<span class="small">[go.dev/wiki/SlowBots](https://go.dev/wiki/SlowBots)</span>

</div>

<!--
SAY

First, the hardware. Shared runners have neighbours, changing clocks, and
shared caches. A real regression can vanish, and a fake one can appear.

So why not add more runners? Read what the Go project says about its
performance builders. Often there is only one physical machine, with a
backlog of work.

More capacity helps correctness. Performance needs the scarce machine.

DO

Read the quote aloud. Ledger row 38.
-->

---

## What's the impact of disabling SMT?

<div class="columns">
<div>

![width:430](../assets/environment-control-smt-experiment.svg)

</div>
<div class="center big">

Spread: <span class="hl-blue">**~24%**</span> → <span class="hl-orange">**0.04%**</span>

**~100× less variance**, and twice as fast.

</div>
</div>

<div class="small center">

AWS m5.metal, FOSDEM 2026 experiment

</div>

<!--
SAY

What does dedicated hardware buy? These are the experiments behind our
FOSDEM talk. Two CPU-bound tasks, on the same physical core, then on separate
cores.

Spread: twenty-four percent with SMT on. Zero point zero four with it off.
About a hundred times less variance. And twice as fast, because the core is
no longer shared.
-->

---

## What's the impact of disabling DFS?

<div class="columns">
<div>

![width:430](../assets/environment-control-dfs-experiment.svg)

</div>
<div class="center big">

Spread: <span class="hl-blue">**0.38%**</span> → <span class="hl-orange">**0.04%**</span>

**~10× less variance**, and the mean got *slower*.

</div>
</div>

<div class="small center">

AWS m5.metal, FOSDEM 2026 experiment

</div>

<!--
SAY

Now frequency scaling. Turn it off: ten times less variance.

And the mean got slower. Turbo is fast, and inconsistent. A benchmark must be
comparable. It does not need to be fast.
-->

---

## Three sysfs writes

```bash
echo off         | sudo tee /sys/devices/system/cpu/smt/control
echo performance | sudo tee /sys/.../scaling_governor
echo 0           | sudo tee /sys/devices/system/cpu/cpufreq/boost
```

<div class="columns">
<div>

### Bare metal

Spread ~24% → **0.04%**

</div>
<div>

### In a VM

The write may **succeed
and be ignored**.

</div>
</div>

<!--
SAY

All of that is three writes. Turn off SMT. Pin the governor. Turn off boost.

On bare metal, the spread goes from about twenty-four percent to zero point
zero four.

In a VM, the write can succeed and do nothing. That is worse than an error.
-->

---

## Workload archetypes

<div class="centered-table">

| Archetype | Pattern | Shape |
| --- | --- | --- |
| **Idle** | background workers | low RPS, low CPU |
| **Latency** | microservices, APIs | high RPS, low CPU/req |
| **Throughput** | queues, batch | high CPU, many clients |
| **Enterprise** | business apps + DB | mixed CPU / I/O |

</div>

<div class="center">

`largeidle` is Idle. `multi` is Enterprise. Both moved:
**shared environment, not shared cause.**

</div>

<!--
SAY

Second, the workloads. One workload is not representative. Our FOSDEM talk
describes four archetypes. Idle: background workers. Latency: APIs with many
small requests. Throughput: queues and batch jobs. Enterprise: business apps
with a database.

Remember the second story. `largeidle` is Idle. `multi` is Enterprise.
Different code, same movement, same moment. That is a shared environment,
not a shared cause.

DO

Ledger row 20. Do not say which archetypes Datadog runs.
-->

---

## A macro gate is a budget

```text
scenario: multi
baseline: uninstrumented process
ceiling:  150% overhead
result:   230%   → FAIL
```

<div class="center">

Micro gates compare commits. Macro gates compare against a **budget**.

</div>

<!--
SAY

Third, the budget. A micro gate compares two commits. A macro gate compares
against a budget: a ceiling that you must not cross.

That is a product decision, not a statistics question. How much of the
customer's machine may we take?

DO

The example values come from the second story, not from Datadog budgets.
-->

---

<!-- _class: section -->
<!-- _paginate: false -->

###### 06

# Detecting Change Over Time

Question 2, across days.

<!--
DO

Section budget 4:00. Question 2, across days. Start by 33:30.
-->

---

<!-- _class: vcenter -->

## A/B is the wrong model for CI

<div class="center big">

Benchstat compares **two** distributions.

CI has a **time series**.

</div>

<br>

<div class="center">

Comparing to the parent commit misses slow drift entirely.

</div>

<!--
SAY

Fourth, time. `benchstat` compares two samples. CI does not have two samples.
It has a time series: one result per commit, for months, with hardware
changes and dependency updates in between.

If you compare each commit with its parent, you ask the noise question every
time. And you miss slow drift completely.
-->

---

## What regressions look like

<div class="columns">
<div>

### In a slide deck

![width:430](../assets/ideal-performance-regression.png)

</div>
<div>

### In real data

![width:430](../assets/actual-performance-regression.png)

</div>
</div>

<!--
SAY

This is how we draw a regression on a slide. This is what it looks like in
real data.

A step change is clear in a drawing. In real data, it hides in the noise.
-->

---

## Change-point detection

<div class="big center">

Not *"slower than its parent?"*

But *"where did it shift and stay shifted?"*

</div>

<div class="columns">
<div>

### Why

Finds lasting shifts.

Ignores one-off spikes.

</div>
<div>

### Implementations

**ED-PELT** · Akinshin

**e-divisive** · Apache Otava, Nyrkiö

Netflix, at scale

</div>
</div>

<!--
SAY

So ask a different question. Not "is this commit slower than its parent?"
Ask "where did the history shift, and stay shifted?"

That is change-point detection. It finds lasting shifts and ignores one-off
spikes. Apache Otava implements it. Netflix wrote about doing this at scale.

It needs history, so it belongs in a nightly job, not in the PR gate.

DO

No statistics. Say what it finds, not how.
-->

---

## Why a baseline, not a pair

<div class="small">

> We never report performance numbers in isolation, and only relative to some
> baseline. […] The state of a machine or VM on one day is likely to be very
> different than the state of a machine or VM on the next day.

</div>

<div class="center">

That is the Go team, about **their own hardware**.

[go.dev/wiki/PerformanceMonitoring](https://go.dev/wiki/PerformanceMonitoring)

</div>

<!--
SAY

The Go team says why, about their own hardware. They never report a number
alone, only relative to a baseline. Because the machine on one day is very
different from the same machine the next day.

If that is true for the Go team, it is true for your CI runner.

DO

Read the quote aloud.
-->

---

## Two patterns

<div class="columns">
<div>

### PR gate

Fast. Strict. Every PR.

Benchmarks that regressed before.

`-count=6`, same-machine A/B

</div>
<div>

### Nightly

Complete. Pinned runner.

All controls applied.

`-count=20`, change-point detection

</div>
</div>

<div class="center">

CI **detects**. A controlled machine **explains**.

</div>

<!--
SAY

So, two patterns. A PR gate: fast and strict. A small set of benchmarks that
regressed before, a same-machine A/B, and a tight threshold.

A nightly suite: complete and slow. Pinned hardware, all controls on, and
change-point detection. Before a release, the budget gate.

CI detects. To explain a result, you still measure on a controlled machine.
-->

---

## Keep a ledger of false positives

<div class="small">

> Known `BenchmarkOTLPProtoSize` false positive, documented for #4891 as a
> same-package code-layout artifact. Touches no code I changed;
> local A/B was ~+0.3%. No action.

</div>

<div class="center big">

Documented noise is **benchmark hygiene**.

</div>

<!--
SAY

The last practice is the cheapest. Remember the first bot comment? The same
benchmark fired again eleven days later, on another pull request.

That time, one comment closed it, because the first investigation was
written down. Without that note, the next person repeats the investigation.
Or worse, they "fix" it.

Write down every false alarm.

DO

Budget 1:00. Start by 37:30.
-->

---

## The minimum viable discipline

```bash
# 1. Use b.Loop and read allocs/op.
# 2. Run enough samples.
go test -bench=. -benchmem -count=10 | tee new.txt
benchstat old.txt new.txt
# 3. Add a control benchmark your change cannot touch.
```

<div class="center big">

Under an hour.

</div>

<!--
SAY

If you take one slide home, take this one.

Use `b.Loop` and read allocations. Run enough samples and compare with
`benchstat`. Add one control benchmark that your change cannot touch.

That is under an hour of work.
-->

---

## Three questions, two scales

<div class="centered-table">

| | Laptop + micro | CI + macro |
| --- | --- | --- |
| **Real work?** | `b.Loop` · `-benchmem` | archetypes · budgets |
| **Stable sample?** | `-count=10` · benchstat | time series · change points |
| **Above noise?** | control benchmark · know the ceiling | bare metal · SMT + DFS off |

</div>

<div class="center">

A sub-10% micro delta can be layout noise.
A shared runner cannot be fixed with more samples.

</div>

<!--
SAY

Three questions, two scales.

Real work: `b.Loop` on the laptop. Real workloads and budgets in CI.

Stable sample: ten runs and `benchstat`. Then a time series with change
points.

Above the noise: a control benchmark and a known ceiling. Then bare metal
with SMT and boost off.

A sub-ten-percent micro delta can be layout noise. A shared runner cannot be
fixed with more samples.

DO

Say the last two lines slowly.
-->

---

<!-- _class: dark -->

# Take it with you

<div class="columns">
<div>

### Check my numbers

[Talk repo: decks, script, captured results](https://github.com/kakkoyun/golab-26)

[Earlier FOSDEM version](https://youtu.be/8211fNI_nc4)

</div>
<div class="center">

![w:250](../../assets/golab-26-repo-qr.png)

**Scan for the talk repo**

</div>
</div>

<!--
SAY

The talk repo is the QR code. It has the deck, the script, and every captured
result, so you can check my numbers.

The earlier FOSDEM talk is there too, if you want the language-neutral
version.
-->

---

<!-- _class: end gopher-rocket -->
<!-- _paginate: false -->

# Questions?

[kakkoyun.me](https://kakkoyun.me) · [github.com/kakkoyun](https://github.com/kakkoyun)

[linkedin.com/in/kakkoyun](https://www.linkedin.com/in/kakkoyun/) · [bsky.app/profile/kakkoyun.me](https://bsky.app/profile/kakkoyun.me) · [x.com/kakkoyun_me](https://x.com/kakkoyun_me)

<span class="small">Talk repo [github.com/kakkoyun/golab-26](https://github.com/kakkoyun/golab-26)</span>

<!--
SAY

OPERA's coordinator was right. A result is not a discovery until someone
else confirms it. That includes your benchmarks.

Trust a number only after the compiler, the sample, and the machine have each
earned it.

Thank you.

DO

Stop. Leave the slide up. Three minutes of Q&A.
-->
