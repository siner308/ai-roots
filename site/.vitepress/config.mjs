import { defineConfig } from 'vitepress'
import { readFileSync, readdirSync, statSync } from 'node:fs'
import { join, resolve } from 'node:path'

const REPO_ROOT = resolve(import.meta.dirname, '..', '..')

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

// Page basenames that actually exist on disk, so the sidebar can never silently
// drop a newly added rule/skill/agent/hook. `rules`/`agents`/`hooks` are flat
// .md dirs (leading `_` stripped to match sync-content.mjs); `skills` is one
// dir per skill holding SKILL.md.
function discover(kind) {
  const dir = join(REPO_ROOT, kind)
  if (kind === 'skills') {
    return readdirSync(dir)
      .filter((n) => {
        try {
          return statSync(join(dir, n, 'SKILL.md')).isFile()
        } catch {
          return false
        }
      })
      .sort()
  }
  return readdirSync(dir)
    .filter((f) => f.endsWith('.md'))
    .map((f) => f.slice(0, -3).replace(/^_/, ''))
    .sort()
}

const DISK_RULES = discover('rules')
const DISK_SKILLS = discover('skills')

// Curated grouping/ordering. Anything on disk but absent here still appears —
// rules fall into an auto "Uncategorized" group, skills append after the
// curated order — so the only cost of forgetting to register a page is that it
// lands at the bottom, never that it vanishes. A build-time warning flags it.
// [English group title, Korean group title, [rule file basenames]]
const RULE_GROUPS = [
  ['Thinking Expansion', '사고 확장', ['thinking-expansion']],
  ['Quality Assurance', '품질 보증', ['evaluation-integrity', 'claude-architect-principles', 'verify-each-instance']],
  ['User Growth', '사용자 성장', ['user-growth-coaching']],
  ['Knowledge Capture', '지식 포착', ['guardrail-maker', 'memory-minimalism']],
  ['Output Conventions', '출력 규약', ['prose-style', 'terminology-discipline', 'comment-discipline']],
  ['Trigger Index', '트리거 인덱스', ['situational-skills']],
]

const SKILL_ORDER = [
  'css-discipline', 'github-pr-markdown', 'model-effort-delegation',
  'parallel-execution-modes', 'parallel-hypothesis-investigation', 'codex-delegation',
  'incremental-verification', 'simulate-dont-just-scan', 'codex-tmux-monitoring',
  'background-task-monitoring', 'web-research', 'web-fetch-block-then-search', 'review',
]

// curated order first, then any disk skill not yet listed (alphabetical)
const SKILLS = [
  ...SKILL_ORDER.filter((n) => DISK_SKILLS.includes(n)),
  ...DISK_SKILLS.filter((n) => !SKILL_ORDER.includes(n)),
]

const GROUPED_RULES = new Set(RULE_GROUPS.flatMap(([, , items]) => items))
const UNGROUPED_RULES = DISK_RULES.filter((n) => !GROUPED_RULES.has(n))
const ORPHAN_SKILLS = SKILLS.filter((n) => !SKILL_ORDER.includes(n))

if (UNGROUPED_RULES.length || ORPHAN_SKILLS.length) {
  console.warn(
    `[sidebar] unregistered pages (shown at bottom): ` +
      `rules=[${UNGROUPED_RULES.join(', ')}] skills=[${ORPHAN_SKILLS.join(', ')}]`,
  )
}

const AGENTS = discover('agents')

const HOOKS = discover('hooks')

function sidebar(ko) {
  const base = ko ? '/ko' : ''
  const groups = RULE_GROUPS.map(([en, kr, items]) => ({
    text: ko ? kr : en,
    collapsed: false,
    items: items.map((n) => ({ text: n, link: `${base}/rules/${n}` })),
  }))
  if (UNGROUPED_RULES.length) {
    groups.push({
      text: ko ? '미분류' : 'Uncategorized',
      collapsed: false,
      items: UNGROUPED_RULES.map((n) => ({ text: n, link: `${base}/rules/${n}` })),
    })
  }
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
    {
      text: ko ? 'Hooks — 강제' : 'Hooks — enforcement',
      collapsed: false,
      items: HOOKS.map((n) => ({ text: n, link: `${base}/hooks/${n}` })),
    },
  ]
}

function nav(ko) {
  const base = ko ? '/ko' : ''
  return [
    { text: 'Rules', link: `${base}/rules/thinking-expansion`, activeMatch: `${base}/rules/` },
    { text: 'Skills', link: `${base}/skills/css-discipline`, activeMatch: `${base}/skills/` },
    { text: 'Agents', link: `${base}/agents/adversarial-reviewer`, activeMatch: `${base}/agents/` },
    { text: 'Hooks', link: `${base}/hooks/comment-discipline`, activeMatch: `${base}/hooks/` },
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
