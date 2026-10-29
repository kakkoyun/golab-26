# Script: Why Your Go Benchmarks Are Lying

GoLab 2026. 45-minute slot: 38 minutes presented, 7 minutes Q&A. 105 pages.
Intermediate Go audience.

**How to use this.** `SAY` lines are the words. They are written to be spoken,
not read. Use short sentences, with one idea each. You do not need them verbatim. Learn
the **beat** (the bold line before each block) and the numbers, and the words
will come. `DO` lines are delivery, not content.

**Memorise in this order:** the 16 beats → the three questions → the two
stories → the numbers. Everything else is recoverable on stage.

---

## The 16 beats

| # | Section | The one thing |
| --- | --- | --- |
| 01 | Why Benchmark? | Speed is a product decision |
| 02 | Why I Care | Consequences, not credentials |
| 03 | A Loose Cable | Careful people ship broken measurements |
| 04 | Before You Measure | Pick the target before the tool |
| 05 | Benchmarking, Quickly | The instrument we are about to distrust |
| 06 | Local and Micro | Trust the laptop first |
| 07 | Compiler Honest | The compiler deletes your work |
| 08 | Regression That Was a Speedup | Noise can be directionally wrong |
| 09 | Statistics | One number is not a measurement |
| 10 | Local Reproduction | Know your noise ceiling |
| 11 | CI and Macro | Same questions, hardware answers |
| 12 | Macrobenchmark Design | Representative is the hard part |
| 13 | CI Environment | Three sysfs writes buy 100× |
| 14 | Change Over Time | A/B cannot see drift |
| 15 | Wiring Into CI | Detect, do not measure |
| 16 | Wire It Up | Under an hour |

**Checkpoints:** §05 by 8:15 · §06 by 10:45 · §11 by 22:45 · §16 by 33:30 · finish by 36:00. If §11 has not started by 25:00, apply the cut ladder in `outline.md`.

> **Note.** The section times are a word-count model: SAY words at 130 words
> per minute, plus 25% for reveals, pauses, and visuals. Nobody has timed this
> cut yet. The timed read-through in `TODO.md` replaces the model.

---

## 01 · Why Benchmark? — 3:30

### Title slide

> **SAY:** Every benchmark you have ever written is a measurement system.
> Most of them are lying to you by default, not on purpose. I want to give
> you three questions that turn a number into something you can trust.

`DO` Do not introduce yourself yet. The personal context is §02.

### Measure customer happiness, not CPU usage

**Beat: the frame for the whole section.**

> **SAY:** I start with the user. The number you are chasing is not CPU
> usage, or allocations, or requests per second. It is whether your user is
> happy. Everything else is a proxy. A benchmark measures the proxy.

`DO` Emphasize this point, then continue directly to "is it actually slow".

### Is it actually slow?

> **SAY:** Before you write a single benchmark: check it is actually slow, in
> production. In-process, that is pprof, or a continuous profiler. Across the
> whole system, the OpenTelemetry eBPF profiler or Parca, and your p99.
>
> Benchmark the path your production evidence says is hot. Not the one that
> looks interesting.

### Could it go faster?

**Beat: slow ≠ improvable.**

> **SAY:** So you found it is slow. Next question: can it actually go
> faster? Slow does not mean improvable. The ceiling is memory bandwidth,
> instruction latency, the physics of the machine. Headroom is the gap
> between where you are and that ceiling. Without headroom, skip "is it
> worth it". You cannot optimize past the physics.

### Is it worth optimizing? (reveal)

> **SAY:** Decide what done looks like, or you will never stop.
>
> An SLO is a target, not a wish. If you are inside your error budget,
> optimizing is optional. Go fix something else. And Amdahl: only the hot
> path pays. Ten percent off code that runs one percent of the time is
> nothing.

### Latency and throughput (two-step reveal)

> **SAY:** Two words that people use interchangeably.
>
> *(reveal 1)* Latency is one operation, start to finish. That is what a
> user feels.
>
> *(reveal 2)* Throughput is operations per second. That is your ceiling.
>
> You can improve one and damage the other. Batching raises throughput and
> makes latency worse.

### The cost of slowness

**Beat: this is a product decision, not an engineering one.**

> **SAY:** Rough thresholds. Under two hundred milliseconds, nobody notices.
> Half a second, it feels a bit slow. Past a second, people notice they are
> waiting. Past five, they leave.
>
> Google measured this directly. Half a second of extra latency cost them
> twenty percent of search traffic.

`DO` Attribute to "the Google search team". Not Marissa Mayer.

### Finding what to optimize

> **SAY:** If you want the "what to optimize" half properly, Daniel Martí
> gave it at GopherCon 2019 and it is still the best talk on it. He covers
> what to optimize. I cover whether you can believe the number when you get
> there.

---

## 02 · Why I Care — 1:00

### How I got here

`DO` Thirty seconds. Consequences, not achievements. No titles, no counts.

> **SAY:** I maintained `client_golang`. Every allocation I added landed in
> somebody's scrape budget. Then Parca, where a profiler that costs five
> percent CPU is a profiler nobody deploys. Now Go instrumentation at
> Datadog, where our SDKs run inside *your* process.
>
> Every one of those jobs punished me for trusting a benchmark I did not
> question.

### Why Datadog cares

> **SAY:** Our code runs in your process. Every nanosecond we spend comes
> out of your budget, not ours. Measurement is product correctness for us.
>
> One public number: profile-guided optimization took three point four
> percent off production CPU. You only get to claim that if you can measure
> it.

`DO` The SpeedLab logo is on screen as proof of investment. Say the name once
and the framing line: Datadog invests in performance testing internally,
and this talk is the spillover. Then continue. Do not ad-lib hardware, budgets,
archetypes, gating, or scale. Ledger row 30 permits only the name and
existence. Row 23 (internal macro practice) stays `pending` and out of scope.

---

## 03 · A Loose Cable — 2:30

`DO` Keep this story connected to the three questions. Keep the §02 biography
separate from the story.

### September 2011 (headline image)

**Beat: a careful team, an extraordinary result.**

> **SAY:** In 2011 a team of physicists announced that neutrinos travelled
> faster than light. The OPERA collaboration fired neutrinos from CERN to a
> detector in Italy, 730 kilometres away. The neutrinos arrived early.
> Faster than light. They did not publish immediately. They spent months
> rechecking the maths, the sensors, and the calibration. Then they
> published, and asked the world for help.

### The cause (connector photo)

**Beat: it was a cable.**

`DO` Let them look at the photo for a beat before you speak.

> **SAY:** It was this. A fibre-optic connector, not quite seated, in the
> GPS timing chain. Seventy-three nanoseconds of bias. That was the whole
> result.
>
> I love this part. A *second* fault, an oscillator, pushed the other way.
> The two errors partially cancelled. The bug hid behind another bug.

`DO` Do not put a number on the oscillator. Ledger row 9.

### Systematic error hides in plain sight

**Beat: the lesson, stated plainly.**

> **SAY:** The physicists were not careless. They were the opposite. A
> precise instrument can be confidently wrong, and stay wrong, through
> months of expert review.

### Your cables

> **SAY:** OPERA had an international collaboration and fifteen thousand tonnes
> of detector. You have `testing.B`, a laptop, and thirty Chrome tabs. Your
> cables are the compiler, the scheduler, and your statistics. Let's go find
> them.

### systematic error survives expert review

`DO` Show the meme. Say the one line, let them laugh, then continue.
**Ten seconds, not thirty.** If you explain the joke, you lose the time you save.

> **SAY:** Which brings us to the only rule that matters today.

### Three questions

**Beat: the contract for the next fifty minutes.**

`DO` Pause after each question. These questions connect the talk. The audience
should hear them four times today.

> **SAY:** Three questions. Is the benchmark measuring real work? Is my sample
> stable enough? And is the difference big compared to the noise?
>
> If you cannot answer all three, you do not have a measurement. You have a
> number.

### Two scales, same three questions

> **SAY:** We ask them twice. First half: your laptop, `testing.B`,
> microbenchmarks. Second half: CI, whole workloads, over time.
>
> Same questions, different answers, because they fail differently.
> Microbenchmarks usually fail on being *representative*. Macrobenchmarks
> usually fail on being *repeatable*. You will leave with the checks for
> both, and three small tools that automate them.

---

## 04 · Before You Measure — 1:15

### Every benchmark needs

**Beat: the frame for the whole talk.**

> **SAY:** Two properties. Representative: it does what production does.
> Repeatable: run it again, get the same answer.
>
> Hold those two words. Almost every failure in this talk breaks one of
> these properties.

### Micro vs macro (two-step reveal)

> **SAY:** *(reveal 1)* Microbenchmarks isolate a function. Nanosecond
> precision. Very easy for the compiler to cheat. Their risk is being *not
> representative*: beautifully precise measurement of something that never
> happens.
>
> *(reveal 2)* Macrobenchmarks run the real workflow. Realistic. Their risk
> is attribution. Something moved, good luck finding out what.

`DO` This replaces the old "this talk is only microbenchmarks" line. Do not
reintroduce it.

### Start macro, then drill

**Beat: the concrete answer to "so what do I do".**

> **SAY:** Macro first: does the workload actually move? Then profile to
> find which component. Then micro on that component, where you can iterate
> in seconds. Then macro again to confirm it survived.
>
> And the order that wastes a fortnight: make a function forty percent
> faster, ship it, watch nothing change, and never find out why.

---

## 05 · Benchmarking, Quickly — 2:30

**Beat: shared vocabulary for the room. Here is the instrument we are
about to distrust.**

`DO` Give a short review, not a tutorial. Most of the room has written a
benchmark. Name the parts, identify the default mistake, then continue.

### Writing one

> **SAY:** One slide on the shape, before we distrust this instrument. A
> `testing.B` benchmark is a function. Setup before the loop is excluded
> from timing. The loop is `b.Loop`, the measured body. The result has to
> sink somewhere the compiler can see, or the body vanishes. We spend the
> next section on that last part.

### Running one

> **SAY:** `-bench` picks what runs. `-benchmem` shows allocations. Leave it
> on, always. `-count` is how many times you repeat, and `-count=1` is the
> default mistake: one run is one draw from a distribution, not a
> measurement. `-benchtime` is either a duration or a fixed iteration count.
> We return to `-count` in the statistics section.

### Reading the output

> **SAY:** Three columns. `ns/op` is nanoseconds per iteration. It has a
> floor: the timer costs about a quarter of a nanosecond, so it can lie.
> `B/op` and `allocs/op` are bytes and allocations per iteration. An
> allocation either happened or it did not. Remember this pair: `ns/op` can
> lie, `allocs/op` cannot.

### Benchmark + pprof

> **SAY:** When `ns/op` is not enough, profile. `-cpuprofile` and
> `-memprofile` dump a profile you read with `go tool pprof`. `-top` prints the
> hottest functions. Here the whole benchmark is one call to `sha256.Sum256`,
> and ninety percent of the time is in the block function. The profile tells
> you where the time is — not whether the time is real.

### Reading compiler output

> **SAY:** The compiler can tell you what it did. `-gcflags=-S` prints the
> assembly. Each line shows the instruction and its source. `GOSSAFUNC`
> dumps every SSA rewrite phase to a browser, so you can watch the compiler
> think. We use `-S` in the next section to prove the compiler deleted our
> work.

---

## 06 · Local and Micro — 12:00 total

### The three questions, micro scale

> **SAY:** First half. Your laptop.
>
> The three questions again, at this scale. Real work: the compiler may
> delete it. Stable sample: one run is a single point. Above the noise: your
> laptop is not a controlled instrument.
>
> And the rule for this half: if you cannot trust the number on your own
> machine, pushing to CI does not fix it. CI just industrialises the lie.

### A benchmark bot comment

**Beat: plant the puzzle. Do not solve it.**

> **SAY:** June this year, dd-trace-go. I restructure a file, push, and the
> benchmark bot says `BenchmarkOTLPProtoSize` is six to nine percent slower
> than main.
>
> Nothing in my diff goes anywhere near OTLP encoding.
>
> Hold that thought. We return to it once we can read a benchmark properly.

`DO` Do not solve the puzzle yet. The payoff is §08.

---

## 07 · Making the Compiler Honest — 4:00

### Stop the compiler deleting your work

> **SAY:** Every technique here stops the compiler deleting the work you are
> trying to time. There are four. All four are test scaffolding. None of
> this belongs in production code. I repeat that when it matters.

### The compiler is not neutral

> **SAY:** Your benchmark is just code. The compiler reads it, notices you never
> use the result, and removes the work. And it is *right* to. The spec allows
> it. Your loop still runs `b.N` times — it just runs empty.

### Dead-code elimination (code)

> **SAY:** `makeBuffer` allocates. The benchmark calls it and throws the result
> away. Watch what happens.

### `make bench-dce`

**Beat: the killer number.**

> **SAY:** Quarter of a nanosecond, versus eleven. Looks like a forty-fold
> speedup. But look at the right-hand column. Zero allocations.
>
> `make([]byte, 64)` has no path that avoids allocating. There is no branch, no
> cache. Zero allocations means the call is gone.

### `ns/op` can lie, `allocs/op` cannot

`DO` Land this slowly. It is the most reusable line in the talk.

> **SAY:** `ns/op` has a floor — a timer costs about a quarter of a nanosecond,
> so an empty loop and a very fast function look identical. But an allocation
> either happened or it did not. `allocs/op` cannot be talked into lying.
>
> Always pass `-benchmem`.

### the compiler deleted your benchmark

`DO` The meme completes the two previous slides. **Ten seconds.**
The numbers on the dog are the ones the audience just saw from `make bench-dce`.

> **SAY:** Those are the real numbers from two slides ago.

### The two-variable sink

> **SAY:** The fix. A package-level variable the compiler cannot prove is
> never read. Accumulate into a local inside the loop, then publish once
> after it. You avoid a global write on every iteration.
>
> This is test-only. Do not put sinks in production code.

### Constant folding

> **SAY:** Second trick. Every input here is a literal, so the compiler just
> computes the answer at build time. You are now benchmarking how fast your CPU
> can load a constant.

### Timer: one-time setup

> **SAY:** Now timers. `ResetTimer` after your setup zeroes the elapsed
> clock. That call does *not* stop the timer.

### Timer: per-iteration setup

> **SAY:** If you must build a fixture every iteration: stop the timer, build
> it, start the timer, *then* do the work. Get that order wrong and you are
> timing the fixture instead of the function.

### `make bench-timer`

> **SAY:** Here is the wrong order. Four sixteen versus five fifty. The
> broken one looks twenty-five percent faster because it times the fixture
> and excludes the function it claims to measure.
>
> A benchmark measuring the wrong thing does not look broken. It looks like
> good news.

### `b.Loop()` · Go 1.24

> **SAY:** Go 1.24 gave us `b.Loop`. Setup before the loop is excluded
> automatically. Timing stops at the end automatically. And it prevents
> dead-code elimination of the loop body.

### What `b.Loop` removes

`DO` Do not read the table. Point at two rows.

> **SAY:** Setup exclusion and DCE prevention are the two that matter. The
> compiler only does this if you write `b.Loop()` literally in the
> condition. Assign it to a variable first and you lose it.

---

## 08 · The Regression That Was a Speedup — 2:15

### Read the benchmark first

**Beat: pay off the plant.**

> **SAY:** Back to our bot comment. First thing I did: read the benchmark.
> That is the entire timed loop. One call, `proto.Size`, on a struct built
> *before* `ResetTimer`.
>
> It does not call `ContextWithSpan`. It does not call `SpanFromContext`. It
> does not call one line of the code I changed. Locally it was rock solid,
> under nought point one percent variance.

### Same machine, both branches

> **SAY:** So I built both branches on the same machine and compared them
> properly. Main: eight eighty-three. My branch: eight forty.
>
> My branch was *faster*. CI had not just got the size wrong. It had got the
> **sign** wrong.

`DO` Let this sit. It is the biggest surprise in the talk.

### The mechanism

> **SAY:** Restructuring the file moved function addresses across the
> package. That moved the hot loop relative to cache lines and
> branch-target-buffer boundaries.
>
> At about three hundred and ninety nanoseconds an iteration, that is worth
> several percent in either direction. Enough to flip a verdict on a runner
> that cannot pin its clock.
>
> Resolution: no code change. Nothing was wrong.

### A known phenomenon

> **SAY:** Emery Berger's "Performance Matters" is the canonical talk. Code
> layout alone, which symbol lands at which address, swings performance by
> ten percent or more.

### A component speedup is not a system speedup

**Beat: the bridge into the second half.**

> **SAY:** Contention, queueing, and dependencies decide how much of a local
> win survives to the top.
>
> A microbenchmark measures the component. Only a macrobenchmark tells you
> whether it mattered.

### A noisy result can be directionally wrong

> **SAY:** The lesson from this story is not "CI is bad". A noisy result can
> be imprecise and point the wrong way. It can block a good change, and wave
> a real regression straight through.

---

## 09 · Statistical Interpretation — 2:15

### One number is a point sample

> **SAY:** Same binary. Same machine. Eight runs apart. Thirty-nine
> nanoseconds, and twenty-seven. A forty-three percent swing, and nothing
> changed but time.
>
> Run it once, file the PR, and you can be forty-three percent wrong in either
> direction.

### `benchstat`

> **SAY:** The tool is `benchstat`, from `x/perf`. Run with `-count`, pipe it in,
> and it compares distributions instead of numbers.

### Read the output (reveal)

> **SAY:** Four things. The number is the *median*, not the mean. The
> plus-minus is spread. `p` tells you whether it is distinguishable from
> noise.
>
> A tilde means no measurable difference, which is a *result*. It is not an
> invitation to rerun until you get a delta.

### What benchstat won't tell you

> **SAY:** There is a question benchstat deliberately does not answer. It
> tells you whether A differs from B. It does not tell you whether this
> machine is a trustworthy place to ask.
>
> Coefficient of variation is standard deviation over mean. It gives you one
> number for how noisy your environment is. Twenty lines of awk, and it is
> the check most people skip.

### Rules of thumb

> **SAY:** Ten runs is the floor, twenty is better. Above about five percent CV,
> stop comparing and go fix your machine — more samples will not save you. And
> significant and *large* are different questions.

### The p-hacking trap

> **SAY:** Do not rerun until you like the answer. Every rerun is a fresh
> draw from the same distribution, and with enough draws any noise looks
> like signal.
>
> Pick your run count before you look at results. Write it down if you have
> to.

### more samples will not fix a noisy machine

`DO` Show the meme to introduce §10. **Ten seconds.** The right-hand button
is the one everybody presses. The next section is about the left one.

> **SAY:** Only one of these buttons works.

---

## 10 · Local Reproduction — 2:30

### What does isolation actually buy?

> **SAY:** "Run it in a container" is standard advice. Almost nobody publishes
> what it actually buys you, so we measured it.
>
> Idle laptop, CV under five percent. Now sixteen background spinners: three
> times slower, four times noisier. Now the same load, but the benchmark pinned
> in a container: back to the idle noise floor, while the host is still fully
> saturated.

`DO` If someone asks about the platform, use the details on the slide. Someone
asked last time. Apple M4 Max, arm64 host, arm64 guest, Apple Virtualization.framework.
No QEMU, no cross-architecture emulation.

### 5.25% is not a triumph / It is a ceiling

> **SAY:** Five percent is not a good number. It is the *best* number this
> machine can give you. Bare-metal Linux with SMT off reaches nought point
> nought five. A hundred times tighter.

### The macOS caveat

`DO` Do not soften this.

> **SAY:** On macOS, Docker runs inside a Linux VM. So `--cpuset-cpus=0`
> pins a *virtual* CPU inside that VM. The VM can still move it across
> physical cores. Nothing inside that container can disable host SMT or pin
> the clock.
>
> You get isolation from your other processes. That is real, and worth
> having. You do not get controlled hardware.

### The inner loop

> **SAY:** Day to day, this is the loop. `benchdiff` stashes your change, runs
> the base, restores, runs again, pipes both into benchstat. Make a change, run
> it, read the interval, decide.
>
> And the free wins: close your indexer, go into airplane mode, let the machine
> reach thermal steady state. Zero setup, real variance reduction.

### Local and micro, answered

> **SAY:** So, first half. Real work: sink, `-benchmem`, watch `allocs/op`,
> prefer `b.Loop`. Stable sample: at least ten runs, read the p-value, check CV.
> Above the noise: pin it, and know your ceiling.
>
> And the one to remember: a delta under ten percent might just be code layout.

---

## 11 · CI and Macro — 10:45 total

### The three questions, macro scale

> **SAY:** Second half. Now it is CI, whole workloads, and time.
>
> Same three questions, different shape. Real work becomes: is the
> *workload* representative? Stable sample becomes: stable across *days*,
> not runs. And above the noise: now the hardware itself is the variable.

### A second bot comment

**Beat: mirror the first story.**

> **SAY:** Second real one. July, OpenTelemetry Go compile-time
> instrumentation. I land a dependency-pinning fix, run the overhead benchmark
> locally, and: `multi` at two hundred and thirty percent overhead against a
> ceiling of one fifty. `largeidle` at two twelve.
>
> Both blown. Looks like I have broken something badly.

### `largeidle` shares zero changed dependencies

> **SAY:** My change touched dependency pinning in `multi`. `largeidle`
> shares *none* of those dependencies. It runs independent code. It cannot
> have regressed.
>
> And yet it moved by the same sixty percent.
>
> When unchanged code gives a different result, the common factor is the
> machine. I ran parallel builds and integration tests all afternoon, even
> as I benchmarked my own build.

`DO` The fix was to wait for CI. There is no local target for that job. It runs
only in CI, on a dedicated runner.

### The mirror image

**Beat: this is why there are two stories.**

> **SAY:** Put the two side by side. First story: CI said slower, the laptop
> was right, and the cause was code layout. Second story: the laptop said
> slower, CI was right, and the cause was machine load.
>
> Neither environment is authoritative by default.
>
> And the tell was identical both times: a benchmark moved that could not
> have moved.

---

## 12 · Designing a Macrobenchmark — 1:30

### What does your app actually do? (reveal)

> **SAY:** Representative is the hard part, so start here. Is your workload
> CPU bound, I/O bound, or mixed, like almost everything real?
>
> Your benchmark workload should look like your production workload.
> Obvious, and almost nobody does it.

### Workload archetypes

> **SAY:** We use four archetypes. Idle: background workers, barely any load.
> Latency: microservices, high request rate, little CPU each. Throughput:
> queues and batch jobs. Enterprise: business apps with databases and API
> calls, mixed.

### Why `largeidle` falsified `multi`

> **SAY:** `largeidle` is the Idle archetype. `multi` is Enterprise.
> Completely different code, completely different shape.
>
> They moved by the same amount, in the same direction, at the same time.
> That is not a shared cause. That is a shared *environment*.

### A macro gate is a budget

> **SAY:** Macro gates work differently from micro gates. Micro compares two
> commits. Macro compares against a *budget*, a ceiling you are not allowed
> to cross.
>
> That is a product question, not a statistical one: how much of the
> customer's machine are we allowed to take?

---

## 13 · Controlling the CI Environment — 3:15

### Why shared runners lie

> **SAY:** Shared runners: competing workloads, variable frequency, shared
> last-level cache. A real ten percent regression vanishes into the noise. A
> phantom ten percent appears out of it.
>
> That is an environment problem. You cannot fix it with statistics.

### Why SMT breaks benchmarks

**Beat: the mechanism, not just the assertion.**

> **SAY:** So why does sharing a core produce twenty-three percent variance?
> A core is a fixed bag of execution units: arithmetic, floating point, load
> and store. Two threads share that bag. Neither gets the full core. Each
> gets a fraction. And the split is nondeterministic: whoever has
> instructions ready wins the next slot. Run to run, your thread gets a
> different fraction, and that fraction swings the runtime. Same code, same
> core, different share every time. That is the twenty-three percent.

### What's the impact of disabling SMT?

> **SAY:** Here is the cost. Two CPU-bound tasks, same core versus separate
> cores.
>
> *(next slide)* Twenty-four percent CV sharing a core. Nought point nought four
> when they are not. About a hundred times less variance. And notice it is also
> twice as fast, because the core stopped being shared.

### Why DFS breaks benchmarks

**Beat: the mechanism, not just the assertion.**

> **SAY:** The frequency story follows the same pattern. The clock is not
> fixed. A governor picks a frequency based on load and how much thermal
> headroom the chip has. Turbo pushes above base when the chip is cool. So
> run one: cool chip, high clock, fast result. Run twenty: warm chip,
> throttled clock, slower result. Same number of cycles, different wall
> time. The benchmark is not comparable across runs. Pin to base frequency
> and every run gets the same clock. The mean gets slower, because no turbo,
> but the variance drops ten times.

### What's the impact of disabling DFS?

> **SAY:** Ten times less variance with it off. And look, the mean got
> *slower*. Turbo is fast and inconsistent.
>
> A benchmark's job is to be comparable, not to post the best number you can
> hit once.

### Three sysfs writes

> **SAY:** All of that is three writes to sysfs. Disable SMT, pin the governor,
> kill boost. On bare metal that takes you from twenty-three percent CV to about
> nought point nought five.
>
> In a VM, none of it works. The hypervisor owns SMT, frequency is virtualised,
> and the write may succeed and be silently ignored — which is worse than
> failing.

---

## 14 · Detecting Change Over Time — 2:00

### A/B is the wrong model for CI

> **SAY:** `benchstat` compares two distributions. CI does not have two
> distributions. It has a time series. One measurement per commit, for
> months, with hardware changes and dependency bumps in the middle.
>
> Compare each commit to its parent and you ask the noise question every
> single time, and you miss slow drift completely.

### What regressions look like

> **SAY:** This is what we draw when we explain regressions. And this is what
> the data actually looks like. A step change is obvious in a diagram and buried
> in variance in real life.

### Change-point detection

> **SAY:** The right question is not "is this commit slower than its parent". It
> is "where in this history did the distribution shift, and stay shifted".
>
> That is change-point detection. It handles non-normal data, finds multiple
> change points, and ignores one-off spikes. ED-PELT, e-divisive means — Apache
> Otava implements it, Netflix documented doing this at scale.
>
> It needs history, so it belongs in nightly trending, not a PR gate.

### Why a baseline, not a pair

`DO` Read the quote aloud. It is the strongest line in the talk and it is not mine.

> **SAY:** And here is why, in their words. They never report a number in
> isolation, only relative to a baseline. Because the state of a machine or VM on
> one day is likely to be very different from the state of that machine the next
> day.
>
> That is the Go team, about their own hardware. If it is true for them, it is
> true for your CI runner.

---

## 15 · Wiring It Into CI — 2:00

### Two patterns

> **SAY:** Two patterns, and they want opposite things. A PR gate is fast and
> strict: a curated set of benchmarks that regressed before, same-machine
> A/B, tight threshold. A nightly suite is complete and slow: pinned runner,
> every control applied, rolling window, change-point detection.
>
> Either way: CI *detects*. It is not your primary measurement. That is still
> your laptop.

### Why not just add more runners?

`DO` Point at the second paragraph, not the first.

> **SAY:** Why not just throw more runners at it?
>
> Read what the Go project says about its own infrastructure. The normal
> test bots get tons of capacity and spin up VMs at will. The performance
> builders get one physical machine, often backlogged with work.
>
> Elastic capacity is the right answer for correctness. It is the wrong
> answer for performance, and the people who maintain Go know it.

### Keep a ledger of false positives

> **SAY:** That same benchmark fired again eleven days later on an unrelated
> PR. That time it took one comment to dismiss because the first
> investigation was written down.
>
> Without that note, the next person repeats the whole investigation. Or
> worse, "fixes" it. Documented noise is benchmark hygiene.

### CI and macro, answered

> **SAY:** Second half. Real work: match the archetype, pin the inputs.
> Stable sample: think in time series, use change points. Above the noise:
> bare metal, SMT off, governor pinned.
>
> A shared runner cannot be fixed with more samples.

---

## 16 · Wire It Up — 2:30

### Three tools

> **SAY:** I built three small things so you do not have to remember all of
> this. They ship from a separate repo called benchlab. One `go install`
> gets you all three binaries. If you use coding agents, one command adds
> them as skills.

`DO` The tools are in `github.com/kakkoyun/benchlab`, **not** the talk repo.
The talk repo has the decks and the captured results. Keep the two repos distinct.
The QR goes to the talk repo.

### `benchenv`

> **SAY:** This one tells you what your machine can and cannot do. Run it
> before a serious session.

### Four *unavailable* lines

`DO` Pause here. This is the closing idea.

> **SAY:** Look at what it says on my laptop. Four `unavailable`. No SMT
> control. No frequency control. No turbo control.
>
> That is the honest answer. macOS does not expose those, so it says so,
> instead of printing a green tick I would believe.
>
> Knowing what you cannot control is worth as much as controlling it.

### The minimum viable discipline

> **SAY:** If you take one slide home, take this one. Add a sink. Run enough
> samples. Compare with benchstat. Check the environment before you believe
> the comparison.
>
> That is under an hour of work to check whether you can trust a benchmark.

### Three questions, two scales

`DO` The final recap. Say the two bold lines slowly.

> **SAY:** So. Three questions, two scales. Real work, stable sample, above the
> noise — asked once on your laptop, once in CI.
>
> A sub-ten-percent micro delta can be layout noise.
> A shared runner cannot be fixed with more samples.

### Take it with you

> **SAY:** Two links. benchlab has the three tools and the agent skills. The
> talk repo, that is the QR, has both decks and every captured result in
> this talk, so you can check my numbers.
>
> And the earlier FOSDEM version is there if you want the language-agnostic
> take.

### Close

> **SAY:** Trust your numbers only after the compiler, the sample, and the
> machine have each earned it.
>
> Thank you.

`DO` Stop. Leave the questions slide up.

---

## Numbers to memorise

| Number | What |
| --- | --- |
| **~73 ns** | OPERA connector bias |
| **500 ms → −20%** | Google search traffic |
| **−3.4%** | Datadog production CPU, from PGO |
| **0.25 vs 11 ns · 0 vs 1 allocs** | DCE demo |
| **416 vs 551 ns** | timer-order demo, broken looks faster |
| **883 → 841 ns** | #4891, main vs branch |
| **43%** | swing, same binary |
| **4.75 / 18.88 / 5.25** | CV: idle / loaded / pinned |
| **~0.05%** | bare metal, SMT off |
| **230% / 212% vs 150%** | #643 overhead vs ceiling |
| **23.9% → 0.044%** | SMT on → off (~100×) |
| **0.383% → 0.041%** | DFS on → off (~10×) |

## Things to never say

- Do not attribute the Google number to Marissa Mayer — "the Google search team".
- Do not put a figure on the OPERA oscillator fault.
- Do not call Docker Desktop on macOS hardware isolation.
- Do not claim statistical significance proves practical importance.
- Do not describe Datadog's internal benchmarking setup — ledger row 23 is unresolved.

## If challenged

Name the committed result file and the environment. Do not improvise a rerun on
stage. Every number above traces to `claims-ledger.md` or `demo/results/`.

## Setup

Present from the **bespoke HTML** if you want the reveals to animate:
`make serve/go-benchmarks-lying` → `localhost:8000/presentation.html`.
The PDF is a correct handout but shows every fragment at once.
