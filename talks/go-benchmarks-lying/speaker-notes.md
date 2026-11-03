# Script: Why Your Go Benchmarks Are Lying

GoLab 2026. 45-minute slot: 42 minutes presented, 3 minutes Q&A. 77 pages.
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

**Message:** benchmarking is not easy. It needs investment, maths, tooling,
and a keen eye. The value is huge, and Datadog and the Go team both do it. If
you ship something on a hot path, invest. Now you know what to do.

**No maths on stage.** Say why a check matters. Do not explain how the
statistics work.

**Footer cues.** A small glyph after GOLAB in the footer is a delivery cue.
`▸` means stop advancing and speak freely. `◆` is a checkpoint: look up, scan
the room, check the time against the checkpoints below. `∙` means pause after
the line. `◦` means slow down, because the slide must land.

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
| Ledger | Write every false alarm down |
| 07 Agents Need Real Benchmarks | Agents optimise what you measure |
| Close | Not easy, worth it. Now you know what to do |

## Timing

The budgets are a model, not a measurement. Replace them after the timed read.
The model is uncertain in both directions: the SAY text is about 3,000 words,
which reads in about 25 to 30 minutes, and stories, laughter, and pauses add
the rest.

Checkpoints: §01 by 3:00 · §02 by 7:30 · §03 by 12:00 · §04 by 17:00 ·
§05 by 21:30 · §06 by 27:30 · ledger by 32:00 · §07 by 33:00 · close by
38:00 · finish by 41:30. If §05 has not started by 24:00, apply the cut
ladder in `outline.md`. If the timed read is short, add the stretch beats
under "Reserve answers".

---

## Why Your Go Benchmarks Are Lying

**SAY**

Every benchmark you write is a measurement system. Like any instrument, it can be precise and still wrong.

Today I give you three questions. They turn a number into a measurement. And I show you how we answer them at Datadog, where a wrong benchmark costs real money, and how the Go team answers them for the toolchain you use every day.

**DO**

Do not introduce yourself yet. Advance.

---

## A benchmark bot comment

**SAY**

June this year. dd-trace-go, the Datadog Go tracer. I restructure one file and push.

The benchmark bot answers: `BenchmarkOTLPProtoSize` is six to nine percent slower than main. Nothing in my diff goes near OTLP encoding.

So. Would you fix it?

Most of us would. A red comment on your pull request feels like an accusation. So we open a profiler, find something that looks slow, and push a fix. The comment turns green, and everybody is happy.

Keep that question. We come back to it.

**DO**

Ask the question. Wait two seconds. Do not solve it. The answer comes in §03.

---

## Why Datadog cares

**SAY**

Why do I care so much? Before Datadog, I maintained Prometheus `client_golang` and worked on the Parca profiler. Each of those jobs punished me for a benchmark I did not question.

At Datadog, our code runs inside your process. Every nanosecond we spend comes out of your budget. For us, overhead is product correctness.

One public number: profile-guided optimisation took three point four percent of CPU off one large production service. Staging was too noisy to show it. The team had to divide CPU by the work done before the change was visible.

We invest in this internally. The effort is called SpeedLab. This talk is the spillover.

**DO**

Say the SpeedLab name once. Ledger row 30 permits the name and its existence only. The practice comes in §05. The PGO number is one service, not all of production. Ledger row 47.

---

## A Loose Cable

**DO**

Section budget 4:30, including the basics slide. Start by 3:00.

---

## September 2011

**SAY**

September 2011. The OPERA experiment fires neutrinos from CERN to a detector in Italy. The neutrinos arrive early. Faster than light.

If that is true, Einstein is wrong. The team knows it. Their coordinator says: a result is never a discovery until other people confirm it.

So they publish, and they ask the world to find their mistake.

**DO**

Let the headline stand for a beat before you speak. Ledger row 46 holds the quote.

---

## "Trivial things we are

**SAY**

And then he says this.

"If there is a problem, it must be a tough, nasty effect, because trivial things we are clever enough to rule out."

Remember that sentence.

**DO**

Read the quote slowly. Pause after "rule out".

---

## The cause

**SAY**

It was this. A fibre-optic connector, not fully seated, in the GPS timing chain. Seventy-three nanoseconds of bias.

A trivial thing.

And a second fault pushed the other way and partly hid the first. The bug hid behind another bug.

**DO**

Let them look at the photo first. Do not put a number on the second fault. Ledger row 9.

---

## Your cables

**SAY**

These physicists were not careless. They were very careful, and the instrument was still wrong.

You have `testing.B`, a laptop, and thirty browser tabs. Your cables are the compiler, the statistics, and the machine.

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

The first one is about the code: did the work you think you measure really run? The second is about the sample: would the same run give the same answer? The third is about the machine: can this machine see a change this small?

If you cannot answer all three, you do not have a measurement. You have a number. We ask them on the laptop first, and then in CI.

**DO**

Pause after each question. The audience hears them again in every section.

---

## One command, two habits

**SAY**

A quick reminder of the instrument. One command.

`-count=10`, because one run is one draw, not a measurement. `-benchmem`, always, because allocations show what the code really did.

We need both in a minute.

**DO**

Thirty seconds. Do not teach the flags.

---

## Is It Real Work?

**DO**

Section budget 4:30. Question 1: real work? Start by 7:30.

---

## The compiler is not neutral

**SAY**

Question one. Real work.

Your benchmark is just code. The compiler reads it, sees that you never use the result, and removes the work. It is right to do that. That is the same optimisation that makes your production code fast.

The compiler does not know that this function is a benchmark. It does not care.

Your loop still runs `b.N` times. It just runs empty.

---

## Dead-code elimination

**SAY**

`makeBuffer` allocates sixty-four bytes. The benchmark calls it and throws the result away. This looks harmless. I have seen this shape in many real repositories.

Watch what happens.

---

## `make bench-dce`

**SAY**

A quarter of a nanosecond, against eleven. It looks forty times faster.

Now look at the allocations. Zero. A quarter of a nanosecond is not enough time to do any work. Zero allocations and no time: the call is gone.

If you only look at time, you celebrate a forty-times speedup. If you look at allocations, you see that you measured nothing.

**DO**

Point at the allocations column.

---

## `ns/op` can lie

**SAY**

Time can lie. A very fast function and an empty loop look the same.

So look at a second witness. Allocations are harder to fool than time. When both are suspiciously low, the compiler has deleted your work.

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

The fix is `b.Loop`, from Go 1.24. Setup before the loop is not timed. The loop body stays alive, so the compiler cannot delete it.

But there is a catch that many people missed. In 1.24 and 1.25, `b.Loop` kept the body alive by blocking inlining. So your benchmark could allocate where your production code does not.

Go 1.26 removed that. Upgrade before you compare.

**DO**

Ledger rows 39 and 40. Go 1.26 is the fix, not the regression. Do not say it backwards.

---

## What `b.Loop` removes

**SAY**

Two rows matter. Setup is not timed, and the body is not deleted. That removes most of the hand-written scaffolding we used to need: the sinks, the timer resets, the global variables.

Write `b.Loop()` literally in the loop condition. If you assign it to a variable first, you lose the protection.

**DO**

Do not read the table. Point at two rows.

---

## The cache can lie too

**SAY**

One more trap for real work, and `b.Loop` does not fix it. If you give the benchmark the same input every iteration, the CPU cache remembers it. You measure the cache, not your function.

Teiva Harsanyi shows this in Go. With one reused input, one matrix size looked about fifty percent faster than its neighbour. With fresh input each iteration, the gap disappeared.

Production does not call your function with warm data every time. Your benchmark should not either.

**DO**

Ledger row 45. Say the idea, not his numbers. Do not explain the cache mechanism: the post does not.

---

## The Regression That Was a Speedup

**DO**

Section budget 5:00. Question 2: stable sample? Start by 12:00. This section answers the opening question.

---

## Read the benchmark first

**SAY**

Back to the bot comment. Would you fix it?

I did not. First, I read the benchmark. This is the whole timed loop. One call, `proto.Size`, on a struct built before the timer starts.

It calls none of the code I changed. And on my machine it was stable: under zero point one percent from run to run.

---

## Same machine, both branches

**SAY**

So I built both branches on the same machine and compared them.

Main: eight hundred eighty-three nanoseconds. My branch: eight hundred forty-one. Same direction with ten spans.

My branch was faster. CI got the sign wrong.

If I had "fixed" it, I would have made a fast change slower to make a bot happy.

**DO**

Let this sit. It is the biggest surprise in the talk.

---

## The mechanism

**SAY**

Why? My change moved function addresses in the package. The hot loop moved relative to cache lines and branch targets.

At this speed, that is worth several percent, in either direction. On a CI runner that cannot pin its clock, that is enough to flip the verdict.

So neither number is the cost of my change. Both are layout. The fix: no code change. Nothing was wrong.

---

## A known phenomenon

**SAY**

This is well known. Emery Berger's talk, Performance Matters, shows that code layout alone can swing performance by ten percent. Where the linker puts your function can matter more than what you changed in it. Watch the talk. It is one of the best performance talks I know.

---

## A noisy result can be

**SAY**

So the lesson is not "CI is bad". A noisy result can point the wrong way.

It can block a good change. And it can let a real regression through.

---

## One number is a point sample

**SAY**

Here is how noisy one number is. Same binary, same machine, a few runs apart. Thirty-nine nanoseconds, then twenty-seven.

A forty-three percent swing, and nothing changed.

One run is one point. You need a sample.

---

## you, when someone says "p-value"

**SAY**

I know. Statistics in a conference talk. Do not worry, I will not show you a single formula. One tool does the maths for you.

**DO**

Ten seconds. Then click to `benchstat`.

---

## `benchstat`

**SAY**

The tool is `benchstat`. Run with `-count`, give it the old and the new results, and it compares the two samples.

It answers one question: is B different from A, beyond the noise? A tilde means no. That is a result. Do not rerun until you get the answer you want.

It cannot tell you whether the machine is trustworthy. If an unchanged benchmark spreads by more than about five percent, fix the machine first.

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

Section budget 4:30. Question 3: above the noise? Start by 17:00.

---

## A second red number

**SAY**

Second story, three weeks later. OpenTelemetry Go compile-time instrumentation. I land a dependency fix and run the overhead benchmark on my laptop.

`multi`: two hundred thirty percent overhead, against a ceiling of one hundred fifty. `largeidle`: two hundred twelve.

Both fail. It looks like I broke something badly.

---

## `largeidle` shares

**SAY**

But my change touched dependencies in `multi` only. `largeidle` shares none of them. It cannot have regressed. And it moved as much as `multi`.

When code that did not change gives a different result, the common factor is the machine. I ran parallel builds all afternoon while I benchmarked.

That is the trick to take home: a control benchmark. Keep one benchmark that your change cannot touch. If it moves, do not trust the others.

**DO**

The fix was to wait for CI. That job runs only in CI, on a dedicated runner.

---

## The mirror image

**SAY**

Put the two stories side by side.

First: CI said slower, the laptop was right, and the cause was code layout.

Second: the laptop said slower, CI was right, and the cause was machine load.

Neither place is right by default. And the tell was the same both times: a benchmark moved that could not have moved.

**DO**

This is the throughline. Say the last line slowly.

---

## PR #4891 and PR #643

**SAY**

Different causes, opposite directions. The same tell.

**DO**

Ten seconds. Then move on to the container run.

---

## What does isolation actually buy?

**SAY**

"Run it in a container" is common advice. So we measured what it buys, on this laptop.

Idle: under five percent spread. Add sixteen background spinners: three times slower, four times noisier. Pin the benchmark in a container under the same load: the spread goes back to about the idle level.

**DO**

This is one local run from August. Do not call it a general result. The platform details are on the slide if someone asks.

---

## 5.25% is not a triumph

**SAY**

Five percent is not a good number. It is the best this laptop can do.

For this benchmark, under this load, a change smaller than that is invisible. For a smaller change, you need a different machine. That is the next section.

**DO**

Do not compare this number with the bare-metal results. They come from a different benchmark on a different machine. Ledger row 8.

---

## The macOS caveat

**SAY**

One caveat. On macOS, Docker runs in a Linux VM. `--cpuset-cpus` pins a virtual CPU.

The VM can still move it across physical cores. Nothing in the container can turn off SMT or pin the clock.

You get isolation from your other processes. You do not get controlled hardware.

**DO**

Do not soften this.

---

## How We Run It at Datadog

**DO**

Section budget 6:00. Start by 21:30.

---

## What we do at Datadog

**SAY**

So how do we do this at Datadog, where overhead is the product? Four things.

Dedicated hardware, not shared CI runners. An overhead budget for each SDK. Several workloads for each SDK, not one. And we gate the release, not only the pull request.

Let me show you why each one is there.

**DO**

Ledger row 23. Say the practice shape only. Give no hardware counts, budget figures, archetype names, or scale. If someone asks for numbers, say that they are internal.

---

## Why not just add more runners?

**SAY**

First, the hardware. Shared runners have neighbours, changing clocks, and shared caches. A real regression can vanish, and a fake one can appear.

So why not add more runners? Read what the Go project says about its scarce builders. Often there is only one physical machine, with a backlog of work.

More capacity helps correctness. Performance needs the scarce machine.

**DO**

Read the quote aloud. Ledger row 38.

---

## FOSDEM 2026, Software Performance devroom

**SAY**

The next data comes from the talk Augusto de Oliveira and I gave at FOSDEM this year. Augusto ran the experiments on bare-metal cloud machines. The video has the full method, if you want more than two charts.

**DO**

Credit Augusto by name. Ledger rows 1 to 3 and 29.

---

## What's the impact of disabling SMT?

**SAY**

What does dedicated hardware buy? These are the experiments behind our FOSDEM talk, on a bare-metal cloud machine. Two CPU-bound tasks, on the same physical core, then on separate cores.

Spread: about twenty-four percent with SMT on. Under a quarter of a percent with it off. About a hundred times less variance. And twice as fast, because the core is no longer shared.

---

## What's the impact of disabling DFS?

**SAY**

Now frequency scaling. The CPU changes its clock with temperature and load. Your benchmark runs at a different speed every minute. Turn it off: ten times less variance.

And the mean got slower. Turbo is fast, and inconsistent. A benchmark must be comparable. It does not need to be fast.

---

## Three sysfs writes

**SAY**

All of that is three writes. Turn off SMT. Pin the governor. Turn off boost.

On bare metal, the spread goes from about twenty-four percent to under a quarter of a percent.

In a VM, the write can succeed and do nothing. That is worse than an error.

---

## you, after three sysfs writes

**SAY**

Three writes to sysfs, and you are in charge of the hardware.

**DO**

Ten seconds. The next slide is for teams without root on bare metal.

---

## No bare metal? Rent the scarce machine

**SAY**

"We do not have bare metal" is the usual answer. Prometheus shows another way. A maintainer comments `/prombench` on a pull request. The automation creates dedicated nodes, runs the pull request against a baseline under the same workload, publishes the results, and deletes the nodes.

Dedicated for one run, and paid for one run. That is how an open-source project gets the scarce machine.

**DO**

Ledger row 44. Keep it short.

---

## Noise goes all the way down

**SAY**

And when you fix all of that, there is another layer. This is Brendan Gregg, in 2008. He shouts at a disk array, and the disk latency goes up.

Vibration is benchmark noise too. There is always one more layer.

**DO**

Let the picture land first. Ten seconds of laughter is fine. Ledger row 24.

---

## Workload archetypes

**SAY**

Second, the workloads. One workload is not representative. Our FOSDEM talk describes four archetypes. Idle: background workers. Latency: APIs with many small requests. Throughput: queues and batch jobs. Enterprise: business apps with a database.

Remember the second story. `largeidle` is Idle. `multi` is Enterprise. Different code, same movement, same moment. That is a shared environment, not a shared cause.

**DO**

Ledger row 20. Do not say which archetypes Datadog runs.

---

## The load generator can lie too

**SAY**

A macrobenchmark needs a load generator, and the load generator can lie too. Gil Tene calls this coordinated omission.

The server stalls. A simple load generator waits for the reply before it sends the next request. So the requests that would have hit the stall are never sent, and never measured. Your p99 looks better, because you measured less.

If your workload is about latency, check how your load generator behaves when the server is slow. Watch Gil's talk.

**DO**

Ledger rows 13 and 22. No numbers. Walk the four boxes left to right.

---

## A macro gate is a budget

**SAY**

Third, the budget. A micro gate compares two commits. A macro gate compares against a budget: a ceiling that you must not cross. For a tracer or a profiler, the question is simple. How much slower is your service with us inside it?

That is a product decision, not a statistics question. How much of the customer's machine may we take?

The numbers on this slide come from the OpenTelemetry story, not from our budgets.

**DO**

The example values come from the second story, not from Datadog budgets.

---

## Detecting Change Over Time

**DO**

Section budget 4:30. Question 2, across days. Start by 27:30.

---

## A/B is the wrong model for CI

**SAY**

Fourth, time. `benchstat` compares two samples. CI does not have two samples. It has a time series: one result per commit, for months, with hardware changes and dependency updates in between.

If you compare each commit with its parent, you ask the noise question every time. And you miss slow drift completely.

---

## What regressions look like

**SAY**

This is how we draw a regression on a slide: a clean step. This is what it looks like in real data: a cloud of points, and somewhere inside it, the step.

A step change is clear in a drawing. In real data, it hides in the noise.

---

## Change-point detection

**SAY**

So ask a different question. Not "is this commit slower than its parent?" Ask "where did the history shift, and stay shifted?"

That is change-point detection. It finds lasting shifts and ignores one-off spikes. Apache Otava implements it. Netflix wrote about doing this at scale.

It needs history, so it belongs in a nightly job, not in the PR gate.

**DO**

No statistics. Say what it finds, not how.

---

## you, nodding along to change-point detection

**SAY**

You do not need the maths. You need the tool that does it, and the history to feed it.

**DO**

Ten seconds. This is the release valve after the statistics. Smile, then continue.

---

## Change points in the wild

**SAY**

This is not only a Datadog idea. Netflix's TV UI team wrote about dropping static thresholds for their performance tests. A fixed limit fired on noise, and it missed slow regressions. They moved to anomaly detection and change-point detection in CI.

And in the same FOSDEM room as our talk, Henrik Ingo gave a whole talk on continuous performance engineering: how to set up the infrastructure for low noise, and how to use change-point detection to alert with fewer false positives. If this section interests you, watch that talk next.

**DO**

Ledger rows 21 and 51. Do not claim more than the talk abstract says.

---

## Why a baseline, not a pair

**SAY**

The Go team says why, about their own hardware. They never report a number alone, only relative to a baseline. Because the machine on one day is very different from the same machine the next day.

If that is true for the Go team, it is true for your CI runner.

**DO**

Read the quote aloud.

---

## The Go team does this

**SAY**

And they do not just say it. This is the Go performance dashboard. Every commit to the toolchain, on dedicated machines, compared against the last release.

The runtime and compiler teams look at this. When you upgrade Go and your service gets faster for free, this is part of why.

**DO**

Do not read the charts. Let the shape make the point: a time series, not a pair. Ledger row 36.

---

## Before merge, on request

**SAY**

And before merge? If you contribute to Go, you can ask for performance results on your change. There are two SlowBot builders. `perf_vs_parent` measures your change in isolation. `perf_vs_tip` measures it against the current tip.

It is opt-in, because those machines are scarce. The cheap pairwise check runs before merge. The signal they trust is the time series after merge. That is the same split as our two patterns.

**DO**

Ledger row 37. A practical tip for Go contributors in the room.

---

## Two patterns

**SAY**

So, two patterns. A PR gate: fast and strict. A small set of benchmarks that regressed before, a same-machine A/B, and a tight threshold.

A nightly suite: complete and slow. Pinned hardware, all controls on, and change-point detection. Before a release, the budget gate.

CI detects. To explain a result, you still measure on a controlled machine, like I did with the first bot comment.

---

## BenchmarkOTLPProtoSize, eleven days later

**SAY**

And then, somehow, our old friend came back.

**DO**

Ten seconds. The next slide is the payoff.

---

## Keep a ledger of false positives

**SAY**

The last practice is the cheapest. Remember the first bot comment? The same benchmark fired again eleven days later, on another pull request.

That time, one comment closed it, because the first investigation was written down. Without that note, the next person repeats the investigation. Or worse, they "fix" it.

Write down every false alarm.

**DO**

Budget 0:45. Start by 32:00.

---

## Agents Need Real Benchmarks

**DO**

Section budget 5:00. Start by 33:00. This is the newest material. Slow down.

---

## A benchmark is a prediction

**SAY**

One more Datadog story, and then the newest one.

When we rolled out profile-guided optimisation, the benchmark said five point four percent less CPU. Staging was too noisy to tell. Production said three point four.

A benchmark is a prediction. Production is the answer. And that matters a lot right now, because of who writes our benchmarks next.

**DO**

Ledger row 47. One service, not all of production.

---

## "Get the benchmark wrong, and the agent

**SAY**

Agents. I have seen coding agents do great work on Go performance. Give an agent a benchmark, and it optimises it, fast and without getting tired.

That is the problem. It optimises exactly what the benchmark measures. Our team put it like this: get the benchmark wrong, and the agent finds real speedups on the wrong hill.

**DO**

Read the quote slowly. Ledger row 48.

---

## the agent, after it made the benchmark faster

**SAY**

Faster, yes. Better? Only if the benchmark looks like production.

**DO**

Ten seconds. Let the laugh land, then go to the DODO diagram.

---

## Ground the benchmark in production

**SAY**

So at Datadog we built DODO, the Observability-Driven Optimizer.

It reads two signals from production. The continuous profiler says where the CPU time goes. Live Debugger captures real calls, with real inputs and real state. An agent writes a benchmark from those. A second agent optimises the code against it.

**DO**

Point along the diagram from left to right.

---

## Fit first, then freeze

**SAY**

The trick is the first loop. The agent writes a benchmark, runs it, and compares its CPU profile with production. It keeps going until the two match.

Then the benchmark is frozen. The optimising agent may change the code. It may not change the benchmark. Otherwise it improves the score instead of the code.

And it runs on the same CPU architecture as production. Question three, again.

**DO**

This is question one, real work, answered by production data.

---

## What it found

**SAY**

We pointed it at one of our largest services, already heavily optimised. Three changes cut more than eight percent of that critical service's CPU. On the order of ten thousand cores, all day.

My favourite one: about a quarter of real tags contain uppercase letters. The agent kept that mix in the benchmark and found a fast path for it. A synthetic benchmark would never show that.

**DO**

Ledger row 48. Say "on the order of ten thousand cores". Do not give a dollar figure.

---

## Even optimized code had room

**SAY**

Here is every target from the first evaluation. Each bar is how much of its CPU cost one function saved. These functions sit in a service that we had already tuned for years.

The team expected little left in the hottest code, and they were surprised. Some functions lost most of their CPU cost. One saved four percent. The benchmark decided which ideas were real, not the agent's confidence.

**DO**

Do not read the bars. Point at the top and the bottom. Ledger row 48.

---

## `dodo-cli` · internal beta

**SAY**

Internally it is a CLI. `explore` ranks the hottest functions in production by how much room they have. `optimize` builds the grounded benchmark and then runs the agent loop.

It works for Go, Java, and experimental Python, with Claude Code or Codex. It is an internal beta, so I cannot give it to you today. But you can copy the idea: give your agent production data, not a guess.

**DO**

Ledger row 49. Features only. No install steps, no internal numbers.

---

## Benchmarking is not easy

**SAY**

So, honestly: benchmarking is not easy.

It needs investment, in dedicated hardware. It needs maths, statistics you can trust. It needs tooling. And it needs a keen eye, someone who asks what could not have moved.

But the value is huge. Datadog does this. The Go team does this.

**DO**

Budget for the close: 3:30. Start by 38:00.

---

## On a hot path? Invest.

**SAY**

So if you ship a library, a tool, or a service on a hot path, invest in it. The measurement is part of the product.

**DO**

Pause after "invest".

---

## Now you know what to do

**SAY**

And now you know what to do. Three questions, two scales.

Real work: `b.Loop` on the laptop. Real workloads and budgets in CI.

Stable sample: ten runs and `benchstat`. Then a time series with change points.

Above the noise: a control benchmark and a known ceiling. Then bare metal with SMT and boost off.

A sub-ten-percent micro delta can be layout noise. A shared runner cannot be fixed with more samples.

**DO**

Say the last two lines slowly.

---

## Take it with you

**SAY**

The talk repo is the QR code. It has the deck, the script, every captured result, and the claims ledger with a source for each claim, so you can check my numbers. That is the same rule as the rest of the talk: do not trust a number you cannot check.

The earlier FOSDEM talk is there too, if you want the language-neutral version.

---

## Questions?

**SAY**

OPERA's coordinator was right. A result is not a discovery until someone else confirms it. That includes your benchmarks, and your agents' benchmarks.

Trust a number only after the compiler, the sample, and the machine have each earned it.

Thank you.

**DO**

Stop. Leave the slide up. Three minutes of Q&A.

---

## Reserve answers

Name the committed result file and the environment. Do not improvise a rerun
on stage. Every number below traces to `claims-ledger.md` or `demo/results/`.

### Stretch beats

Use these only if the timed read is short. Each one is public and already in
the ledger.

* **prombench** (row 44): Prometheus maintainers comment `/prombench` on a
  pull request. It creates dedicated nodes, runs the benchmark against a named
  baseline, and deletes the nodes afterwards. A way to rent the scarce machine.
* **The observer effect** (row 45): reuse one input across iterations, and the
  CPU cache gives you a faster benchmark than production. Create fresh input
  per iteration. Say the idea, not the numbers.
* **Netflix** (row 21): Netflix wrote about catching regressions with
  change-point detection before they reach users.
* **Coordinated omission** (row 22): a load generator that waits for a slow
  server stops measuring the slowness it caused. Gil Tene's talk explains it.

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
| **~24% → 0.04–0.24%** | SMT on → off (~100×), AWS m5.metal |
| **−5.4% → −3.4%** | PGO: benchmark → production |
| **>8% · O(10k) cores** | DODO, one critical Datadog service |
| **~25%** | real tags with uppercase letters (NormalizeTags) |
| **0.38% → 0.04%** | DFS on → off (~10×), AWS m5.metal |

### Things to never say

* Do not put a figure on the OPERA oscillator fault.
* Do not call Docker Desktop on macOS hardware isolation.
* Do not claim statistical significance proves practical importance.
* Do not compare the laptop spread with the bare-metal numbers.
* Do not give Datadog hardware counts, budget figures, archetype names, or
  scale. Ledger row 23 permits the practice shape only.
* Do not give dollar figures for DODO or PGO. Do not give `dodo-cli` install
  steps. Ledger rows 47 to 49.

### Setup

Present from the bespoke HTML if you want the reveals to animate:
`make serve/go-benchmarks-lying` → `localhost:8000/presentation.html`.
The PDF is a correct handout but shows every fragment at once.
