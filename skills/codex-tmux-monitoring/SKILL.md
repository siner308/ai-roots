---
name: codex-tmux-monitoring
description: "Apply when tempted to monitor a long-running subprocess (especially Codex) via tmux split panes, sentinel strings, or a foreground tail/grep loop. Explains why that pattern was unreliable and that you should use run_in_background Bash plus the harness completion notification, with tee to a log for user-visible streaming."
---


  # Codex tmux Split-Pane Monitoring Was Unreliable                               
                                                                                  
  A previous version of model-effort-delegation told Claude to run every 
  /codex:* command inside a tmux split pane with a === CODEX DONE === sentinel and
  a foreground tail -f "$LOG" | grep -qm1 'CODEX DONE' to wake the main session.  
  The                                                                             
  pattern looked rigorous on paper. In practice it failed reliably.               
                                                                                  
  ## What actually happened                                                       
                                                                                  
  A /codex:review run under the typical cc tmux harness produced this state: 
                                                                                  
  • Codex finished and printed === CODEX DONE === to its pane.                   
  • The sentinel string was present in the log file when grepped after the fact. 
  • The tmux split pane stayed open (no read -p, but no clean exit instruction   
  either).                                                                        
  • Claude never noticed completion. The user had to type "it's done" to advance 
  the turn.                                                                       
                                                                                  
  So both halves of the contract were broken: the user did not get an auto-closing
  pane (manual close required), and Claude did not get a deterministic wake-up    
  despite the sentinel landing.                                                   
                                                                                  
  ## Why the wake-up failed                                                       
                                                                                  
  Claude's main turn only advances on (a) user input, or (b) completion of a      
  run_in_background: true Bash. The rule's code block did not mark tail -f | grep -
  qm1 with run_in_background: true. A line of prose elsewhere said "run this in   
  background," but the example was the only thing actually executed, and it ran in
  foreground — at which point the main session was blocked, the harness was      
  waiting, and even when the sentinel did arrive there was no event the harness   
  translated into "Claude's turn is up."                                          
                                                                                  
  Even if the foreground/background was fixed, the design conflated two           
  independent goals into one mechanism:                                           
                                                                                  
  1. Wake Claude when codex exits.                                                
  2. Show codex's reasoning live to the user.                                     
                                                                                  
  Goal 1 is solved natively by run_in_background: true Bash — the harness fires a
  completion notification when the subprocess exits. Goal 2 is solved by tee-ing  
  to                                                                              
  a log path and letting the user run their own tail -f. Forcing both through a   
  tmux + sentinel + grep wrapper added new failure modes (sentinel race with tee  
  flush, foreground-vs-background ambiguity, manual pane close) without making    
  either goal more reliable than the simpler decomposition.                       
                                                                                  
  ## What we use now                                                              
                                                                                  
  • run_in_background: true Bash with 2>&1 | tee /tmp/codex-*.log. Completion    
  notification wakes Claude. No sentinel.                                         
  • If the user wants live reasoning, Claude tells them the log path. The user   
  runs tail -f in their own terminal. Claude does not script the live view.       
  • read -p 'press enter to close' and split panes are gone entirely. The previous
  user feedback to remove read -p (recorded in a per-project memory) is now       
  subsumed by the broader pattern removal.                                        
                                                                                  
  ## Signals this lesson applies                                                  
                                                                                  
  • A long-running subprocess where Claude's turn must resume on completion.     
  • A temptation to wrap the subprocess in a wake-up sentinel that Claude itself 
  watches.                                                                        
  • A pattern that requires Claude to run a foreground tail, grep, or polling loop
  to detect completion.                                                           
                                                                                  
  In all three cases: use run_in_background: true Bash and trust the harness's    
  completion notification (Rung 1 of lessons/background-task-monitoring.md). Do   
  not                                                                             
  invent a second monitoring channel.                                             
                                                                                  
  ## Rules                                                                        
                                                                                  
  • Do not script tmux split panes from Claude's side to deliver subprocess output
  to the user. The user's own terminal already runs tmux; Claude does not need to 
  drive it.                                                                       
  • Do not write sentinel strings whose only consumer is a Claude-side grep      
  waiting on them. The completion of the background Bash is itself the            
  deterministic signal.                                                           
  • When two goals (wake Claude / show output to user) tempt you toward one      
  mechanism, decompose them. The simpler pair almost always beats the unified     
  wrapper.                                                                        

