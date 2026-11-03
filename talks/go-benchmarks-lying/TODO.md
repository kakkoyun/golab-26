# TODO — Why Your Go Benchmarks Are Lying

Open work for this talk. Closed items get deleted, not archived; git history is
the archive.

Companion files: `outline.md` (structure, timing, cut ladder) ·
`speaker-notes.md` (the spoken script) · `slides/presentation.md` (the deck) ·
`../../research/go-benchmarks-lying/claims-ledger.md` (every factual claim).

**Delivered at GopherCon UK 2026** at 127 pages. The GoLab 2026 cut is 88
pages, 42 minutes presented, 3 minutes Q&A, fragment floor 0.

---

## Blocking

### Time the GoLab cut against a clock

The times in `outline.md` are a word-count model. Earlier estimates in this
repository were wrong three times. This cut may run short: the SAY text is
about 3,000 words. If it does, use the stretch beats in the script. Read the script aloud at delivery pace with
the final deck. Record the time at each divider. Write the real numbers into
`outline.md` and `speaker-notes.md`. If the total is over 42 minutes, apply the
cut ladder in `outline.md`.

### Test the presenter setup offline

Serve the offline HTML with the network off. Check presenter view, the clicker,
reveals, fonts, images, and notes. Keep the PDF and the script on the laptop.

### Finish the meme layout

Deferred by the speaker. The two `meme fit` slides ("PR #4891 and PR #643" and
"you, after three sysfs writes") show the GIF at the left edge, not centred.
The deck rule `section.meme.fit p:first-of-type` does not take effect in the
PDF. Find out why before you add more CSS. With `bg contain`, the GIF
subtitles go under the caption band. The first frame of `meme-captain-now.gif`
is almost empty, so the PDF handout shows a blank-looking frame. Check every
meme in the bespoke HTML, where GIFs animate.

---

## After GoLab

### Re-capture the demo results under the golab-26 module path

`demo/go.mod` declares `github.com/kakkoyun/golab-26/demo`. The captured files
in `demo/results/` still print the old `gopherconuk-26` path. Re-capture them on
a quiet machine. Do not edit captured output by hand.

The `payload` string in `demo/bloop_bench_test.go` still says "GopherCon UK
2026". It is benchmark input, so change it only in the same re-capture.

### Re-measure the local container run on an idle machine

The deck shows one run from August 2026 and labels it that way (ledger row 8).
Two later attempts failed: one ran beside Marp and PDF builds, and `benchenv`
refused the other because of load. Do not override that gate. Redo the run with
nothing else running, then confirm or change the slide.

### Fold in Scott's marked-up PDF

Still not received. When it lands, diff his notes against what is already
addressed.

### Send Scott the podcast link

For marketing to help promote, once published.

---

## Nice to have

### Decide what to do with the assets that the GoLab cut orphaned

No slide references these files now: `bp-feedback-flow.png`,
`go1.26_b_loop_change.png`, `golang_perf_dashboard_charts.png`,
`golang_performance_dashboard.png`, `golang_performance_monitoring.png`,
`golang_slowbot.png`, `golang_slowbot_quote.png`. Some are evidence for ledger
rows. Delete the others after GoLab, or put them back on a slide.

---

## Done — do not redo

Kept short deliberately. These come up repeatedly, so they are recorded to stop
them being "fixed" again.

* **Incident first, Datadog first.** The GoLab cut opens on the #4891 bot
  comment, then Datadog's stake, then OPERA. The general "why benchmark"
  material and most Go basics were cut on purpose. The audience is
  Intermediate, and 92 pages in 45 minutes was too dense for the other talk.
* **No maths on stage.** No formulas, no p-values, no CV definition. Say why a
  check matters, not how the statistics work. Prefer bar charts and diagrams
  to tables of numbers. The bars are plain HTML with classes: Marp strips
  inline `style` attributes.
* **The message is "invest".** Benchmarking is not easy: investment, maths,
  tooling, a keen eye. Datadog and the Go team do it. The close says so. Do
  not bring back "under an hour", which contradicts it.
* **DODO uses the public blog only** (row 48). `dodo-cli` gets its name, beta
  status, and features (row 49). No dollar figures, no install steps, no PR
  links from the internal Confluence space.
* **Own tooling stays off the slides.** The benchlab panels and the tool list
  were cut. The close points at the talk repository only.
* **OPERA stays.** Drop it only if another story replaces it. The Ereditato
  quote (row 46) is the improvement: "trivial things we are clever enough to
  rule out", and then the cause was a loose connector.
* **Datadog practice is on a slide, inside row 23.** Four items only:
  dedicated hardware, per-SDK budget, several workloads per SDK, release gate.
  No hardware counts, budget figures, archetype names, or scale. The archetype
  table is the public FOSDEM taxonomy, not Datadog's list.
* **The PGO number is one service.** −3.4% CPU on one large service (row 47),
  not "production CPU".
* **#643 was a local run, not a bot comment.** The slide title says "A second
  red number" for that reason.
* **The local container run is one run.** It is labelled with its date and
  file. Do not compare it with the bare-metal numbers, which come from a
  different benchmark (row 8).
* **No internal vocabulary on slides.** Dividers are numbered `01`–`06`. Long
  divider titles cross into the right panel. Check each one in the PDF.
* **Slides carry mottos, data, visuals, and links only.** Prose belongs in
  `speaker-notes.md`.
* **`*` is the only list marker on slides.** Every list is an intentional Marp
  reveal. `make check/fragments` guards the count.
* **Presenter notes are generated.** Edit `speaker-notes.md`, then run
  `make sync/notes`. `make check/notes` checks both talks.
* **The `b.Loop` removes-table is correct. Do not "fix" it.** Go 1.26 is the
  fix, not the regression. What 1.26 removed is the inlining suppression that
  1.24 and 1.25 used to implement keepalive. The keepalive remains. Ledger rows
  39 to 41.
* **`allocs/op` is a second witness, not proof.** In the DCE benchmark,
  `make([]byte, 64)` does not escape after inlining
  (`demo/results/gcflags-m-m.txt`). The deck says "the work is gone", not
  "`make` cannot skip allocating". Ledger row 50.
* **SMT off is "under 0.25%", not "0.04%".** The two no-SMT runs were 0.044%
  and 0.235%. "~100×" only holds for the range. Ledger row 2.
* **The #4891 "~390 ns" figure is gone.** The war-story notes give ~390 ns per
  iteration and an 883 ns table side by side. The slide now says
  "sub-microsecond" so it does not depend on either.
* **An editor or agent autofix strips trailing commas from headings.** The
  repository sets `MD026: false` on purpose. If punctuation disappears from a
  heading, suspect format-on-save.
