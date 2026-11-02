# Claims Ledger

> Every load-bearing claim in this research corpus must have an entry here.
> A claim is "load-bearing" if it would change the talk's argument or a blog post's conclusion if wrong.
>
> **Verdicts:**
>
> - `CONFIRMED` — verified against a primary source (repo, spec, issue, official blog); cite `[S-NNN]`
> - `PLAUSIBLE` — consistent with evidence but not directly confirmed; must be flagged in prose, never asserted
> - `REFUTED` — found to be wrong; do not use; note what is correct instead
> - `PENDING` — not yet researched; placeholder only

## Format

```
### [C-NNN] The claim (exact wording to be used in talk/blog)
- **Verdict:** CONFIRMED | PLAUSIBLE | REFUTED | PENDING
- **Source(s):** [S-NNN], [S-NNN]
- **Notes:** verification method, caveats, version constraints
```

---

## Thesis / Go Runtime Hook Point

### [C-001] Go has no runtime hook point — you cannot monkey-patch a running Go process the way you can with JVM agents or Python's import hooks

- **Verdict:** CONFIRMED
- **Source(s):** S-TH-01 (runtime/proc.go "hall of shame"), S-TH-02 (internal/runtime/exithook), S-TH-03 (golang/go#28909 LD_PRELOAD), S-TH-04 (Dynatrace limitations)
- **Notes:** Native machine code, no classloader, no bytecode. Pure-Go builds are static. A default cgo build (for example one that imports net) is internally linked but dynamic, and on glibc the loader runs LD_PRELOAD constructors. Verified 2026-11-02 with Go 1.26.5 in Docker on Debian arm64 and Alpine. Only internal exit-time hook is scoped to program termination. Go team labels go:linkname abusers a "hall of shame" in runtime/proc.go.

### [C-002] Orchestrion injects a field `__dd_gls_v2 any` into `runtime.g` and exposes it via `go:linkname` get/set function variables

- **Verdict:** CONFIRMED ✅
- **Source(s):** S-TH-05a (gls.orchestrion.yml, commit b97e7cbb4), S-TH-05b (gls.go, commits b97e7cbb4 + 577c7760f)
- **Notes:** Complete mechanism (three steps):
  1. **Aspect** `gls.orchestrion.yml` (`internal/orchestrion/gls.orchestrion.yml` in dd-trace-go, commit b97e7cbb4) targets `struct-definition: runtime.g`, uses `add-struct-field` to inject `__dd_gls_v2 any` into the `g` struct.
  2. **Injects** `go:linkname` function-variable symbols: `__dd_orchestrion_gls_get.V2` = `func() any { return getg().m.curg.__dd_gls_v2 }` and `__dd_orchestrion_gls_set.V2` = `func(val any) { getg().m.curg.__dd_gls_v2 = val }`.
  3. **Patches** `runtime.goexit1` with `getg().__dd_gls_v2 = nil` to zero the field when a goroutine exits (prevents memory leaks).
  - dd-trace-go's `gls.go` then links to the symbols via go:linkname with no-op defaults when Orchestrion is absent.
  - The SHA "5fef9c1ba9ac9ff0ac966714d0342f7f85dbc4fa" does NOT exist — use b97e7cbb4 (v2.0.0) for the yml file.
  - Orchestrion applies this aspect. Orchestrion's go.mod does not depend on otelc. otelc has its own rule (instrumentation/runtime/otelc.yaml) that adds otel_trace_context and otel_baggage_container to runtime.g.

### [C-002b] go:linkname for variables is fragile — BSS resolution is order-dependent; broke between Go 1.22 and 1.23

- **Verdict:** CONFIRMED
- **Source(s):** S-TH-06 (golang/go#72032)
- **Notes:** Unlike function linkname (which supports bodiless forward declarations), variable linkname has no definition/reference separation. If both sides are uninitialized, linker choice is arbitrary. Manifested as breaking change Go 1.22 → 1.23. Go team documented in #72032.
- The quote on the slide is Cherry Mui (cherrymui, 2025-03-03), not Ian Lance Taylor. CL 660696 fixed it: the linker keeps the larger BSS symbol. Go 1.25, backported to Go 1.23.9 (#73091) and 1.24.3 (#73092).

### [C-003] dd-trace-go has 51 integration wrappers in contrib/ (not ~54)

- **Verdict:** CONFIRMED (corrected)
- **Source(s):** S-TH-07 (dd-trace-go contrib/ directory, counted from v2 branch)
- **Notes:** Prior lead said ~54 — wrong. Actual count: 51 subdirs in contrib/. Use "over 50" or link to supported_integrations.md rather than a specific number that will drift.

---

## OBI

### [C-010] OBI (OpenTelemetry eBPF Instrumentation) is the renamed/donated successor to Grafana Beyla

- **Verdict:** CONFIRMED
- **Source(s):** S-OBI-01 (Grafana Beyla OSS page), S-OBI-02 (Beyla README + community issue #2406)
- **Notes:** Grafana Labs donated Beyla to CNCF/OTel in 2025 via community issue #2406. Beyla continues as Grafana's distribution. New repo: github.com/open-telemetry/opentelemetry-ebpf-instrumentation, module: go.opentelemetry.io/obi.

### [C-011] OBI requires supported Linux kernels with BTF; the required capabilities depend on the enabled features

- **Verdict:** CONFIRMED
- **Source(s):** S-OBI-04, S-OBI-06, S-OBI-07
- **Notes:** Baseline platform support is Linux 5.8+ with BTF, or documented RHEL-family 4.18+ backports. Network flow capture, application observability, context propagation, and Go library propagation require different capabilities. Do not publish one fixed list as universal. Re-verified at v1.0.0 on 2026-11-01: platform rows unchanged. Correction: since v0.14.0, OBI falls back to tracefs when a restrictive `perf_event_paranoid` blocks PMU access, so most probe attachment no longer needs `CAP_SYS_ADMIN`. `CAP_SYS_ADMIN` is still needed for features that use `bpf_probe_write_user()`: library-level Go context propagation and Go Trace API span capture (C-078). Do not say that `perf_event_paranoid` forces `CAP_SYS_ADMIN`. Code-verified at v1.0.0: `tracefs.WithFallback` wraps both uprobe and kprobe attachment (`pkg/internal/ebpf/{uprobe,kprobe}`). `pkg/obi/os.go` sets the kernel minimum to 5.8, or 4.18 for RHEL.

### [C-012] OBI is language-agnostic at network-protocol level; also provides Go-specific library uprobes for 13 libraries

- **Verdict:** CONFIRMED
- **Source(s):** S-OBI-04, S-OBI-06
- **Notes:** Code nuance, 2026-11-01: the gin `!= v1.7.5` exclusion lives in the offset generator input (`configs/offsets/tracker_input.json`). The runtime does not check for it. A gin v1.7.5 binary gets DWARF offsets or the `since 1.7.0` entry in `offsets.json`. The slide keeps the documented baseline. If asked: v1.7.5 is outside the generated and validated range, not a known crash. Language-agnostic: Go, Java (JDK 8+), .NET, Node.js, Python, Ruby, C, C++, Rust, GenAI SDKs. Go-specific uprobe support for 13 named libraries (net/http, gin, gRPC, gorilla/mux, go-redis, Kafka, database/sql, etc.). Re-verified at v1.0.0 on 2026-11-01: the Go library table is identical to v0.10.0 (diffed). Pin the slide link to the v1.0.0 tag.

### [C-013] OBI current release: v0.10.0 (2026-06-30), Development status (breaking changes expected)

- **Verdict:** REFUTED (superseded 2026-11-01). Use C-076
- **Source(s):** S-OBI-03 (pkg.go.dev), S-OBI-04 (README), S-OBI-09, S-OBI-12
- **Notes:** True until 2026-08-17. OBI then shipped v0.11.0 through v0.15.2 and v1.0.0 on 2026-10-30. The "v0: breaking changes are still possible" chip is wrong now. Trap: the README at the v1.0.0 tag still says "OBI is currently in Development". The v1.0.0 release notes say that this wording is left over from the pre-v1 phase and that the stable-surface declaration applies. Do not quote the README as the current status.

### [C-014] "Zero code changes" holds for HTTP/gRPC RED metrics and 13 Go library spans; does NOT hold for custom spans, business-logic events, SQL query details

- **Verdict:** CONFIRMED
- **Source(s):** S-OBI-04 (official docs caveat)
- **Notes:** Official docs explicitly: "Use language agents or manual instrumentation when you need custom spans, application-specific attributes, business events, or other in-process telemetry." Be precise in the talk: "zero changes for standard observability." Update 2026-11-01: custom spans still need code, but in Go that code no longer needs an SDK. OBI can export spans written with the global `otel.Tracer` API (C-078). The boundary holds: the application still authors the business span.

### [C-015] OBI can correlate JSON logs with traces by enriching writes with trace and span IDs, but it does not export logs

- **Verdict:** CONFIRMED
- **Source(s):** S-OBI-08
- **Notes:** Corrected 2026-11-01. Code-verified at v1.0.0: the default config sets `LogEnricher.PlainText.Enabled: true` (`pkg/obi/config.go`). Enrichment applies to selected JSON and plain-text logs while a span is active. Plain-text enrichment adds `key=value` fields and is on by default for selected services since v0.11.0. The earlier note "Plain text is unchanged" is wrong now. Existing log forwarding remains responsible for export. Current docs require Linux 6.0+, BPFFS, and a kernel without lockdown for this feature.

### [C-016] Uprobe instrumentation has infrastructure, BPF-program, and compatibility costs even though recent kernels improved hot-path scalability

- **Verdict:** CONFIRMED
- **Source(s):** S-UP-01, S-UP-02, S-UP-03, S-UP-04 (OBI PR #1851), S-UP-05 (static-PIE incident)
- **Notes:** Attached uprobes cross into the kernel. RCU-protected lookup and consumer traversal removed major scalability bottlenecks in newer kernels. A BPF program can still serialize a concurrent path through shared state. Go 1.26's removal of `pcHeader.textStart` required OBI to change symbol resolution; that issue is fixed and should be presented as maintenance evidence, not a current defect.

  **Static-PIE incident (script depth, not a slide):** `aws-load-balancer-controller` v3.2.0 changed one build flag to static-PIE. No application code changed. On nodes running OBI its pods exited 139, `kubectl logs --previous` empty, `GOTRACEBACK=crash` silent because the SIGSEGV beat the Go runtime's signal handler. Static-PIE is `ET_DYN` with no `PT_INTERP`; the external linker restructured segments, `runtimeText` from `.gopclntab` stopped matching `prog.Vaddr`, and the computed offset put the uprobe in the wrong place. Fixed by PR #1851, deriving `runtime.text` from `runtime.moduledata` after Go 1.26 removed `pcHeader.textStart`. Trap: fixed, maintenance cost, never a live defect; the team changed build flags, not application code. Not Kemal's incident.

---

## otelc (OTel Go compile-time instrumentation)

### [C-020] otelc uses `-toolexec` to rewrite Go AST at compile time (not at link time, not at runtime)

- **Verdict:** CONFIRMED
- **Source(s):** S-O-03 (orchestrion repo + golang/go#69887), S-O-04 (OTel blog), S-O-05 (otelc repo)
- **Notes:** Both DataDog/orchestrion and otelc intercept `go tool compile` via `-toolexec`, rewrite .go source ASTs (using github.com/dave/dst in Orchestrion) before the compiler sees them. Orchestrion maintainer quote in #69887 confirms mechanism verbatim.

### [C-021] Orchestrion was donated to OTel as otelc

- **Verdict:** REFUTED — do not use
- **Source(s):** S-O-01, S-O-04
- **Notes:** Orchestrion was NOT donated. DataDog + Alibaba co-founded OTel Go Compile-Time Instrumentation SIG and built `otelc` (open-telemetry/opentelemetry-go-compile-instrumentation) from scratch, inspired by Orchestrion. Two separate tools with same mechanism, different codebases and default tracers.

### [C-021b] DataDog/orchestrion (CLI: `orchestrion`) and OTel SIG's otelc (CLI: `otelc`) are two distinct tools using the same -toolexec + AST rewriting mechanism

- **Verdict:** CONFIRMED (re-verified 2026-08-13)
- **Source(s):** S-O-01, S-O-03, S-O-04, S-O-05
- **Notes:** orchestrion: GA v1.12.0, defaults to dd-trace-go/v2 but vendor-agnostic. otelc: stable v1.0.1 (2026-07-14), defaults to OTel SDK. Both intercept go tool compile via -toolexec. On no slide; ledger only.

### [C-022] otelc current release version: v1.0.1 (2026-07-14), first stable non-retracted release

- **Verdict:** CONFIRMED (re-verified 2026-08-13)
- **Source(s):** S-O-04 (OTel blog), S-O-05 (repo)
- **Notes:** v1.0.1 shipped 2026-07-14. v1.0.0 was retracted over a bad `otelc pin` module path; v1.0.1 is the first stable non-retracted release. Still latest as of 2026-08-13. On-screen pin otelc v1.0.1 holds.

### [C-023] otelc is a production-capable, cross-platform build-time path rather than a local-development-only tool

- **Verdict:** CONFIRMED
- **Source(s):** S-O-04, S-O-07, S-O-08
- **Notes:** Official docs describe fleet-wide build-pipeline use. The repository builds/tests across Linux, macOS, and Windows. Current supported integrations produce traces, HTTP/gRPC metrics, runtime metrics, and trace IDs in supported log output. Runtime behavior still depends on the selected SDK and integration bundle.
- Re-checked at otelc v1.2.0 (2026-10-12): go.mod declares go 1.26.0 and the README badge says Go 1.26+. Log hooks for log, log/slog, logrus, and zap add trace and span IDs only and emit no OTel log records. CI runs on Linux, macOS, and Windows.

### [C-024] The OpenTelemetry host injector does not package Go; the Operator's Go option is a separate feature-gated eBPF sidecar

- **Verdict:** CONFIRMED
- **Source(s):** S-I-01, S-I-02
- **Notes:** Keep the host injector and Kubernetes Operator mechanisms distinct in the talk.

### [C-025] Alibaba, Datadog, and Quesma founded the OpenTelemetry Go compile-time instrumentation SIG

- **Verdict:** CONFIRMED
- **Source(s):** S-O-09
- **Notes:** The three organizations contributed independent experience. Do not describe Orchestrion as renamed or donated wholesale into otelc.

### [C-026] Customer adoption of Orchestrion-based Go auto-instrumentation grew by about 20%

- **Verdict:** CONFIRMED by the speaker and approved for public use
- **Source(s):** S-DD-01
- **Notes:** Use only the approved percentage. Do not publish a denominator, customer names, or the earlier "mostly new users" interpretation without separate clearance.

---

## opentelemetry-ebpf-profiler

### [C-030] opentelemetry-ebpf-profiler was donated to OTel by Elastic (formerly Elastic Universal Profiling)

- **Verdict:** CONFIRMED
- **Source(s):** S-P-01 (OTel blog June 2024), S-P-02 (CNCF blog March 2024), S-P-04 (community issue #1918)
- **Notes:** Pledged March 2024, transfer completed June 2024 via community issue #1918.

### [C-031] The OTel profiling signal uses OTLP profiles (not a vendor format)

- **Verdict:** CONFIRMED (with important nuance)
- **Source(s):** S-P-07 (OTel spec), S-P-08 (OTLP 1.11.0)
- **Notes:** OTLP profiles exist but are NOT stable — Alpha in OTel spec, Development tier in OTLP 1.11.0. Do NOT say "stable" in talk/blog. The profiler ships as an OTel Collector receiver (otelcol-ebpf-profiler), emitting natively via existing pipelines — no separate converter.

### [C-032] opentelemetry-ebpf-profiler supports whole-system continuous profiling without code changes

- **Verdict:** CONFIRMED (with deployment caveats)
- **Source(s):** S-P-05 (README + internals.md)
- **Notes:** "No code changes" holds for profiled apps (no recompilation, no agent injection, no restarts). BUT: requires the otelcol-ebpf-profiler DaemonSet deployed, root/CAP_BPF+CAP_PERFMON on the agent, minimum Linux kernel version (verify exact version). macOS dev requires Linux VM/container.

### [C-033] opentelemetry-ebpf-profiler unwinds Go stacks via .gopclntab (works on stripped production binaries)

- **Verdict:** CONFIRMED
- **Source(s):** S-P-05, S-P-06 (doc/gopclntab.md)
- **Notes:** Go executables lack .eh_frame (unless CGo), so profiler uses .gopclntab. Works on fully static stripped binaries. Covers OS-thread CPU stacks — goroutine-level profiling NOT confirmed.

### [C-034] CPU profiling is the confirmed profiling type; off-CPU is not yet in current release

- **Verdict:** CONFIRMED (CPU) / PLAUSIBLE NOT YET (off-CPU)
- **Source(s):** S-P-03 (profiles-alpha blog 2026)
- **Notes:** The data model supports off-CPU but the current profiler implementation has off-CPU as future work. Do not claim off-CPU support without verification against current CHANGELOG.

### [C-035] Current version is v0.0.202627 (calendar-week tags, no formal numbered releases)

- **Verdict:** CONFIRMED (re-verified 2026-08-13)
- **Source(s):** S-P-05 (GitHub repo tags)
- **Notes:** Versioning scheme is ISO week-based. Now at v0.0.202633 (2026-08-11). On no slide; ledger only.

### [C-036] Profiles are OpenTelemetry's fourth observability signal; the Profiles specification remains Alpha

- **Verdict:** CONFIRMED
- **Source(s):** S-P-07, S-P-08
- **Notes:** Logs, metrics, traces, and profiles are the four signal categories used in the talk. Do not call profiling the third signal or imply a stable profile data model.

### [C-037] OTEP 4947 proposes a Go-specific pprof-label path for sharing request context with profile readers

- **Verdict:** CONFIRMED as a proposal, not as shipped behavior
- **Source(s):** S-P-09
- **Notes:** Go is outside the primary TLSDESC mechanism for the foreseeable future because of goroutine concurrency and FFI cost. Go SDKs identify `go_pprof_labels_v1`; readers consume pprof labels directly. Compile-time instrumentation can arrange those labels, but the talk must describe this as proposed work.

---

## Go Runtime Futures

### [C-040] golang/go#63185 — flight recording — SHIPPED in Go 1.25

- **Verdict:** CONFIRMED (with API correction)
- **Source(s):** S-RF-01 (issue), S-RF-02 (go.dev blog Sept 2025), S-RF-03 (flightrecorder.go source)
- **Notes:** CLOSED Proposal-Accepted, milestoned Go 1.25. JFR-style circular-buffer tracer. API: `trace.NewFlightRecorder(cfg FlightRecorderConfig)` with struct fields `MinAge time.Duration, MaxBytes uint64`. Methods: `Start()`, `Stop()`, `Enabled()`, `WriteTo(w io.Writer)`. The prior lead mentioned `SetMinAge` as a method — WRONG. Shipped API uses struct fields. Do not use old API in talk or blog.

### [C-041] golang/go#69887 proposes -toolexec/compile-time instrumentation improvements (OPEN)

- **Verdict:** CONFIRMED (scope correction)
- **Source(s):** S-RF-04 (issue)
- **Notes:** Filed 2024-10-15 by Romain Marcadier (DataDog/Orchestrion). OPEN, Proposals Incoming. Does NOT propose general runtime hooks — proposes 5 improvements to -toolexec tooling: per-package build-ID influence, build-graph edges, go/ast API, source mapping, -p parallelism. Root gaps: cache invalidation, no visibility into build flags without crawling process tree.

### [C-042] golang/go#75654 and #38270 describe httptrace hook gaps (different classes)

- **Verdict:** CONFIRMED
- **Source(s):** S-RF-05 (#75654), S-RF-04 (research context for #38270)
- **Notes:** #75654 (2025-09-29, OPEN active): client-side — no hook for response body completion; OTel Go uses PutIdleConn as workaround which never fires for HTTP/2, causing client spans to never close (otel-contrib#4876, still open). #38270 (2020, OPEN Proposal-Hold Unplanned): server-side request lifecycle hooks. DIFFERENT classes — not the same problem. Prior lead described both as "hook-gap bugs" which is accurate but imprecise.

### [C-043] golang/go#67120 is the runtime/metrics recommended set proposal (OPEN, Incoming)

- **Verdict:** RESOLVED by non-use
- **Source(s):** S-RF-04
- **Notes:** Title confirmed verbatim. Cited nowhere in the deck or script. No action needed.

---

## Speaker-attested claims (keynote restructure, 2026-08-13)

### [C-050] Datadog Live Debugger adds logpoints and variable snapshots to running Go services without a redeploy

- **Verdict:** CONFIRMED by the speaker and approved for public use
- **Source(s):** S-DD-02 (speaker attestation)
- **Notes:** Scope: what the slide and script say, nothing more. Uses eBPF through Datadog's `system-probe`; Go support requires Linux 5.17+. Logpoints expire automatically. Bits Live Debugger is in preview. Do not shill the product; this is a brain teaser for what is possible.

### [C-051] A Go injector hook exists in development (not released), loaded via LD_PRELOAD at process start

- **Verdict:** CONFIRMED by the speaker, in development, not released
- **Source(s):** S-DD-03 (speaker attestation)
- **Notes:** The most important note in the ledger: the mechanism is deliberately undisclosed. Never add linking model, entry path, or binary-compatibility detail to any slide or script line. If asked, defer to next year's talk. The invocation shows `LD_PRELOAD=./libdd_go_hook.so` with `DD_SERVICE` and `DD_TRACE_DEBUG=1`; `DD_TRACE_DEBUG=1` shows span creation and trace-id extraction on stderr. No `make go-hook.so` on the slide: a build the room cannot reproduce reads as a tease. Amber `in development` chip.

### [C-052] OBI roadmap: v0.11.0 targeted mid-August, proposed path to v1.0.0 by late October

- **Verdict:** SUPERSEDED (2026-11-01) by the actual releases. Use C-076 and S-OBI-12
- **Source(s):** OBI SIG notes, Aug 12 2026, public, linked from open-telemetry/community. The old row cited S-OBI-05, which is the Kubernetes setup page. That citation was wrong. S-OBI-12 has the actual dates
- **Notes:** Proposed in August: v0.11.0 on 18 Aug, v0.12 on 22 Sep, rc1 on 5 Oct, v1.0.0 on 26 Oct. Actual: v0.11.0 on 17 Aug, v0.12.1 on 20 Aug, v0.13.0 on 4 Sep, v0.14.0 on 2 Oct, v1.0.0-rc.1 on 7 Oct, v1.0.0-rc.2 on 16 Oct, v1.0.0 on 30 Oct. The roadmap is history now. Do not present it as a plan.

### [C-053] Usama Saqib's FOSDEM 2026 talk covers production eBPF pitfalls at Datadog

- **Verdict:** CONFIRMED
- **Source(s):** S-UP-06 (FOSDEM 2026 public page)
- **Notes:** Title, speaker, and abstract scope as cited on the slide. The talk covers kprobe performance across kernel versions, a fentry kernel bug, and the pain of scaling uprobes. Twenty-eight minutes, public. URL: <https://fosdem.org/2026/schedule/event/H3LM7G-performance_and_reliability_pitfalls_of_ebpf/>

---

## GoLab expansion (2026-10-29)

Public sources only. Full quotes, pins, and access dates are in
`08-ebpf-primer.md` (E-numbers), `09-process-start-injection.md` (I-numbers),
and `10-live-debugger.md` (S-DD and S-GO keys). Rows marked "owner review"
appear on a slide only after the owner approves them (see the talk `TODO.md`).

### [C-060] The verifier checks a BPF program before it runs. A JIT can translate it. Maps hold state. Helpers supply kernel services

- **Verdict:** CONFIRMED
- **Source(s):** 08-ebpf-primer.md S01, S02 (ebpf.io "What is eBPF", kernel verifier docs)
- **Notes:** Load-time checks. A hit does not re-verify. The loader diagram on the slide is eBPF.io "Loader", CC BY 4.0, credited on the slide.

### [C-061] BTF and CO-RE adapt kernel field reads at load time. They do not describe Go library layouts

- **Verdict:** CONFIRMED
- **Source(s):** 08-ebpf-primer.md S02 (E05, E06)

### [C-062] A uprobe places a breakpoint in the mapped code of the process. The kernel runs the handler, then emulates or single-steps the original instruction

- **Verdict:** CONFIRMED
- **Source(s):** 08-ebpf-primer.md S03, S04 (E08, E10, E11)
- **Notes:** Conventional x86 path. Newer kernels improve scaling (S05, S06). Do not quote a per-hit nanosecond number: the kernel benchmark measures an empty probe.

### [C-063] On amd64, Go ABIInternal (Go 1.17+) passes the first integer arguments in AX, BX, CX. A goroutine can change threads between entry and exit, so OBI keys state by PID and the g pointer

- **Verdict:** CONFIRMED
- **Source(s):** 08-ebpf-primer.md S07, S08, S11 (E15, E16, E20, E21)

### [C-064] Conventional uretprobes are unsafe for Go. OBI attaches ordinary uprobes at RET instructions instead

- **Verdict:** CONFIRMED
- **Source(s):** 08-ebpf-primer.md S09, S10 (E17, E18, E19), OBI v0.10.0, re-verified at v1.0.0 (d23be0d6)
- **Notes:** The saved-return-address replacement conflicts with Go stack copying and frame metadata. At v1.0.0, `pkg/internal/goexec/instructions_amd64.go` `FindReturnOffsets` still collects `x86asm.RET` offsets, and `instructions.go` still says that Go linkage prevents uretprobes. `bpf/common/go_addr_key.h` still keys state by PID and goroutine address (C-063).

### [C-065] OBI reads field offsets from DWARF when present, otherwise from build versions and a prepared offset database

- **Verdict:** CONFIRMED
- **Source(s):** 08-ebpf-primer.md S12 (E22, E23), OBI v0.10.0, re-verified at v1.0.0 (d23be0d6)
- **Notes:** At v1.0.0, `structmembers.go` still tries DWARF first and falls back to the embedded `offsets.json`. The `runtime.moduledata` resolver from PR #1851 (C-016) is still in `instructions.go`.

### [C-066] USDT is a NOP plus an ELF note with a name and argument recipe. A tracer attaches an ordinary uprobe at the site. An optional semaphore signals a present tracer

- **Verdict:** CONFIRMED
- **Source(s):** 08-ebpf-primer.md S14 (E24, E25)

### [C-067] Upstream Go emits no USDT probes. Salp and libstapsdt add them through cgo. Polar Signals builds a Go tracer that consumes USDT notes

- **Verdict:** CONFIRMED
- **Source(s):** 08-ebpf-primer.md S15–S18 (E26–E30)
- **Notes:** Re-checked against Go 1.27 (current 1.27.3); its release notes have no USDT support. Polar Signals' work is a consumer, not Go compiler support. The speaker's fork is a proof of concept that this research did not build.

### [C-068] ld.so maps LD_PRELOAD objects before all others, and shared-object initializers run before the executable gains control

- **Verdict:** CONFIRMED
- **Source(s):** 09-process-start-injection.md I-04 (man7 ld.so(8)), I-05 (System V ABI)

### [C-069] A CGO_ENABLED=0 Go binary has no PT_INTERP, so ld.so never runs and LD_PRELOAD is never read. The internal linker runs no shared-object constructors

- **Verdict:** CONFIRMED
- **Source(s):** 09-process-start-injection.md I-04, I-08 (golang/go#28909, Ian Lance Taylor)
- **Notes:** #28909 is musl-specific (its title ends with 'and musl libc'). glibc runs preloaded constructors in the loader. The slide now says 'With musl'.

### [C-070] The OpenTelemetry injector ships Java, Node.js, .NET, Ruby, and Python (Python off by default). It does not inject Go

- **Verdict:** CONFIRMED
- **Source(s):** 09-process-start-injection.md I-06 (README at commit 22a9aa877)
- **Notes:** Supersedes the C-024 language list, which lacked Ruby.

### [C-071] Datadog SSI uses LD_PRELOAD on Linux and lists Java, Python, Ruby, Node.js, .NET, and PHP. Go is not in the list

- **Verdict:** CONFIRMED (public docs), owner review
- **Source(s):** 09-process-start-injection.md I-12, I-13 (docs.datadoghq.com SSI overview, injector guide, compatibility page)

### [C-072] golang/go#81450 proposes cgo without a C toolchain for prebuilt C libraries. golang/go#81662 adds GOEXPERIMENT=cgobindings and is accepted. The design proposal is still in review

- **Verdict:** CONFIRMED (re-checked 2026-10-29 with `gh api`)
- **Source(s):** 09-process-start-injection.md I-01, I-02
- **Notes:** #81662 labelled Proposal-Accepted on 2026-10-01 (aclements). #81450 labels: Proposal, cgo. Re-check before delivery. Any claim about which binaries an injector can reach afterwards is inference and stays off the slides.

### [C-073] Live Debugger logpoints collect data without pausing the application. Logpoints expire with the debug session

- **Verdict:** CONFIRMED (public docs), owner review
- **Source(s):** 10-live-debugger.md S-DD-L1 (docs.datadoghq.com/tracing/live_debugger/)

### [C-074] Live Debugger for Go needs Linux 5.17+, Agent 7.73+, and Go SDK 2.9+. Capture logpoints run at most 1 per second. Logpoints without capture run at most 5000 per second per service instance. Sensitive identifiers are redacted before data leaves the host

- **Verdict:** CONFIRMED (public docs), owner review
- **Source(s):** 10-live-debugger.md S-DD-L1, S-DD-SCRUB
- **Notes:** No public overhead number exists. Do not state one.

### [C-075] Live Debugger maps a source line to a PC through the DWARF line table, attaches a uprobe, and reads variables through DWARF location lists. A variable with no location at that PC is reported unavailable

- **Verdict:** CONFIRMED (public code), owner review
- **Source(s):** 10-live-debugger.md, datadog-agent `pkg/dyninst` at fd1f089014df9e80e6949323f7349041deadff5c
- **Notes:** Mechanism from public code, not a product guarantee. The sequence diagram simplifies the backend-to-system-probe hop, which the public docs do not describe.

---

## OBI v1.0.0 (refresh 2026-11-01)

### [C-076] OBI v1.0.0 (2026-10-30) is the first stable core release. The v1 contract covers Config v2, documented CLI flags, environment variables, binaries and images, stable-classified telemetry, and the support matrix. The Go module API and the Collector receiver are outside it

- **Verdict:** CONFIRMED
- **Source(s):** S-OBI-09 (v1.0.0 release notes), S-OBI-11 (VERSIONING.md after-v1 rules), S-OBI-03 (Go proxy: `obi@latest` v1.0.0, `obi/collector@latest` v0.15.2)
- **Notes:** Published 2026-10-30T17:50:30Z, commit d23be0d6. Code-verified: `git log v1.0.0-rc.2..v1.0.0` has one commit (#3972). Outside CI and tests, it changes only the schema URL (`pkg/export/attributes/names/schema_version.go`) and `collector/go.mod`, so "promoted unchanged from rc.2" holds. The tag sits on a release line off rc.2, not on `main`. On 2026-11-01, `main` had 130 commits after rc.2 that are not in v1.0.0. Read docs at the `v1.0.0` tag, not at `main`. The celebration slide says "30 October. Three days ago." That is true only for delivery on 2026-11-02. Minor releases may add compatible features. Incompatible changes to stable surfaces need v2. Two traps for a Go room: (1) `go.opentelemetry.io/obi@v1.0.0` does not make the exported Go packages stable. The release notes say so explicitly. (2) The Collector receiver is `go.opentelemetry.io/obi/collector` on its own v0 line, at `collector/v0.15.2`. Say "stable core", never "OBI is stable" without the qualifier. Config v1 is frozen: supported, but no fixes or features.

### [C-077] At v1.0.0 the stable telemetry is HTTP server and client spans and duration metrics, SQL client spans, and `db.client.operation.duration`. gRPC telemetry is release candidate. Go runtime metrics are development

- **Verdict:** CONFIRMED
- **Source(s):** S-OBI-10 (TELEMETRY.md, `schemas/obi/groups/{http,db,rpc,go}/*.yaml` at v1.0.0), S-OBI-13 (the code emits these metric names from `pkg/export/attributes/metric.go`)
- **Notes:** Read from `stability:` fields in the registry YAML. Stable metrics: `http.server.request.duration`, `http.client.request.duration`, `db.client.operation.duration`, plus JVM and .NET runtime metrics. Stable spans: `obi.http.server`, `obi.http.client`, `obi.db.sql.client`. `obi.rpc.grpc.server`, `obi.rpc.grpc.client`, `rpc.server.call.duration`, and `rpc.client.call.duration` are `release_candidate`. All `go.*` runtime metrics are `development`. Signal and attribute stability are independent: a stable span can carry unprotected attributes. Network flow attribute names are excluded pending semconv alignment (#1092).

### [C-078] OBI can export Go spans that the application writes with the global `otel.Tracer` API when no `TracerProvider` is registered. It activates the Auto SDK and needs `CAP_SYS_ADMIN` for `bpf_probe_write_user`

- **Verdict:** CONFIRMED
- **Source(s):** S-OBI-06 (SUPPORT_MATRIX.md v1.0.0, "Go Global Trace API And Auto SDK Activation" and "Go Trace API Embedded Auto SDK"), S-OBI-12 (v0.11.0, v0.15.2 notes), S-OBI-13 (code at v1.0.0), `examples/go-trace-api` at v1.0.0
- **Notes:** Since v0.11.0 with the external `go.opentelemetry.io/auto/sdk` module (v1.1.0 to v1.2.1, `otel` v1.33.0 to v1.47.0). Since v0.15.2 also through the Auto SDK embedded in `go.opentelemetry.io/otel/trace` (v1.35.0 to v1.47.0, `auto/sdk` optional). Docs and code differ: SUPPORT_MATRIX.md says "through v1.46.0", but the allowlist in `pkg/internal/goexec/structmembers.go` at v1.0.0 has v1.47.0 for `otel` and `otel/trace`. Commit 841c8b43 (#3724, 2026-10-14) added it without a matrix update. Use the code range. No slide states the range. Code-verified: activation has no config flag and starts when the binary qualifies (`goAutoSDKActivationProbesEnabled` in `gotracer.go`). It needs the same check as Go context propagation (`SupportsContextPropagationWithProbe` in `pkg/ebpf/common/common.go`): below 5.10 it assumes support, on 5.10+ it needs `CAP_SYS_ADMIN` and lockdown `none`. The 16 KiB limit is `k_go_auto_span_json_max_len = 16 * 1024` in `bpf/common/common.h`. Needs amd64 or arm64 and recognised module checksums and versions. Oversized spans are dropped without a warning. If an SDK provider is registered, OBI defers to it. The application still authors the span. This narrows C-014 and does not refute it.

### [C-079] OBI v1.0.0 ships with documented operational limitations: application metrics can stay missing after a Pod restart until OBI restarts, and child spans can start before their parents

- **Verdict:** CONFIRMED
- **Source(s):** S-OBI-09 ("Known operational limitations"), S-OBI-10 ("Known v1 emission limitations")
- **Notes:** Both root causes are unconfirmed. No workaround is documented for span ordering. Port-based discovery can also select a helper or port-forwarder. Script and Q&A only: use it to say "canary it", not to disparage the release.

---

## GoLab 2026 schedule

### [C-080] GoLab lists "Why Your Go Benchmarks Are Lying (And How to Stop Them)" (Kemal Akkoyun, 45 min) on 3 November 2026 at 10:45 in room Golab #2. The zero-touch talk is on 2 November at 15:30, so "tomorrow" holds

- **Verdict:** CONFIRMED
- **Source(s):** golab.io/talks/why-your-go-benchmarks-are-lying-and-how-to-stop-them and golab.io/speakers/akkoyun, retrieved 2026-11-01
- **Notes:** The plug slide says "Tomorrow · 10:45 · Golab #2". The word "tomorrow" depends on the zero-touch talk keeping its 2 November slot. Re-check the GoLab schedule in the week of the talk; if either slot moves, update the slide or drop the word "tomorrow".

---

## Lifecycle flow and future asks

### [C-081] Build-time and startup instrumentation can enable SDK signals, but the SDK and integrations determine actual coverage

- **Verdict:** CONFIRMED as a capability distinction, not a guarantee for every distribution
- **Source(s):** C-023, C-051; <https://opentelemetry.io/docs/zero-code/go/compile-time/>; <https://docs.datadoghq.com/tracing/trace_collection/dd_libraries/go/>; <https://github.com/open-telemetry/opentelemetry-injector>
- **Notes:** Public sources checked on 2026-11-02. Orchestrion-built applications include profiler instrumentation, enabled with `DD_PROFILING_ENABLED=true`. Upstream otelc and Orchestrion are distinct. The signal indicators describe the intervention path. They do not claim that upstream otelc ships every profile type or that the development Go injector implements every SDK feature. OBI log enrichment remains distinct from log export (C-015).

### [C-082] The speaker asks for explicit probe contracts that could help OBI, injector tooling, and live debugging at declared sites

- **Verdict:** CONFIRMED as a speaker-stated aspiration, not existing integrations
- **Source(s):** C-066, C-067; speaker direction in the 2026-11-02 narrative review
- **Notes:** USDT declares a site and argument locations. The proposed consumers still need integrations. USDT does not provide a dynamic loader, arbitrary source-line probes, or access to every variable. Do not connect this aspiration to the undisclosed injector mechanism.

### [C-083] The speaker asks for ABI-stable goroutine-local trace-context storage and propagation contracts

- **Verdict:** CONFIRMED as a speaker-stated ask; current build-time storage is verified in C-002
- **Source(s):** C-002, C-002b, C-023; speaker direction in the 2026-11-02 narrative review
- **Notes:** The current dd-trace-go integration uses build-time rewriting to add goroutine-local storage. The desired stable Go ABI is not a shipped runtime feature. Storage alone does not extract or inject protocol context. Propagation also needs library hooks and rules for inheritance across goroutines. Do not describe OTEP 4947 as the proposal for this storage ABI. It is a separate profile-correlation proposal.

### [C-084] Live Debugger metrics are a goal, and tracing is a longer-term goal with a 12+ month horizon

- **Verdict:** CONFIRMED by the speaker as goals, not release commitments
- **Source(s):** Speaker direction in the 2026-11-02 narrative review; <https://docs.datadoghq.com/tracing/live_debugger/>; <https://docs.datadoghq.com/tracing/trace_collection/dynamic_instrumentation/>; <https://docs.datadoghq.com/tracing/trace_collection/library_config/go/>
- **Notes:** The speaker supplied the tracing horizon. The public pages do not establish that horizon. Public docs distinguish Live Debugger logs and snapshots from Dynamic Instrumentation metrics, spans, and span tags. The Go configuration page mentions metric probes. Do not infer a Live Debugger release from that wording. The draft says "goals, not release commitments". Exact public wording remains subject to the final publication review.

### [C-085] The eBPF profiler team is working on memory profiling

- **Verdict:** CONFIRMED by the speaker as work in progress
- **Source(s):** Speaker direction in the 2026-11-02 narrative review; C-034 for the current CPU scope
- **Notes:** No release date, overhead number, or promised allocation or heap view. The future slide states work in progress. Exact public wording remains subject to the final publication review.

### [C-086] Calling prebuilt native instrumentation libraries is a potential use of the cgo proposal

- **Verdict:** CONFIRMED as a proposed use case, not shipped behavior
- **Source(s):** C-072; speaker direction in the 2026-11-02 narrative review
- **Notes:** The proposal covers calls to prebuilt C libraries without a C compiler at build time. Native instrumentation libraries are a potential application. Do not imply that the proposal embeds arbitrary binaries or establishes an injector path. The connection to injection is explicitly tentative. Keep the accepted experiment distinct from the design proposal under review.

### [C-087] Dynatrace OneAgent 1.203+ injects into statically linked pure-Go binaries on Linux when Go static monitoring is on and the parent process is dynamically linked

- **Verdict:** CONFIRMED
- **Source(s):** <https://docs.dynatrace.com/docs/ingest-from/technology-support/application-software/go/support/go-known-limitations> (checked 2026-11-02)
- **Notes:** Not supported: static cgo binaries, CGO_ENABLED=0 with -buildmode=pie (no libc), a static container entrypoint under cloud-native full-stack injection. musl needs -linkmode=external.

## Asks for the Go team

### [C-088] The 31 July 2025 Go runtime diagnostics sync notes record Rhys and Michael Knyszek on instrumentation hooks and eBPF

- **Verdict:** CONFIRMED
- **Source(s):** <https://github.com/golang/go/issues/57175#issuecomment-3283520959> (notes posted by mknyszek, 2025-09-12)
- **Notes:** The notes record Rhys: "We don't have a great way to add instrumentation in general. Companies will maintain patches to add hooks. What should we do?" and Michael K: "Maybe eBPF is the answer?" The notes use first names. The slide uses Rhys Hiltner and Michael Knyszek. Present it as thanks, not blame.

### [C-089] The 19 December 2024 sync discussed USDT, and the Go team asked how it would look

- **Verdict:** CONFIRMED
- **Source(s):** <https://github.com/golang/go/issues/57175#issuecomment-2596101614> (posted 2025-01-16)
- **Notes:** Felix raised USDT. thepudds: "it's more stable over time because it's in the source code". Rhys: "Years ago we were interested, but didn't know exactly what we'd use them for." Michael K: "How would this look?"

### [C-090] Go 1.27 moved HTTP/2 into net/http/internal/http2 and added typedesclen to the runtime moduledata

- **Verdict:** CONFIRMED
- **Source(s):** GitHub contents API, checked 2026-11-02: `src/net/http/internal/http2` exists at go1.27.3 and not at go1.26.10; `src/runtime/symtab.go` has `typedesclen` at go1.27.3 and not at go1.26.10
- **Notes:** This is the receipt for the cost of inference without a contract. Present it as a fact about the release, not as blame on the Go team.

### [C-091] The Go team rejects goroutine-local storage, and pprof labels flow through contexts by design

- **Verdict:** CONFIRMED
- **Source(s):** <https://github.com/golang/go/issues/68785> (seankhliao, 2025-11-18; ianlancetaylor, 2025-11-20); #21355 and #69478 are closed; `src/runtime/runtime2.go` at go1.27.3 has `labels unsafe.Pointer // profiler labels` in `runtime.g`; dd-trace-go sets pprof labels (`internal/traceprof`)
- **Notes:** seankhliao: "as I understand, we've rejected anything that could be used as goroutine local storage." ianlancetaylor: "The profile labeling code is designed around passing contexts with attached labels. That is intentional." The ask is a read contract for existing labels, not a new GLS API. Speaker-stated ask.

### [C-092] The Go team called golang/go#69887 a problem report, not a proposal

- **Verdict:** CONFIRMED
- **Source(s):** <https://github.com/golang/go/issues/69887> (matloob, 2024-12-17; aclements, 2024-12-24)
- **Notes:** matloob: "Adding dedicated support for source rewriting tools would result in a significant increase in complexity in the go command". aclements: "This isn't so much a 'proposal' as it is a 'problem report', which is still very helpful!" Trap: #69887 lists seven toolchain directions, not five (dedicated support, build-ID influence, build-graph edges, go/ast, source mapping, -p, shared build flags). The deck says "the gaps" without a count.

### [C-093] A dynamic probe that refers to a stack address is the objection in golang/go#22008

- **Verdict:** CONFIRMED
- **Source(s):** <https://github.com/golang/go/issues/22008> (open; ianlancetaylor, 2017-09-25)
- **Notes:** ianlancetaylor: "I don't see how we could support a dynamic probe executed by the kernel that refers to a local address on the stack." Q&A only. A USDT site is fixed at compile time, and its note gives value locations at that site.

### [C-094] The OpenTelemetry eBPF profiler reads allocator USDT probes for allocation profiling, but not the Go heap

- **Verdict:** CONFIRMED
- **Source(s):** <https://github.com/open-telemetry/opentelemetry-ebpf-profiler/pull/1746> (merged 2026-10-20); live heap is PR #1747 (open); the latest tag v0.0.202640 (2026-10-02) predates the merge
- **Notes:** PR #1746 consumes `otel_memory` USDT probes from an instrumented allocator such as jemalloc. This does not profile the Go heap. It narrows C-085 to allocation profiling merged on main, not in a tag.

### [C-095] The plugin package needs the exact toolchain and dependency versions

- **Verdict:** CONFIRMED
- **Source(s):** <https://pkg.go.dev/plugin> (src/plugin/plugin.go at go1.27.3)
- **Notes:** The package warns that "Runtime crashes are likely to occur unless all parts of the program (the application and all its plugins) are compiled using exactly the same version of the toolchain, the same build tags, and the same values of certain flags and environment variables." The start-up matrix (libc, link mode, build mode) is generic and also confirmed by C-001, C-069, C-087. The speaker attests the vendor cost.

### [C-096] Datadog plans on the "Where our tools go next" slide are goals, not release commitments

- **Verdict:** CONFIRMED by the speaker as goals, not release commitments
- **Source(s):** Speaker direction on 2026-11-02 ("plans on slides too"; the talk is not recorded); C-084 for the tracing horizon; C-051 for the injector plan
- **Notes:** Live Debugger metrics are a goal. Traces are a longer-term goal of 12+ months. The Go injector is in development, and the plan is Go in Single-Step Instrumentation. The eBPF profiler has CPU profiles, and allocation profiling is merged on main. The injector mechanism stays undisclosed.
