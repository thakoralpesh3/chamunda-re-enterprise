---
name: cloudflare-security-audit
description: >-
  Audits the cybersecurity posture of this host machine, active edge tunnels, GitHub cloud repositories,
  and all autonomous agents (present and future) against Cloudflare Zero Trust, OWASP, and Edge WAF
  security standards. Detects insecure network origin bindings, exposed ports, leaked secrets,
  missing pre-push hooks, unauthenticated endpoints, and generates automated defensive mitigations and hardening solutions.
---

# Cloudflare Security Audit & Zero Trust Defensive Guide

This skill equips Antigravity and autonomous agents with Cloudflare-standard cybersecurity auditing, vulnerability assessment, and defensive threat remediation for **GitHub Repositories, the Host Laptop, and the Multi-Agent Ecosystem**.

---

## 1. Cloudflare Zero Trust Security Principles

Every agent, host process, and cloud repository must adhere to four foundational tenets:

1. **Origin Cloaking (No Open Inbound WAN Ports)**:
   - Services should never bind to raw `0.0.0.0` with ports exposed directly to the public internet without an authentication layer.
   - External internet access MUST route strictly through encrypted, outbound-only Cloudflare Tunnels (`cloudflared`) or Zero Trust Access Policies.
2. **Defensive Edge Hardening & HTTP Response Headers**:
   - All web servers and agent APIs must return defensive security headers:
     - `X-Content-Type-Options: nosniff` (Prevents MIME sniffing attacks)
     - `X-Frame-Options: SAMEORIGIN` (Mitigates Clickjacking)
     - `Referrer-Policy: strict-origin-when-cross-origin`
     - `Content-Security-Policy: default-src 'self' ...`
3. **Continuous Secret Scanning & Git Pre-Push Interception**:
   - Codebases and git histories must have zero unredacted API tokens, secret keys, or authentication cookies.
   - All Git repositories MUST have active client-side `.git/hooks/pre-push` hooks to block credentials before they can ever reach public GitHub.
4. **Supply Chain & CI/CD Least Privilege**:
   - Every repository must have `.github/dependabot.yml` configured for automated package vulnerability patching.
   - GitHub Actions workflows must specify `permissions: contents: read` to prevent unconstrained token privileges.

---

## 2. Security Assessment Vectors

The audit evaluates six distinct cybersecurity domains:

| Domain | Cloudflare Standard | Evaluation Metric |
| :--- | :--- | :--- |
| **Origin Binding** | Strict Loopback / Authenticated Tunnel | Services must bind to `127.0.0.1` or LAN subnet; zero unauthorized WAN port exposures. |
| **Edge Tunneling** | TLS 1.3 / HTTP/2 Encrypted Cloudflared | Outbound tunnel health, connection protocol, rate-limit avoidance, and origin DNS resolution. |
| **GitHub Cloud Posture** | Pre-Push Protection & Dependabot | Active `.git/hooks/pre-push` secret interceptors, sanitized remote URLs, and Dependabot supply chain monitoring. |
| **CI/CD Workflow Hardening** | Least-Privilege Action Permissions | Workflows must enforce `permissions: contents: read` without unpinned third-party risks. |
| **SAST & Secret Leaks** | Zero Token Exposure | Automated scanning for AWS, Gemini, OpenAI, Stripe, and private SSH/cryptographic keys. |
| **Host Integrity** | Anti-Hacker Sentry & Heuristic Watcher | Detection of rogue executables in `/tmp` or `/dev/shm`, reverse shell listeners, and CPU/RAM exhaustion. |
| **Future Agent Defense** | Dynamic Auto-Discovery & Zero-Day Scrutiny | Any newly created agent directory is automatically detected, registered, and scanned before public exposure. |

---

## 3. Autonomous Commands & Tools

- **Run Full System & GitHub Audit**:
  ```bash
  aradhya-audit
  ```
- **Apply Automated Defensive Fixes (Laptop, GitHub & Agents)**:
  ```bash
  aradhya-audit --fix
  ```
  *(Installs pre-push hooks in all repos, deploys dependabot.yml, hardens .gitignore, and injects workflow permissions)*
- **Output Machine-Readable Telemetry**:
  ```bash
  aradhya-audit --json
  ```
- **Live Mobile Endpoints**:
  ```text
  GET  /api/security/audit
  POST /api/security/remediate
  ```
