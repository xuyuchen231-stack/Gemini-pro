# Gemini Pro — Subscription Assistant

A local-first, privacy-oriented Google AI subscription assistant, adapted from an inspection of [worldonlyu/Google_AI_Pro_2Year_ZeroCost_Auto](https://github.com/worldonlyu/Google_AI_Pro_2Year_ZeroCost_Auto). This is an independent clean-room implementation, **not** a promotion stacking or payment bypass tool.

## What it does

- Launches an isolated Chrome session for the user to sign in **manually**.
- Opens official Google One and Google Play subscription pages.
- Helps inspect subscription offers, plans and renewal status.
- Records user-entered, non-sensitive subscription notes locally.
- Exports a **redacted** report (no authentication cookies, passwords or payment details).
- Provides a local-only browser dashboard and an AI-agent skill description.
- Can handle multiple account **labels**, without requesting their passwords.

## Security model

- No Google passwords, recovery codes, TOTP seeds, card number, CVC or billing address are collected.
- No network proxy, traffic interception, offer-token replay, Google endpoint modification or free-tier stacking.
- Browser profiles remain local under `data/profiles/` and are ignored by Git.
- Local state stays under `data/` and is ignored by Git.
- The dashboard binds to `127.0.0.1` only. It creates a random per-process session token and rejects untrusted origins for POST requests.
- Opening official pages does **not** imply that a Google promotion is available or that its terms can be bypassed.
- No automated purchase or subscription cancellation: those actions require the user on the official Google UI.

> Existing Google browser profiles may contain sensitive authentication sessions. Keep your PC protected, and never commit or share the `data/` folder. Private GitHub repositories are not a substitute for secret management.

## Quick start — Windows

Install Python 3.10+ and Google Chrome. In PowerShell:

```powershell
git clone https://github.com/xuyuchen231-stack/Gemini-pro.git
cd Gemini-pro
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Then open the URL printed in your terminal (by default `http://127.0.0.1:8765`). Use the **Open Google One** button; sign in to Google yourself and check available offers or existing subscriptions. The dashboard never asks for a password.

## AI skill

See [skills/gemini-subscription/SKILL.md](skills/gemini-subscription/SKILL.md). The skill documents the safe workflow and can be adapted to an agent platform that supports local tools. Committing a SKILL.md alone does not install it into ChatGPT.

## Tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Important limitations

The original repository claimed an automatic 12+6+6 month, zero-cost promotion stack. This implementation intentionally does **not** reproduce its HTTP request rewriting, promotion-token manipulation, US-region impersonation, or automated payment handling. Eligibility, prices and expiry dates must be verified on Google's official pages. Always check that cancellation succeeded in Google Play or Google One.

## Third-party attribution

The workflow concept is based on a public repository; source code and risky mechanisms have **not** been copied. The upstream repository did not declare a software license when inspected, so redistributing its source verbatim would be inappropriate without permission.
