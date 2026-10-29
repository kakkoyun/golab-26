# Outline: Zero-Touch Go Instrumentation

> **Format:** GoLab 2026. 45-minute slot: 38 minutes presented, 7 minutes Q&A. Intermediate Go audience.
> **Deck:** `slides/presentation.md` (84 pages)
> **Script:** `speaker-notes.md` (SAY/DO format)

## Thesis

The debugging loop is slow. An agent alone does not fix it. Three approaches take
the rebuild out of it: build, process start, kernel. A live debugger then reads
production state with no redeploy. Then the agent, holding the framework, closes
the loop.

GoLab lists the talk as Intermediate. The GoLab version therefore builds eBPF up
from first principles before it uses it, and it explains the process-start path
and live debugging in depth. Those two topics are the differentiators of this
version.

## Beat sheet

| Section | Est. | Running | Purpose |
| --- | ---: | ---: | --- |
| Open | 2:10 | 2:10 | The debugging loop, told straight. The agent joke. Why Go is different. |
| 01 Why Go resists | 1:50 | 4:00 | Native code, static linking, movable stacks, go:linkname, the lifecycle map. |
| 02 eBPF, from the ground up | 7:20 | 11:20 | Nine steps: checked program, CO-RE, hooks, one uprobe hit, Go registers and goroutine identity, RET-site probes, instruction and field offsets, USDT, the missing Go producer. |
| 03 OBI | 4:35 | 15:55 | OBI as the primer applied. Coverage, signals, platform contract, privileges, uprobe costs, Usama reference. Meme A. |
| 04 otelc | 3:30 | 19:25 | Three-org convergence, -toolexec, production adoption, portability, signal depth, GLS, variable-linkname fragility. Meme B. |
| 05 Injector | 3:05 | 22:30 | The loader sequence, the runtimes every injector ships, why a static Go binary has no loader, the teaser. |
| 06 Profiles | 2:40 | 25:10 | The fourth signal. The `.gopclntab` unwind path, deployment cost, OTEP 4947 correlation bridge. |
| 07 Live debugging | 3:25 | 28:35 | Probe a running process. Line to address, unavailable variables, public limits, other ways. |
| 08 When to reach for what | 1:00 | 29:35 | Decision table, practical combination, 20% adoption. |
| 09 What comes next | 3:20 | 32:55 | cgo without a C toolchain, the agentic close, takeaways, take-home kit, SIG call to action. |

Timing is a **word-count model**, not a measurement: 3,422 SAY words at 130
words per minute, plus 25% for pauses and visuals, gives 32:55. The cuttable
static-PIE anecdote adds about 1:25. This deck has more silent beats than the
benchmarks talk (two jokes, three memes, five punchline pages), so the real
overhead is probably higher. The remaining 3-4 minutes to 38:00 are buffer, not
missing content. The timed read-through in `TODO.md` replaces the model.

Checkpoints: open the primer by ~4:00, OBI by ~11:30, otelc by ~16:00, the
injector by ~19:30, live debugging by ~25:00, the decision section by ~28:30.

## Cut ladder

Nothing is cut up front. In order, with why each is safe:

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
- The take-home kit
- The uprobe-hit and RET-site primer slides (the Go-specific core of the primer)
- "A static Go binary has no loader"

## Narrative transitions

### Open to 01

The loop is slow. The agent joke says the agent alone does not fix it. Why?
Because Go compiled away the attachment point.

### 01 to 02 (eBPF primer)

Two of the three paths run on eBPF. Build it from the bottom before using it.
Each step needs the one before it.

### 02 to 03 (OBI)

The primer ends with Go missing a USDT producer. OBI is what you build when the
program declares nothing: it infers sites and layouts from the outside. The
cost is Linux, privileges, and kernel contracts.

### 03 to 04 (otelc)

OBI reaches deployed workloads without rebuilding, but cannot infer arbitrary
business semantics. otelc moves the intervention earlier, where source
structure is still available. The cost is owning the build.

### 04 to 05 (Injector)

Build and kernel are two legs. The third is process start. Every other runtime
gives the dynamic loader an agent entry point. A static Go binary never starts
the loader. The binary is the constraint.

### 05 to 06 (Profiles)

Tracing follows requests. Profiling finds CPU cost. The two signals become
stronger when they share request context.

### 06 to 07 (Live debugging)

Every tool so far emits telemetry that you planned. The bug from the opening
needs one variable that you did not plan. A live debugger puts a uprobe at a
source line in a running process.

### 07 to 08 (Decision)

Return to the lifecycle map. Start with the constraint you cannot change. Add
the next layer only when its signal pays for its operational cost.

### 08 to 09 (Close)

The loop from the open, now short. The agent places the probe and reads
production evidence. No redeploy. Same move as the joke, except now the agent
has the framework.

## Facts that must remain precise

- OBI supports Linux amd64 and arm64, kernel 5.8+ with BTF, plus documented
  RHEL-family backports.
- OBI trace-log correlation enriches selected JSON logs and does not export
  them.
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
  work, not a shipped guarantee.
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
