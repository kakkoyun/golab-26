# TODO: Zero-Touch Go Instrumentation

GoLab 2026 version (expanded from the GopherCon UK keynote).

Companion files: `outline.md` (structure, timing, cut ladder) ·
`speaker-notes.md` (SAY/DO script) · `slides/presentation.md` (the deck) ·
`../../research/without-a-single-line/claims-ledger.md` (every load-bearing claim).

**State:** working narrative draft, 43-minute target, hard stop at 45, no Q&A. The time budgets need a
timed read-through.

---

## Blocking

- [ ] Owner review of the future and public-source claims: C-060 to C-075
  (injector and Live Debugger) and C-081 to C-096 (section 08). Tracing is a
  speaker-stated 12+ month goal. Open points: the Live Debugger diagram
  simplifies the backend-to-`system-probe` hop. Decide whether the close slide
  needs Targeted redaction mode. The docs do not label Go Live Debugger GA or Preview.
- [ ] Merge and push before 15:30 on 2 November. The section 08 QR code points
  to `talks/without-a-single-line/go-asks.md` on `main`.

## Should-do

- [ ] Timed read-through of SAY content at delivery pace. Record splits at
  each divider and update the budgets in `outline.md` and `speaker-notes.md`.
- [ ] Layout pass on section 08: check the divider caption, Ask 1, and the
  recap table from the back of the room.
- [ ] Diagram legibility: Kroki renders small. Prefer fewer nodes or a
  top-down layout over a smaller font.
- [ ] Visual inspection of every changed page (`make build/pdf`, then
  `pdftoppm -r 60`). Confirm the eBPF.io loader diagram and its CC BY 4.0
  credit are legible at width 860.
- [ ] Rehearse the cut ladder in `outline.md`. Never cut the never-cut list.

## Nice-to-have

None currently.

---

## Done: do not redo

- **Open with the debugging loop, told straight.** No show of hands. The
  decision keeps the open short.
- **The agent joke is a plant.** It pays off at the agentic close. Do not move
  or cut it for time. Reason: the callback needs the setup.
- **The install-command slide stays removed.** The owner removed it in the
  narrative review. Keep the resource links, SIG call, and benchmarks plug.
- **The injector is a teaser.** The Datadog Go injector mechanism is undisclosed,
  and the contradiction with the LD_PRELOAD slide is the device. Defer to next year.
- **Teach eBPF through OBI.** Go-specific details stay with that example. USDT
  belongs in the future section. No duplicate primer slides.
- **The static-PIE account is script depth.** It is cuttable. It is not a slide
  and not the speaker's incident. It shows the maintenance cost of inferred layouts.
- **Internal claims are speaker-attested ledger rows.** C-050, C-051, and C-053
  follow the C-026 pattern. C-052 is superseded by the actual releases.
- **OBI v1.0.0 is a "stable core", not "stable".** The Go module API, Collector
  receiver, gRPC telemetry, and Go runtime metrics are outside v1. The README
  still says "Development", so do not quote it.
- **All three screenshots are cropped on purpose.** Originals keep an `_orig`
  suffix. Do not swap them back.
- **Reveals only for the important beats.** Two lists reveal: the opening
  loop and "What makes Go different". Every other list is an HTML `<ul>`. Reason:
  a click per item slowed the talk and diluted the reveals that matter.
- **The SIG call follows the takeaways.** Keep the resource links at the end.
- **"Combine the layers" was absorbed.** The 20% line moved to the practical-
  combination slide. The table is "When to reach for what."
- **The narrative stays editable.** Do not add a fixed-order test or remove
  slide punctuation to satisfy a heading comparison.
- **No em dashes on slides.** Use colons and commas instead.
