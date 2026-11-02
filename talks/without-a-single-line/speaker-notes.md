# Speaker notes: Zero-Touch Go Instrumentation

GoLab 2026. 45-minute slot: 38 minutes presented, 7 minutes Q&A. Intermediate Go audience.

Deck: `slides/presentation.md`. Section headings below match slide titles
verbatim, so you can find your place by what is on screen.

## Contract

**SAY** lines are the words, written to be spoken. Short sentences, one idea
each. **DO** lines are delivery cues, kept separate so the prose stays sayable.
Memorise the purpose of each slide, then let the words follow.

## Beat table

| Section | One thing |
| --- | --- |
| Open | The debugging loop is slow. An agent alone does not fix it. |
| 01 Why Go resists | Go compiled away the attachment point other runtimes have. |
| 02 otelc | The build path can enable all four signals. Coverage depends on the SDK and integrations. |
| 03 Injector | SDK capabilities through a different attachment path. The binary is the constraint. |
| 04 OBI | Traces and metrics from the kernel. Explain eBPF through the OBI example. |
| 05 Profiles | CPU profiles without rebuilding. Correlation needs shared request context. |
| 06 Live debugging | Dynamic logs and snapshots answer the unplanned question. |
| 07 Choose the signal and the layer | Match the evidence to the deployment constraint. |
| 08 What comes next | Explicit probes, native libraries, stable context storage, correlation, and more signals. |
| 09 From question to evidence | Resolve the opening bug and the agent joke. Invite concrete contributions. |

## Timing

The times in `outline.md` are working budgets, not measurements. They reserve
36 minutes for content and two minutes for pauses and overruns. The new future
material needs rehearsal. Do not assume that removing the install slide makes
room for all of it.

Checkpoints: otelc by 4:00, injector by 8:00, OBI by 11:00, profiles by 20:00,
live debugging by 22:30, selection by 26:00, future work by 28:00, and the
closing callback by 32:00. Adjust these budgets together after a timed read.
The optional static-PIE anecdote needs about 1:25 within the OBI budget.

---

## Zero-Touch

**DO**

Let the title establish the subject. Advance to the production bug.

---

## The bug you cannot reproduce locally

**SAY**

There is a bug. It happens in production. You cannot reproduce it locally.

So you add a log line. You redeploy.

Wrong place. You add another log line. You redeploy again.

**DO**

Let it sit. Two beats of silence after "again." Do not rescue the silence.
The discomfort is the point.

---

## What if you did not have to?

**SAY**

What if you did not have to?

**DO**

Say only this. Let the question stand. Advance.

---

## Every new dependency creates another place to forget

**SAY**

You wrapped every HTTP client and database call by hand.

The first service gets careful instrumentation. The fiftieth inherits gaps.

At fleet scale, instrumentation coverage is a platform problem.

Automatic instrumentation gives us a baseline. Later, we still need a way to
ask the question that the baseline misses.

**DO**

Keep it concrete. Do not abstract. The line to land is "a platform problem."

---

## Other runtimes have an attachment point

**SAY**

Every other runtime has a place to intervene after the source was written.

The JVM has javaagent. Python has import hooks. .NET has profiling APIs.

Go compiles that place away. It made deployment simple. It made late
instrumentation hard.

**DO**

Do not teach every mechanism. Point out that each has one. Go does not.

---

## Why we care

**SAY**

I wrapped handlers by hand for years. Then I worked on profiling at Parca.
Now I work on compile-time instrumentation. Hand-written coverage decays.

Datadog builds at all three intervention points. I need the right combinations
to work in customer services.

**DO**

Twenty seconds. Explain why the comparison matters. Do not imply work on OBI.

---

## Agent joke (slide 1)

**SAY**

Right. That is the talk. Thanks, everyone.

**DO**

Deadpan. Beat. Two seconds of silence. Do not explain the joke. Do not milk
the fake-out.

---

## Agent joke (slide 2)

**SAY**

Not really. The agent still has to pick a mechanism, and it has to know what
that mechanism costs. That is what we need to understand.

**DO**

The turn. This is the sentence that earns the rest of the talk. Ten seconds
total for both slides. Do not explain the joke.

This is a plant. It pays off at the agentic close, when the agent has the
framework that it was missing.

---

## Why Go resists instrumentation

**SAY**

So why is Go the hard one?

**DO**

Tie the missing attachment point to the opening problem. Build-time
instrumentation still requires a rebuild. Zero-touch does not mean that
every approach avoids deployment.

---

## What makes Go different

**SAY**

The compiler emits native machine code. The linker produces static binaries by
default. There is no classloader, no general runtime hook API.

And goroutines move between OS threads on movable stacks.

There is no single point where an agent can safely rewrite every function at
startup.

**DO**

Reveal each line. Do not rush. The last line is the one that matters.

---

## Choose where to intervene

**SAY**

There are three practical places to intervene. Build time. Process start. The
kernel.

Build time preserves Go semantics but requires a rebuild. Process-start
injection avoids source edits but depends on binary and linker surfaces.
Kernel observation avoids the rebuild but inherits Linux, privilege, and
compatibility constraints.

We will follow that order: build, process start, then kernel.

**DO**

Point to each intervention point. This is the binary's lifecycle, not a
requirement to install all three approaches.

---

## Three intervention points. Four signals

**SAY**

At each point, ask which evidence we can collect. Traces, metrics, logs, and
profiles answer different questions about production.

We will track those signals in the same order throughout the talk.

**DO**

Introduce the signal indicators. They describe capabilities, not a ranking.
The SDK and integrations determine the build and injector coverage.

---

## otelc: instrument during the build

**SAY**

Start at the build, while source structure is still available. We can add
instrumentation without writing wrappers throughout the application.

This route can reach all four signals. The SDK and integrations determine
which ones it produces. We still need a rebuild.

**DO**

Point to the four signal indicators. Say that these are capabilities of the
build path, not a claim that upstream otelc enables every signal by default.

---

## Three organizations converged upstream

**SAY**

Three organizations converged. Datadog's Orchestrion, Alibaba's rules engine,
Quesma's instrgen. They formed the OpenTelemetry Go compile-time SIG and
built otelc, a vendor-neutral tool.

Orchestrion remains a production Datadog distribution of the same core idea.

**DO**

Do not say Orchestrion was donated or renamed to otelc. It was not. Two separate
tools, same mechanism, different codebases and default tracers.

---

## A short convergence timeline

**SAY**

The projects matured in parallel. Profiling, eBPF instrumentation, and
compile-time instrumentation did not collapse into one agent. They learned to
compose.

This year both instrumentation projects reached v1. otelc in July. OBI in
October.

**DO**

Move quickly. The dates corroborate; they are not the argument. Do not
celebrate OBI here. The OBI section opens with that slide.

---

## `-toolexec` puts otelc before the compiler

**SAY**

otelc wraps the Go command. It becomes a proxy for tool invocations. It
rewrites supported syntax before go tool compile sees it. The resulting binary
contains normal SDK calls. There is no process to attach at startup.

It covers your code, dependencies, and supported standard-library paths.

**DO**

The diagram is the point. Do not over-explain the proxy mechanism.

---

## Production evidence

**SAY**

Customer adoption of Orchestrion-based Go auto-instrumentation grew by about
twenty percent. This is a production path, not a local debugging trick.

**DO**

Say exactly this. Do not add a customer denominator. Do not claim that most
users were new. The approved wording is the percentage alone.

---

## Build-time instrumentation is portable

**SAY**

No runtime privilege. No Linux kernel dependency. One build-command change.
Tested on Linux, macOS, and Windows. Go 1.25 or newer.

The trade-off is build ownership, not operating-system access.

**DO**

Read across the table, not every row.

---

## Signal depth depends on the integration bundle

**SAY**

Upstream otelc today instruments traces, HTTP and gRPC metrics, runtime
metrics, and supported log records.

Orchestrion with dd-trace-go provides traces, runtime metrics, correlated
logs, and continuous profiles.

Not every Datadog integration has moved to otelc yet.

**DO**

Connect the examples to the section's four signal indicators. The build path
can install SDK instrumentation. The selected bundle determines coverage.
Do not say otelc alone automatically enables every profile type.

---

## And it can reach deep

**SAY**

Build-time rewriting can also reach Go runtime internals.

**DO**

Advance to the linkname example, then the goroutine-local storage aspect.

---

## What Go actually has

**SAY**

Go does have linkname, a way to reach into runtime internals from your own
package.

The Go team calls the people who do this a hall of shame. Not an
instrumentation API.

**DO**

Read only the phrase "hall of shame." Do not read the whole code block.

---

## Compile time can reach Go internals! Dark Magic

**SAY**

Compile-time instrumentation can reach into Go internals. This aspect adds a
field to runtime.g for goroutine-local storage, typed accessors, and exit
cleanup.

dd-trace-go owns this tracer-context integration. otelc supplies the rewriting
engine.

**DO**

The aspect file belongs in dd-trace-go because it defines tracer-specific
runtime context. That is why the path says dd-trace-go, not otelc.

Give the Palpatine GIF one beat. It cackles at the dark magic with you. Do
not name the film.

---

## `go:linkname` variables are fragile

**SAY**

Variable linknames are fragile. Unlike function linknames, variables have no
definition/reference separation. When both sides are uninitialized BSS symbols,
the linker chooses by symbol loading order.

Ian Lance Taylor said it in golang/go 72032: the choice is arbitrary. In the
implementation it depends on the symbol loading order.

This broke between Go 1.22 and 1.23.

**DO**

Keep the distinction between function and variable linknames. Do not
over-explain BSS layout unless asked.

---

## the linker picks by symbol loading order

**SAY**

The linker picks by symbol loading order.

**DO**

Ten seconds. Do not explain the joke. The caption is the punchline to the
linkname slide. Advance.

---

## The build path has boundaries too

**SAY**

The build path has boundaries. You need control of the Go build pipeline. You
need Go 1.25 or newer. Coverage stops at the supported integration set.
Toolchain internals like -toolexec and go:linkname can change.

No root access and no kernel version gate, but the binary must be rebuilt.
What if we cannot change the build?

**DO**

Use that question to move to process start. Do not imply that more signals
make this approach available to every service.

---

## Process start: the injector

**SAY**

Next is process start. An injector activates instrumentation before the
application runs. The SDK can supply the same signal types as the build path.
The supported SDK and integrations still determine the coverage.

The constraint changes from build ownership to a compatible startup path.

**DO**

Point to the same four signal indicators. This explains capability, not a
claim that the development Go hook already implements every SDK feature.
Startup injection does not mean attachment to an already running process.

---

## How process-start injection works

**SAY**

On Linux, a dynamically linked program does not start at main. It starts in
the dynamic loader, ld.so.

The loader reads LD_PRELOAD. It maps those libraries before all others. The
ELF rules say that their initializers run before the program gains control.

So the injector runs first. It sets startup environment variables. The language
runtime does the rest: Java loads an agent, Node.js loads a module, .NET loads
a profiler.

**DO**

The two quotes in the footer are the evidence. Read neither aloud.

---

## Runtime hooks that injectors use

**SAY**

Each non-Go runtime on this table has a designed entry point for an agent. The
injector only has to find it.

The OpenTelemetry injector is a small shared library. It covers Java, Node.js,
.NET, Ruby, and Python. Datadog Single Step Instrumentation uses the same
LD_PRELOAD mechanism on Linux and lists Java, Python, Ruby, Node.js, .NET, and
PHP.

Look at the last row. Go has no such entry point.

**DO**

The two language lists come from the public pages in the footer. Python is off
by default in the OpenTelemetry injector. Say so if asked.

---

## Runtime injection is a narrower route

**SAY**

Runtime injection exists for Go, but it is narrow.

Dynatrace supports eligible dynamically linked binaries. The OpenTelemetry
host injector ships Java, Node.js, .NET, Ruby, and Python. It does not inject
Go.
The OpenTelemetry Operator has a separate, feature-gated Go eBPF sidecar.

Datadog is working on a Go path for Single-Step Instrumentation.

**DO**

Do not promise a public release date. Separate the public language lists from
the Go work in development. The next slides explain the Go restriction.

---

## A static Go binary has no loader

**SAY**

Now a default Go binary. With CGO_ENABLED=0 there is no interpreter entry in
the ELF file. The kernel never starts ld.so. There is no libc. Nobody reads
LD_PRELOAD.

With cgo it is not much better. The internal linker does not run the
constructors of preloaded libraries. Ian Lance Taylor said it plainly in that
issue: if you want LD_PRELOAD, use external linking.

**DO**

This is the problem statement for the section. Be exact: the variable is not
ignored, it is never read.

---

## `LD_PRELOAD` reaches only some Go binaries

**SAY**

The default Go binary gives the loader no entry point.

LD_PRELOAD works when the build uses the external linker and a compatible
dynamic path. It does not reach the default internally linked binary. Static
cgo and pure-Go PIE builds narrow the surface further.

**DO**

Be precise. Do not say LD_PRELOAD never works with Go. It works for some builds.
This slide is the problem statement for the section.

---

## The teaser

**SAY**

We made it work.

I am not going to tell you how today. That is next year's talk.

What you see is the invocation and the result. LD_PRELOAD, a service name,
debug mode on. Span creation and trace-id extraction on stderr.

**DO**

The contradiction is the device. The room will connect this slide to the
LD_PRELOAD slide. Get there first.

Do not be drawn on mechanism. Not the linking model, not the entry path, not
.gopclntab. Not on a slide, not in the script, not if asked. Defer.

The chip is amber: in development, not released.

---

## No rebuild

**SAY**

No rebuild. No source change. No kernel version gate. One line.

**DO**

One line. Advance.

---

## OBI: observe from the kernel

**SAY**

The third intervention point is the kernel. We can observe a deployed program
without rebuilding it or loading an SDK at startup.

OBI supplies traces and metrics. Its log feature adds correlation, not log
export. The costs are Linux, privileges, and compatibility.

**DO**

Point to the signal indicators. Introduce OBI, explain one uprobe hit, then
apply it. Keep the Go-specific details attached to the OBI example.

---

## OBI v1.0.0 shipped

**SAY**

And some news before we start. OBI v1.0.0 shipped on the thirtieth of
October. Three days before this talk. Congratulations to the OBI maintainers
and contributors.

**DO**

Celebrate it. Smile, pause, let the room clap if it wants to. Ten seconds,
no more. Do not explain "stable" here: the next slide does that. Do not name
maintainers. If the talk moves off 2 November, change "Three days ago" on
the slide.

---

## somehow, it works

**SAY**

Somehow, it works.

**DO**

Two seconds. The Palpatine GIF is the wink at the v1.0.0 news. Do not
explain it. This is the first beat of a two-part gag: the callback lands
after the pitfalls section, before Profiles.

---

## OpenTelemetry eBPF Instrumentation

**SAY**

OBI is the upstream successor to Grafana Beyla, donated to OpenTelemetry in
2025.

One DaemonSet can observe a mixed-language node. Network protocols give broad
coverage. Go-specific uprobes add library-level detail.

What does v1 mean here? A stable core: the configuration, the command line,
the images, and the telemetry marked stable. Not everything. The Go module API is not stable, even with a v1 tag.
And gRPC telemetry is still a release candidate.

**DO**

Reveal each line. Two chips: teal for the stable core, amber for what is
outside it. Say "stable core", never "OBI is stable". Do not quote the README:
at the v1.0.0 tag it still has the old "Development" wording, and the release
notes say that is a known follow-up.

---

## A checked program runs at an event

**SAY**

eBPF lets you attach a small program to an event in Linux.

A loader sends the program to the kernel. The verifier checks every memory
access and every operation before the program can run. A supported JIT can turn the bytecode into native instructions.

The program calls helpers for kernel services. It keeps state in maps. User
space reads the maps.

Loading, verification, and JIT compilation happen once, at load time. After that, the program runs each time
the event occurs.

**DO**

Credit the diagram verbally to eBPF.io. Do not say the verifier proves the
whole system safe. It checks this program.

---

## Choose the place to observe

**SAY**

Next, choose where to look. A tracepoint is a named kernel event. A kprobe
observes a kernel function. Fentry and fexit use a fast trampoline, but only
for kernel and BPF functions.

For a Go function, the hook is a uprobe: an instruction in a user-space
binary. A uretprobe observes a return. Keep that one in mind, because Go
breaks it.

**DO**

Point at the uprobe row. Do not let the room think that fentry works for Go
functions.

---

## A uprobe hit enters the kernel

**SAY**

Here is one uprobe hit. The loader finds the instruction from the symbol. The
kernel puts a breakpoint into the mapped code of the process. The file on disk
does not change.

When the goroutine reaches the breakpoint, the thread enters the kernel and our
handler runs. Then the kernel must still do the work of the original
instruction. It emulates the instruction, or it single-steps a copy. Then Go
code continues.

Newer kernels made this path scale much better. But each active hit still
crosses into the kernel. Keep that cost in mind as we apply the mechanism to OBI.

**DO**

Fifty seconds. Do not quote a nanosecond number on stage. The kernel benchmark
numbers in the research are for an empty probe, not for a real handler.

---

## OBI turns observations into spans

**SAY**

OBI uses that mechanism at supported HTTP, gRPC, and SQL functions.
It attaches uprobes at entry and at each RET instruction.

The handlers read request data. They keep timestamps and trace context in a
map keyed by process ID and goroutine. At the end site, a completed event goes
through a ring buffer to OBI in user space. OBI exports OTLP spans and metrics.

On supported paths, OBI can also write the outgoing trace header, so the next
service continues the trace.

**DO**

Show the result before the Go-specific details. Explain that the next slides
answer why OBI tracks goroutines, probes RET sites, and resolves field offsets.
Do not teach those details twice.

---

## Read Go values, not C arguments

**SAY**

Now the Go part. Go does not pass arguments the way C does. On amd64, since Go
1.17, the first integer arguments go in AX, BX, and CX. When enough registers remain, a string uses two of them. Otherwise Go passes it on the stack. A tracer that expects the C order reads garbage.

Second problem. The goroutine can start a function on one thread and finish it
on another. So the thread ID cannot tie entry and exit together. OBI uses the
process ID and the address of the goroutine, the g pointer.

**DO**

Say amd64 out loud. arm64 uses different registers. The g pointer and the
numeric goroutine ID are different values. Do not mix them.

---

## Probe the RET, not the return address

**SAY**

Here is why uretprobes and Go do not mix. A uretprobe replaces the saved
return address on the stack with a trampoline address.

Go copies stacks when they grow. To do that, the runtime walks every frame.
It finds an address that does not belong to any Go function. The runtime can
reject the stack, and the process can crash.

So OBI does not use uretprobes for Go. It disassembles the function, finds
every RET instruction, and puts an ordinary uprobe on each one. The return
address is never touched.

**DO**

Forty-five seconds. This explains OBI's RET-site probes. Do not skip it.

---

## CO-RE adapts kernel layouts, not Go layouts

**SAY**

A field in a kernel struct can move between kernel builds. BTF describes the types of the current kernel. CO-RE uses BTF to adjust the field reads
in the program before it loads. One compiled object can then work across supported kernel layouts.

Remember the limit. CO-RE knows kernel types. It knows nothing about a Go HTTP
request. For Go, we need a separate source of layouts. That is the next step.

**DO**

Thirty seconds. The dotted branch on the diagram is the point.

---

## Find the instruction and the field

**SAY**

A tracer needs two different things. An instruction address, to attach the
probe. And a field offset, to read the request inside the function.

The function address comes from the symbol table or from Go's own runtime
tables. Field offsets come from DWARF, if the binary still has debug
information. If it does not, OBI reads the Go and library versions from the
build information and looks the offsets up in a prepared database.

A function address is not a type layout. That is the Go-side half of the CO-RE
problem.

**DO**

Thirty-five seconds. Link back to the CO-RE slide.

---

## No source change. No rebuild. No rollout

**SAY**

No source change. No rebuild. No application rollout.

**DO**

Pause after each line. Then add: the DaemonSet still has a deployment and
security cost. Zero-touch describes the application, not the platform.

---

## Go library coverage: 13 documented baselines

**SAY**

Thirteen documented baselines. HTTP, gRPC, databases, messaging.

The support matrix is the contract. Library internals can change faster than a
slide deck.

**DO**

Do not read all thirteen. Point to a few categories. Call out the corrected names
only if useful: github.com/redis/go-redis/v9, not the old v8 path. Gin excludes
v1.7.5.

---

## What OBI emits

**SAY**

OBI emits traces and metrics. HTTP, gRPC, database, messaging. RED and runtime
metrics.

Its log feature enriches selected JSON and plain-text writes with trace and
span IDs while a span is active. It leaves log shipping to your existing
pipeline. It is not a log exporter.

In v1, the stable part is HTTP and SQL: their spans and duration metrics.
gRPC is a release candidate. Go runtime metrics are still in development.

**DO**

Say explicitly: correlation is log support, but OBI is not a log exporter.
The stability line is the small print at the bottom. Say it once. It tells
the room which dashboards are safe to build on.

---

## The platform contract

**SAY**

Linux only. amd64 and arm64. Kernel 5.8 or newer, with BTF. Deploy as a host
process, sidecar, or DaemonSet. macOS and Windows need a Linux VM or remote
cluster.

**DO**

Read across the table, not every row. This is the constraint, not the detail.

---

## Privileges depend on the mode

**SAY**

Privileges are a ladder, not one list.

Network capture needs BPF and raw-socket access. Application observability
adds process and executable inspection, plus perf monitoring and uprobes.
Context propagation adds network administration. Go library propagation may
need SYS_ADMIN because it uses bpf_probe_write_user.

**DO**

Speak the ladder as four rungs, never as a table. CAP_SYS_PTRACE inspects
/proc. It does not PTRACE_ATTACH. If asked about perf_event_paranoid: since
v0.14.0, OBI falls back to tracefs, so most probes attach without SYS_ADMIN.
The write helper still needs SYS_ADMIN. Secure Boot and kernel lockdown can
still turn it off even when a manifest looks correct.

---

## What actually works without source changes

**SAY**

OBI can see service boundaries, HTTP and gRPC spans, RED and runtime metrics,
supported library operations, and log correlation.

It cannot infer a tenant ID, a checkout stage, or a domain event unless those
semantics already cross an instrumented boundary.

One thing moved. If you write a span with otel.Tracer and register no SDK,
OBI can now export it. You still write the span. You do not need the SDK.

**DO**

This is the boundary slide. The honesty is the point. The otel.Tracer line
is the small print: it needs SYS_ADMIN, because OBI writes into the process
to turn on the Auto SDK.

---

## But it still has a cost

**SAY**

The application avoids a rollout. The observer still has a cost.

**DO**

Pause before the cost slide.

---

## zero-touch means zero cost... right?

**SAY**

Zero-touch does not mean zero cost.

**DO**

Let the meme ask the question. The next slide answers with the table. Two
seconds, then advance. Do not answer the meme aloud.

---

## Uprobes have real costs

**SAY**

Uprobes have real costs.

Infrastructure: an attached uprobe crosses into the kernel. Heavy contention
once hurt scalability across many CPUs. Kernel 6.12 includes major
RCU-protected hot-path improvements. Do not describe old scalability results
as current on every kernel.

Program: the BPF program itself can serialize a hot path if it touches shared
state. Instrumenting a thread-safe function does not guarantee the observer
preserves its concurrency.

Compatibility: uprobes target compiled locations and inferred layouts. Go
1.26 removed pcHeader.textStart. OBI changed its resolver in PR 1851.

**DO**

Credit Usama Saqib verbally for the two-category framing. Point to his public
FOSDEM talk in the footer.

**Static-PIE anecdote (cuttable, allow about 1:25):**

Here is what that compatibility cost looks like in practice. A Kubernetes
controller changed one build flag to static-PIE. No application code changed.
On nodes running OBI, its pods exited 139. kubectl logs previous was empty.
GOTRACEBACK equals crash was silent, because the SIGSEGV beat the Go
runtime's signal handler.

Static-PIE is ET_DYN with no PT_INTERP. The external linker restructured
segments. The runtimeText offset OBI derived from .gopclntab stopped matching
prog.Vaddr, and the computed offset put the uprobe in the wrong place.

Fixed by PR 1851, which derives runtime.text from runtime.moduledata after Go
1.26 removed pcHeader.textStart.

The line it earns: that is the maintenance cost of inferring a layout you did
not compile.

**DO**

This anecdote is marked cuttable. If running long, skip it and keep only the
PR 1851 line on the slide. Present these as evidence of maintenance cost, not
as current unfixed defects. The issue was fixed. The team changed build flags,
not application code.

---

## Usama Saqib: pitfalls of production eBPF

**SAY**

Usama Saqib covers this in depth at FOSDEM 2026. The pitfalls of building
production eBPF at Datadog: kprobe performance across kernel versions, a fentry
kernel bug, and the pain of scaling uprobes.

Twenty-eight minutes, public, and it goes deeper than this section can.

**DO**

Credit him verbally. Point to the slide link. Do not read the screenshot.

---

## somehow, it works

**SAY**

Somehow, it works.

**DO**

Ten seconds. Do not explain the joke. Explaining the joke spends the time it
bought. The caption is the punchline to the uprobe section. This is the
callback to the Palpatine gag at the v1.0.0 news. Advance.

---

## Profiles: observe CPU from the kernel

**SAY**

We now know where to intervene. What evidence does the problem need?

The build path can include profiling. This profiler gives us another route:
CPU profiles from outside the application, without rebuilding it.

**DO**

Point to profiles in the signal indicators. This is another way to collect
that signal, not a claim that profiling only exists at the kernel layer.

---

## Traces tell you which request was slow

**SAY**

Traces tell you which request was slow. Profiles tell you where the CPU went.

**DO**

Pause between the two questions. Both lines appear on one slide.

---

## OpenTelemetry eBPF Profiler

**SAY**

The OpenTelemetry eBPF Profiler originated as Elastic Universal Profiling and
joined OpenTelemetry in June 2024.

It samples CPU from the kernel. It profiles every process on a node. No
application rebuild, no injected library. It emits the OpenTelemetry Profiles
signal.

The Profiles specification is Alpha.

**DO**

The profiler itself can still be useful, but do not imply a stable wire or
data-model contract.

---

## But how does it read a stripped binary?

**SAY**

How does the profiler read a stripped Go binary?

**DO**

Advance to the runtime metadata.

---

## Go metadata tells the profiler how to unwind

**SAY**

The Go runtime needs .gopclntab to print its own stack traces. So the table
stays even in a static, stripped binary.

The profiler reads it once and prepares unwind rules: how to find the caller
from each function. It loads the rules into BPF maps. When a CPU sample fires,
the BPF unwinder walks the stack with those rules. Then the same table turns
addresses into Go function names.

Ordinary Go frames can use frame pointers. The table covers the rest. You need
no special debug build.

**DO**

Forty seconds. Let the room read the quote while you finish. Do not say that
the profiler ignores frame pointers.

---

## Zero-touch profiling still has a deployment cost

**SAY**

No source changes, no rebuild, no in-process agent. Stripped binaries are
supported.

But the agent needs Linux node access, BPF and perf monitoring or root, and a
DaemonSet or Collector distribution. CPU profiling is the confirmed core
signal.

**DO**

Read across the table, not every row.

---

## Traces and profiles. Apart

**SAY**

We have request timing and CPU samples. To connect a request to its samples,
the profiler needs request context. We will return to the proposed bridge
at the end.

Even with both signals, we can still miss the variable that explains the bug.

**DO**

Establish the correlation need. Keep the OTEP mechanism in the future section.
Return to the opening bug as you enter live debugging.

---

## each one points at the other

**SAY**

Each signal points at the other one for the missing context.

**DO**

Two seconds. The Spider-Man GIF carries the beat. Advance.

---

## Live debugging: probe a running process

**SAY**

Back to the bug from the opening. You need one variable, on one line, in
production. Every tool so far adds telemetry that you planned. This one
answers a question that you did not plan. The signal here is a dynamic log,
with a snapshot of the available variables.

**DO**

Point to logs in the signal indicators. Metrics and traces remain goals, not
capabilities of this logpoint. Name the opening loop: the log line, the
redeploy, the wrong place.

---

## The probe goes to the running process

**SAY**

You pick a line in the debugger and write a message. The backend sends the
logpoint to the Datadog agent on that host. The system probe finds the line in
the binary and attaches a uprobe.

The service keeps running. Nothing restarts. When the line runs, the probe
captures the values. The snapshot appears in your debug session.

**DO**

The diagram is simplified. The public docs do not describe the hop from the
backend to the system probe in detail, so do not add steps to it on stage.
It can take a couple of minutes after you create a logpoint before it
captures. Say so if someone asks why it is not instant.

---

## From a line to a machine address

**SAY**

This is the same uprobe as OBI, with DWARF line and variable information.

The DWARF line table maps file and line to machine addresses. The tool prefers a statement row for that line. If only other rows match, it uses the first one. That gives a PC. It turns the PC into a file offset
and attaches the uprobe there.

When the probe hits, DWARF location lists say where each variable lives at that
PC: in a register, or on the stack.

**DO**

The mechanism comes from the public datadog-agent repository. Present it as
how the code works, not as a product guarantee.

---

## Some variables are not there

**SAY**

The compiler does not keep every variable alive at every line. After inlining
and register allocation, some values have no location at that PC.

The probe still fires. The snapshot marks those variables as unavailable.
Some lines have no safe place for a probe at all, and the tool tells you.

**DO**

If the room laughs at "unavailable", let it. Every Go developer who used a
debugger on an optimised binary has seen it.

---

## Bounded by design

**SAY**

A debugger in production needs hard limits.

A logpoint that captures variables runs at most once per second. Without
capture, the limit is five thousand per second per service instance.
Logpoints expire when the debug session ends. The system probe redacts values with sensitive names, such as password, before the data leaves the host.

For Go, you need Linux 5.17 or newer and Agent 7.73 or newer on the same host. The docs strongly recommend the Go SDK 2.9 or newer.

**DO**

Every number on this slide is from the public docs in the footer. Do not add an overhead percentage. The public docs give no measured overhead figure for Go.

---

## Other ways, and their cost

**SAY**

There are other ways. A Delve breakpoint shows the available variables, but it stops the program. The Go 1.25 flight recorder does not stop anything, but you must
add it to the code, and it records an execution trace, not variable values. A
hand-written uprobe works, but you do the DWARF work yourself.

A logpoint gives bounded variable snapshots with no code change and no pause. You decode nothing by hand.

**DO**

Read the last row, not the whole table. Delve tracepoints do not stop the
program. If someone says so, agree, and say that they print events, not
snapshots.

---

## Choose the signal and the layer

**SAY**

We can now choose on two grounds. Which signal answers the question?
Which intervention point can our service support?

**DO**

Return to the lifecycle map in words. Compare signal coverage before the
constraint table.

---

## What each approach gives you

**SAY**

The build and injector paths can activate SDK instrumentation across all four
signals. Actual coverage depends on the bundle.

OBI emits traces and metrics, and correlates existing logs. The eBPF Profiler
emits profiles. Live Debugger gives us logs and variable snapshots.

Similar signals do not mean identical coverage or deployment costs.

**DO**

Keep the same signal order as the section indicators. The Go injector is in
development. Metrics and traces from live probes remain goals for the closing
section. The table describes application evidence, not each agent's diagnostic
telemetry.

---

## When to reach for what

**SAY**

No rebuild window: OBI. Non-Linux target: otelc or Orchestrion.
Mixed-language boundary coverage: OBI. Rich Go library semantics: otelc or
Orchestrion. No privileged runtime agent: otelc or Orchestrion. Whole-node
CPU profiles: the eBPF Profiler. A missing variable: a live logpoint.

**DO**

Read examples across the table, not every row. The first constraint usually
decides the first tool.

---

## A practical production combination

**SAY**

Use build-time instrumentation where you own the Go build. OBI for
rebuild-free and mixed-language boundaries. The profiler for whole-node CPU.

Use a live logpoint when that baseline does not answer the question.
Add each layer only when the signal pays for its cost.

Those are choices we can make now. What should become easier to build?

**DO**

This is an example, not a universal stack. Do not repeat the adoption number.
Keep its approved wording on screen. Use the final question to enter the
future section before the closing callback.

---

## What comes next

**SAY**

We saw the same cost several times: tools infer details that Go does not
publish as an instrumentation contract. What should Go expose so we infer less?

**DO**

Separate proposals, experiments, and aspirations. This section answers the
limitations from the lifecycle tour.

---

## User Statically-Defined Tracing (USDT)

**SAY**

USDT lets the program declare its own probes.

The producer puts a NOP at the probe site and writes an ELF note. The note
names the probe and gives a recipe for each argument: which register, which
stack slot. A tracer reads the note and attaches an ordinary uprobe at the NOP.
An optional semaphore tells the program that a tracer is present, so it can
skip expensive argument preparation when nobody listens.

USDT does not make a hit free. It makes the contract explicit.

**DO**

Expand the acronym before you use it. USDT runs on uprobes. It is not a
separate kernel mechanism.

---

## Go needs a USDT producer

**SAY**

The Go 1.26.0 source that we checked emits no native USDT probes. Salp and libstapsdt let an application
add them through cgo. Polar Signals builds the other side, a Go tracer that
reads USDT notes.

My fork experiments with producer support in the toolchain itself. It is a
proof of concept. It shows what a stable contract could look like, for eBPF
tools and for injectors.

**DO**

The fork is a proof of concept. Do not claim that it builds today or that the
commands on the slide run. Do not invent a reason why Go has no USDT.

---

## Declared probes can reduce inference

**SAY**

I want us to explore shared probe contracts for OBI, injector tooling, and
live debugging. Named events and declared arguments could remove some of the
inference at those sites.

That needs producer support and integrations. USDT does not provide a loader,
or make every source variable available.

**DO**

Present this as an aspiration. Do not claim these integrations exist. Do not
connect USDT to the undisclosed Go injector mechanism.

---

## cgo without a C toolchain

**SAY**

One more thing to watch. Today, a standard cgo build needs a C compiler at build time.

Proposal 81450 removes that need for prebuilt C libraries. You write the
bindings in Go syntax. The cgo tool generates the glue in Go and assembly.
The proposal also rewrites runtime/cgo in Go and assembly. And the internal linker learns to
reference shared libraries on Linux.

The Go team accepted the experiment, so the code can land behind a flag. The
design itself is still in review.

The useful connection is native instrumentation libraries. If we need a
prebuilt native library, this proposal could make it easier to call from Go
without a C build toolchain.

There may be a connection to an injector design, but that connection is weak.
This work does not promise new linking defaults or preload support.

**DO**

Say "accepted experiment" and "design in review". Do not say the proposal is
accepted. Do not predict which binaries an injector can reach after it ships.
That is the owner-review boundary in the outline. Re-check the issue labels
the week of the talk.

---

## Give trace context a stable Go ABI

**SAY**

We also need a stable place to keep trace context while a goroutine handles
a request. Instrumentation extracts context from the incoming request and
injects it into the outgoing request.

We use otelc rewriting to add goroutine-local storage for the dd-trace-go
integration. You saw that runtime.g field earlier. The ask is a stable Go ABI
for this storage, so integrations do not depend on private runtime layouts.

Storage alone is not propagation. We still need extraction and injection
hooks, and rules for context inheritance when work moves to another goroutine.

**DO**

Present the stable ABI as an ask, not an existing Go feature. Distinguish the
current build-time integration from a standard runtime contract. Then connect
request propagation to the profile-correlation proposal.

---

## Correlation is the missing bridge

**SAY**

Correlation is the missing bridge.

Native runtimes can publish request context through thread-local storage. Go
cannot rely on that model. Goroutines move between OS threads, and crossing
FFI on every event is too costly.

The proposed Go path uses pprof labels. The scheme is go_pprof_labels_v1.

**DO**

Say "proposed" before explaining it. This is OTEP 4947. Credit Scott Gerring
and Ivo Anjo verbally for connecting compile-time instrumentation to this
profiling path. Link only to the public OTEP. Do not claim the complete OTEP
path ships today.

---

## Compile time sets context. eBPF reads evidence

**SAY**

Compile-time instrumentation can arrange request context inside the Go process.
An out-of-process profiler can read the resulting labels. One approach supplies
semantics. The other supplies continuous evidence.

That is the goal: request context reaches profiles through a shared contract.

**DO**

Keep the proposal status visible. This is the reason to combine the layers,
not a claim that the complete OTEP path ships today.

---

## Memory profiling is in progress

**SAY**

The eBPF profiler currently gives us CPU profiles. The profiler team is working
on memory profiling too. That extends the questions we can answer with the
same signal category.

**DO**

This is work in progress, not a release announcement. Do not promise a date
or specific allocation and heap views.

---

## Live probes can grow beyond logs

**SAY**

A snapshot answers what happened in one event. A metric can answer how often
it happens. Metrics are one goal. Tracing is another, on a longer horizon:
twelve months or more.

Those are goals, not release commitments. Today, the logpoints in this talk
give us logs and variable snapshots.

**DO**

The horizon comes from the speaker, not the public documentation. Do not give
a release date. Public docs distinguish Live Debugger logpoints from Dynamic
Instrumentation metrics. Do not merge those product claims.

---

## From question to evidence

**SAY**

Those proposals can make the tools easier to build. Now return to the bug
that we can investigate with the tools we already have.

**DO**

End the future section. The agent callback uses current preview capabilities,
not a promise that depends on the proposals.

---

## The loop, without the redeploy

**SAY**

Remember the loop from the opening. The bug you cannot reproduce. The log line.
The redeploy. The wrong place.

Now: describe the bug in words. The agent places the probe and reads production
evidence. No source edit, no restart, no redeploy.

Bits Live Debugger does this today, in preview.

Same move as the opening joke. Except now the agent has the framework.

**DO**

This is the one place enthusiasm is the point. Still bounded. Name the product
once. The specifics: system-probe, the kernel floor at 5.17, logpoints that
expire automatically, the preview tier. These go here in the script because the
slide carries the idea, not the product spec.

This is the callback to the joke. The agent was missing the framework. Now it
has it.

---

## Takeaways

**DO**

Pause. Advance to the two lines that the audience should remember.

---

## Start from the constraint you cannot change

**SAY**

Start from the constraint you cannot change.

Add a layer only when its signal pays for its operational cost.

**DO**

Slow down. These two lines are the whole talk. Let them land.

---

## Get involved in the SIGs

**SAY**

If you want to help, bring a concrete requirement: a probe site, a context
contract, or a deployment restriction. The SIGs need those cases.

github.com/open-telemetry/community has every SIG's calendar, notes, and
channels.

Go Compile-Time Instrumentation. eBPF Instrumentation. The Injector. Profiling.

**DO**

Point to the community repo. All channels are listed there.

---

## Shameless plug

**SAY**

One more thing, and I am not sorry about it.

Tomorrow morning, ten forty-five, room Golab number two: my other talk. Why
Your Go Benchmarks Are Lying, and How to Stop Them.

Today was about observing what you shipped. Tomorrow is about knowing whether
it got faster.

**DO**

Deadpan. Own the plug. Say the time and the room slowly enough to photograph.

---

## Take it with you

**SAY**

The talk repository has both decks, the research, and the earlier FOSDEM
recording. The zeroins toolkit has the four commands.

Pick the constraint you cannot change. Then choose the layer that can still
reach your service.

**DO**

End with this line. Stop. Let the questions slide stay up.

---

## Questions?

**DO**

Stop. Leave the links visible for questions.

## Reserve answers

Answers to likely questions. Keep them bounded.

**Is OBI production ready now?** v1.0.0 shipped on 30 October, after two
release candidates on 7 and 16 October. The stable contract covers Config v2,
the CLI and environment variables, binaries and images, telemetry marked
stable, and the support matrix. Config v1 still works but is frozen. The
release notes list known limitations: metrics can stay missing after a Pod
restart until OBI restarts, and a child span can start before its parent.
Canary it, as the release notes say.

**Can I import OBI as a Go library?** The module tag is v1.0.0, but the
release notes exclude the Go API from the stable contract. The Collector
receiver is a separate module, still on v0.15.2.

**Go-Auto sunset.** The slide's claim is about the OpenTelemetry Operator's
feature gate, not about a Go-Auto project. The claim holds either way. Do not
discuss an Orchestrion sunset.

**Telemetry cost.** Real question. Answer with open-source backends and short
retention. You can always use an open-source observability backend and keep
signals for a shorter time in your local environment.

**OBI custom spans.** In Go, this shipped. Since v0.11.0, OBI can export
spans written with the global otel.Tracer API when no TracerProvider is
registered. Since v0.15.2 it also uses the Auto SDK embedded in otel/trace.
Limits: recognised otel versions only, amd64 or arm64, SYS_ADMIN, no kernel
lockdown, spans up to 16 KiB. If you register an SDK, OBI defers to it. The
boundary stays: the business span is still code you write.

**Injector mechanism.** Deferred to next year. The mechanism is deliberately
undisclosed. Do not add linking model, entry path, or binary-compatibility
detail. If asked, say: that is next year's talk.

## Guard rails that survive the rewrite

Never say Orchestrion was donated or renamed to otelc. C-021 is REFUTED and
both projects' people are reachable.

Never present one capability list as universal. Privileges vary by feature.

Never claim the OTEP path ships today. It is proposed work.

The standing line on the ethos slide is small print and is not read aloud.

## Public references for questions

| Claim | Public reference |
| --- | --- |
| zeroins toolkit and Agent Skill | <https://github.com/kakkoyun/zeroins> |
| opentelemetry-agent-skills | <https://github.com/ollygarden/opentelemetry-agent-skills> |
| OBI requirements and signals | <https://opentelemetry.io/docs/zero-code/obi/> |
| OBI capability ladder | <https://opentelemetry.io/docs/zero-code/obi/security/> |
| OBI trace-log correlation | <https://opentelemetry.io/docs/zero-code/obi/trace-log-correlation/> |
| OBI Go support matrix | <https://github.com/open-telemetry/opentelemetry-ebpf-instrumentation/blob/v1.0.0/SUPPORT_MATRIX.md> |
| OBI v1.0.0 release notes | <https://github.com/open-telemetry/opentelemetry-ebpf-instrumentation/releases/tag/v1.0.0> |
| OBI v1.0.0 telemetry contract | <https://github.com/open-telemetry/opentelemetry-ebpf-instrumentation/blob/v1.0.0/TELEMETRY.md> |
| uprobe performance pitfalls | <https://fosdem.org/2026/schedule/event/H3LM7G-performance_and_reliability_pitfalls_of_ebpf/> |
| RCU-protected uprobe hot path | <https://lists.openwall.net/linux-kernel/2024/08/13/142> |
| Go 1.26 OBI resolver change | <https://github.com/open-telemetry/opentelemetry-ebpf-instrumentation/pull/1851> |
| otelc v1 and mechanism | <https://opentelemetry.io/blog/2026/go-compile-time-instrumentation-v1/> |
| otelc supported libraries | <https://opentelemetry.io/docs/zero-code/go/compile-time/supported-libraries/> |
| OpenTelemetry Injector languages | <https://github.com/open-telemetry/opentelemetry-injector> |
| OpenTelemetry Operator Go sidecar | <https://opentelemetry.io/docs/platforms/kubernetes/operator/automatic/> |
| Go pprof-label context proposal | <https://github.com/open-telemetry/opentelemetry-specification/blob/main/oteps/profiles/4947-thread-ctx.md#alternative-for-go-support> |
| OpenTelemetry community SIGs | <https://github.com/open-telemetry/community> |
