---
marp: true
theme: golab
# fragment-floor: 17. `*` is the ONLY list marker allowed on slides. Every list
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

---

## A benchmark bot comment

<div class="big center">

`BenchmarkOTLPProtoSize`

**6-9% slower than main**

</div>

<br>

<div class="center">

Nothing in the diff touches OTLP encoding.

**Hold that thought.**

</div>

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

### <span class="hl-blue">−3.4%</span> production CPU

from PGO alone.

</div>
</div>

<div class="center">

![width:200](../assets/dd_speedlab_logo.png)

<span class="small">Datadog invests in performance testing internally. This talk is the spillover.</span>

</div>

### Overhead is product correctness

---

<!-- _class: section -->
<!-- _paginate: false -->

###### 01

# A Loose Cable

---

## September 2011

<div class="center">

![width:660](../assets/particles-break-light-speed-headline.png)

</div>

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

---

<!-- _class: vcenter -->

## Systematic error

## hides in plain sight

<br>

It looks like signal.

It survives expert review.

---

## Your cables

<div class="big">

compiler · scheduler · statistics

</div>

---

<!-- _class: meme -->

![bg contain](../assets/meme-trust-nobody.png)

systematic error survives expert review

---

## Three questions

<div class="big">

1. **Real work?**
2. **Stable sample?**
3. **Above the noise?**

</div>

---

## Running one

```bash
go test -bench=. -benchmem -count=10 -benchtime=1s ./...
```

* `-bench`: what to run (`.` = all)
* `-benchmem`: show allocs (always on)
* `-count`: repetitions; `-count=1` is the default mistake
* `-benchtime`: duration, or `Nx` fixed iterations

`-count=1` is one draw from the distribution.

---

## Reading the output

###### bloop_bench_test.go

```text
BenchmarkHash_BLoop-16   6834830   356.2 ns/op   0 B/op   0 allocs/op
```

* `ns/op`: time per iteration (has a floor; can lie)
* `B/op`: bytes allocated per iteration
* `allocs/op`: allocations per iteration (cannot lie)

`ns/op` can lie. `allocs/op` cannot.

---

<!-- _class: section -->
<!-- _paginate: false -->

###### 02

# Making the Compiler Honest

Question 1: real work?

---

<!-- _class: vcenter -->

## Stop the compiler

## deleting your work

<br>

<span class="chip caution">TEST-ONLY SCAFFOLDING</span>

---

## The compiler is not neutral

It sees the result is unused.

It removes the work, **correctly**.

<br>

<div class="big">

Your loop still runs `b.N` times.

It just runs empty.

</div>

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

---

<!-- _class: vcenter -->

## `ns/op` can lie

## `allocs/op` cannot

<br>

<div class="center">

Always `-benchmem`.

</div>

---

<!-- _class: meme -->

![bg contain](../assets/meme-this-is-fine.png)

the compiler deleted your benchmark

---

## `b.Loop()` · Go 1.24

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

<div class="small">

Proposal #61515 · Austin Clements

</div>

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

---

<!-- _class: section -->
<!-- _paginate: false -->

###### 03

# The Regression That Was a Speedup

Question 2: stable sample?

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

---

## The mechanism

<div class="big">

Function addresses moved.

Cache lines and branch targets moved with them.

</div>

<br>

At ~390 ns/iteration, alignment is worth several percent, **either direction**.

<div class="center">

**Resolution: no code change.**

</div>

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

---

<!-- _class: vcenter -->

## A noisy result can be

## **directionally wrong**

<br>

<div class="center">

It blocks good changes and waves regressions through.

</div>

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

---

## `benchstat`

```bash
go test -bench=. -benchmem -count=20 . | tee new.txt
benchstat old.txt new.txt
```

<div class="centered-table">

| Environment | sec/op | Difference |
| --- | --- | --- |
| idle | `11.32n ± 5%` | n/a |
| noisy | `37.40n ± 25%` | `+230.34% (p=0.000)` |

</div>

---

## Read the output

* `11.32n`: the **median**
* `± 5%`: spread
* `p=0.000`: distinguishable from noise
* `~`: **no measurable difference.** That is a result.

---

## What `benchstat` won't tell you

<div class="checklist">
<div>✅</div><div>Is A different from B?</div>
<div>❌</div><div>Is this machine trustworthy?</div>
</div>

<br>

$$ CV = \frac{\sigma}{\mu} $$

<div class="center">

Benchstat compares distributions. **CV characterises the machine.**

</div>

---

## Rules of thumb

<div class="centered-table">

| Question | Answer |
| --- | --- |
| How many runs? | `-count=10` floor, 20 better |
| Most reproducible? | `-benchtime=100x` |
| CV too high? | **>5%: fix the machine first** |
| Significant but tiny? | Different question |

</div>

---

<!-- _class: meme -->

![bg contain](../assets/meme-two-buttons.png)

more samples will not fix a noisy machine

---

<!-- _class: section -->
<!-- _paginate: false -->

###### 04

# The Machine Was the Variable

Question 3: above the noise?

---

## A second bot comment

<div class="centered-table">

| Scenario | Overhead | Ceiling |
| --- | --- | --- |
| `multi` | <span class="hl-blue">**230%**</span> | 150% |
| `largeidle` | <span class="hl-blue">**212%**</span> | 150% |

</div>

<div class="center">

The fix looks like a serious regression.

</div>

---

<!-- _class: vcenter -->

## `largeidle` shares

## **zero** changed dependencies

<br>

<div class="center big">

It cannot have regressed.

The common factor was the **machine**.

</div>

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

---

## What does isolation actually buy?

<div class="centered-table">

| Condition | mean ns/op | **CV%** |
| --- | --- | --- |
| idle host | 11.46 | **4.75** |
| + 16 spinners | 34.97 | <span class="hl-blue">**18.88**</span> |
| pinned container, same load | 16.28 | <span class="hl-orange">**5.25**</span> |

</div>

<div class="small center">

Apple M4 Max · darwin/**arm64** · container linux/**arm64** under
Apple Virtualization.framework · no QEMU, no emulation

</div>

---

<!-- _class: vcenter -->

## 5.25% is not a triumph

## It is a ceiling

<br>

<div class="center big">

Bare-metal Linux, SMT off: **~0.05%**

</div>

---

## The macOS caveat

* `--cpuset-cpus=0` pins a **vCPU inside a VM**
* The VM can still migrate it across physical cores
* Nothing inside can disable host SMT or pin the clock

<br>

<div class="center">

**Get:** isolation from neighbours. **Don't get:** controlled hardware.

</div>

---

<!-- _class: section -->
<!-- _paginate: false -->

###### 05

# How We Run It at Datadog

Question 3, at hardware scale.

---

<!-- _class: vcenter -->

## Why shared runners lie

<div class="center big">

A real 10% regression **vanishes**.

A phantom 10% regression **appears**.

</div>

<br>

<div class="center">

An **environment** problem, not a statistics problem.

</div>

---

## Why not just add more runners?

<div class="center">

![width:1000](../assets/golang_slowbot_quote.png)

</div>

<div class="center">

Elastic capacity is fine for correctness.
Performance needs the **scarce** machine.

<span class="small">[go.dev/wiki/SlowBots](https://go.dev/wiki/SlowBots)</span>

</div>

---

## What's the impact of disabling SMT?

<div class="columns">
<div>

![width:430](../assets/environment-control-smt-experiment.svg)

</div>
<div>

| Task | mean ± stddev | CV |
| --- | --- | --- |
| smt-1 | 1537.64 ± 367.29 | <span class="hl-blue">23.887%</span> |
| smt-2 | 1536.88 ± 366.84 | <span class="hl-blue">23.869%</span> |
| no-smt-1 | 737.37 ± 0.32 | <span class="hl-orange">0.044%</span> |
| no-smt-2 | 737.93 ± 1.74 | <span class="hl-orange">0.235%</span> |

</div>
</div>

<div class="center big">

**~100× less variance**, and twice as fast.

</div>

---

## What's the impact of disabling DFS?

<div class="columns">
<div>

![width:430](../assets/environment-control-dfs-experiment.svg)

</div>
<div>

| Configuration | mean ± stddev | CV |
| --- | --- | --- |
| DFS on | 533.97 ± 2.046 | <span class="hl-blue">0.383%</span> |
| DFS off | 738.18 ± 0.306 | <span class="hl-orange">0.041%</span> |

</div>
</div>

<div class="center big">

**~10× less variance**, and the mean got *slower*.

</div>

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

CV ~23% → **~0.05%**

</div>
<div>

### In a VM

The write may **succeed
and be ignored**.

</div>
</div>

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

---

## Why `largeidle` falsified `multi`

<div class="columns">
<div>

### `largeidle`

**Idle** archetype

</div>
<div>

### `multi`

**Enterprise** archetype

</div>
</div>

<br>

<div class="center big">

Different code. Same movement. Same moment.

**Shared environment, not shared cause.**

</div>

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

---

<!-- _class: section -->
<!-- _paginate: false -->

###### 06

# Detecting Change Over Time

Question 2, across days.

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

---

## Change-point detection

<div class="big center">

Not *"slower than its parent?"*

But *"where did it shift and stay shifted?"*

</div>

<div class="columns">
<div>

### Properties

* Non-normal data
* Multiple change points
* Ignores one-off spikes

</div>
<div>

### Implementations

**ED-PELT** · Akinshin

**e-divisive** · Apache Otava, Nyrkiö

Netflix, at scale

</div>
</div>

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

CI **detects**. It is not your primary measurement.

</div>

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

---

## The minimum viable discipline

```bash
# 1. Add a sink.
# 2. Run enough samples.
go test -bench=. -benchmem -count=10 | tee new.txt
benchstat old.txt new.txt
# 3. Check the machine before you believe it.
benchenv
```

<div class="center big">

Under an hour.

</div>

---

## Three questions, two scales

<div class="centered-table">

| | Local + micro | CI + macro |
| --- | --- | --- |
| **Real work?** | sink · `-benchmem` · `b.Loop` | archetype · pinned inputs |
| **Stable sample?** | `-count=10` · benchstat · CV | time series · change points |
| **Above noise?** | pin it · know the ceiling | bare metal · SMT + DFS off |

</div>

<div class="center">

A sub-10% micro delta can be layout noise.
A shared runner cannot be fixed with more samples.

</div>

---

<!-- _class: dark -->

# Take it with you

<div class="columns">
<div>

### Benchmarks you can audit

[github.com/kakkoyun/benchlab](https://github.com/kakkoyun/benchlab)

`honestbench` · `benchgate` · `benchenv` · Agent Skills

[Talk repo, decks, captured results](https://github.com/kakkoyun/golab-26)

[Earlier FOSDEM version](https://youtu.be/8211fNI_nc4)

</div>
<div class="center">

![w:250](../../assets/golab-26-repo-qr.png)

**Scan for the talk repo**

</div>
</div>

---

<!-- _class: end gopher-rocket -->
<!-- _paginate: false -->

# Questions?

[kakkoyun.me](https://kakkoyun.me) · [github.com/kakkoyun](https://github.com/kakkoyun)

[linkedin.com/in/kakkoyun](https://www.linkedin.com/in/kakkoyun/) · [bsky.app/profile/kakkoyun.me](https://bsky.app/profile/kakkoyun.me) · [x.com/kakkoyun_me](https://x.com/kakkoyun_me)

<span class="small">Talk repo [github.com/kakkoyun/golab-26](https://github.com/kakkoyun/golab-26) · Tools [github.com/kakkoyun/benchlab](https://github.com/kakkoyun/benchlab)</span>
