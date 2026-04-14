# ai-roots

[한국어](README.ko.md) | **English**

A collection of thinking foundations and lessons learned that expand Claude Code's capabilities.

Even non-experts can solve complex problems through casual conversation — Claude automatically applies architect-grade reasoning.

## Roots — Thinking Foundations

### Thinking Expansion
| File | Description |
|------|-------------|
| `roots/az-mindset.md` | A-Z token priming + complexity-based thinking expansion (Devil's Advocate, First Principles, Systems Thinking) |
| `roots/progressive-deepening.md` | Internal quality gate that detects shallow answers and automatically digs one level deeper |
| `roots/capability-overhang.md` | Unlock hidden knowledge — domain token injection, cross-domain connections, skill composition |

### Quality Assurance
| File | Description |
|------|-------------|
| `roots/evaluation-integrity.md` | Self-evaluation bias prevention — verifiability classification, generation/evaluation separation, drift detection |
| `roots/claude-architect-principles.md` | Auto-apply architect-grade problem solving — enforcement matching, context discipline, generation/review separation |

### Problem-Solving Strategy
| File | Description |
|------|-------------|
| `roots/parallel-hypothesis-investigation.md` | Decompose complex problems into layered hypotheses and investigate with parallel agents simultaneously |
| `roots/parallel-execution-modes.md` | Choose between sequential, subagent, and team-based parallelism based on task independence and communication needs |

### User Growth
| File | Description |
|------|-------------|
| `roots/user-growth-coaching.md` | Post-solve coaching to improve user's question patterns — nudge vague requests toward specific ones |

### Knowledge Capture
| File | Description |
|------|-------------|
| `roots/guardrail-maker.md` | Auto-detect user corrections as tacit knowledge and propose persistent guardrails to prevent recurring mistakes |

### Conventions
| File | Description |
|------|-------------|
| `roots/github-pr-markdown.md` | Enforce GitHub-flavored Markdown conventions for PRs |

## Lessons — Retrospective Learnings

Lessons are concrete patterns learned from real mistakes. They describe what works better, not what to avoid.

| File | Description |
|------|-------------|
| `lessons/incremental-verification.md` | Break uncertain work into smallest verifiable steps — inline test first, script later, scale gradually |

## Installation

```bash
git clone https://github.com/siner308/ai-roots.git
cd ai-roots
chmod +x install.sh
./install.sh
```

The entire `ai-roots` directory is symlinked into `~/.claude/rules/ai-roots`. Claude Code recursively loads all `.md` files from both `roots/` and `lessons/`.

## Inspiration

- [AI Frontier EP82](https://aifrontier.kr/ko/episodes/ep82) — A-Z Token Priming, Domain Token Injection, Skill Composition
- [AI Frontier EP87](https://aifrontier.kr/ko/episodes/ep87) — March of Nines
- [AI Frontier EP89](https://aifrontier.kr/ko/episodes/ep89) — Click vs Clunk, Problem Definition > Problem Solving
- [AI Frontier EP91](https://aifrontier.kr/ko/episodes/ep91) — Capability Overhang
- [AI Frontier EP92](https://aifrontier.kr/ko/episodes/ep92/) — Close the Loop, Verifiable vs Non-verifiable
- [Anthropic Harness Design](https://www.anthropic.com/engineering/harness-design-long-running-apps) — Generator/Evaluator Separation, Self-evaluation Bias
- [CCAF Exam Guide](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F8lsy243ftffjjy1cx9lm3o2bw%2Fpublic%2F1773274827%2FClaude+Certified+Architect+%E2%80%93+Foundations+Certification+Exam+Guide.pdf) — Agentic Architecture, Tool Design, Context Management
- [CCAF 101 Study Notes](https://bitboom.github.io/ccaf101/) — CCAF Korean Study Notes
