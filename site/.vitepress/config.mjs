import { defineConfig } from 'vitepress'

const GH = 'https://github.com/siner308/ai-roots'

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
  title: 'ai-roots',
  description: 'Thinking foundations, situational skills, and agents for Claude Code.',
  base: '/ai-roots/',
  lastUpdated: true,
  cleanUrls: false,
  ignoreDeadLinks: true,
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
