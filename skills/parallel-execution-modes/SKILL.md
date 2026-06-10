---
name: parallel-execution-modes
description: "Apply when work can be parallelized — choosing between sequential, subagents, and teams; deciding inline vs subagent; and foreground vs background execution. Use before spawning agents, or when a task fans out across three or more files or two or more independent subtasks."
---


  # Parallel Execution Modes                                                      
                                                                                  
  When work can be parallelized, there are three distinct strategies. Choose based
  on whether workers need to communicate and how independent the tasks are.       
                                                                                  
  ## The Three Modes                                                              
                                                                                  
  Mode          │When to use                 │Token …│Cross-worker communication  
  ──────────────┼────────────────────────────┼───────┼────────────────────────────
  **Sequential**│Tasks depend on each other,…│Lowest │N/A                         
  **Subagents** │Independent tasks where onl…│Medium │None (report back to main o…
  **Teams**     │Complex work where workers …│Highest│Direct messaging between te…
                                                                                  
  ## Decision Protocol                                                            
                                                                                  
  1. **Can tasks be parallelized at all?** If each step depends on the previous   
  result, use sequential.                                                         
  2. **Do workers need to talk to each other?** If yes → teams. If no → subagents.
  3. **Is the work complex enough to justify coordination overhead?** Research,   
  review, competing hypotheses, cross-layer changes → teams. Focused lookups, test
  runs, file analysis → subagents.                                               
                                                                                  
  ## Inline vs Subagent Threshold                                                 
                                                                                  
  Even when only one worker is needed, the choice between handling work inline    
  (main session) and delegating to a subagent matters.                            
                                                                                  
  **Delegate to a subagent when ANY hold:**                                       
                                                                                  
  • Expected duration ≥ 5 minutes AND result can be summarized briefly          
  • Independent — no mid-execution user input or main-context reference needed  
  • Two or more parallelizable tasks → spawn concurrently                       
  • Verbose output (bulk grep, long logs, hundreds of files) would pollute main  
  context                                                                         
  • Long-running work suitable for background — builds, test suites, pipelines  
                                                                                  
  **Keep inline:**                                                                
                                                                                  
  • 1–2 file localized edits                                                    
  • Follow-up edits on a file just read (no re-exploration needed)               
  • Interactive work requiring ongoing user dialogue                             
  • Tasks needing mid-stream judgment or producing long streaming output         
  • Briefing cost would exceed the work itself                                   
                                                                                  
  For model selection (Fable/Opus/Sonnet/Haiku) within the chosen executor, see model-  
  effort-delegation.md.                                                           
                                                                                  
  ## Responsiveness Default                                                       
                                                                                  
  Two independent axes, applied in order:                                         
                                                                                  
  1. Inline vs subagent (threshold above). Cost of getting this wrong = context   
  duplication / spawn overhead. Short, localized tasks stay INLINE — a foreground
  subagent would duplicate context too, so "foreground" is never the fix for a    
  short task; "inline" is.                                                        
  2. Foreground vs background — decided ONLY for work already sent to a subagent.
  Cost of getting this wrong = the main session is blocked. Prefer                
  run_in_background: true so the main session stays free to take new user         
  requests while the subagent runs.                                               
                                                                                  
  ### Fan-out as a duration proxy                                                 
                                                                                  
  Estimating wall-clock up front is unreliable; observable fan-out is a better    
  trigger.                                                                        
  A task that spans **≥3 files** or **≥2 independent sub-tasks** is a long-task 
  candidate — default it to a backgrounded (and, if the items are independent,   
  concurrent) subagent.                                                           
                                                                                  
  Guard against count alone (Goodhart): it is count × per-item cost, not count.  
  Three one-line edits, three trivial renames, three files read for a single      
  answer                                                                          
  —                                                                              
  all stay inline. The proxy fires only when each item carries non-trivial work.  
                                                                                  
  • After dispatching in background, return control: continue unrelated work or  
  await the user.                                                                 
  • React to the completion event (Rung 1 of lessons/background-task-monitoring. 
  md),                                                                            
  then optionally chain follow-up subagents — the main session orchestrates, it  
  does not block.                                                                 
                                                                                  
  ## Subagents (Agent tool)                                                       
                                                                                  
  Spawn via the Agent tool. Each subagent runs in its own context window and      
  returns a single result to the caller. Workers are invisible to each other.     
                                                                                  
  Best for:                                                                       
                                                                                  
  • Researching independent questions in parallel                                
  • Delegating isolated implementation tasks                                     
  • Protecting main context from verbose tool output                             
                                                                                  
  ## Teams (TeamCreate tool)                                                      
                                                                                  
  Requires CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 in settings. Teammates share a  
  task list, message each other directly, and self-coordinate without the lead's  
  involvement.                                                                    
                                                                                  
  Best for:                                                                       
                                                                                  
  • Debugging with competing hypotheses (teammates actively disprove each other) 
  • Cross-layer work: frontend + backend + tests each owned by a different       
  teammate                                                                        
  • Code review with distinct lenses (security, performance, test coverage)      
  running simultaneously                                                          
  • Open-ended research where findings in one lane should influence another      
                                                                                  
  Practical limits:                                                               
                                                                                  
  • Start with 3–5 teammates; coordination overhead grows faster than throughput
  beyond that                                                                     
  • Aim for 5–6 tasks per teammate — small enough to check in, large enough to be
  self-contained                                                                  
  • Each teammate has its own context window; token cost scales linearly with team
  size                                                                            
  • Teammates do not inherit the lead's conversation history — include all task-
  specific context in the spawn prompt                                            
                                                                                  
  ## Rules                                                                        
                                                                                  
  • Default to subagents for parallelism unless workers need to cross-communicate
  or debate findings.                                                             
  • Default to sequential when there are only 1-2 obvious things to check —     
  parallelism has overhead.                                                       
  • When spawning teams, give each teammate a distinct, non-overlapping scope to 
  prevent file conflicts and redundant work.                                      
  • Teams are experimental and do not support session resumption for in-process  
  teammates.                                                                      
  • Never use teams as a substitute for clear task decomposition — a well-scoped
  subagent beats a poorly-briefed teammate.                                       

