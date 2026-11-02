# Asks for the Go team

This page supports the GoLab 2026 talk "How to instrument Go without changing a single line of code". These are draft problem reports, not proposals. Feedback is welcome. Open an issue on [github.com/kakkoyun/golab-26](https://github.com/kakkoyun/golab-26), or find Kemal Akkoyun at the conference.

## The question

The Go runtime diagnostics sync asked the question first.

> "We don't have a great way to add instrumentation in general. Companies will maintain patches to add hooks. What should we do?"
>
> Go runtime diagnostics sync, 31 July 2025 ([notes](https://github.com/golang/go/issues/57175#issuecomment-3283520959), posted 12 September 2025)

> "Maybe eBPF is the answer?"
>
> Go team, same meeting

Our answer is yes, if Go gives eBPF something stable to read. The asks below describe what that could look like.

## 1. Goroutine-local storage and context propagation

### Problem

Tracers need the current trace context on the current goroutine. Go has no supported place for it. Build-time tools rewrite the runtime to add one, and each tool picks its own field and layout. Out-of-process readers, such as eBPF profilers, cannot trust any of them.

### Evidence

- Orchestrion, with the dd-trace-go aspect, adds `__dd_gls_v2 any` to `runtime.g`.
- otelc adds `otel_trace_context` and `otel_baggage_container` to `runtime.g`.
- Storage alone does not propagate context. Libraries still need hooks to extract and inject it, and rules for what a new goroutine inherits.

### Prior discussion

- [golang/go#68785](https://github.com/golang/go/issues/68785), closed as not planned. On the issue, 18 November 2025: "as I understand, we've rejected anything that could be used as goroutine local storage." The Go team, 20 November 2025: "The profile labeling code is designed around passing contexts with attached labels. That is intentional."
- [golang/go#21355](https://github.com/golang/go/issues/21355) and [golang/go#69478](https://github.com/golang/go/issues/69478) are closed.

### Ask

Give trace context one supported slot, with a layout that out-of-process readers can trust, and rules for what a new goroutine inherits. Two tools already build this slot outside the runtime.

## 2. USDT probes in Go

### Problem

A USDT probe is a NOP at the probe site and an ELF note. The note names the probe and says where each argument lives. Tracers attach an ordinary uprobe at the NOP. Go 1.27 emits no USDT probes. Tools that need a stable probe site must add one through cgo, or infer the site from the binary.

### Evidence

- The OpenTelemetry eBPF profiler allocation profiling reads `otel_memory` USDT probes from an instrumented allocator: [PR #1746](https://github.com/open-telemetry/opentelemetry-ebpf-profiler/pull/1746), merged 20 October 2026.
- Salp and libstapsdt add USDT probes through cgo.
- Proof of concept, toolchain side: [kakkoyun/go, branch poc_usdt](https://github.com/kakkoyun/go/tree/poc_usdt).

### Prior discussion

- The 19 December 2024 sync discussed USDT. One participant: "it's more stable over time because it's in the source code". Another: "Years ago we were interested, but didn't know exactly what we'd use them for." The Go team: "How would this look?" ([notes](https://github.com/golang/go/issues/57175#issuecomment-2596101614), posted 16 January 2025).
- [golang/go#22008](https://github.com/golang/go/issues/22008) (open). The Go team, 25 September 2017: "I don't see how we could support a dynamic probe executed by the kernel that refers to a local address on the stack." A USDT site is fixed at compile time. Its note says where each value lives at that site. The objection applies to dynamic probes, not to compiled-in sites.

### Ask

Let the toolchain emit SDT notes at a small set of runtime sites. Start with goroutine start and exit, GC phases, and allocation samples.

## 3. Close the `-toolexec` gaps

### Problem

otelc and Orchestrion both build on `-toolexec`. A tool cannot add its own inputs to a package build ID, so the build cache can reuse a stale result when the inputs of the tool change. Tools also lack visibility into build flags without crawling the process tree.

### Evidence

- [golang/go#69887](https://github.com/golang/go/issues/69887) lists the directions: per-package build-ID influence, new build-graph edges, a better `go/ast` API, source mapping, `-p` parallelism, and shared build flags.

### Prior discussion

- The Go team, 17 December 2024: "Adding dedicated support for source rewriting tools would result in a significant increase in complexity in the go command."
- The Go team, 24 December 2024: "This isn't so much a 'proposal' as it is a 'problem report', which is still very helpful!"

### Ask

Close those gaps. This is not a request for a new build mode.

## 4. One supported start-up door

### Problem

An agent that starts before `main` must handle a matrix. Libc can be glibc, musl, or none. The link mode can be internal or external. The build mode can be exe, PIE, or static. The `plugin` package does not solve this. Its documentation warns that runtime crashes are likely unless the application and all its plugins use exactly the same toolchain version, build tags, flag and environment values, and dependency sources.

Other runtimes give an agent one documented door. Java has `JAVA_TOOL_OPTIONS`. Go has no equivalent.

### Evidence

- [pkg.go.dev/plugin](https://pkg.go.dev/plugin) (src/plugin/plugin.go at go1.27.3).
- [golang/go#28909](https://github.com/golang/go/issues/28909) (musl constructors) and [golang/go#12465](https://github.com/golang/go/issues/12465) (c-shared with `LD_PRELOAD`) are open.

### Prior discussion

- The diagnostics sync noted that companies maintain patches to add hooks, and asked what Go should do. Sync of 31 July 2025 ([notes](https://github.com/golang/go/issues/57175#issuecomment-3283520959)).

### Ask

Tell agent authors which start-up door Go supports. Native agent libraries may fit cgo without a C toolchain. The accepted experiment is `GOEXPERIMENT=cgobindings` ([golang/go#81662](https://github.com/golang/go/issues/81662)). Its design, [golang/go#81450](https://github.com/golang/go/issues/81450), is still in review. The fit is still open.

## Bonus: stable runtime offsets

### Problem

Tools that infer by symbol or offset break when the runtime changes. Go 1.27 moved HTTP/2 into `net/http/internal/http2`. It also added `typedesclen` to the runtime `moduledata`. Tools that infer layout had to update for both.

### Evidence

- `src/net/http/internal/http2` exists at go1.27.3 and not at go1.26.10.
- `src/runtime/symtab.go` has `typedesclen` at go1.27.3 and not at go1.26.10.
- [golang/go#57175](https://github.com/golang/go/issues/57175) records the diagnostics discussion.

### Ask

Document the runtime structures that out-of-process tools read, and keep their layout stable across releases.
