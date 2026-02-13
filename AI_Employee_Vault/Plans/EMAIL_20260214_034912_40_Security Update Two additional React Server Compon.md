---
title: "Email Processing Request: Security Update: Two additional React Server Components
 vulnerabilities"
created: 2026-02-14T03:49:12.113353
email_uid: "40"
email_from: "ship@info.vercel.com"
email_to: "('syedshurii22@gmail.com',)"
email_date: "Fri, 12 Dec 2025 13:32:31 +0000 (UTC)"
status: pending
priority: medium
action_required: standard_processing
---

# Email Processing Request

## Email Information
- **Subject**: Security Update: Two additional React Server Components
 vulnerabilities
- **From**: `ship@info.vercel.com`
- **To**: `('syedshurii22@gmail.com',)`
- **Date**: Fri, 12 Dec 2025 13:32:31 +0000 (UTC)
- **Size**: 60702 bytes
- **UID**: `40`

## Email Content
Important security updates affecting React and Next﻿.js applications

‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ‍͏ ͏ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ ͏‌ ­ ­ ­ ­ 

|  |   
---  
We're informing you about two additional vulnerabilities (CVE-2025-55184 and CVE-2025-55183) identified in the React Server Components (RSC) implementation, affecting frameworks such as Next.js.   
The React2Shell incident sparked community research into React Server Components, and these vulnerabilities were discovered by an external security researcher through Vercel and Meta's bug bounty program. We're grateful for this community effort.  
There is no evidence these vulnerabilities have been exploited.  
What we've found:

  * **CVE-2025-55184 (High Severity – Denial of Service):** A malicious HTTP request sent to any App Router endpoint can, when deserialized, cause the server process to hang and consume CPU. This impacts all versions handling RSC requests. The initial fix was incomplete and did not fully prevent denial-of-service attacks for all payload types, resulting in CVE-2025-67779. 
  * **CVE-2025-55183 (Medium Severity – Source Code Exposure):** A malicious HTTP request sent t...

## Action Required
Review this email and determine appropriate action based on Company Handbook guidelines.

## Instructions
1. Review the email content above
2. Determine appropriate action based on Company Handbook rules
3. Execute the required action
4. Move this file to Done when completed
5. Update Dashboard with status

## Status
- [ ] Email reviewed
- [ ] Action determined
- [ ] Action executed
- [ ] Status updated
