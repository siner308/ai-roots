---
name: model-effort-delegation
description: "Apply when deciding which executor (main session vs subagent vs team), which model (Fable/Opus/Sonnet/Haiku), and what effort level fits a task — i.e. before delegating non-trivial work. Covers strict downgrade conditions (plan precision + verification loop), escalation triggers, blast-radius override, and the subagent briefing standard."
---


  # Model, Effort, and Subagent Delegation                                        
                                                                                  
  For every task, deliberately choose the **executor** (main session vs subagent),
  **model** (Fable / Opus / Sonnet / Haiku), and **effort level**. Concentrate expensive      
  models on architectural judgment; delegate well-specified implementation to     
  cheaper models.                                                                 
                                                                                  
  ## Principle                                                                    
                                                                                  
  Keep the main session on Opus — for planning, review, conversation, and        
  localized edits. Delegate large, independent work to Sonnet/Haiku subagents.    
  **The more specific the plan, the better weaker models preserve quality** — so 
  the prerequisite for delegation is a precise plan. One tier above Opus, **Fable 5** is the most capable model available — reserve it for exceptional reasoning the everyday Opus tier cannot crack (see Top tier below), not routine work.                              
                                                                                  
  ## Executor Selection                                                           
                                                                                  
  For executor topology (main session / subagent / team) and the inline-vs-       
  subagent                                                                        
  threshold, see parallel-execution-modes.md. This rule covers the orthogonal     
  choice                                                                          
  of *which model* runs in the chosen executor.                                   
                                                                                  
  **Per-executor application.** The rule applies per executor, not per session. In
  a team, the team lead plays the same role as main Opus (planning, coordination, 
  review); each teammate is selected by task type using the table below; downgrade
  conditions and escalation triggers apply to each teammate independently.        
                                                                                  
  ## Model Selection                                                              
                                                                                  
  Task                              │Model │Rationale                             
  ──────────────────────────────────┼──────┼──────────────────────────────────────
  Architecture design, migration pl…│Opus  │Trade-off judgment, ripple prediction 
  PR/code review, root-cause debugg…│Opus  │Hypothesis-falsification, tail cases …
  Plan-driven feature implementation│Sonnet│Clear spec narrows judgment space     
  Verifiable refactoring            │Sonnet│Transformation rules are clear, tests…
  Test writing                      │Sonnet│Repetitive patterns, framework conven…
  Bulk exploration, grep summaries  │Haiku…│Path + summary is enough              
  Format conversion, comment adds, …│Haiku │Mechanical work                       
  Log inspection, status checks     │Haiku │Read-only, no judgment                
                                                                                  
  ### Top tier — Fable 5 (most demanding work)

  **Fable 5** (`claude-fable-5`; Agent tool selector `model: "fable"`) is Anthropic's most capable widely released model — one tier above Opus 4.8 — for the most demanding reasoning and long-horizon agentic work. Adaptive thinking is always on; 1M-token context.

  Reach for it only when the everyday Opus tier is genuinely insufficient:

  - **Exceptionally hard reasoning** — architecture or root-cause debugging where Opus has stalled on the reasoning itself, not where the spec was merely unclear.
  - **Long-horizon agentic work** that must hold a very large context coherently and whose blast radius justifies the top model.

  **Not the default.** Fable 5 costs roughly 2× Opus 4.8 ($10 / $50 vs $5 / $25 per MTok, input / output), so Opus stays the ceiling for everyday architectural work and you escalate to Fable 5 deliberately, for the exceptional case.

  ### Downgrade Conditions — STRICT                                              
                                                                                  
  To downgrade to Sonnet/Haiku, BOTH must be true:                                
                                                                                  
  1. The plan specifies file paths, function signatures, and verification method  
  2. A **verification loop exists** — tests, type checker, lint, or similar      
                                                                                  
  If either is missing, keep Opus. Downgrading without a verification loop        
  produces silent quality regressions (see evaluation-integrity).                 
                                                                                  
  ## Effort Selection                                                             
                                                                                  
  Orthogonal to model choice. Tune thinking budget to task risk.                  
                                                                                  
  Effort     │When to use                                                         
  ───────────┼────────────────────────────────────────────────────────────────────
  **high**   │Hard-to-reverse operations (DDL, production config, force-push), ar…
  **medium** │Standard feature implementation, review, multi-layer refactoring    
  **low / of…│Single-file edits, mechanical transforms, tasks where verification …
                                                                                  
  **Blast radius overrides effort.** A task that looks small but is hard to       
  reverse stays at high + Opus.                                                   
                                                                                  
  ## Escalation Triggers                                                          
                                                                                  
  If any signal appears during subagent execution, **escalate to Opus**:          
                                                                                  
  • Same mistake repeated 3+ times                                               
  • Situation requiring a **design decision** not covered by the plan            
  • Failure rooted in **code comprehension gaps**, not spec ambiguity            
  • Verification loop fails repeatedly with unclear cause                        
                                                                                  
  Escalation is part of the rule, not a failure. Stubbornly pushing a weak model  
  leads to hysteresis — the wrong direction gets locked in. The ladder has one rung above Opus: when Opus itself stalls on genuinely hard reasoning (not spec ambiguity), escalate to **Fable 5** — reserved for that exceptional case, given its cost.                      
                                                                                  
  ## Cross-Provider Delegation (Codex)                                            
                                                                                  
  If Codex CLI is available on PATH, see the codex-delegation skill for mode       
  selection, three-turn rescue protocol, security-sensitive review triggers       
  (/review), capability routing, execution mechanics, and plan-stage review. Codex
  delegation is orthogonal to the in-platform model tiers above — those
  model tiers still apply to Claude-side work.                                    
                                                                                  
  ## Subagent Briefing Standard                                                   
                                                                                  
  When delegating to a weaker executor, the briefing MUST include:                
                                                                                  
  • **File paths** and edit scope (explicit starting points)                     
  • **Function signatures** or pseudocode                                        
  • **Existing code patterns** to follow (reference file + pattern)              
  • **Verification method** — which test or command determines success          
  • **Edge cases** and explicit out-of-scope items                               
  • Request the subagent report **reasoning behind decisions** (for later        
  traceability)                                                                   
                                                                                  
  If the briefing would be thin, inline Opus is cheaper in practice.              
                                                                                  
  ## Examples                                                                     
                                                                                  
  ### Threshold-based delegation                                                  
                                                                                  
    Request: "Add avatar upload to the user profile page"                         
    1. Main Opus: explore existing upload patterns inline (~2 min)                
    2. Main Opus: write plan — file paths, API endpoint, component structure,    
  verification                                                                    
    3. Sonnet subagent: implement (independent, ~15 min)                          
    4. Main Opus: review the result                                               
                                                                                  
  ### Inline handling                                                             
                                                                                  
    Request: "Add a nil check to the function you just looked at"                 
    → Main Opus edits inline. Briefing cost exceeds the work.                    
                                                                                  
  ### Parallel delegation                                                         
                                                                                  
    Request: "Add the same endpoint pattern to 5 microservices"                   
    → Spawn 5 Sonnet subagents in parallel. Main does plan + review only.        
                                                                                  
  ### Over-delegation (bad)                                                       
                                                                                  
    Request: "Fix a typo in README"                                               
    Wrong: Haiku subagent — spawn overhead is 10× the work                      
    Right: Inline edit                                                            
                                                                                  
  ### Under-delegation (bad)                                                      
                                                                                  
    Request: "Audit the whole codebase for deprecated API usage"                  
    Wrong: Main Opus runs repeated greps — main context gets polluted            
    Right: Delegate to Haiku Explore agent                                        
                                                                                  
  ## Rule Summary                                                                 
                                                                                  
  • Main session stays on Opus — focus on planning, review, conversation,       
  localized edits                                                                 
  • **Fable 5** is the ceiling above Opus — reserve it for exceptional reasoning or long-horizon agentic work Opus cannot crack; ~2× Opus cost, so never the default
  • Delegate to a subagent when: ≥5 min + independent + verifiable              
  • Downgrade only when BOTH plan precision and a verification loop exist        
  • Never downgrade model or effort when blast radius is high                    
  • Escalate to Opus after 3 failures or when a design decision surfaces; escalate Opus → Fable 5 only when Opus itself stalls on genuinely hard reasoning         
  • Briefings must include file paths, signatures, verification, and a request for
  decision reasoning                                                              
  • If Codex CLI is available, see the codex-delegation skill for cross-provider  
  rules (three-turn cap, adversarial review via /review, capability routing, plan-
  stage review).                                                                  
  • **Project CLAUDE.md can strengthen these defaults** — e.g., per-PR two-     
  reviewer rule. Project rules override the minimum where they are stricter; the  
  minimum applies where the project is silent.                                    

