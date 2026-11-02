# TODO: Zero-Touch Go Instrumentation

GoLab 2026 version (expanded from the GopherCon UK keynote).

Companion files: `outline.md` (structure, timing, cut ladder) ·
`speaker-notes.md` (SAY/DO script) · `slides/presentation.md` (the deck) ·
`../../research/without-a-single-line/claims-ledger.md` (every load-bearing claim).

**State:** working narrative draft, 38-minute target. Lifecycle order and
signal tracking now connect the sections. Future asks remain near the end.
The time budgets need a timed read-through.

---

## Blocking

- [ ] Review the exact public wording of the future claims in C-081 to C-096.
  Live Debugger tracing has a speaker-stated 12+ month horizon, not a release
  commitment. Memory profiling is work in progress. The read contract for
  pprof labels is an ask, and the cgo-to-injector connection remains tentative.
  Section 08 claims are C-088 to C-096.

- [ ] Merge and push before 15:30 on 2 November. The section 08 QR code points
  to `talks/without-a-single-line/go-asks.md` on `main`.

- [ ] **Blocking: owner review of the new public-source claims.** The GoLab
  expansion adds ledger rows C-060 to C-075 from public sources. The owner
  approves each injector and Live Debugger row before delivery, as agreed. The
  full research and quotes are in `research/without-a-single-line/08-ebpf-primer.md`,
  `09-process-start-injection.md`, and `10-live-debugger.md`. Open points:
  - The Live Debugger sequence diagram simplifies the hop from the backend to
    `system-probe`. The public docs do not describe that hop.
  - Bits Live Debugger needs Targeted redaction mode. The close slide does not
    say so. Decide whether to add it.
  - The public docs do not label Go Live Debugger itself as GA or Preview. Only
    Bits Live Debugger is labelled Preview.

## Should-do

- [ ] **Timed read-through.** Read the current SAY content aloud at delivery
  pace. Record splits at each divider. Update the working budgets in
  `outline.md` and `speaker-notes.md`. Pay particular attention to the expanded
  future section. The removed install slide does not prove that everything fits.
- [ ] Layout pass on section 08: the divider caption sits under the GIF in the
  right panel. Check the Ask 1 slide and the recap table from the back of the
  room.
- [ ] **Diagram legibility pass.** Kroki renders Mermaid at a small native size.
  The theme now scales each diagram to the content width, but long
  left-to-right chains still have small labels. Check every diagram from the
  back of a room. Prefer fewer nodes or a top-down layout over a smaller font.
- [ ] **Visual inspection of every changed page.** `make build/pdf` then
  `pdftoppm -f N -l N -r 60 -png` on every changed page. Confirm that the
  eBPF.io loader diagram is readable at width 860 and that its CC BY 4.0
  credit is legible.
- [ ] **Rehearse the cut ladder.** If running long, follow the nine-rung
  ladder in `outline.md`. Never cut anything on the never-cut list.

## Nice-to-have

None currently.

---

## Done: do not redo

These decisions are settled. They keep getting re-litigated, so the reason is
recorded here.

- **The open is the debugging loop, told straight.** No show of hands, by
  decision. The bug, the log line, the redeploy, the wrong place, the second
  redeploy. Then stop.
- **The agent joke is a plant, not decoration.** It pays off at the agentic
  close. Do not move or cut it for time. It is two
  slides, full-bleed, no title, no caption. The beat is spoken: deadpan fake-out,
  then the turn. Ten seconds total.
- **The install-command slide is removed.** The owner removed "Take it home"
  during the narrative review. Keep the final resource links, the SIG call to
  action, and the benchmarks plug. Do not restore an installation walkthrough.
- **The injector is a teaser.** The Datadog Go injector mechanism is
  deliberately undisclosed, and the apparent contradiction with the LD_PRELOAD
  slide is the device, not a bug. The GoLab version explains process-start
  injection in general from public sources only. Never add the Datadog Go
  injector's linking model, entry path, or binary-compatibility detail to any
  slide or script line. If asked, defer to next year's talk.
- **Teach eBPF through OBI.** Keep the Go-specific uprobe, goroutine, RET-site,
  and layout explanations attached to that example. USDT belongs in the future
  section, where it answers the inference problem. Do not add duplicate primer
  slides.
- **The static-PIE account is script depth.** It lives in the uprobe-cost
  section of `speaker-notes.md`, marked cuttable. Not Kemal's incident, not a
  slide. It is the maintenance cost of inferring a layout you did not compile.
- **Internal claims are speaker-attested ledger rows.** C-050 (Live Debugger),
  C-051 (injector teaser), C-053 (Usama talk) follow the C-026 pattern. Not
  unsourced slide text. C-052 (OBI roadmap) is superseded by the actual
  releases.
- **OBI v1.0.0 is a "stable core", not "stable".** Checked against the
  v1.0.0 release notes, TELEMETRY.md, and the schema registry on 2026-11-01
  (C-076 to C-079). The Go module API, the Collector receiver, gRPC telemetry,
  and Go runtime metrics are outside the v1 contract. Do not quote the README
  status line: it still says "Development", and the release notes call that
  wording a known follow-up.
- **All three screenshots are cropped on purpose.** The two joke screenshots
  are cropped to one identical 16:9 region (image 1 shifted 2px to align
  content). The Usama FOSDEM grab is cropped to title plus poster. The USDT PoC
  and OTel agent skills screenshots are cropped to drop GitHub chrome. Originals
  are kept beside the crops with an `_orig` suffix. Do not swap them back in.
- **Reveals remain selective.** The deck declares its current fragment floor.
  Lists inside `.columns` remain outside the fragment count.
- **The SIG call follows the takeaways.** Ask for concrete probe, context, and
  deployment requirements. Keep the resource links at the end.
- **"Combine the layers" was absorbed.** It restated the decision table and the
  practical-combination slide. The 20% adoption line moved to the
  practical-combination slide in its cleared wording. The decision table is
  retitled "When to reach for what."
- **The narrative remains editable.** Review section flow with the speaker.
  Do not impose a fixed-order test or remove slide punctuation to satisfy a
  heading comparison.
- **No em dashes on slides.** Colons and commas are used instead.
