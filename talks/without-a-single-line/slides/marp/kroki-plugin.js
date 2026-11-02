const { deflateSync } = require('zlib')

const krokiLangs = [
  'actdiag',
  'blockdiag',
  'bpmn',
  'bytefield',
  'c4plantuml',
  'ditaa',
  'dot',
  'erd',
  'excalidraw',
  'graphviz',
  'mermaid',
  'nomnoml',
  'nwdiag',
  'packetdiag',
  'pikchr',
  'plantuml',
  'rackdiag',
  'seqdiag',
  'svgbob',
  'umlet',
  'vega',
  'vegalite',
  'wavedrom',
]

const entrypoint = 'https://kroki.io/'

// Kroki draws the diagram on its own server and returns an image. The slide
// theme cannot style the inside of that image, so colour and type must travel
// with the diagram source. A Mermaid init directive does that. The values are
// the GoLab tokens: white nodes, deep-teal structure, graphite edges, a yellow
// note, and a violet activation. Mermaid rejects a multi-name fontFamily, so
// the stack goes through themeCSS, where a machine without Rubik falls back to
// Arial rather than to a serif.
const golabMermaid = {
  theme: 'base',
  themeVariables: {
    primaryColor: '#ffffff',
    primaryBorderColor: '#006459',
    primaryTextColor: '#101010',
    secondaryColor: '#eafcfa',
    secondaryBorderColor: '#006459',
    secondaryTextColor: '#101010',
    tertiaryColor: '#f5f5f5',
    tertiaryBorderColor: '#006459',
    tertiaryTextColor: '#101010',
    lineColor: '#454545',
    textColor: '#101010',
    clusterBkg: '#eafcfa',
    clusterBorder: '#006459',
    edgeLabelBackground: '#f5f5f5',
    noteBkgColor: '#f8fc61',
    noteTextColor: '#101010',
    noteBorderColor: '#006459',
    actorBkg: '#ffffff',
    actorBorder: '#006459',
    actorTextColor: '#101010',
    signalColor: '#454545',
    signalTextColor: '#101010',
    labelBoxBkgColor: '#eafcfa',
    labelBoxBorderColor: '#006459',
    labelTextColor: '#101010',
    activationBkgColor: '#e4cbff',
    activationBorderColor: '#6200ce',
  },
  themeCSS:
    '#container, #container text, #container tspan, #container foreignObject div, #container foreignObject span { font-family: Rubik, "Helvetica Neue", Arial, sans-serif !important; }',
}

const initDirective = `%%{init: ${JSON.stringify(golabMermaid)}}%%\n`

// A diagram that already sets its own directive keeps it.
const hasInit = (content) => /^\s*%%\{/.test(content)

const withGolabTheme = (lang, content) =>
  lang === 'mermaid' && !hasInit(content) ? initDirective + content : content

const marpKrokiPlugin = (md) => {
  const { fence } = md.renderer.rules

  md.renderer.rules.fence = (tokens, idx, options, env, self) => {
    const info = md.utils.unescapeAll(tokens[idx].info).trim()

    if (info) {
      const [lang] = info.split(/(\s+)/g)

      if (krokiLangs.includes(lang)) {
        const source = withGolabTheme(lang, tokens[idx].content)
        const data = deflateSync(source).toString('base64url')

        // <marp-auto-scaling> is working only with Marp Core v3
        return `<p><marp-auto-scaling data-downscale-only><img src="${entrypoint}${lang}/svg/${data}"/></marp-auto-scaling></p>`
      }
    }

    return fence.call(self, tokens, idx, options, env, self)
  }
}

module.exports = marpKrokiPlugin
