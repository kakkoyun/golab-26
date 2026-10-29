# golab-26

Talks for GoLab 2026, the international conference on Go in Italy, held
November 1st to 3rd, 2026. Each talk has an outline, a spoken script, a deck,
and a list of open work.

## Talks

| Talk | Slot | Room | Link | Deck |
| --- | --- | --- | --- | --- |
| How to instrument Go without changing a single line of code | November 2nd, 2026, 15:30. 45 minutes. | Golab #1 | [golab.io](https://golab.io/talks/how-to-instrument-go-without-changing-a-single-line-of-code) | `talks/without-a-single-line/slides/presentation.md` |
| Why Your Go Benchmarks Are Lying (And How to Stop Them) | November 3rd, 2026, 10:45. 45 minutes. | Golab #2 | [golab.io](https://golab.io/talks/why-your-go-benchmarks-are-lying-and-how-to-stop-them) | `talks/go-benchmarks-lying/slides/presentation.md` |

Both talks plan for 38 minutes presented and 7 minutes of Q&A.

## Quick start

Install the Node.js dependencies once:

```sh
npm install
```

Run the checks and builds through `make`:

```sh
make help                  # list all targets
make check/fast            # fast checks while you edit
make check                 # full checks before you finish
make build/pdf/<talk>      # build the PDF handout for one talk
make watch/<talk>          # rebuild one talk on change
```

Replace `<talk>` with the talk directory name, for example
`without-a-single-line` or `go-benchmarks-lying`.

## Reference

- `themes/golab/README.md` describes the Marp theme that the decks use.
- `AGENTS.md` describes the conventions for writing and editing the talks.

## Creative MCP tools

The project-level `.mcp.json` gives Claude Code a small media toolkit for
writing and designing talks.

| Server | Use |
| --- | --- |
| `meme` | Search meme templates and create captioned images |
| `giphy` | Search rated GIFs and stickers |
| `readwise` | Search highlights and Reader documents |
| `fal` | Find generative-media models and run them when requested |
| `pexels` | Search stock photos and videos |
| `pixabay` | Search stock photos, illustrations, vectors, and videos |

The credential-backed servers require Node.js 20 or newer and the 1Password
CLI. Their API keys remain as `op://` references and are resolved only when each
server starts. Clones outside the author's 1Password account must replace those
references and the `--account` value.

Claude Code asks for approval before starting project MCP servers. Run `claude`,
open `/mcp`, approve the servers, and authenticate Readwise. `claude mcp list`
shows their connection status.

Download selected media into `talks/<talk>/assets/` instead of depending on
remote URLs. Keep the provider attribution with the asset. Animated GIFs work in
HTML decks, but PDF exports capture a static frame.

fal model execution can incur charges. Check pricing before running a model.
