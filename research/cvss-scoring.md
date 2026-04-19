# iOS Vulnerability CVSS Scoring

How to evaluate iOS security vulnerabilities using CVSS 3.1.

---

## Quick scoring examples

### CVE-2019-8900 (checkm8)
- **Attack Vector:** Local (physical access required)
- **Attack Complexity:** Low (USB + prepared packets)
- **Privileges Required:** None
- **User Interaction:** None
- **Scope:** Changed (bootrom → kernel)
- **CIA Impact:** High on all three
- **CVSS:** 9.8 CRITICAL

### CVE-2022-22587 (IOMobileFrameBuffer, iOS 15.1)
- **Attack Vector:** Local (app → kernel)
- **Attack Complexity:** Low
- **Privileges Required:** Low (app can run)
- **Scope:** Changed
- **CIA:** High
- **CVSS:** 8.8 HIGH

### CVE-2023-28206 (IOSurfaceAccelerator)
- **CVSS:** 8.1 HIGH
- Used in jailbreaks for post-exploit sandbox escape

---

## Scoring formula (simplified)

```
Base Score = min(9.9, 8.6 * (AV + AC + PR + UI + S + C + I + A))
AV: Local=0.85, Adjacent=0.62, Network=1.0
AC: Low=0.77, High=0.44
PR: None=0.85, Low=0.62, High=0.27
UI: None=0.85, Required=0.62
S: Unchanged=0.0, Changed=1.0
```

Full specification: https://nvlpubs.nist.gov/vuln/detail/CVE-xxxx-xxxxx
