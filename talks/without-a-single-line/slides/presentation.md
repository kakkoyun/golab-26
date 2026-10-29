---
marp: true
theme: golab
# fragment-floor: 27. Eight lists use `*` fragment bullets for selective
# progressive reveal. Lists inside .columns are excluded on purpose. MD004 is
# disabled, so a mixed `*`/`-` deck lints clean. Reveals animate only in
# bespoke HTML; the PDF handout shows everything at once.
math: mathjax
html: true
paginate: true
header: "Zero-Touch Go Instrumentation · GoLab 2026"
footer: " "
style: |
  .columns { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1.5rem; }
  .columns3 { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1rem; }
  .medium { font-size: 1.0em; }
  .small  { font-size: 0.8em; }
  .tiny   { font-size: 0.6em; }
---

<!-- _class: title gopher-network -->
<!-- _paginate: false -->
<!-- _header: "" -->

##### GoLab · 2026

# Zero-Touch

### Go Instrumentation

How to Instrument Go Without Changing a Single Line of Code

### Kemal Akkoyun · Datadog

---

<!-- _paginate: false -->

## Why observability matters

<br>

You cannot fix what you cannot *see*.

**Traces**, **metrics**, **logs**, **profiles**: the four signals that tell you what your code is doing in production.

---

<!-- _paginate: false -->

## The bug you cannot reproduce locally

<br>

* Added a log line. Redeployed.
* Wrong place. Did it again.

---

<!-- _class: vcenter -->
<!-- _paginate: false -->

# What if you did not have to?

---

<!-- _class: vcenter -->

# Every new dependency creates another place to forget

<br>

You wrapped every HTTP client and database call by hand.

The first service gets careful instrumentation.

The fiftieth inherits gaps.

---

## Other runtimes have an attachment point

| Runtime | Zero-code mechanism |
| --- | --- |
| **JVM** | `-javaagent`, JVMTI, bytecode rewriting |
| **Python** | Import hooks, `sys.settrace` |
| **.NET** | CLR profiling APIs and startup hooks |
| **Go** | Native binary. No classloader. No bytecode. |

<br>

### Go made deployment simple. It made late instrumentation hard

---

<!-- _class: vcenter -->

## Why we care

| Layer | What | Constraint |
| --- | --- | --- |
| *Build time* | `otelc` | Rebuild required |
| *Process start* | Injector | Binary/linking restrictions |
| *Runtime + kernel* | eBPF + profiling | Linux, privileges, kernel contracts |

<br>

I wrapped handlers by hand for years. Every job taught me the same thing: hand-written instrumentation *decays*.

Datadog builds at all three layers. Each solves a different constraint.

---

<!-- _paginate: false -->
<!-- _header: "" -->

![bg contain](../assets/cc_opening_joke_1.png)

---

<!-- _paginate: false -->
<!-- _header: "" -->

![bg contain](../assets/cc_opening_joke_2.png)

---

<!-- _class: section -->
<!-- _paginate: false -->

###### 01

# Why Go resists instrumentation

---

## What makes Go different

* The compiler emits native machine code.
* The internal linker produces static binaries by default.
* There is no classloader or general runtime hook API.
* Goroutines move between OS threads and use movable stacks.

<br>

There is no single point where an agent can safely rewrite every function at startup.

---

## What Go actually has

###### runtime/proc.go

```go
// gopark should be an internal detail,
// but widely used packages access it using linkname.
// Notable members of the hall of shame include:
// ...
```

<br>

The Go team calls this access pattern a "hall of shame," not an instrumentation API.

---

## Choose where to intervene

<div class="center">

```mermaid
flowchart LR
    A[source] --> B[build] --> C[link] --> D[process start] --> E[runtime] --> F[kernel]
    B --> G[otelc]
    D --> H[injector]
    F --> I[eBPF]
```

</div>

| Layer | Trade-off |
| --- | --- |
| **Build** | Rebuild required; rich Go semantics; portable binary |
| **Process start** | No source change; binary/linking restrictions |
| **Kernel** | No rebuild; Linux, privileges, and kernel contracts |

---

## Runtime injection is a narrower route

* Dynatrace OneAgent supports eligible dynamically linked Go binaries.
* The OpenTelemetry host injector ships Java, Node.js, .NET, Ruby, and Python agents. It does not inject Go.
* Datadog is working on a Go path for Single-Step Instrumentation.

<br>

Runtime injection is useful, but Go's default static binary leaves less surface to attach to.

---

<!-- _class: punchline dark -->
<!-- _paginate: false -->

# Three open-source projects. *Three approaches.*

---

## A short convergence timeline

| Date | Milestone |
| --- | --- |
| Jun 2024 | Elastic's profiler joins OpenTelemetry |
| Jan 2025 | Alibaba, Datadog, and Quesma form the Go compile-time SIG |
| 2025 | Beyla becomes OpenTelemetry eBPF Instrumentation |
| Jul 2026 | `otelc` v1 becomes stable |

The projects did not collapse into one agent. They learned to compose.

---

<!-- _class: section -->
<!-- _paginate: false -->

###### 02

# eBPF, from the ground up

---

## A checked program runs at an event

<div class="center">

![width:860](../assets/ebpf-io-loader.png)

</div>

Load once. The verifier checks it. It runs when the event occurs.

<div class="tiny">

Diagram: eBPF.io authors, "Loader", [ebpf.io/what-is-ebpf](https://ebpf.io/what-is-ebpf/), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

</div>

---

## CO-RE adapts kernel layouts, not Go layouts

<div class="center">

```mermaid
flowchart LR
    A[BPF object + relocations] --> C[loader]
    B[target kernel BTF] --> C
    C --> D[adjusted field reads]
    D --> E[verifier]
    F[Go library layouts] -.->|separate resolver| G[Go field offsets]
```

</div>

BTF describes the kernel's types. CO-RE fixes field reads at load time.

**A Go HTTP request is not a kernel type.**

---

## Choose the place to observe

| Hook | Observes |
| --- | --- |
| tracepoint | a named kernel event |
| kprobe | a kernel function or instruction |
| fentry / fexit | a kernel or BPF function, through a BPF trampoline |
| **uprobe** | **an instruction in a user-space binary** |
| uretprobe | a function return, through a return trampoline |

<br>

The hook decides what you can see. For Go code, the hook is a **uprobe**.

---

## A uprobe hit enters the kernel

<div class="center">

```mermaid
flowchart LR
    A[Go instruction] -->|breakpoint trap| B[BPF handler in the kernel]
    B --> C[emulate or single-step the original]
    C --> D[Go code resumes]
```

</div>

<div class="small">

Conventional x86 path. The kernel patches the mapped code, not the file on disk. Every active hit has a cost.

</div>

---

## Read Go values, not C arguments

<div class="center">

```mermaid
flowchart LR
    A[goroutine g] --> B[thread A at entry]
    A --> C[thread B at exit]
    B --> D[key: PID + g]
    C --> D
    D --> E[one request]
```

</div>

A goroutine is the identity. A thread is only the carrier.

<div class="small">

amd64 ABIInternal (Go 1.17+): the first integer arguments go in `AX`, `BX`, `CX`, not in the C order.

</div>

---

## Probe the RET, not the return address

<div class="columns">
<div>

### Conventional uretprobe

Replaces the saved return address with a trampoline.

Go copies the stack when it grows. The runtime can reject the foreign frame.

<span class="chip caution">crash risk in Go</span>

</div>
<div>

### What OBI does

Finds every `RET` instruction in the function.

Attaches an ordinary uprobe at each one.

The caller address stays untouched.

</div>
</div>

---

## Find the instruction and the field

<div class="center">

```mermaid
flowchart LR
    A[Go ELF] -->|symbols, runtime tables| B[where to attach]
    A -->|DWARF, or versions + offset database| C[where the fields are]
    B --> D[attach and read]
    C --> D
```

</div>

A function address is not a type layout.

---

## User Statically-Defined Tracing (USDT)

<div class="center">

```mermaid
flowchart LR
    N[ELF note] -->|name + argument recipe| T[tracer]
    T -->|attach uprobe| P[NOP at the probe site]
    T -.->|optional| S[semaphore]
    S -.->|tracer present| P
```

</div>

The producer names the probe and says where each value lives.

---

## Go needs a USDT producer

<div class="columns">
<div>

![width:480](../assets/github_kakkoyun_usdt_poc.png)

</div>
<div>

* Go 1.26.0 emits no native USDT probes.
* Salp and libstapsdt add them through cgo.
* Polar Signals builds a Go tracer that reads them.

```bash
# github.com/kakkoyun/go/tree/poc_usdt
go tool usdt list ./...
```

<span class="chip caution">proof of concept</span>

</div>
</div>

---

<!-- _class: section -->
<!-- _paginate: false -->

###### 03

# OBI: observe from the kernel

---

## OpenTelemetry eBPF Instrumentation

**OBI** is the upstream successor to Grafana Beyla, donated to OpenTelemetry in 2025.

* No application rebuild.
* One DaemonSet can observe a mixed-language node.
* Network protocols provide broad coverage.
* Go-specific uprobes add library-level detail.

<br>

<span class="chip caution">v0: breaking changes are still possible</span>

---

## OBI turns observations into spans

<div class="center">

```mermaid
flowchart LR
    A[HTTP entry uprobe] --> D[state keyed by PID + g]
    B[SQL and gRPC uprobes] --> D
    C[RET-site uprobes] --> D
    D --> E[ring buffer]
    E --> F[OBI user space]
    F --> G[OTLP spans + metrics]
    D -.-> H[outgoing trace header]
```

</div>

Probe sites give events. Correlation turns them into spans.

---

<!-- _class: punchline dark -->
<!-- _paginate: false -->

# No source change. No rebuild. No *rollout*.

---

## Go library coverage: 13 documented baselines

<div class="columns">
<div>

- `net/http`
- `golang.org/x/net/http2`
- `gorilla/mux`
- `gin-gonic/gin`
- `google.golang.org/grpc`
- `net/rpc/jsonrpc`
- `database/sql`

</div>
<div>

- `go-sql-driver/mysql`
- `lib/pq`
- `redis/go-redis/v9`
- `segmentio/kafka-go`
- `IBM/sarama`
- `mongo-driver` v1 and v2

</div>
</div>

<div class="tiny">

`gin >= v1.6.0, != v1.7.5` · `redis/go-redis/v9 >= v9.0.0` · [OBI support matrix](https://github.com/open-telemetry/opentelemetry-ebpf-instrumentation/blob/main/SUPPORT_MATRIX.md)

</div>

---

## What OBI emits

<div class="columns">
<div>

### Native signals

**Traces**
HTTP, gRPC, database, messaging

**Metrics**
RED and runtime metrics

</div>
<div>

### Log correlation

OBI can enrich selected **JSON logs** with `trace_id` and `span_id` while a span is active.

It leaves log shipping to your existing pipeline. It is not a log exporter.

</div>
</div>

<div class="tiny">

[OpenTelemetry: OBI trace-log correlation](https://opentelemetry.io/docs/zero-code/obi/trace-log-correlation/)

</div>

---

## The platform contract

| Requirement | OBI |
| --- | --- |
| Operating system | Linux only |
| Architecture | `amd64`, `arm64` |
| Kernel | 5.8+, or documented RHEL 4.18+ backports |
| Kernel metadata | BTF |
| Deployment | Host process, sidecar, or DaemonSet |
| macOS / Windows | Linux VM or remote cluster |

---

## Privileges depend on the mode

| Mode | Additional access |
| --- | --- |
| Network flow capture | `CAP_BPF`, `CAP_NET_RAW` |
| Application observability | Process/ELF access, `CAP_PERFMON`, uprobes |
| Context propagation | `CAP_NET_ADMIN` |
| Go library propagation | May require `CAP_SYS_ADMIN` |

<br>

`kernel.perf_event_paranoid`, Secure Boot, and kernel lockdown can change what works.

---

## What actually works without source changes

<div class="columns">
<div>

### OBI handles

- Service boundaries
- HTTP and gRPC spans
- RED and runtime metrics
- Supported library operations
- JSON log correlation

</div>
<div>

### Application code still owns

- Business events
- Domain-specific attributes
- Arbitrary internal functions
- Unsupported libraries
- Custom sampling decisions

</div>
</div>

---

<!-- _class: punchline dark -->
<!-- _paginate: false -->

# But it still has a *cost*

---

## Uprobes have real costs

<div class="columns">
<div>

### Infrastructure cost

An attached uprobe crosses into the kernel. Heavy contention once hurt scalability across many CPUs.

Kernel 6.12 includes major RCU-protected hot-path improvements.

</div>
<div>

### Program and compatibility cost

Shared BPF state can serialize a concurrent application path.

Go runtime and library layout changes can invalidate offsets. Go 1.26 required an OBI symbol-resolution fix.

</div>
</div>

<div class="tiny">

[Usama Saqib, FOSDEM 2026](https://fosdem.org/2026/schedule/event/H3LM7G-performance_and_reliability_pitfalls_of_ebpf/) · [Linux uprobe hot-path series](https://lists.openwall.net/linux-kernel/2024/08/13/142) · [OBI PR #1851](https://github.com/open-telemetry/opentelemetry-ebpf-instrumentation/pull/1851)

</div>

---

## Usama Saqib: pitfalls of production eBPF

<div class="columns">
<div class="center">

![width:480](../assets/usama_saqib_fosdem_2026.png)

</div>
<div>

He covers the pitfalls found building production eBPF at Datadog: kprobe performance across kernel versions, a fentry kernel bug, and the pain of scaling uprobes.

Twenty-eight minutes, public, and it goes deeper than this section can.

[Performance and reliability pitfalls of eBPF, FOSDEM 2026](https://fosdem.org/2026/schedule/event/H3LM7G-performance_and_reliability_pitfalls_of_ebpf/)

</div>
</div>

---

<!-- _class: meme -->
<!-- _paginate: false -->

![bg contain](../assets/meme_somehow_it_works.png)

somehow, it works

---

<!-- _class: section -->
<!-- _paginate: false -->

###### 04

# otelc: instrument during the build

---

## Three organizations converged upstream

<div class="center">

```mermaid
flowchart LR
    A[Datadog Orchestrion] --> D[OpenTelemetry Go compile-time SIG]
    B[Alibaba rules engine] --> D
    C[Quesma instrgen] --> D
    D --> E[otelc]
```

</div>

`otelc` is a vendor-neutral tool built by the SIG.

Orchestrion remains a production Datadog distribution of the same core idea.

---

## `-toolexec` puts otelc before the compiler

<div class="center">

```mermaid
flowchart TD
    A[go build ./...] --> B[-toolexec otelc]
    B --> C[parse and rewrite .go]
    C --> D[go tool compile]
    D --> E[binary with instrumentation]
```

</div>

---

<!-- _class: vcenter -->

## Production evidence

| | |
| ---: | --- |
| <span style="font-size: 2.5em; color: var(--purple); font-weight: 700;">v1</span> | <span style="font-size: 2.5em; color: var(--purple); font-weight: 700;">20%</span> |
| Stable upstream tool | Growth in customers adopting auto-instrumentation |

<br>

One build-command change can standardize instrumentation across a fleet.

---

## Build-time instrumentation is portable

| | otelc |
| --- | --- |
| Runtime privilege | None |
| Linux kernel dependency | None |
| Build pipeline change | `otelc go build` |
| Tested build targets | Linux, macOS, Windows |
| Go baseline | Go 1.25+ |
| Runtime cost | Injected SDK and instrumentation code |

<br>

The trade-off is build ownership, not operating-system access.

---

## Signal depth depends on the integration bundle

<div class="columns">
<div>

### Upstream otelc today

- Traces
- HTTP and gRPC metrics
- Go runtime metrics
- `slog` and Logrus records

</div>
<div>

### Orchestrion + dd-trace-go

- Traces
- Runtime metrics
- Correlated logs
- Continuous profiles

</div>
</div>

Not every Alibaba and Datadog integration has moved to otelc yet. We will have much more.

---

<!-- _class: punchline dark -->
<!-- _paginate: false -->

# And it can reach *deep*

---

## Compile time can reach Go internals! Dark Magic!

###### gls.orchestrion.yml

```yaml
join-point:
  struct-definition: runtime.g
advice:
  - add-struct-field:
      name: __dd_gls_v2
      type: any
```

<div class="small">

The aspect adds goroutine-local storage, typed accessors, and exit cleanup.

`dd-trace-go` owns this tracer-context integration. otelc supplies the rewriting engine.

</div>

---

## `go:linkname` variables are fragile

Unlike function linknames, variables have no definition/reference separation.

When both sides are uninitialized BSS symbols, the linker chooses by symbol loading order.

> "the choice is arbitrary. In the implementation it depends on the symbol loading order"
>
> Ian Lance Taylor, [golang/go#72032](https://github.com/golang/go/issues/72032)

This broke between Go 1.22 and 1.23.

---

<!-- _class: meme -->
<!-- _paginate: false -->

![bg contain](../assets/meme_linker_loading_order.png)

the linker picks by symbol loading order

---

## The build path has boundaries too

* Requires control of the Go build pipeline.
* Requires Go 1.25 or newer for current otelc.
* Coverage stops at the supported integration set.
* Toolchain internals such as `-toolexec` and `go:linkname` can change.

<br>

No root access and no kernel version gate, but the binary must be rebuilt.

---

<!-- _class: section -->
<!-- _paginate: false -->

###### 05

# Process start: the injector

---

## How process-start injection works

<div class="center">

```mermaid
sequenceDiagram
    participant K as kernel exec
    participant L as ld.so
    participant P as preloaded library
    participant R as language runtime
    K->>L: start the dynamic loader
    L->>P: map LD_PRELOAD first
    L->>P: run its initializers
    P->>R: set one environment variable
    R->>R: load the agent before main
```

</div>

<div class="tiny">

[ld.so(8)](https://man7.org/linux/man-pages/man8/ld.so.8.html): preloaded objects load "before all others" · System V ABI: shared-object initializers run "before the executable file gains control"

</div>

---

## Runtime hooks that injectors use

| Runtime | The hook the injector sets |
| --- | --- |
| Java | `JAVA_TOOL_OPTIONS=-javaagent:…` |
| Node.js | `NODE_OPTIONS=--require …` |
| .NET | CLR profiler and startup-hook variables |
| Python | `sitecustomize` on `PYTHONPATH` |
| Ruby | `RUBYOPT=-r …` |
| **Go** | **none** |

<div class="small">

[OpenTelemetry injector](https://github.com/open-telemetry/opentelemetry-injector): Java, Node.js, .NET, Ruby, Python · [Datadog SSI](https://docs.datadoghq.com/tracing/trace_collection/automatic_instrumentation/single-step-apm/): Java, Python, Ruby, Node.js, .NET, PHP

</div>

---

## A static Go binary has no loader

<div class="center">

```mermaid
flowchart LR
    A[kernel exec] --> B[no PT_INTERP]
    B --> C[no ld.so]
    C --> D[LD_PRELOAD never read]
    D --> E[runtime.main]
```

</div>

`CGO_ENABLED=0` gives no dynamic loader and no libc. Nothing reads the variable.

Even with cgo, the internal linker runs no shared-object constructors ([golang/go#28909](https://github.com/golang/go/issues/28909)).

---

## `LD_PRELOAD` reaches only some Go binaries

```bash
LD_PRELOAD=./tracer.so ./python-app
LD_PRELOAD=./tracer.so ./go-app

go build -ldflags="-linkmode=external"
```

| Build | Result |
| --- | --- |
| Dynamically linked process | Injection can work |
| Default internally linked Go binary | No dynamic-loader hook |
| Static cgo or pure-Go PIE | No compatible library-injection path |

---

## The teaser

```bash
LD_PRELOAD=./libdd_go_hook.so \
DD_SERVICE=my-service \
DD_TRACE_DEBUG=1 \
./my-go-app
```

`DD_TRACE_DEBUG=1` shows span creation and trace-id extraction on stderr.

<span class="chip caution">in development</span>

---

<!-- _class: punchline dark -->
<!-- _paginate: false -->

## No rebuild.
## No source change.
## No kernel version gate.

### *One line.*

---

<!-- _class: section -->
<!-- _paginate: false -->

###### 06

# Profiles complete the four signals

---

<!-- _class: punchline dark -->
<!-- _paginate: false -->

## Traces tell you which request was slow

## Profiles tell you where the *CPU* went

---

## OpenTelemetry eBPF Profiler

Originated as Elastic Universal Profiling and joined OpenTelemetry in June 2024.

* Samples CPU from the kernel.
* Profiles every process on a node.
* Requires no application rebuild or injected library.
* Emits the OpenTelemetry Profiles signal.

<br>

<span class="chip note">Profiles: Alpha specification</span>

---

<!-- _class: punchline dark -->
<!-- _paginate: false -->

# But how does it read a *stripped* binary?

---

## Go metadata tells the profiler how to unwind

<div class="center">

```mermaid
flowchart LR
    A[.gopclntab] -->|prepared once| B[unwind rules in BPF maps]
    C[CPU sample] --> D[BPF unwinder]
    B --> D
    D -->|symbolize with .gopclntab| E[named Go stack]
```

</div>

> "The information remains present even for fully static and stripped executables."
>
> [OpenTelemetry eBPF Profiler documentation](https://github.com/open-telemetry/opentelemetry-ebpf-profiler/blob/main/doc/gopclntab.md)

---

## Zero-touch profiling still has a deployment cost

| Application | Profiler agent |
| --- | --- |
| No source changes | Linux node access |
| No rebuild | `CAP_BPF` + `CAP_PERFMON` or root |
| No in-process agent | DaemonSet / Collector distribution |
| Stripped binaries supported | CPU profiling is the confirmed core signal |

<br>

The eBPF profiler will add memory profiling soon. But `pprof` still has the edge: more profile types, more granular data, and no kernel privileges.

---

<!-- _class: punchline dark -->
<!-- _paginate: false -->

# Traces and profiles. *Apart.*

---

## Correlation is the missing bridge

Native runtimes can publish request context through thread-local storage.

Go cannot rely on that model: goroutines move between OS threads, and crossing FFI on every event is too costly.

The proposed Go path uses **pprof labels**:

<!-- code-header: none -->

```yaml
threadlocal.schema_version: "go_pprof_labels_v1"
```

<div class="tiny">

[OTEP 4947: Alternative for Go support](https://github.com/open-telemetry/opentelemetry-specification/blob/main/oteps/profiles/4947-thread-ctx.md#alternative-for-go-support)

</div>

---

<!-- _class: punchline dark -->
<!-- _paginate: false -->

### Compile time sets context. eBPF reads *evidence*.

### Together, request context reaches profiles

---

<!-- _class: section -->
<!-- _paginate: false -->

###### 07

# Live debugging: probe a running process

---

## The probe goes to the running process

<div class="center">

```mermaid
sequenceDiagram
    participant D as developer
    participant B as Datadog backend
    participant S as system-probe
    participant A as Go service
    D->>B: pick a line, write a message
    B->>S: logpoint definition
    S->>A: find the line, attach a uprobe
    Note over A: the service keeps running
    A->>S: probe hit
    S->>D: snapshot in the debug session
```

</div>

<div class="tiny">

Simplified. [Datadog Live Debugger](https://docs.datadoghq.com/tracing/live_debugger/): "non-breaking breakpoints that collect diagnostic data without pausing the application"

</div>

---

## From a line to a machine address

<div class="center">

```mermaid
flowchart LR
    A[file:line] -->|DWARF line table| B[PC]
    B -->|file offset| C[uprobe]
    C -->|DWARF location list| D[register or stack]
```

</div>

The same uprobe as before. DWARF supplies the address and the variable locations.

---

## Some variables are not there

<div class="columns">
<div>

### The compiler moved them

Inlining and register allocation leave some values with no location at that PC.

</div>
<div>

### The probe still fires

The snapshot marks the variable **unavailable**.

Some lines have no safe place for a probe.

</div>
</div>

---

## Bounded by design

| Control | Public limit |
| --- | --- |
| Logpoint with variable capture | 1 execution per second |
| Logpoint without capture | 5000 per second per service instance |
| Lifetime | Expires with the debug session |
| Sensitive values | Redacted before the data leaves the host |

<div class="small">

Go: Linux 5.17+, Datadog Agent 7.73+, Go SDK 2.9+ recommended · [Live Debugger docs](https://docs.datadoghq.com/tracing/live_debugger/) · [Sensitive data scrubbing](https://docs.datadoghq.com/tracing/live_debugger/sensitive-data-scrubbing/)

</div>

---

## Other ways, and their cost

| | Code change | Stops the program | Reads variables |
| --- | --- | --- | --- |
| Delve breakpoint | no | **yes** | yes |
| Flight recorder (Go 1.25) | **yes** | no | no, execution trace |
| Hand-written uprobe | no | no | by hand |
| Live Debugger logpoint | no | no | yes, bounded |

---

<!-- _class: section -->
<!-- _paginate: false -->

###### 08

# When to reach for what

---

## When to reach for what

| Constraint | Prefer |
| --- | --- |
| No rebuild window | OBI or injector |
| Non-Linux target | otelc |
| Mixed-language boundary coverage | OBI |
| Rich Go library semantics | otelc |
| No privileged runtime agent | otelc or injector |
| Whole-node CPU profiles | eBPF Profiler |
| Request-correlated profiles | Compile-time context + profiler |

---

## A practical production combination

<div class="center">

```mermaid
flowchart TD
    subgraph Build [Build pipeline]
        A[otelc]
    end
    subgraph Linux [Linux cluster]
        B[OBI]
        C[eBPF Profiler]
    end
    A -->|semantic spans, metrics, logs, pprof labels| OUT[Your backend]
    B -->|boundaries, mixed-language coverage| OUT
    C -->|whole-node CPU profiles| OUT
```

</div>

Start with the constraint you cannot change. Add the other layer when its signal earns the cost.

**20% adoption growth** is evidence that Go users want the build-time path too.

---

<!-- _class: section -->
<!-- _paginate: false -->

###### 09

# What comes next

---

## cgo without a C toolchain

* [#81450](https://github.com/golang/go/issues/81450): call prebuilt C libraries with no C compiler at build time
* Bindings in Go syntax. Glue in Go and assembly. `runtime/cgo` without C.
* The internal linker learns dynamic imports on Linux.

<br>

<span class="chip note">GOEXPERIMENT=cgobindings accepted (#81662)</span> <span class="chip caution">design still in review</span>

---

<!-- _class: vcenter -->

## The loop, without the redeploy

<br>

Describe the bug in words. The agent places the probe and reads *production evidence*.

No source edit. No restart. No *redeploy*.

<br>

Bits Live Debugger does this today, in preview.

Same move as the opening joke, except now the agent has the *framework*.

---

<!-- _class: punchline dark -->
<!-- _paginate: false -->

# Takeaways

---

<!-- _class: punchline dark -->
<!-- _paginate: false -->

## Start from the *constraint* you cannot change.

## Add a layer only when its *signal* pays for its *operational cost*.

---

<!-- _class: terminal -->

# Take it home

```bash
go install github.com/kakkoyun/zeroins/cmd/...@latest
obi-integration net/http     # offline OBI v0.10.0 catalog
otelc-aspect    net/http     # offline otelc v1.0.1 catalog
npx skills add kakkoyun/zeroins --all
```

<br>

Catalog lookups are offline and read-only. `kubectl-obi` and `kubectl-profiler` are experimental privileged wrappers needing an explicit OTLP endpoint.

For more agent skills for instrumenting Go applications, see [github.com/ollygarden/opentelemetry-agent-skills](https://github.com/ollygarden/opentelemetry-agent-skills).

---

## Get involved in the SIGs

<div class="columns">
<div class="center">

![width:400](../assets/meme_we_want_you.png)

</div>
<div>

[github.com/open-telemetry/community](https://github.com/open-telemetry/community) has every SIG's calendar, notes, and channels.

- Go Compile-Time Instrumentation (`otelc`)
- eBPF Instrumentation (OBI)
- Injector
- Profiling

</div>
</div>

---

<!-- _class: dark -->

# Take it with you

<div class="columns">
<div>

### Talk material

[github.com/kakkoyun/golab-26](https://github.com/kakkoyun/golab-26)

Both decks · research · [earlier FOSDEM version](https://youtu.be/0TvrSebuDPk)

### zeroins toolkit

[github.com/kakkoyun/zeroins](https://github.com/kakkoyun/zeroins)

`obi-integration` · `otelc-aspect`<br>
`kubectl-obi` · `kubectl-profiler`

</div>
<div class="center">

![w:250](../../assets/golab-26-repo-qr.png)

**Scan for the talk repository**

</div>
</div>

---

<!-- _paginate: false -->
<!-- _class: end gopher-balloon -->

# Questions?

[kakkoyun.me](https://kakkoyun.me) · [github.com/kakkoyun](https://github.com/kakkoyun)

[linkedin.com/in/kakkoyun](https://www.linkedin.com/in/kakkoyun/) · [bsky.app/profile/kakkoyun.me](https://bsky.app/profile/kakkoyun.me) · [x.com/kakkoyun_me](https://x.com/kakkoyun_me)

<span class="small">Talk repo [github.com/kakkoyun/golab-26](https://github.com/kakkoyun/golab-26) · Tools [github.com/kakkoyun/zeroins](https://github.com/kakkoyun/zeroins)</span>
