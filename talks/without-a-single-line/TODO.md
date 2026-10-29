# TODO: Zero-Touch Go Instrumentation

GoLab 2026 version (expanded from the GopherCon UK keynote).

Companion files: `outline.md` (structure, timing, cut ladder) ·
`speaker-notes.md` (SAY/DO script) · `slides/presentation.md` (the deck) ·
`../../research/without-a-single-line/claims-ledger.md` (every load-bearing claim).

**State:** 84 pages, 38-minute target, 27 fragment reveals, 9 sections. The
word-count model gives about 33 minutes plus a 1:25 cuttable anecdote. The
actual read-through against a clock is still required before delivery.

Count `---` separators minus one to get pages.

---

## TODO

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
- [ ] **Blocking: re-check golang/go#81450 and #81662 the week of the talk.** The
  slide says the GOEXPERIMENT is accepted and the design is in review. Both can
  change before 2 November 2026.
- [ ] **Timed read-through.** Read the SAY content aloud at delivery pace against
  a clock. Record splits at each divider. Write the real number into `outline.md`
  and `speaker-notes.md`. The word-count model is about 33 minutes.
- [ ] **Diagram legibility pass.** Kroki renders Mermaid at a small native size.
  The theme now scales each diagram to the content width, but long
  left-to-right chains still have small labels. Check every diagram from the
  back of a room. Prefer fewer nodes or a top-down layout over a smaller font.
- [ ] **Visual inspection of every changed page.** `make build/pdf` then
  `pdftoppm -f N -l N -r 60 -png` on every changed page. Confirm that the
  eBPF.io loader diagram is readable at width 860 and that its CC BY 4.0
  credit is legible.
- [ ] **Rehearse the cut ladder.** If running long, follow the eight-rung
  ladder in `outline.md`. Never cut anything on the never-cut list.

---

## Done: do not redo

These decisions are settled. They keep getting re-litigated, so the reason is
recorded here.

- **The open is the debugging loop, told straight.** No show of hands, by
  decision. The bug, the log line, the redeploy, the wrong place, the second
  redeploy. Then stop.
- **The agent joke is a plant, not decoration.** It pays off at the agentic
  close and at the take-home skill. Do not move or cut it for time. It is two
  slides, full-bleed, no title, no caption. The beat is spoken: deadpan fake-out,
  then the turn. Ten seconds total.
- **The injector is a teaser.** The Datadog Go injector mechanism is
  deliberately undisclosed, and the apparent contradiction with the LD_PRELOAD
  slide is the device, not a bug. The GoLab version explains process-start
  injection in general from public sources only. Never add the Datadog Go
  injector's linking model, entry path, or binary-compatibility detail to any
  slide or script line. If asked, defer to next year's talk.
- **The primer replaces four old pages.** "How OBI works", the two `.gopclntab`
  slides, and the old USDT slide became primer steps or the "OBI turns
  observations into spans" and unwind-path slides. Do not add them back next to
  the primer.
- **The static-PIE account is script depth.** It lives in the uprobe-cost
  section of `speaker-notes.md`, marked cuttable. Not Kemal's incident, not a
  slide. It is the maintenance cost of inferring a layout you did not compile.
- **Internal claims are speaker-attested ledger rows.** C-050 (Live Debugger),
  C-051 (injector teaser), C-052 (OBI roadmap), C-053 (Usama talk) follow the
  C-026 pattern. Not unsourced slide text.
- **All three screenshots are cropped on purpose.** The two joke screenshots
  are cropped to one identical 16:9 region (image 1 shifted 2px to align
  content). The Usama FOSDEM grab is cropped to title plus poster. The USDT PoC
  and OTel agent skills screenshots are cropped to drop GitHub chrome. Originals
  are kept beside the crops with an `_orig` suffix. Do not swap them back in.
- **Reveals are selective at 23, by decision.** Six lists use `*` fragment
  bullets. Lists inside `.columns` are excluded on purpose. `fragment-floor`
  is 23. This is not drift.
- **Tooling sits at the end because takeaways precede the call to action.** The
  take-home terminal slide and the SIG CTA come after the takeaways, not before.
- **"Combine the layers" was absorbed.** It restated the decision table and the
  practical-combination slide. The 20% adoption line moved to the
  practical-combination slide in its cleared wording. The decision table is
  retitled "When to reach for what."
- **Both mid-deck terminal slides were deleted.** Tooling was stranded
  mid-deck. It now lives at the end as one take-home terminal slide.
- **No em dashes on slides.** Colons and commas are used instead.
