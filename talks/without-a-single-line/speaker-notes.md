# Speaker notes: Zero-Touch Go Instrumentation

GoLab 2026. 45-minute hard stop: 43 minutes presented, 2 minutes buffer, no Q&A. Intermediate Go audience.

Deck: `slides/presentation.md`. Section headings below match slide titles
verbatim, so you can find your place by what is on screen.

## Contract

**SAY** lines are the words, written to be spoken. **DO** lines are delivery
cues. Memorise the purpose of each slide, then let the words follow.

The slides carry delivery cues as a small glyph after GOLAB in the footer.
`▸` means stop advancing and speak freely. `◆` is a checkpoint: look up,
scan the room, check the time. `∙` means pause after the line, and a headline
that ends in `…` says the same. `◦` means slow down, because the slide must
land. A word in yellow or italics takes the stress. A question headline means
ask it, then wait.

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
| 08 Asks for the Go team | Four asks: USDT probes, a read contract for pprof labels, `-toolexec` gaps, one start-up door. Then the tool plans. |
| 09 From question to evidence | Resolve the opening bug and the agent joke. Invite concrete contributions. |

## Timing

The `outline.md` times are working budgets, not measurements. They reserve 43
minutes for content and two minutes for pauses and overruns. The slot has no Q&A. Rehearse the new
future material. Removing the install slide does not make room for all of it.

Checkpoints: otelc by 5:00, injector by 9:30, OBI by 13:00, profiles by 23:00,
live debugging by 26:00, selection by 30:30, future work by 32:30, and the
closing callback by 37:30. Adjust these together after a timed read. The
optional static-PIE anecdote needs about 1:25 within the OBI budget.

---

## Zero-Touch

**DO**

Let the title stand. Advance.

---

## The bug you cannot reproduce locally

**SAY**

Imagine it is Friday, twenty to five. Checkout is slow, for one tenant
only. Staging is fine. Your laptop is fine.

So you add a log line around the cart total. You redeploy. Twenty minutes.

Wrong function. You move the log line. You redeploy again.

By the third deploy, the spike is gone. You never saw the value.

**DO**

Two beats of silence after "again." Do not rescue the silence.

---

## What if you did not have to?

**SAY**

What if you did not have to?

**DO**

Let the question stand. Advance.

---

## Every new dependency creates another place to forget

**SAY**

You wrapped every HTTP client and database call by hand.

The first service gets careful instrumentation. The fiftieth inherits gaps.

At fleet scale, instrumentation coverage is a platform problem.

Automatic instrumentation gives us a baseline. Later, we still need a way to
ask the question that the baseline misses.

**DO**

Land "a platform problem."

---

## Go compiled away the attachment point

**SAY**

Every other runtime has a place to intervene after the source was written.

The JVM has javaagent. Python has import hooks. .NET has profiling APIs.

Go compiles that place away. It made deployment simple. It made late
instrumentation hard.

**DO**

Point out that each runtime has one. Go does not.

---

## Hand-written instrumentation decays

**SAY**

I wrapped handlers by hand for years. Then I worked on profiling at Parca.
Now I work on compile-time instrumentation. Hand-written coverage decays.

Datadog builds at all three intervention points. I need the right combinations
to work in customer services.

**DO**

Bare beat. Let "decays" land. Do not imply work on OBI.

---

## Agent joke (slide 1)

**SAY**

Right. That is the talk. Thanks, everyone.

**DO**

Show only the full-screen screenshot. No footer or page number.
Deadpan. Two seconds of silence. Do not explain the joke.

---

## Agent joke (slide 2)

**SAY**

Not really. The agent still has to pick a mechanism, and it has to know what
that mechanism costs. That is what we need to understand.

**DO**

Show only the full-screen screenshot. No footer or page number.
The turn. Ten seconds for both slides. Do not explain the joke.
This is a plant. It pays off at the agentic close.

---

## Why Go resists instrumentation

**SAY**

So why is Go the hard one?

**DO**

Tie the missing attachment point to the opening problem. Build-time
still requires a rebuild.

---

## What makes Go different

**SAY**

The compiler emits native machine code. Pure-Go builds are static by default. There is no classloader, no general runtime hook API.

And goroutines move between OS threads on movable stacks.

There is no single point where an agent can safely rewrite every function at
startup.

**DO**

Reveal each line. Do not rush. Land the last line.

---

## Let the constraint pick the layer

**SAY**

There are three practical places to intervene. Build time. Process start. The
kernel.

Build time preserves Go semantics but requires a rebuild. Process-start
injection avoids source edits but depends on binary and linker surfaces.
Kernel observation avoids the rebuild but inherits Linux, privilege, and
compatibility constraints.

The reason this matters is that you rarely pick the layer. The constraint
picks it for you.

We will follow that order: build, process start, then kernel.

**DO**

Point to each intervention point. Not all three are required.

---

## Three intervention points. Four signals

**SAY**

At each point, ask which evidence we can collect. Traces, metrics, logs, and
profiles answer different questions about production.

We will track those signals in the same order throughout the talk.

Three parts. First, the three ways in. Second, the evidence they still miss.
Third, how to choose, and what Go could make easier.

**DO**

Introduce the signal indicators. They show capabilities, not a ranking.

---

## otelc: instrument during the build

**SAY**

Start at the build, while source structure is still available. We can add
instrumentation without writing wrappers throughout the application.

This route can reach all four signals. The SDK and integrations determine
which ones it produces. We still need a rebuild.

**DO**

Point to the four signal indicators. Upstream otelc does not enable every signal by default.

---

## Three organizations converged upstream

**SAY**

Three organizations converged. Datadog's Orchestrion, Alibaba's rules engine,
Quesma's instrgen experience. They formed the OpenTelemetry Go compile-time SIG and
built otelc, a vendor-neutral tool.

Orchestrion remains a production Datadog distribution of the same core idea.

**DO**

Do not say Orchestrion was donated or renamed to otelc. Two separate tools.

---

## A short convergence timeline

**SAY**

The projects matured in parallel. Profiling, eBPF instrumentation, and
compile-time instrumentation did not collapse into one agent. They learned to
compose.

This year both instrumentation projects reached v1. otelc in July. OBI in
October.

**DO**

Move quickly. Do not celebrate OBI here.

---

## `-toolexec` puts otelc before the compiler

**SAY**

otelc wraps the Go command. It becomes a proxy for tool invocations. It
rewrites supported syntax before go tool compile sees it. The resulting binary
contains normal SDK calls. There is no process to attach at startup.

It covers your code, dependencies, and supported standard-library paths.

**DO**

The diagram is the point. Do not over-explain the proxy.

---

## about 20%

**SAY**

Customer adoption of Orchestrion-based Go auto-instrumentation grew by about
twenty percent. This is a production path, not a local debugging trick.

**DO**

Say exactly this. Do not add a denominator or claim that most users were new.

---

## Build-time instrumentation is portable

**SAY**

No runtime privilege. No Linux kernel dependency. One build-command change.
Tested on Linux, macOS, and Windows. Go 1.26 or newer.

The trade-off is build ownership, not operating-system access.

**DO**

Read across the table, not every row.

---

## Signal depth depends on the integration bundle

**SAY**

Upstream otelc today instruments traces, HTTP and gRPC metrics, runtime
metrics, and trace IDs in supported log output.

Orchestrion with dd-trace-go provides traces, runtime metrics, correlated
logs, and continuous profiles.

Not every Datadog integration has moved to otelc yet.

**DO**

Connect the examples to the four signal indicators. Do not say otelc alone enables every profile type.

---

## And it can reach deep

**SAY**

Build-time rewriting can also reach Go runtime internals.

**DO**

Advance to the linkname example.

---

## Runtime internals are reachable. They are not an API

**SAY**

Go does have linkname, a way to reach into runtime internals from your own
package.

The Go team calls the people who do this a hall of shame. Not an
instrumentation API.

**DO**

Read only the phrase "hall of shame."

---

## Compile time can reach Go internals! Dark Magic

**SAY**

Compile-time instrumentation can reach into Go internals. This aspect adds a
field to runtime.g for goroutine-local storage, typed accessors, and exit
cleanup.

dd-trace-go owns this aspect. Orchestrion applies it. otelc ships its own
`runtime.g` rule.

**DO**

Give the Palpatine GIF one beat. Do not name the film.

---

## `go:linkname` variables are fragile

**SAY**

Variable linknames are fragile. Unlike function linknames, variables have no
definition/reference separation. When both sides were uninitialized BSS symbols,
the linker chose by symbol loading order.

The Go team said it in golang/go 72032: the choice is arbitrary. In the
implementation it depends on the symbol loading order.

This broke between Go 1.22 and 1.23. Go 1.25 now keeps the larger symbol.
Go 1.23.9 and 1.24.3 got the fix too.

What that means is: a tool that worked on one Go release can break on the
next one.

**DO**

Keep the function and variable linkname distinction. Do not explain BSS layout unless asked.

---

## the linker picked by symbol loading order

**SAY**

The linker picked by symbol loading order.

**DO**

Ten seconds. Do not explain the joke. Advance.

---

## The build path has boundaries too

**SAY**

The build path has boundaries. You need control of the Go build pipeline. You
need Go 1.26 or newer. Coverage stops at the supported integration set.
Toolchain internals like -toolexec and go:linkname can change.

No root access and no kernel version gate, but the binary must be rebuilt.
What if we cannot change the build?

**DO**

Move to the link slide. Do not imply more signals reach every service.

---

## The long version: Hooking into the Go Toolchain

**SAY**

This section is the short version. I wrote a guest post that takes the long
way. It starts from a stopwatch wrapper around `-toolexec` and builds up to
otelc itself.

If you want the internals step by step, that is the post.

**DO**

Short stop. Point at the link, not the screenshot. Then move to process start.

---

## Process start: the injector

**SAY**

Next is process start. An injector activates instrumentation before the
application runs. The SDK can supply the same signal types as the build path.
The supported SDK and integrations still determine the coverage.

The constraint changes from build ownership to a compatible startup path.

**DO**

Point to the four signal indicators. Startup injection is not attachment to a running process.

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

Python is off by default in the OpenTelemetry injector. Say so if asked.

---

## Runtime injection is a narrower route

**SAY**

Runtime injection exists for Go, but it is narrow.

Dynatrace OneAgent injects into eligible Go binaries, including static pure-Go
ones started by a dynamic parent. The OpenTelemetry
host injector ships Java, Node.js, .NET, Ruby, and Python. It does not inject
Go.
The OpenTelemetry Operator has a separate, feature-gated Go eBPF sidecar.

Datadog is working on a Go path for Single-Step Instrumentation.

**DO**

Do not promise a release date. Separate public language lists from Go work in development.

---

## A static Go binary has no loader

**SAY**

Now a default Go binary. With CGO_ENABLED=0 there is no interpreter entry in
the ELF file. The kernel never starts ld.so. There is no libc. Nobody reads
LD_PRELOAD.

With cgo, the binary is often dynamic. On glibc, the loader runs preloaded
constructors, even with internal linking. On musl, internal linking skips them.
The Go team said it plainly in that issue: anybody who wants to use
LD_PRELOAD must force the use of external linking.

**DO**

Be exact: the variable is not ignored, it is never read.

---

## `LD_PRELOAD` reaches only some Go binaries

**SAY**

The default Go binary gives the loader no entry point.

LD_PRELOAD works when the Go binary is dynamically linked. A default cgo build
is dynamic, so the loader runs preloaded constructors on glibc. A CGO_ENABLED=0
binary has no loader at all. A pure-Go PIE has a loader, but no libc for the
agent.

**DO**

Be precise. Do not say LD_PRELOAD never works with Go.

---

## We made it work

**SAY**

We made it work.

I am not going to tell you how today. That is next year's talk.

What you see is the invocation and the result. LD_PRELOAD, a service name,
debug mode on. Span creation and trace-id extraction on stderr.

**DO**

Get there first. Do not be drawn on mechanism: not the linking model, entry path,
or .gopclntab. Defer. The chip is amber: in development, not released.

---

## No rebuild

**SAY**

No rebuild. No source change. No kernel version gate. One line.

**DO**

Advance.

---

## OBI: observe from the kernel

**SAY**

The third intervention point is the kernel. We can observe a deployed program
without rebuilding it or loading an SDK at startup.

OBI supplies traces and metrics. Its log feature adds correlation, not log
export. The costs are Linux, privileges, and compatibility.

**DO**

Point to the signal indicators. Explain one uprobe hit, then apply it to OBI.

---

## OBI v1.0.0 shipped

**SAY**

And some news before we start. OBI v1.0.0 shipped on the thirtieth of
October. Three days before this talk. Congratulations to the OBI maintainers
and contributors.

**DO**

Smile, pause, let the room clap. Ten seconds. Do not explain "stable" here. If the talk moves off 2 November, change "Three days ago" on the slide.

---

## One DaemonSet, a whole node, no rebuild

**SAY**

Imagine a platform team with forty Go services and no rebuild window this
quarter. They deploy one DaemonSet. The same afternoon, they see HTTP and SQL
spans for every supported service, Go or not. What they do not see is the
tenant ID. Hold on to that.

OBI is the upstream successor to Grafana Beyla, donated to OpenTelemetry in
2025.

One DaemonSet can observe a mixed-language node. Network protocols give broad
coverage. Go-specific uprobes add library-level detail.

What does v1 mean here? A stable core: the configuration, the command line,
the images, and the telemetry marked stable. Not everything. The Go module API is not stable, even with a v1 tag.
And gRPC telemetry is still a release candidate.

**DO**

Two chips: teal for the stable core, amber for what is outside it. Say "stable core", never "OBI is stable". Do not quote the README.

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

Credit the diagram verbally to eBPF.io. Do not say the verifier proves the system safe.

---

## For Go code, the hook is a uprobe

**SAY**

Next, choose where to look. A tracepoint is a named kernel event. A kprobe
observes a kernel function. Fentry and fexit use a fast trampoline, but only
for kernel and BPF functions.

For a Go function, the hook is a uprobe: an instruction in a user-space
binary. A uretprobe observes a return. Keep that one in mind, because Go
breaks it.

**DO**

Point at the uprobe row. Do not imply fentry works for Go functions.

---

## A uprobe hit enters the kernel

**SAY**

Here is one uprobe hit. Think of it this way: a breakpoint that does not
stop the program.

The loader finds the instruction from the symbol. The
kernel puts a breakpoint into the mapped code of the process. The file on disk
does not change.

When the goroutine reaches the breakpoint, the thread enters the kernel and our
handler runs. Then the kernel must still do the work of the original
instruction. It emulates the instruction, or it single-steps a copy. Then Go
code continues.

Newer kernels made this path scale much better. But each active hit still
crosses into the kernel. Keep that cost in mind as we apply the mechanism to OBI.

**DO**

Fifty seconds. Do not quote a nanosecond number on stage.

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

Show the result first. The next slides explain the Go details.

---

## Read Go values, not C arguments

**SAY**

Now the Go part. Go does not pass arguments the way C does. On amd64, since Go
1.17, the first integer arguments go in AX, BX, and CX. When enough registers remain, a string uses two of them. Otherwise Go passes it on the stack. A tracer that expects the C order reads garbage.

Second problem. The goroutine can start a function on one thread and finish it
on another. So the thread ID cannot tie entry and exit together. OBI uses the
process ID and the address of the goroutine, the g pointer.

**DO**

Say amd64 out loud. Do not mix the g pointer and the goroutine ID.

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

What that means is: OBI never touches the stack that Go needs to move.

**DO**

Forty-five seconds. Do not skip it.

---

## CO-RE adapts kernel layouts, not Go layouts

**SAY**

A field in a kernel struct can move between kernel builds. BTF describes the types of the current kernel. CO-RE uses BTF to adjust the field reads
in the program before it loads. One compiled object can then work across supported kernel layouts.

Remember the limit. CO-RE knows kernel types. It knows nothing about a Go HTTP
request. For Go, we need a separate source of layouts. That is the next step.

**DO**

Thirty seconds. The dotted branch is the point.

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

Thirty-five seconds. Link back to CO-RE.

---

## No source change. No rebuild. No rollout

**SAY**

No source change. No rebuild. No application rollout.

**DO**

Pause after each line. Then add: the DaemonSet still has a deployment and security cost.

---

## Go library coverage: 13 documented baselines

**SAY**

Thirteen documented baselines. HTTP, gRPC, databases, messaging.

The support matrix is the contract. Library internals can change faster than a
slide deck.

**DO**

Do not read all thirteen. Point to a few categories.

---

## OBI emits traces and metrics. Logs get correlation

**SAY**

OBI emits traces and metrics. HTTP, gRPC, database, messaging. RED and runtime
metrics.

Its log feature enriches selected JSON and plain-text writes with trace and
span IDs while a span is active. It leaves log shipping to your existing
pipeline. It is not a log exporter. It needs Linux 6.0 or newer and no kernel
lockdown.

In v1, the stable part is HTTP and SQL: their spans and duration metrics.
gRPC is a release candidate. Go runtime metrics are still in development.

**DO**

Say explicitly: correlation is log support, not a log exporter. Say the stability line once.

---

## OBI needs Linux, BTF, and kernel 5.8 or a backport

**SAY**

Linux only. amd64 and arm64. Kernel 5.8 or newer, with BTF. Deploy as a host
process, sidecar, or DaemonSet. macOS and Windows need a Linux VM or remote
cluster.

**DO**

Read across the table, not every row.

---

## Privileges depend on the mode

**SAY**

Privileges are a ladder, not one list.

Network capture needs BPF and raw-socket access. Application observability
adds perf monitoring, raw sockets, and process and executable inspection.
Context propagation adds network administration. Go library propagation may
need SYS_ADMIN on kernel 5.10 or newer because it uses bpf_probe_write_user.

What that means is: the feature you turn on decides the access you ask for.

**DO**

Speak the ladder as four rungs, never as a table. CAP_SYS_PTRACE inspects /proc. It does not PTRACE_ATTACH. Since v0.14.0, most probes attach without SYS_ADMIN. The write helper still needs SYS_ADMIN. Secure Boot and kernel lockdown can still turn it off.

---

## What actually works without source changes

**SAY**

OBI can see service boundaries, HTTP and gRPC spans, RED and runtime metrics,
supported library operations, and log correlation.

Remember the platform team. It cannot infer their tenant ID, a checkout stage, or a domain event unless those
semantics already cross an instrumented boundary.

One thing moved. If you write a span with otel.Tracer and register no SDK,
OBI can now export it. You still write the span. You do not need the SDK.

**DO**

The honesty is the point. The otel.Tracer line needs SYS_ADMIN.

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

Two seconds, then advance. Do not answer the meme aloud.

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

Credit Usama Saqib verbally. Point to his FOSDEM talk in the footer.

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

Cuttable. If running long, skip it and keep only the PR 1851 line. Present it as maintenance cost, not an unfixed defect.

---

## Usama Saqib: pitfalls of production eBPF

**SAY**

Usama Saqib covers this in depth at FOSDEM 2026. The pitfalls of building
production eBPF at Datadog: kprobe performance across kernel versions, a fentry
kernel bug, and the pain of scaling uprobes.

Twenty-eight minutes, public, and it goes deeper than this section can.

**DO**

Credit him verbally. Do not read the screenshot.

---

## somehow, it works

**SAY**

Somehow, it works.

**DO**

Ten seconds. Do not explain the joke. Advance.

---

## Profiles: observe CPU from the kernel

**SAY**

That was the first part, the three ways in. Second part: the evidence they
still miss.

We now know where to intervene. What evidence does the problem need?

The build path can include profiling. This profiler gives us another route:
CPU profiles from outside the application, without rebuilding it.

**DO**

Point to profiles in the signal indicators.

---

## Traces tell you which request was slow

**SAY**

Traces tell you which request was slow. Profiles tell you where the CPU went.

**DO**

Pause between the two questions.

---

## One profiler, every process on the node

**SAY**

The OpenTelemetry eBPF Profiler originated as Elastic Universal Profiling and
joined OpenTelemetry in June 2024.

It samples CPU from the kernel. It profiles every process on a node. No
application rebuild, no injected library. It emits the OpenTelemetry Profiles
signal.

The Profiles specification is Alpha.

**DO**

Do not imply a stable wire or data-model contract.

---

## But how does it read a stripped binary?

**SAY**

How does the profiler read a stripped Go binary?

**DO**

Advance.

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

Forty seconds. Do not say the profiler ignores frame pointers.

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

Establish the correlation need. Keep the OTEP mechanism for the future section.

---

## each one points at the other

**SAY**

Each signal points at the other one for the missing context.

**DO**

Two seconds. Advance.

---

## Live debugging: probe a running process

**SAY**

Back to Friday, twenty to five. You need one value, the cart total, on one
line, in production. Every tool so far adds telemetry that you planned. This one
answers a question that you did not plan. The signal here is a dynamic log,
with a snapshot of the available variables.

**DO**

Point to logs in the signal indicators. Metrics and traces are goals, not capabilities. Name the opening loop.

---

## The probe goes to the running process

**SAY**

You pick a line in the debugger and write a message. The backend sends the
logpoint to the Datadog agent on that host. The system probe finds the line in
the binary and attaches a uprobe.

The service keeps running. Nothing restarts. When the line runs, the probe
captures the values. The snapshot appears in your debug session.

**DO**

Do not add steps to the diagram. A logpoint can take a couple of minutes to
capture. If asked why it is not instant, say so.

---

## From a line to a machine address

**SAY**

This is the same uprobe as OBI, with DWARF line and variable information.

The DWARF line table maps file and line to machine addresses. The tool prefers a statement row for that line. If only other rows match, it uses the first one. That gives a PC. It turns the PC into a file offset
and attaches the uprobe there.

When the probe hits, DWARF location lists say where each variable lives at that
PC: in a register, or on the stack.

**DO**

The source is the public datadog-agent code. Present it as how the code works,
not as a product guarantee.

---

## Some variables are not there

**SAY**

The compiler does not keep every variable alive at every line. After inlining
and register allocation, some values have no location at that PC.

The probe still fires. The snapshot marks those variables as unavailable.
Some lines have no safe place for a probe at all, and the tool tells you.

**DO**

If the room laughs at "unavailable", let it.

---

## Bounded by design

**SAY**

A debugger in production needs hard limits.

A logpoint that captures variables runs at most once per second. Without
capture, the limit is five thousand per second per service instance.
Logpoints expire when the debug session ends. The system probe redacts values with sensitive identifiers, such as password, before the data leaves the host.

For Go, you need Linux 5.17 or newer and Agent 7.73 or newer on the same host. The docs strongly recommend the Go SDK 2.9 or newer.

**DO**

Do not add an overhead percentage. The public docs give none for Go.

---

## Other ways, and their cost

**SAY**

There are other ways. A Delve breakpoint shows the available variables, but it stops the program. The Go 1.25 flight recorder does not stop anything, but you must
add it to the code, and it records an execution trace, not variable values. A
hand-written uprobe works, but you do the DWARF work yourself.

A logpoint gives bounded variable snapshots with no code change and no pause. You decode nothing by hand.

**DO**

Read the last row, not the whole table. Delve tracepoints print events, not snapshots.

---

## Choose the signal and the layer

**SAY**

Third part: how to choose, and what Go could make easier.

We can now choose on two grounds. Which signal answers the question?
Which intervention point can our service support?

**DO**

Compare signal coverage before the constraint table.

---

## Similar signals, different coverage

**SAY**

The build and injector paths can activate SDK instrumentation across all four
signals. Actual coverage depends on the bundle.

OBI emits traces and metrics, and correlates existing logs. The eBPF Profiler
emits profiles. Live Debugger gives us logs and variable snapshots.

Similar signals do not mean identical coverage or deployment costs.

**DO**

Keep the signal order. Say once: SDK means it depends on the SDK and
integrations. The Go injector is in development. Live probe metrics and traces remain goals.

---

## When to reach for what

**SAY**

No rebuild window: OBI. Non-Linux target: otelc or Orchestrion.
Mixed-language boundary coverage: OBI. Rich Go library semantics: otelc or
Orchestrion. No privileged runtime agent: otelc or Orchestrion. Whole-node
CPU profiles: the eBPF Profiler. A missing variable: a live logpoint.

**DO**

Read examples across the table, not every row.

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

---

## Asks for the Go team

**SAY**

These are asks, not demands. I have four, and a bonus.

If you work on Go, I will find you in the hallway.

**DO**

One beat. Deadpan. Do not explain the GIF.

---

## They already asked the question

**SAY**

In a Go runtime diagnostics sync, the question came up like this:

"We don't have a great way to add instrumentation in general. Companies will maintain patches to add hooks. What should we do?"

The Go team answered: "Maybe eBPF is the answer?"

Our answer is yes, if Go gives eBPF something stable to read.

Go 1.27 moved HTTP/2 into a new internal package. It also added a field to moduledata. Tools that inferred by symbol or offset had to catch up.

**DO**

Say it as thanks, not blame. Say "the Go team". Do not name people.

---

## Ask 1: USDT probes in Go

**SAY**

USDT lets a program declare its own probes. The producer puts a NOP at the probe site and writes an ELF note. The note names the probe and says where each value lives.

Go 1.27 emits no USDT probes. Salp adds them through cgo. My fork is a proof of concept. It shows the toolchain side.

The OpenTelemetry eBPF profiler now reads allocator USDT probes for memory profiles. The Go allocator has none.

So the ask is simple. Let the toolchain emit these notes. Start with runtime sites: goroutine start and exit, GC phases, and allocation samples.

In the December 2024 sync, the Go team asked, "How would this look?" The fork is one answer.

**DO**

If someone cites golang/go#22008, a USDT site is fixed at compile time. Call the fork a proof of concept, not a plan.

---

## Ask 2: a read contract for pprof labels

**SAY**

This ask does not add goroutine-local storage. The Go team rejected that many times.

Profile labels already flow through contexts, as designed. dd-trace-go already sets pprof labels.

OpenTelemetry proposal 4947 tells Go readers to read pprof labels. Today, eBPF readers infer where the label field lives in each release. Build-time tools add fields to runtime.g.

The ask is to document where the labels live, and keep that layout stable for out-of-process readers.

**DO**

Lead with "no new API". Then say "read contract". Present proposal 4947 as proposed work.

---

## Ask 3: close the `-toolexec` gaps

**SAY**

otelc and Orchestrion both build on `-toolexec`. A tool cannot add its own inputs to a package build ID. Then the build cache can reuse a stale result.

Issue 69887 lists the gaps. On that issue, the Go team called it "a problem report, which is still very helpful".

The ask is to close those gaps. It is not a new build mode.

**DO**

Do not repeat the 20% number as a claim about Go users.

---

## Ask 4: one supported start-up door

**SAY**

Other runtimes give an agent one documented door. Java has JAVA_TOOL_OPTIONS.

Go gives an agent a matrix. The agent must handle libc, which is glibc, musl, or none. It must handle link mode, internal or external. It must handle build mode, exe, PIE, or static.

The plugin package does not solve this. Its documentation says crashes are likely unless the application and its plugins use the same toolchain version, build tags, flags, and dependency sources. For a vendor, the support matrix grows fast.

The ask is simple. Tell agent authors which door Go supports.

Native agent libraries may fit cgo without a C toolchain. The accepted experiment is GOEXPERIMENT cgobindings. The fit is still open.

**DO**

Keep this generic. Never describe how the Datadog injector links or enters.

---

## Four asks. I will find you in the hallway

**SAY**

Four asks. USDT probes. A read contract for pprof labels. The `-toolexec` gaps. One start-up door.

There is one bonus. Stable runtime offsets, such as moduledata.

The QR code leads to draft problem reports in the talk repository.

If you work on Go, I will find you in the hallway. If you do not, please introduce me.

**DO**

Pause on the QR code for three seconds.

---

## Where our tools go next

**SAY**

Live Debugger has logpoints and variable snapshots today. Metrics are a goal. Traces are a longer-term goal, more than twelve months away.

The Go injector is in development. The plan is Go in Single-Step Instrumentation.

The eBPF profiler has CPU profiles today. Allocation profiling is merged on main. Live heap is in review.

These are goals, not release commitments.

**DO**

Say "goals" out loud. Do not give a release date.

---

## From question to evidence

**SAY**

Those proposals can make the tools easier to build. Now return to the bug
that we can investigate with the tools we already have.

**DO**

End the future section. The agent callback uses current preview capabilities.

---

## The loop, without the redeploy

**SAY**

Remember Friday. The slow tenant. The log line. The redeploy. The wrong place.

Now: describe the bug in words. The agent places the probe and reads production
evidence. No source edit, no restart, no redeploy.

Bits Live Debugger does this today, in preview.

Same move as the opening joke. Except now the agent has the framework.

**DO**

This is the one place enthusiasm is the point. Name the product once. Give the specifics here: system-probe, kernel 5.17, logpoints that expire, preview tier.

---

## Takeaways

**SAY**

Go gave us simple binaries. We paid for them with late instrumentation.
That bill is getting smaller.

**DO**

Pause. Advance to the two lines to remember.

---

## Start from the constraint you cannot change

**SAY**

Start from the constraint you cannot change.

Add a layer only when its signal pays for its operational cost.

**DO**

Slow down. These two lines are the whole talk.

---

## Get involved in the SIGs

**SAY**

If you want to help, bring a concrete requirement: a probe site, a context
contract, or a deployment restriction. The SIGs need those cases.

These tools are built in the open, in these SIGs. Bring them your case.

github.com/open-telemetry/community has every SIG's calendar, notes, and
channels.

Go Compile-Time Instrumentation. eBPF Instrumentation. The Injector. Profiling.

**DO**

Point to the community repo.

---

## Shameless plug

**SAY**

One more thing, and I am not sorry about it.

Tomorrow morning, ten forty-five, room Golab number two: my other talk. Why
Your Go Benchmarks Are Lying, and How to Stop Them.

Today was about observing what you shipped. Tomorrow is about knowing whether
it got faster.

**DO**

Deadpan. Say the time and the room slowly enough to photograph.

---

## Take it with you

**SAY**

The talk repository has both decks, the research, and the earlier FOSDEM
recording. The zeroins toolkit has the four commands.

Pick the constraint you cannot change. Then choose the layer that can still
reach your service.

**DO**

Advance to the last slide.

---

## Grazie!

**SAY**

Next time production surprises you, do not redeploy to ask. Ask. Without
changing a single line of code.

Grazie.

**DO**

End with this line. Stop. The slot has no Q&A: point to the hallway and
leave the links visible.

## Reserve answers

Answers for hallway questions. The slot has no Q&A. Keep them bounded.

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
