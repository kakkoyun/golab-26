# Outline: Zero-Touch Go Instrumentation

> **Format:** GoLab 2026. 45-minute slot: 38 minutes presented, 7 minutes Q&A. Intermediate Go audience.
> **Deck:** `slides/presentation.md` (working draft)
> **Script:** `speaker-notes.md` (SAY/DO format)

## Thesis

Automatic instrumentation supplies baseline evidence without hand-written
wrappers throughout the application. Follow the lifecycle: build, process
start, then kernel. Track traces, metrics, logs, and profiles at each point.
The SDK and integrations determine what each path can provide.

When the baseline misses a production question, a live probe can capture the
missing values. The closing proposals address the limitations that the audience
now understands. Then the agent returns to the opening bug with a useful
mechanism and its constraints.

Build-time instrumentation still requires a rebuild. Zero-touch does not mean
zero operational cost. This remains a working narrative, not a fixed sequence.

## Beat sheet

| Section | Budget | Running | Purpose |
| --- | ---: | ---: | --- |
| Open and 01 Why Go resists | 4:00 | 4:00 | The production bug, coverage gaps, agent joke, lifecycle map, and four signals. |
| 02 otelc | 4:00 | 8:00 | SDK-dependent signals, build ownership, runtime storage, and linkname fragility. |
| 03 Injector | 3:00 | 11:00 | SDK capabilities at startup, the loader constraint, and the development teaser. |
| 04 OBI | 9:00 | 20:00 | Explain eBPF through OBI. Traces and metrics, Go-specific mechanics, and operational costs. |
| 05 Profiles | 2:30 | 22:30 | A kernel route to CPU profiles. Establish the need for request correlation. |
| 06 Live debugging | 3:30 | 26:00 | Return to the bug. Capture logs and variables within explicit limits. |
| 07 Choose the signal and the layer | 2:00 | 28:00 | Compare signal coverage and deployment constraints. Include live debugging. |
| 08 What comes next | 4:00 | 32:00 | USDT, native libraries, a stable context ABI, profile correlation, memory profiling, and live-probe goals. |
| 09 From question to evidence | 4:00 | 36:00 | Agent callback, takeaways, concrete SIG asks, benchmarks plug, and resources. |
| Buffer | 2:00 | 38:00 | Pauses, audience reactions, and overruns. |

These are working budgets, not measurements. The expanded future section needs
a timed read-through. Removing the install slide does not prove that the new
material fits. Keep the optional static-PIE anecdote within the OBI budget,
or omit it. Allow about 1:25 if included.

Checkpoints: otelc by 4:00, injector by 8:00, OBI by 11:00, profiles by 20:00,
live debugging by 22:30, selection by 26:00, future work by 28:00, and the
closing callback by 32:00. Revise the budgets after rehearsal.

## Cut ladder

Nothing is cut up front. Cut in this order. Each rung says why it is safe.

1. **Convergence timeline** (-0:40). The three-organisations slide carries the
   argument. The dates corroborate.
2. **"Find the instruction and the field"** (-0:35). Say one sentence about DWARF
   and the offset database on the OBI slide instead.
3. **"CO-RE adapts kernel layouts, not Go layouts"** (-0:30). Keep the spoken
   line "CO-RE knows kernel types, not Go types" on the hooks slide.
4. **Full 13-library enumeration** (-0:40). "Thirteen documented baselines" and
   the support-matrix link survive on the OBI intro slide.
5. **The static-PIE anecdote** (-1:25). Script only, costs no page.
6. **"Other ways, and their cost"** (-0:45). The live-debugging section still
   makes its point without the comparison.
7. **Usama reference slide** (-0:25). Generous, not load-bearing. The footer
   link and the verbal credit remain.
8. **Zero-touch profiling deployment-cost table** (-0:40). The OBI
   platform-contract table already taught the room to expect a privilege and
   platform bill.
9. **Shameless plug** (-0:15). The plug can be spoken over the take-it-with-you
   slide in five seconds if the room is behind.

## Never-cut list

Do not cut these to buy time. Trimming the jokes recreates the density problem
they exist to fix.

- The agent joke (both slides)
- Both memes
- The loop open
- The injector teaser
- The agentic close
- The uprobe-cost slide
- The OTEP correlation argument
- The decision table
- The lifecycle map
- The final resource links
- The uprobe-hit and RET-site slides (the Go-specific core of the kernel section)
- "A static Go binary has no loader"

## Narrative transitions

### Open and Go constraints to build time

The agent needs both a mechanism and a reason to choose it. Start where source
structure remains available. Introduce the four signals as evidence, not a
ranking of tools.

### Build time to process start

The build path can enable SDK signals, but it needs build ownership. Ask what
is possible when we cannot change the build. Startup injection changes the
attachment path, not the SDK's capabilities.

### Process start to kernel

Go restricts the startup path. An external observer gives another option.
Introduce OBI, explain one uprobe hit, then show how OBI turns events into spans.
Attach the Go-specific details to that example instead of a standalone primer.

### Kernel to profiles

OBI supplies boundary traces and metrics. CPU profiles answer another question.
The build path can include profiling too. This section offers a kernel route,
not exclusive ownership of the profiling signal.

### Profiles to live debugging

Request context can connect profiles and traces, but both can still miss a
variable. Return to the opening bug. A live logpoint asks for the missing
value while the service runs.

### Live debugging to selection

Compare both dimensions: the evidence needed and the intervention point that
the service can support. Show one useful combination, not a universal stack.

### Selection to future work

The audience now knows the costs of inferred layouts, missing hooks, and
separate context stores. USDT, native-library support, and stable context
storage address those limits. Separate proposals and aspirations from current
signals. Memory profiling is work in progress. Live Debugger metrics and
tracing are goals, with tracing on a 12+ month horizon, not a release commitment.

### Future work to close

The future work can improve the tools. The agent callback uses evidence that
current preview tools already capture. Resolve the opening joke and bug,
state the decision rule, and invite specific contributions. Keep the resource
links. Do not restore the install-command slide.

## Facts that must remain precise

- OBI supports Linux amd64 and arm64, kernel 5.8+ with BTF, plus documented
  RHEL-family backports.
- OBI v1.0.0 (30 Oct 2026) is a stable core, not a stable everything. The Go
  module API, the Collector receiver, and gRPC telemetry are outside the v1
  contract.
- OBI trace-log correlation enriches selected JSON and plain-text logs and
  does not export them.
- OBI's support matrix documents 13 Go library baselines, including
  gin >= v1.6.0, != v1.7.5 and github.com/redis/go-redis/v9 >= v9.0.0.
- Privileges vary by feature. Do not present one capability list as universal.
- Recent kernels improved uprobe scalability, but attached probes still cost
  context switches and BPF programs can introduce contention.
- otelc is a stable production build-time path, not a local-development tool.
- otelc's CI covers Linux, macOS, and Windows builds. It has no eBPF or
  Linux-kernel runtime dependency.
- Upstream otelc currently produces traces, HTTP/gRPC metrics, runtime metrics,
  and supported log records. Orchestrion with dd-trace-go can also enable
  continuous profiling and Datadog log correlation.
- Not every Datadog integration has moved to otelc.
- Profiles are the fourth observability signal. The OpenTelemetry Profiles
  specification remains Alpha.
- OTEP 4947 proposes a Go-specific pprof-label path. Present it as proposed
  work, not a shipped guarantee. It is distinct from the ask for ABI-stable
  trace-context storage. Current build-time goroutine-local storage does not
  establish a stable Go runtime API.
- The Live Debugger metrics and tracing goals, including the 12+ month tracing
  horizon, are speaker-attested aspirations. They are not release commitments.
- Memory profiling is speaker-attested work in progress. Do not promise a date
  or specific allocation and heap views.
- Native instrumentation libraries are a potential use of the cgo proposal.
  Its connection to the injector path remains tentative.
- The OpenTelemetry host injector does not inject Go. The OpenTelemetry
  Operator has a separate feature-gated Go eBPF sidecar.
- Do not imply that Kemal contributes to OBI. His eBPF experience comes from
  Parca and parca-agent.
- The zeroins catalog commands are offline and read-only. Its Kubernetes
  wrappers are experimental and require explicit telemetry endpoints plus
  confirmation of context, namespace, transport, and privilege impact.
- Do not discuss an Orchestrion sunset.
- Keep the 20% adoption statement within its approved wording. Do not add a
  denominator or the "mostly new users" interpretation.
- The Datadog Go injector mechanism is still undisclosed. The GoLab version
  explains process-start injection from public sources only: ld.so(8), the
  System V ABI, golang/go#28909, the OpenTelemetry injector README, and the
  public Datadog SSI docs. Never add the Datadog Go injector's linking model,
  entry path, or binary compatibility to any slide or script line. If asked,
  defer to next year's talk. The owner reviews every injector and Live
  Debugger claim before delivery (see `TODO.md`).
- Proposal golang/go#81450 (cgo without a C toolchain) is in review. Only the
  GOEXPERIMENT issue golang/go#81662 is accepted. Do not call the proposal
  accepted. Do not predict which Go binaries an injector can reach after it
  ships.
- The OpenTelemetry host injector ships Java, Node.js, .NET, Ruby, and Python
  (Python off by default). Datadog SSI lists Java, Python, Ruby, Node.js, .NET,
  and PHP. Neither lists Go.
- OBI does not use uretprobes for Go. It attaches ordinary uprobes at RET
  instructions.

## Public audience resources

- Talk repository: <https://github.com/kakkoyun/golab-26>
- zeroins toolkit: <https://github.com/kakkoyun/zeroins>
- opentelemetry-agent-skills: <https://github.com/ollygarden/opentelemetry-agent-skills>
- Prior FOSDEM version: <https://youtu.be/0TvrSebuDPk>
- OBI documentation: <https://opentelemetry.io/docs/zero-code/obi/>
- Go compile-time instrumentation: <https://opentelemetry.io/docs/zero-code/go/compile-time/>
- OTEP 4947: <https://github.com/open-telemetry/opentelemetry-specification/blob/main/oteps/profiles/4947-thread-ctx.md#alternative-for-go-support>
- Usama Saqib's public eBPF pitfalls talk: <https://fosdem.org/2026/schedule/event/H3LM7G-performance_and_reliability_pitfalls_of_ebpf/>
- OpenTelemetry community SIGs: <https://github.com/open-telemetry/community>
