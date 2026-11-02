# Preparation plan: Why Your Go Benchmarks Are Lying

Preparation for 3 November 2026. Written on 2 November.

Status: preparation not started. This versioned plan is the handoff for
implementation in a separate session. It replaces the August assumptions in
`plans/go-benchmarks-lying.md` for this delivery. It does not replace the talk's
`TODO.md`, `outline.md`, or `speaker-notes.md`.

## Scope and decisions

Apply the useful preparation passes from `without-a-single-line` to
`go-benchmarks-lying`. Transfer the method and the verified support. Keep the
benchmark talk's own argument, evidence, and delivery constraints.

The current outline specifies a 45-minute slot: 38 minutes presented and
7 minutes of Q&A. Keep that budget unless Kemal changes it. The decision to
skip Q&A belonged to the other talk. Confirm tomorrow's room, time, recording
policy, and presenter setup before rehearsal. History records 10:45 in GoLab
room 2, but this plan does not confirm the current schedule.

Implementation starts in a separate session. Discuss major content changes
before editing. Use a linked worktree for tracked changes. Obtain approval of
the final staged diff and commit message before committing. Do not copy the
emergency main-branch edits from the earlier sessions.

## What we did, and what transfers

The sessions checked evidence, repaired the argument, reduced reading and
clicking, and made the deck usable on stage.
The last sessions also removed or replaced earlier additions. The latest
accepted state matters more than the number of passes.

| Pass | What happened in the first talk | Decision for benchmarks |
| --- | --- | --- |
| Facts and releases | Checked release notes, tagged code, commit history, quotes, links, and small reproductions. Corrected claims that documentation alone did not settle. [H1, H3] | Repeat for claims still visible or spoken. Record versions and exact evidence. Do not upgrade every dependency. |
| Narrative | Compared alternative structures before choosing one. Connected mechanisms to the opening problem and closed with a callback. [H4] | Audit the two-scale argument and transitions. Preserve WHY-first, both incidents, and the three questions. Do not impose the instrumentation lifecycle. |
| Spoken script | Shortened SAY sentences, DO cues, the outline, and the TODO. Shortened ledger explanations without removing sources or traps. [H3, H5] | Repeat after the factual and structural decisions. Keep numbers, attribution limits, and reserve answers. |
| Slide density and reveals | Changed topic headlines into claims. Moved detail into the script. Reduced reveal bullets from 62 to 6. [H5] | Review each list. Use static HTML lists where a reveal adds no meaning. Six is not a target for this talk. |
| Humor | Added candidate memes, rendered them, enlarged one, then removed one after narrative review. [H5, H6] | Keep the three existing protected memes. Add a new one only if it earns its time and place. No meme quota. |
| Theme application | Inspected PNGs, measured diagrams, corrected sizing and captions, and checked the final state after integration. [H7, H9] | Reuse the existing GoLab theme. Inspect benchmark charts, tables, code panels, images, and footers. Avoid a theme redesign. |
| Stage support | Added generated presenter notes, subtle footer cues, an offline HTML target, and a diagram guard. [H3, H5, H7] | Reuse support where it fits. The benchmark script still needs adaptation. Test the actual presenter workflow offline. |
| Close and resources | Reduced the sales pitch, removed an install slide, kept useful resources, and added a plug for the next talk. [H2, H4, H8] | Review the tool-heavy close for audience value. Keep talk-repository and benchlab links distinct. Do not advertise a talk that already happened as tomorrow's talk. |

Use this order for future talks:
facts and constraints, narrative approval, script, slide density and visuals,
presenter notes, cues, integrated verification, timed rehearsal, freeze.
Content comes before cues. Approval comes before major edits. [H4, H5]

## Current gaps, checked at `d3deb90`

These are repository observations, not a fresh public-source audit.

* The benchmark deck has 105 Markdown slide blocks and 45 reveal bullets.
  It has no static `<ul>` lists, footer cue directives, or generated notes.
* The other deck has 90 generated note entries. A read-only call to
  `tools/sync_presenter_notes.py` recognizes all 90 and reports no alignment
  problems. On the benchmark script, it recognizes zero entries and reports
  105 alignment problems.
* The benchmark script groups slide entries under `###` headings. It uses
  `> **SAY:**` and inline `` `DO` `` cues. The current tool expects separate
  `##` slide entries with `**SAY**` or `**DO**`. A path override alone is not
  enough to generate usable notes.
* `Makefile` sets `NOTES_TALK := talks/without-a-single-line`. The default
  notes check therefore does not check the benchmark talk.
* The benchmark outline labels timing as a word-count model. Its TODO requires
  a real timed read. The TODO also repeats an old 59:30 timing claim, although
  the current outline models 36:00 within the 38-minute target.
* The outline and script still call ledger row 23 pending or unresolved.
  The ledger marks it verified. The settled decision is to keep the slide
  generic anyway. Correct the status references without restoring internal detail.
* The TODO records two rejected CV remeasurement attempts. Ledger row 8 still
  includes an unsupported Mac-VM CV floor. A `verified` label does not settle
  the quantitative statement in its notes.
* The TODO requires a fresh check of benchlab output. Row 25 records a check
  against `benchlab@102fc97` on 12 August, not this delivery.
* Shared theme CSS, the offline target, the footer guard, and Vale scope already
  exist. The Mermaid palette change lives in the other talk's plugin. The
  benchmark deck currently has no Kroki diagram fences, so copying that plugin
  has no present delivery benefit.

## Execution checklist

### 0. Establish the candidate and the delivery contract

* [ ] Confirm the slot and Q&A split with Kemal. Record any change in both the
  outline and the script. Confirm whether the talk is recorded.
* [ ] Create `.worktrees/benchmarks-prep` on branch `benchmarks-prep` from the
  agreed current main. Read the current TODO and its settled decisions first.
* [ ] Record the base commit, clean status, slide count, and reveal count.
  Run `make check/fast`, then `make check` before editing. Save each exit code
  and log locally. Stop on a failure and identify its cause.
* [ ] Read the script aloud through the opening, both incident transitions,
  and the close. List problems by slide title, not only by page number.

Output: a baseline record and an agreed delivery budget. A historical green
check is not evidence for the current candidate.

### 1. Resolve factual risks before polishing

* [ ] Map every visible number, quote, attribution, and technical claim to a
  ledger row or captured result. Include factual statements in SAY blocks.
  Mark each result as confirmed, changed, unsupported, or awaiting owner input.
* [ ] Check version-sensitive claims against the cited release notes, source,
  and relevant commits. Prioritize `b.Loop`, DCE protection, code-layout
  effects, and tool behavior. Preserve the direction of the Go 1.26 fix.
  Separate historical behavior from current behavior. Do not silently retarget
  Go 1.26.5 captures to the currently installed Go version.
* [ ] Resolve the CV evidence in ledger row 8, the local-environment slides,
  the script, and `demo/results/`. Use the quiet-run procedure below. If no
  valid run is possible, ask Kemal to approve qualified historical evidence
  or removal of the unsupported comparison. Never present an unmeasured floor
  as established fact.
* [ ] Rebuild the three benchlab binaries from one recorded commit. Compare
  only the panels and claims still used in this cut. Record command, version,
  environment, raw output, and the result in row 25. Recheck the nine-check
  `benchenv` panel. Do not restore the two removed tool panels.
* [ ] Correct the stale row-23 status references in the outline and script.
  Keep the internal-practice slide generic. Preserve its disclosure limits.
* [ ] Check every audience link and decode the closing QR. Confirm that the
  talk QR reaches the talk repository and that the tool link reaches benchlab.
  Keep unavailable results open. Do not report a network failure as a dead URL.

Output: corrected ledger, deck, script, and TODO in one consistent candidate.
No unsupported factual claim remains on a slide. Public research uses public
queries only. Never send internal source, logs, or private documents to web search.

#### Quiet-run procedure for the CV evidence

1. Finish all builds and render jobs first. Do not benchmark beside agents,
   browsers under load, Marp, PDF builds, or other benchmark runs.
2. Inspect the demo's documented commands and `cv-experiment.sh`. Record
   hardware, OS, Go version, Docker configuration, and environment checks.
3. Run the environment check. If it warns about load, stop and wait for a
   quiet machine. Do not bypass the check to obtain a number before the talk.
4. Preserve the old captures. Save fresh raw captures separately. Recalculate
   the table from those captures. Check that compared runs measure the same
   benchmark and payload. Record all relevant flags.
5. Resolve the module-path and payload changes in the same recapture. Never
   edit captured output by hand. If any Go source changes, use the Go guidance
   and run the repository verifier afterwards.
6. Compare new evidence with the existing 4.75 / 18.88 / 5.25 CV table and the
   “5.25% is not a triumph” slide. Change the interpretation when evidence
   requires it. Do not adjust evidence to preserve a punchline.

A local experiment cannot establish a universal Mac-VM floor. Separate local
measurements from the cited bare-metal experiment and state the conditions.

### 2. Agree the narrative changes

* [ ] Give Kemal a one-sentence message and a section-level beat sheet before
  moving material. Each section needs a question, answer, transition, and budget.
* [ ] Preserve the current structure unless Kemal approves a replacement:
  WHY and stakes, OPERA and the three questions, local/micro, CI/macro, recap.
  Keep the unresolved #4891 plant and payoff, the #643 mirror incident, and
  the common lesson: a benchmark moved that could not have moved.
* [ ] Check the opening for a clear promise within two minutes. Check that
  the local-to-CI transition explains why a local result is insufficient.
  Close by answering the opening promise with the 3×2 recap.
* [ ] Check the current cut ladder against slides that still exist. Remove
  stale timing language from the outline and TODO. Preserve the never-cut list
  unless Kemal explicitly changes it.
* [ ] Review “Three tools” and “Take it with you”. Propose a short practical
  action and clear resource links. Do not copy the other talk's SIG call,
  Go-team asks, agent joke, injector teaser, or roadmap.

Output: an approved change list. If the order stays unchanged, record that
choice. Do not add a fixed-order test while the narrative remains editable.

### 3. Tighten the script, then adapt presenter notes

* [ ] Shorten SAY blocks to spoken sentences with one idea each. Put delivery
  instructions in DO. Keep each number, caveat, attribution, and callback.
  Apply `de-slop`, then `humanizer`, while preserving STE rules.
* [ ] Shorten repeated explanation in the outline, ledger, and TODO. Preserve
  sources, versions, uncertainty, and “do not say” limits. Delete closed TODO
  items. Keep only decisions that prevent repeated mistakes in its Done section.
* [ ] Adapt the benchmark script to the existing per-slide note format.
  Prefer that migration over a last-minute parser rewrite. Preserve useful
  section budgets and reserve answers outside generated slide entries.
  Map repeated titles, reveal pairs, bare images, and split headings explicitly.
  Preserve the comma in “Measure customer happiness,”.
* [ ] Generate notes with the explicit talk override. Inspect alignment output.
  Do not edit generated comments directly. Every content slide needs a script
  entry. Include the title, dividers, and image beats where presenter guidance helps.
* [ ] Check both talks after the migration. Decide whether to extend the default
  Makefile check to both talks. Until then, run both explicit commands below.
* [ ] Test several notes in Marp presenter view, including the longest entry.
  Check scrolling and readability on the actual presenter display. Retain the
  standalone script as a fallback.

```bash
make sync/notes NOTES_TALK=talks/go-benchmarks-lying
make check/notes NOTES_TALK=talks/go-benchmarks-lying
make check/notes NOTES_TALK=talks/without-a-single-line
```

Acceptance: every generated entry belongs to its intended slide, with zero
alignment problems. On a temporary copy, change one SAY line and prove that
`--check` fails. Regenerate the real candidate and prove that both talks pass.
Do not weaken the checker to accept unmapped slides.

### 4. Reduce reading and clicks, then inspect visuals

* [ ] Review each of the 45 reveal bullets. Keep progressive disclosure only
  when it builds a prediction, contrast, or argument. Convert reference lists
  to HTML `<ul>`, never `-` bullets. Update the fragment floor to the intentional
  new count. Record the retained reveals by title.
* [ ] Review dense pages first. Current candidates are `benchenv`,
  `Benchmark + pprof`, “Reading compiler output”, the SMT and DFS pages,
  “Why a baseline, not a pair”, and “Three questions, two scales”.
  These are text-density candidates, not proven render defects.
* [ ] Give each slide one claim and one piece of evidence. Put explanatory
  prose in SAY. Keep code, captured output, chart labels, and citations legible.
  Do not rewrite captured output to shorten a panel.
* [ ] Preserve the three existing memes. Check their setup, pause, and payoff.
  A new meme requires a clear narrative purpose, local media, and a timing cost.
  Put talk assets in `talks/go-benchmarks-lying/assets/`, not `slides/assets/`.
* [ ] Reuse the current theme. Inspect chart contrast, screenshot crops, captions,
  table width, code clipping, yellow footer contrast, and section-title fit.
  Use the existing `fullscreen` treatment only for an intentional image-only slide.
* [ ] Render the PDF. Inspect a whole-deck contact sheet, then open changed or
  dense pages at readable size. Check that no image or footer disappears.

When a slide title or content changes, update its script entry and regenerate
notes before the next check. Do not leave generated notes behind the source.

Output: an inspected deck, not only a successful build. Avoid asset cleanup,
new diagram infrastructure, or shared-theme redesign before this delivery.

### 5. Add delivery cues and prove offline use

* [ ] After the content stabilizes, add the established footer cues where useful:
  `▸` speak freely, `◆` checkpoint, `∙` pause, `◦` slow down. Put the legend
  in the script. Do not add em dashes as a second cue channel.
* [ ] Match checkpoint cues to real section splits. Do not copy the first
  talk's checkpoint times. Image-only slides can remain free of footer cues.
* [ ] Regenerate notes after the final content edits. Build the HTML, PDF,
  and offline HTML. Check both note targets explicitly. Run the full
  repository verifier on the final integrated candidate.
* [ ] Serve the offline HTML with the network disabled. Test the presenter
  view, clicker, reveals, fonts, local images, GIFs if used, and notes.
  Confirm that rendering needs no remote resource. Audience hyperlinks can
  remain online. Keep the PDF and standalone script available locally.

```bash
make sync/notes NOTES_TALK=talks/go-benchmarks-lying
make check/fast
make check
make check/notes NOTES_TALK=talks/go-benchmarks-lying
make check/notes NOTES_TALK=talks/without-a-single-line
make build/offline/go-benchmarks-lying
python3 tools/check_slide_footer.py talks/go-benchmarks-lying/slides/presentation.pdf
# Find each changed page by title, then substitute its current PDF page number.
pdftoppm -f N -l N -r 60 -png talks/go-benchmarks-lying/slides/presentation.pdf /tmp/benchmark-page
```

`make check` already builds both HTML decks and PDFs and runs the diagram,
footer, Go, and static checks. The extra footer command makes the target
artifact explicit. The offline target inlines Kroki images only. It does not
prove that every possible remote asset works offline.

### 6. Measure, cut if needed, and freeze

* [ ] Kemal delivers one full timed read with the final deck and notes. Record
  cumulative time at each divider. Preserve the 38-minute content target and
  7-minute Q&A unless the delivery contract changes.
* [ ] If content exceeds 38 minutes, use the approved cut ladder. Update deck,
  script, and outline together. Repeat affected checks and time the new cut.
  Never compensate by skipping caveats or speaking faster.
* [ ] Rehearse the opening, both incident payoffs, the scale transition, the
  closing line, and at least one live cut. Confirm that cues and click count help.
* [ ] Record the candidate commit, checks, visual inspection, measured splits,
  unresolved limits, and exact local presentation file in the talk's TODO or
  local evidence record. Kemal reviews the rendered candidate and approves
  publication payloads separately.
* [ ] Freeze content. Retain only fixes for false claims, broken rendering,
  missing notes, or delivery failure. Do not start asset cleanup or new features.

## Acceptance checks

| Check | Input | Expected result | Location |
| --- | --- | --- | --- |
| Factual coverage | Final visible and spoken claims | Source or capture for each claim. No unsupported slide claim. Versions and disclosure limits remain explicit. | Local audit with public primary sources |
| CV evidence | Quiet-run captures and environment record | Reproducible table, or an owner-approved fallback that makes no unsupported floor claim. | Quiet measurement machine |
| Tool evidence | Binaries from a recorded benchlab commit | Used panels match raw output. Ledger row 25 records the check. | Local |
| Narrative | Approved beat sheet and headline sequence | Three questions work at both scales. Both incidents resolve. Close answers the opening. | Owner review |
| Script alignment | Both decks and scripts | Zero alignment problems. A changed temporary script makes the check fail. | Local |
| Reveals | Final deck and declared floor | Only deliberate reveals remain. No `-` list markers appear in the deck. | Local and HTML preview |
| Visuals | Final PDF and images of changed pages | Readable evidence, no clipping, no footer collision, no missing images. | Local visual review |
| Repository checks | Exact integrated candidate | `make check/fast` and `make check` exit 0. Both explicit notes checks pass. | Local |
| Offline presentation | Final offline HTML and actual presenter setup | Notes, reveals, fonts, and media work without the network. | Presenter machine |
| Timing | Full out-loud run with the candidate | Content finishes within the agreed budget. Recorded section splits replace estimates. | Human rehearsal |

No acceptance check above is complete merely because this plan exists.

## If time becomes short

Do these first: resolve unsupported claims, verify the current candidate,
prepare the offline fallback, and measure delivery time. Simplify the opening,
transitions, and close before cosmetic changes. Keep the separate script if
presenter-note migration cannot finish safely.

Defer new memes, new diagrams, parser redesign, asset deletion, broad research
rewrites, blog work, Scott's pending PDF, and podcast promotion. Never defer a
false claim or conceal a failed check. Do not run the CV experiment under load.

## History evidence

Method: searched recent local history, then inspected original Pi user turns
and assistant outcomes. Compared those records with landed commits and the
current files at `d3deb90`. Reviewed nine main sessions and nine related child
sessions, including one interrupted fact-edit attempt. `ctx` returned no
matches, so retrieval used `recall` and the original Pi records. No transcript
paths or internal research content are included here.

All identifiers below refer to Pi. Events identify the relevant source turns.
Historical check results apply to their historical candidates only.

| Ref | Session ID | Events | Evidence and landed changes |
| --- | --- | --- | --- |
| H1 | `01a1983c-eef5-7023-8a65-f5cc10a21192` | `27ca89c9`, `fa0e9eb5`, `580c456f`, `fb6a3e51` | Release and code audit, human review, public-only Vale scope. `e5a6698`, `a3e4b3b`, `38b8957`. |
| H2 | `01a1985c-ac28-766d-b599-212a2c8235e4` | `8711dafe`, `b03e64c6` | Lighter close, second-talk plug, integrated checks. `185a689`. |
| H3 | `01a1985e-54c4-74ad-82ab-18521bbbb71f` | `b9b71361`, `e297a4a4`, `f17339d6`, `2ca74ade`, `3c02eca3` | Public fact audit, source checks and experiments, scope control, concise helper docs, offline build. `f7629e6`, `86a1f6c`, `bd59815`, `f707f93`. |
| H4 | `01a19ae6-1c68-73d5-a6a9-968a9b9b8eb9` | `db7fbd3c`, `faa10545`, `8ac32bc7`, `d8aedf00`, `61d4a888` | Alternatives before structural edits, approved lifecycle, preserve punctuation, avoid rigid order tests. `0f8f4ef`. |
| H5 | `01a19b30-4169-7299-9129-aa90a88d5a33` | `63918d32`, `12508122`, `6798d021`, `d8d989ed`, `fce8d962`, `9bf684f9` | Weekend Language audit, content before cues, fewer reveals, native presenter notes, footer cues. `706ca07`, `d30b441`, `bbd8160`, `b2c430b`. |
| H6 | `01a19b86-80db-7644-93e9-093bee6db328` | `ebf1937f`, `0d4e3887`, `7a572c66`, `eebed3c6` | Meme candidates, rendered review, image sizing. `4c29966`, `dba46e8`. Later `791c16a` removed the Poe meme. |
| H7 | `01a19bab-9529-733b-89d9-3924b3f7db73` | `5d0e12fd`, `fa2c6b79`, `6cdcab35`, `c187c4f5` | Preserve GoLab identity, inspect all slides, fix diagram application, recheck integrated content, inspect footer defects. `6d8aa54`, `9d86bbd`, `1119592`. |
| H8 | `01a19c59-0113-74d1-bda6-57d18d2c9fa4` | `e6a4f666` | Put a source link beside the relevant material. `0809084`. The otelc link itself is talk-specific. |
| H9 | `01a19c88-cba3-733b-89d9-3926cb1f6b80` | `7930c6d0`, `3d39d0dc` | Final screenshot and footer review. Explicit image-only treatment. `0cb7a46`. |

## Planning verification

Checked the original local draft at `d3deb90` on 2 November:

* Passed: all nine cited session IDs and their event IDs exist in the original
  Pi records. All 21 cited change commits are ancestors of the snapshot.
* Passed: execution input paths exist. Git ignores the original draft under
  `plans/`. The tracked tree was clean at that check. The plan contains
  36 open execution tasks.
* Passed: `make check/notes NOTES_TALK=talks/without-a-single-line` exits 0.
* Expected failure: `make check/notes NOTES_TALK=talks/go-benchmarks-lying`
  exits 2 and reports 105 missing script entries. The tool also prints
  “presenter notes match the script” because it recognizes no entries. That
  line alone does not mean that the check passes.
* Not run during the history analysis: full builds, slide checks, fresh
  public-source checks, CV measurements, offline presenter tests, and timed
  rehearsal. No deck or tool changed.

## Planning completion

* [x] Inspect recent Pi history and check landed changes.
* [x] Separate reusable passes, inherited fixes, and talk-specific decisions.
* [x] Compare the benchmark deck, script, outline, TODO, ledger, and build support.
* [x] Save an ordered plan with acceptance checks and evidence references.

Preparation begins at execution step 0. No preparation checkbox is complete yet.
