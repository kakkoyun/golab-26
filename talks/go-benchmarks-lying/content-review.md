# Benchmark talk content review

Reviewed against `9923dfa` on 3 November 2026. This revision has 88 slides.
Slide numbers below include dividers. Sources: [deck](slides/presentation.md),
[script](speaker-notes.md), [outline](outline.md), and
[claims ledger](../../research/go-benchmarks-lying/claims-ledger.md).

This review uses Weekend Language and covers content that affects the argument,
audience decisions, or delivery time. It excludes layout, typography, and cue
polish. The deck and script remain unchanged.

## Keep the stronger evidence from recent changes

The two personal incidents, OPERA, and the false-positive ledger carry the
argument. Keep them. Keep the DODO lesson: validate the benchmark against
production, then freeze it before optimization.

The expanded #643 story now shows both outcomes. On CI, `largeidle` and `multi`
stay below their ceilings. The separate `baseline` scenario exceeds its ceiling
twice. PR #650 then raises that ceiling to 550% with an explicit decision
(ledger row 53). Preserve this distinction. The story must not suggest that
all the failures disappeared on a better machine.

## 1. Bring the incident forward and establish a usable time budget

High priority. Weekend Language: organize the narrative and reduce slide load.

The first personal incident starts on slide 9. The preceding script contains
533 spoken words, about four minutes at the outline's 130 words per minute,
before pauses. The three promised questions arrive on slide 19.

The current script contains about 4,196 SAY words, about 32 minutes at that
rate before pauses and visual explanations. The timing notes still say about
3,000 words. Section 01 has a 3:00 checkpoint, but the preceding 758 words
already need about 5.8 minutes. These estimates do not establish the actual
runtime. They show that the current checkpoints cannot guide delivery.

Open with the bot comment and "Would you fix it?" Give Datadog's stake briefly,
then state the three questions. If the general speed introduction stays, reduce
it to a short statement of the customer impact.

Time the resulting script with the deck. If it exceeds 42 minutes, cut the
standalone talk recommendations, algorithm list, and internal CLI feature tour
before cutting the incidents or their results. Keep source links with the
relevant evidence. Do not add more delivery cues to compensate for excess content.

## 2. Present the 16 ns result as an increase

High priority. Weekend Language: preserve technical accuracy.

Slide 12, "The benchmark that matters", says "~16 ns per push and pop".
The script calls this the cost. The screenshot and ledger row 52 show a change
from 236 ns to 252 ns per push/pop cycle. The 16 ns is the increase.

Show the before and after values. Say: "16 ns added per push/pop cycle. No new
allocations in this benchmark." This preserves the distinction between the
changed path and the unrelated benchmark that the bot flagged.

## 3. Keep the statistical lesson useful without claiming certainty

High priority. Weekend Language: simplify the explanation without changing the facts.

Slide 38 says that `~` means "no" difference. Slide 49 says that a change smaller
than the observed spread is invisible. Its script calls that spread the best
this laptop can achieve. These statements can lead the audience to dismiss
real changes.

Use "No statistically significant difference detected" for `benchstat`.
Describe 5.25% as the spread observed in that local run. It does not establish
a hard detection limit or the laptop's best possible result.

More samples can help distinguish a small change from random noise. More samples
do not correct systematic bias or an uncontrolled change in conditions. The
[benchstat documentation](https://pkg.go.dev/golang.org/x/perf/cmd/benchstat)
explains both the meaning of `~` and the benefit of reducing noise or increasing
sample size. Preserve the warning against repeated runs until a preferred
answer appears.

The same precision matters on slide 64, "A/B is the wrong model for CI".
The later PR gate correctly uses same-machine A/B. Say "A/B alone misses
long-term drift" and explain why comparisons and history serve different needs.

## 4. Make the incident conclusions match the evidence

High priority. Weekend Language: keep the story's lesson accurate.

The repeated line "a benchmark moved that could not have moved" conflicts with
the code-layout explanation. Unchanged source can run differently after the
binary layout changes. Opposite results on two machines do not, by themselves,
prove which result represents production.

Use "A benchmark moved when I expected no change." In the #4891 story, separate
the observed local speedup from the explanation of code layout. Describe the
investigation that supports the explanation. Do not make a sign reversal alone
the proof that CI is wrong.

For #643, retain the new CI result and the budget decision. A control benchmark
helps question a measurement. It does not establish that every reported
regression is false. The useful audience action is to investigate the measurement
before changing code, then decide what to do about a confirmed cost.

## Message and next action

If performance matters to your users, invest in measurements that check the
work, the sample, and the machine.

End with one first action: on the next performance PR, check that the benchmark
measures the changed path, then run a controlled comparison. Keep the full
checklist in the repository.

No explicit story placeholders remain. Actual delivery time and the current
rendered layout remain unverified by this content review.
