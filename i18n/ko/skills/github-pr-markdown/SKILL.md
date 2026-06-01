---
name: github-pr-markdown
description: "pull request 본문이나 제목을 만들거나 수정할 때(gh pr create, gh pr edit, gh api PR 업데이트), 또는 PR 설명을 작성할 때 — 다른 스킬이나 워크플로가 PR 설명을 만들어내는 경우도 포함 — 적용한다. GitHub-flavored Markdown을 강제한다: ASCII 대시 불릿, task-list 체크박스, 백틱 코드 참조, 필수 Summary/Test plan 섹션, 그리고 gh CLI 마크다운 손상을 피하는 안전한 API-PATCH 본문 전달."
---


  # GitHub PR Markdown Convention                                                 
                                                                                  
  CRITICAL: PR을 만들거나 수정할 때(gh pr create, gh pr edit, PR 본문            
  작성), 유효한 GitHub-flavored Markdown을 만들어야 한다. 깨진 마크다운          
  (망가진 체크박스, 벗겨진 백틱, 맨 URL)은 제출을 막는 결함이다 — 제출          
  전에 고친다.                                                                   
                                                                                  
  ## Rules                                                                        
                                                                                  
  ### Structure                                                                   
                                                                                  
  • PR 제목은 70자 미만. 자세한 건 본문에                                         
  • 섹션은 ## 사용 (PR 제목이 H1이므로 본문에서 #은 절대 쓰지 않음)             
  • 섹션 사이에는 빈 줄 하나                                                     
                                                                                  
  ### Formatting — STRICT                                                        
                                                                                  
  • 불릿: 항상 -  (ASCII 대시 + 공백) 사용. •, ·, * 같은 유니코드 불릿은 절대   
  쓰지 않음                                                                       
  • Task list: 항상 - [ ] / - [x] (대시 + 공백 + 대괄호) 사용. -  접두사 없는   
  맨 [ ]는 체크박스로 렌더되지 않음                                              
  • 코드 참조: 항상 백틱으로 감쌈 (`componentName`, `fileName.ts`).             
  백틱이 셸 이스케이프를 견뎌야 함 — 최종 출력에서 확인                          
  • Markdown으로 충분하면 raw HTML 쓰지 않음                                     
  • 표는 GFM table 문법(파이프 + 정렬) 사용                                      
                                                                                  
  ### Links and References — STRICT                                              
                                                                                  
  • 이슈/PR 참조는 owner/repo#123 또는 #123                                       
  • URL: 항상 [text](url) 형식. 맨 URL 금지                                       
  • 이미지는 ![alt text](url), alt text는 설명적으로                              
                                                                                  
  ### Required PR Body Sections                                                   
                                                                                  
    ## Summary                                                                    
    - bullet point 1                                                              
    - bullet point 2                                                              
                                                                                  
    ## Test plan                                                                  
    - [ ] Verification item 1                                                     
    - [ ] Verification item 2                                                     
                                                                                  
  • ## Summary와 ## Test plan 섹션은 필수                                         
  • ## Breaking changes나 ## Notes 같은 추가 섹션은 필요하면 넣어도 됨           
                                                                                  
  ### Body Delivery — STRICT                                                     
                                                                                  
  gh CLI는 모든 본문 전달 방식에서 마크다운을 손상시킨다(--body, --body-file, gh 
  pr                                                                              
  edit --body-file): 대시가 •로, 백틱이 벗겨지고, - [ ]가 [ ]로 바뀐다.          
  **PR 본문을 절대 **gh** CLI로 넘기지 않는다. 항상 GitHub API를 직접 쓴다.**    
                                                                                  
  안전한 방법 — 빈 본문으로 PR을 만들고 API로 PATCH:                            
                                                                                  
    # 1. Create PR with empty body                                                
    gh pr create --title "the pr title" --body "" --draft                         
                                                                                  
    # 2. Write body payload with Python (preserves exact bytes)                   
    python3 -c "                                                                  
    import json                                                                   
    body = '''## Summary                                                          
                                                                                  
    - First bullet with \x60code ref\x60                                          
                                                                                  
    ## Test plan                                                                  
                                                                                  
    - [ ] Verification item                                                       
    '''                                                                           
    with open('/tmp/pr-payload.json', 'w', encoding='utf-8') as f:                
        json.dump({'body': body}, f, ensure_ascii=False)                          
    "                                                                             
                                                                                  
    # 3. PATCH via GitHub API                                                     
    curl -s -X PATCH \                                                            
      -H "Authorization: token $(gh auth token)" \                                
      -H "Content-Type: application/json; charset=utf-8" \                        
      -d @/tmp/pr-payload.json \                                                  
      https://api.github.com/repos/OWNER/REPO/pulls/NUMBER                        
                                                                                  
  수정할 때는 업데이트된 본문으로 2-3단계를 다시 쓴다.                           
                                                                                  
  Notes:                                                                          
                                                                                  
  • Python 문자열에서는 셸 해석을 피하려고 백틱 대신 \x60을 쓴다                 
  • **비-ASCII 문자를 바이트 이스케이프로 인코딩하지 않는다** (예: \xec\x97\x90).
  유니코드 텍스트를 그대로 쓴다                                                  
                                                                                  
  ### Pre-submit Verification                                                     
                                                                                  
  PR을 만들거나 수정한 뒤, API로 raw 본문을 확인한다:                            
                                                                                  
    gh pr view NUMBER --json body --jq .body | head -10                           
                                                                                  
  확인 항목:                                                                      
                                                                                  
  1. -  불릿이 ASCII 대시인지 (•가 아닌지)                                       
  2. - [ ] 체크박스에 -  접두사가 있는지                                          
  3. 코드 참조 둘레에 백틱 ` 가 있는지                                            
                                                                                  
  하나라도 실패하면, payload를 다시 쓰고 위처럼 API로 PATCH 한다.                
