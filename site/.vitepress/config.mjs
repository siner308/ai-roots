import { defineConfig } from 'vitepress'
import { readFileSync } from 'node:fs'
import { join } from 'node:path'

const GH = 'https://github.com/siner308/ai-roots'
const SITE = 'https://siner308.github.io/ai-roots/'
const OG_IMAGE = `${SITE}og-image.png`
const SITE_TITLE = 'ai-roots'
const SITE_DESC = 'Thinking foundations, situational skills, and agents for Claude Code.'

// First prose paragraph of a source markdown file, flattened to plain text for
// use as og:description. Skips frontmatter, headings, blockquotes, list markers,
// and tables; strips inline markdown so search/social cards show clean text.
function firstParagraph(srcDir, relativePath) {
  let raw
  try {
    raw = readFileSync(join(srcDir, relativePath), 'utf8')
  } catch {
    return ''
  }
  raw = raw.replace(/^---\n[\s\S]*?\n---\n/, '')
  const lines = []
  for (const line of raw.split('\n')) {
    const t = line.trim()
    if (!t) {
      if (lines.length) break
      continue
    }
    if (/^(#{1,6}\s|>|\||[-*+]\s|\d+\.\s)/.test(t)) {
      if (lines.length) break
      continue
    }
    lines.push(t)
  }
  return lines
    .join(' ')
    .replace(/`([^`]*)`/g, '$1')
    .replace(/\*\*([^*]+)\*\*/g, '$1')
    .replace(/\*([^*]+)\*/g, '$1')
    .replace(/\[([^\]]+)\]\([^)]*\)/g, '$1')
    .replace(/\s+/g, ' ')
    .trim()
}

const truncate = (s) => (s.length > 200 ? `${s.slice(0, 197).trimEnd()}…` : s)

// [English group title, Korean group title, [rule file basenames]]
const RULE_GROUPS = [
  ['Thinking Expansion', '사고 확장', ['concept-priming', 'progressive-deepening', 'capability-overhang']],
  ['Quality Assurance', '품질 보증', ['evaluation-integrity', 'claude-architect-principles']],
  ['User Growth', '사용자 성장', ['user-growth-coaching']],
  ['Knowledge Capture', '지식 포착', ['guardrail-maker', 'memory-minimalism']],
  ['Output Conventions', '출력 규약', ['plain-language-output', 'terminology-discipline', 'comment-discipline']],
  ['Trigger Index', '트리거 인덱스', ['situational-skills']],
]

const SKILLS = [
  'css-discipline', 'github-pr-markdown', 'model-effort-delegation',
  'parallel-execution-modes', 'parallel-hypothesis-investigation', 'codex-delegation',
  'incremental-verification', 'simulate-dont-just-scan', 'codex-tmux-monitoring',
  'background-task-monitoring', 'review',
]

const AGENTS = ['adversarial-reviewer']

function sidebar(ko) {
  const base = ko ? '/ko' : ''
  const groups = RULE_GROUPS.map(([en, kr, items]) => ({
    text: ko ? kr : en,
    collapsed: false,
    items: items.map((n) => ({ text: n, link: `${base}/rules/${n}` })),
  }))
  return [
    ...groups,
    {
      text: ko ? 'Skills — 상황별' : 'Skills — situational',
      collapsed: false,
      items: SKILLS.map((n) => ({ text: n, link: `${base}/skills/${n}` })),
    },
    {
      text: 'Agents',
      collapsed: false,
      items: AGENTS.map((n) => ({ text: n, link: `${base}/agents/${n}` })),
    },
  ]
}

function nav(ko) {
  const base = ko ? '/ko' : ''
  return [
    { text: 'Rules', link: `${base}/rules/concept-priming`, activeMatch: `${base}/rules/` },
    { text: 'Skills', link: `${base}/skills/css-discipline`, activeMatch: `${base}/skills/` },
    { text: 'Agents', link: `${base}/agents/adversarial-reviewer`, activeMatch: `${base}/agents/` },
  ]
}

export default defineConfig({
  title: SITE_TITLE,
  description: SITE_DESC,
  base: '/ai-roots/',
  lastUpdated: true,
  cleanUrls: false,
  ignoreDeadLinks: true,
  head: [
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:site_name', content: SITE_TITLE }],
    ['meta', { property: 'og:image', content: OG_IMAGE }],
    ['meta', { name: 'twitter:card', content: 'summary_large_image' }],
    ['meta', { name: 'twitter:image', content: OG_IMAGE }],
  ],
  transformPageData(pageData, { siteConfig }) {
    const desc = pageData.description || firstParagraph(siteConfig.srcDir, pageData.relativePath) || SITE_DESC
    pageData.description = truncate(desc)
  },
  transformHead({ pageData }) {
    const title = pageData.title ? `${pageData.title} | ${SITE_TITLE}` : SITE_TITLE
    const description = pageData.description || SITE_DESC
    const path = pageData.relativePath
      .replace(/(^|\/)index\.md$/, '$1')
      .replace(/\.md$/, '.html')
    const url = SITE + path
    const locale = pageData.relativePath.startsWith('ko/') ? 'ko_KR' : 'en_US'
    return [
      ['meta', { property: 'og:title', content: title }],
      ['meta', { property: 'og:description', content: description }],
      ['meta', { property: 'og:url', content: url }],
      ['meta', { property: 'og:locale', content: locale }],
      ['meta', { name: 'twitter:title', content: title }],
      ['meta', { name: 'twitter:description', content: description }],
    ]
  },
  themeConfig: {
    search: { provider: 'local' },
    socialLinks: [{ icon: 'github', link: GH }],
  },
  locales: {
    root: {
      label: 'English',
      lang: 'en',
      themeConfig: {
        nav: nav(false),
        sidebar: sidebar(false),
        editLink: {
          pattern: `${GH}/edit/main/:path`,
          text: 'Edit the source on GitHub',
        },
      },
    },
    ko: {
      label: '한국어',
      lang: 'ko',
      link: '/ko/',
      themeConfig: {
        nav: nav(true),
        sidebar: sidebar(true),
        outline: { label: '이 페이지', level: [2, 3] },
        docFooter: { prev: '이전', next: '다음' },
        lastUpdatedText: '마지막 수정',
        darkModeSwitchLabel: '다크 모드',
        returnToTopLabel: '맨 위로',
        sidebarMenuLabel: '메뉴',
        langMenuLabel: '언어 변경',
      },
    },
  },
})
