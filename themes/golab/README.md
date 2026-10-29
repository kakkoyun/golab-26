# GoLab theme

Use `golab.css` for the GoLab 2026 slides. The theme uses the GoLab 2026 speaker template as its visual source.
The theme includes Rubik and JetBrains Mono fonts. It does not load fonts
from the network.

```text
golab.css      Marp theme
deck.md        layout samples
preview.html   HTML sample
fonts/         Rubik and JetBrains Mono
assets/        GoLab template art and sample images
```

Run `make check/theme` to render the sample. Run `make check` to check both
talk decks. The build copies `fonts/` and `assets/` beside each deck.

## Colour rule

The source template uses yellow `#F8FC61`, pink `#FF009A`, violet `#7800FF`,
teal `#13E4D1`, and light grey `#F5F5F5`. These values come from the template
images and slide XML. The theme uses the following text colours on light slides:

| Role | Colour | Use |
| --- | --- | --- |
| Structure | deep teal `#006459` | Source rails and links |
| Reading | deep violet `#6200CE` | Measurements and output rails |
| Caution | deep pink `#B00060` | Warnings about code that must not ship |

The text shades give at least 4.5:1 contrast on the light background. The
code panel has a white background and a dark syntax palette. The template
accents can fill a slide. White text uses the violet background. Dark text
uses the other accent backgrounds. The yellow footer always uses dark text.

## Layouts

Set a layout with `<!-- _class: section -->` before the slide content.
The class names and Markdown structure match the earlier theme.

| Class | Content |
| --- | --- |
| none | Heading, paragraph, table, or code panel on light grey |
| `title` | `#####` kicker, `#` title, `###` name, paragraph for role |
| `section` | `######` short number, `#` title, optional paragraph |
| `stat` | Large number in `#`, explanation in a paragraph |
| `compare` | `#` title, `######` delta, two blockquotes |
| `terminal` | `#` title and a shell code fence |
| `chart` | `#` title and a `.bars` chart |
| `meme` | Full-slide image and one caption paragraph |
| `emoji` | List with emoji in place of markers |
| `end` | `#` title, optional `.qr` image, links or list |
| `agenda` | Numbered list with the current item in bold |
| `speaker` | Image, name, role, and a list |
| `photo` | Full-slide image, kicker, title, and text |
| `punchline` | Centred heading with optional emphasis |
| `dark` | Violet background and white text |
| `vcenter` | Vertically centred content |

Add `yellow`, `pink`, `violet`, `teal`, or `light` to a class to change its
background. The title defaults to yellow. The section uses a grey left panel
and a teal right panel. The end and punchline layouts default to violet.
The other layouts default to light grey.

The title and end layouts also accept `gopher-hero`, `gopher-rocket`,
`gopher-network`, `gopher-sage`, `gopher-hiking`, `gopher-balloon`, and
`gopher-none`. The default title uses the template hamster gopher. The rocket
and balloon modifiers use the template cocktail gopher. The hero, sage, and network modifiers use the template hamster gopher.
The hiking modifier uses a CC0 gopher. The speaker layout uses the template
tree gopher.

## Markdown contract

A `######` heading is a utility slot. It is a number on a section slide.
It is the delta label on a compare slide. Place it before a code fence to
make a filename tab. Put the source file name in the tab. Put the source of
captured output in the tab when you have it.

The code fence language selects its rail:

| Language | Rail | Prompt |
| --- | --- | --- |
| `go`, `yaml`, `yml`, `s` | structure | none |
| `asm`, `bash`, `sh`, `shell`, `zsh`, `console` | reading | shell prompt for bare commands |
| `text` after a tab | reading | prompt in the tab |
| `text` without a tab | none | none |

Use `.chip.note` for structure, `.chip.measure` for a reading, and
`.chip.caution` for a warning. A `.cols` or `.columns` block makes two
columns. Use `.wide-left` or `.wide-right` with `.cols` to set their widths.
Use `.card` and `.card.measure` for panels. Use `.bars` for a chart and `.qr`
for a code image. List items have a hanging indent for emoji.

A `*` list makes progressive-reveal fragments in the bespoke HTML. Inactive
items have 18% opacity. The PDF shows the full list. Keep `*` as the only
list marker in a talk deck. The theme hides the Marp `header:` text. Pagination
stays visible in the yellow footer band.

## Licences

Rubik and JetBrains Mono use the SIL Open Font License. The Rubik licence
is in `fonts/OFL-Rubik.txt`. The gopher art credit is in
`assets/ATTRIBUTION.md`. The SVG gophers use CC0. The GoLab template supplies
the other art. Contact the conference before you reuse its art elsewhere.
