---
name: cloudflare-security-audit
description: >-
  Audits the cybersecurity posture of this host machine, active edge tunnels, and all
  autonomous agents (present and future) against Cloudflare Zero Trust, OWASP, and Edge WAF
  security standards. Detects insecure network origin bindings, exposed ports, leaked secrets,
  unauthenticated endpoints, and generates automated defensive mitigations and hardening solutions.
---

# Cloudflare Security Audit & Zero Trust Defensive Guide

This skill equips Antigravity and autonomous agents with Cloudflare-standard cybersecurity auditing, vulnerability assessment, and defensive threat remediation.

---

## 1. Cloudflare Zero Trust Security Principles

Every agent and host process must adhere to three foundational tenets:

1. **Origin Cloaking (No Open Inbound WAN Ports)**:
   - Services should never bind to raw `0.0.0.0` with ports exposed directly to the public internet without an authentication layer.
   - External internet access MUST route strictly through encrypted, outbound-only Cloudflare Tunnels (`cloudflared`) or Zero Trust Access Policies.
2. **Defensive Edge Hardening & HTTP Response Headers**:
   - All web servers and agent APIs must return defensive security headers:
     - `X-Content-Type-Options: nosniff` (Prevents MIME sniffing attacks)
     - `X-Frame-Options: SAMEORIGIN` (Mitigates Clickjacking)
     - `Referrer-Policy: strict-origin-when-cross-origin`
     - `Content-Security-Policy: default-src 'self' ...`
3. **Continuous Secret Scanning & Sanitization**:
   - Codebases and git histories must have zero unredacted API tokens, secret keys, or authentication cookies.
   - Volatile runtime state must be quarantined in `.gitignore`.

---

## 2. Security Assessment Vectors

The audit evaluates five distinct cybersecurity domains:

| Domain | Cloudflare Standard | Evaluation Metric |
| :--- | :--- | :--- |
| **Origin Binding** | Strict Loopback / Authenticated Tunnel | Services must bind to `127.0.0.1` or LAN subnet; zero unauthorized WAN port exposures. |
| **Edge Tunneling** | TLS 1.3 / HTTP/2 Encrypted Cloudflared | Outbound tunnel health, connection protocol, rate-limit avoidance, and origin DNS resolution. |
| **SAST & Secret Leaks** | Zero Token Exposure | Automated scanning for AWS, Gemini, OpenAI, Stripe, and private SSH/cryptographic keys. |
| **Host Integrity** | Anti-Hacker Sentry & Heuristic Watcher | Detection of rogue executables in `/tmp` or `/dev/shm`, reverse shell listeners, and CPU/RAM exhaustion. |
| **Future Agent Defense** | Dynamic Auto-Discovery & Zero-Day Scrutiny | Any newly created agent directory is automatically detected, registered, and scanned before public exposure. |

---

## 3. Autonomous Commands & Tools

- **Run Full System Audit**:
  ```bash
  aradhya-audit
  ```
- **Apply Automated Defensive Fixes**:
  ```bash
  aradhya-audit --fix
  ```
- **Output Machine-Readable Telemetry**:
  ```bash
  aradhya-audit --json
  ```
- **Live Mobile Endpoint**:
  ```text
  GET /api/security/audit
  ```
