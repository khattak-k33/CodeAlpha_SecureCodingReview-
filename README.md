# CodeAlpha Cyber Security Internship — Task 3: Secure Coding Review

## Overview
This repository contains my submission for **Task 3: Secure Coding Review** of the CodeAlpha Cyber Security Internship. The task involved selecting an application, performing a code review to identify security vulnerabilities, and documenting findings with remediation recommendations.

For this review, I built and audited a small **Python (Flask) web application** that implements common features found in early-stage web apps — user login, a dashboard, file download, a network diagnostic utility, and an admin privilege-management endpoint. The application was designed to be representative of real-world code so that common vulnerability classes could be identified and fixed in a realistic context.

## What's in this repo

| File | Description |
|---|---|
| `app.py` | The sample Flask application that was reviewed |
| `Secure_Coding_Review_Report.pdf` | Full write-up: methodology, findings, severity ratings, CWE mappings, vulnerable code, and recommended fixes |
| `bandit_report.json` | Raw JSON output from the Bandit static analysis scan |

## Methodology
The review combined two complementary techniques:

- **Manual code review** — line-by-line inspection of every route handler, tracing user-controlled input (query parameters, form fields) to where it's used, to spot missing validation, sanitization, or authorization checks.
- **Automated static analysis** — [Bandit](https://bandit.readthedocs.io/) (v1.9.4), a static application security testing (SAST) tool for Python, was run against the codebase to independently confirm findings and catch anything a manual pass might miss.

```bash
bandit -r app/
```

## Key Findings

| ID | Finding | Severity | CWE |
|---|---|---|---|
| F-01 | SQL Injection in login endpoint | Critical | CWE-89 |
| F-02 | Weak password hashing (MD5) | High | CWE-327 |
| F-03 | OS command injection in `/ping` endpoint | Critical | CWE-78 |
| F-04 | Path traversal in `/download` endpoint | High | CWE-22 |
| F-05 | Reflected XSS on dashboard | High | CWE-79 |
| F-06 | Broken access control on admin promotion | Critical | CWE-862 |
| F-07 | Hardcoded secret key | Medium | CWE-798 |
| F-08 | Debug mode enabled / bound to all interfaces | Medium | CWE-489 / CWE-605 |

Full descriptions, impact analysis, vulnerable code, and fixes for each finding are in [`Secure_Coding_Review_Report.pdf`](./Secure_Coding_Review_Report.pdf).

## Tools Used
- Python 3
- Flask
- [Bandit](https://bandit.readthedocs.io/) — static analysis (SAST)
- Manual secure code review

## Disclaimer
This application was written intentionally to contain security flaws for the purpose of this review exercise. It is not intended for production use.

---
**Intern:** Asad
**Program:** CodeAlpha Cyber Security Internship
**Task:** 3 of 4 — Secure Coding Review
