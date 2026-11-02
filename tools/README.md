# Tools

The tooling built for these talks now lives in its own MIT-licensed
repositories.

## Benchmark toolkit

[`github.com/kakkoyun/benchlab`](https://github.com/kakkoyun/benchlab) provides
`honestbench`, `benchgate`, `benchenv`, and three benchmark Agent Skills.

```bash
go install github.com/kakkoyun/benchlab/cmd/...@latest
npx skills add kakkoyun/benchlab --all
```

## Zero-touch observability toolkit

[`github.com/kakkoyun/zeroins`](https://github.com/kakkoyun/zeroins) provides
`obi-integration`, `otelc-aspect`, `kubectl-obi`, `kubectl-profiler`, and the
`collect-go-telemetry` Agent Skill.

```bash
go install github.com/kakkoyun/zeroins/cmd/...@latest
npx skills add kakkoyun/zeroins --all
```

The Kubernetes commands are experimental privileged wrappers. They require an
explicit telemetry endpoint and confirmation of the target context, namespace,
transport, and privilege impact before use.

## Repository checks

The slide-specific checks remain here:

- `check_slide_footer.py` catches content that overlaps the footer band.
- `check_code_headers.py` verifies source labels on code panels.
- `check_slide_fragments.py` protects progressive-reveal markers.
- `sync_presenter_notes.py` copies the SAY/DO script into the deck as presenter
  notes. With `--check`, it fails when they drift.
- `check_diagrams.py` fetches each Kroki diagram URL and fails when the service
  does not answer. Marp renders the diagrams over the network, so without this
  check a flaky connection leaves a broken image on a slide and the build still
  reports success.

`make check` runs them against both decks.

The GoLab footer check reserves 70 PDF points at the bottom of each slide.
The theme places the yellow footer band in that area.
