---
name: gemini-subscription-assistant
description: Help a user safely inspect, record and manage Google One / Google AI Pro subscriptions using Google's official webpages and a local privacy-first dashboard.
---

# Gemini Subscription Assistant

## Scope

Support legitimate subscription management, eligibility checks, expiry-date reminders and local note-taking. Never make claims of universal promotional eligibility. This skill is a workflow specification, not a privileged Google API client.

## Procedure

1. Ask the user to run the local dashboard following the repository README.
2. Have the user open Google's official Google One offers page via the dashboard and **sign in themselves**.
3. Help interpret the offer's exact eligibility terms, costs, renewal amount and dates.
4. Help the user record their subscription plan/date in local notes (no account passwords).
5. For cancellations, direct the user to Google Play subscriptions or the original Google subscription billing surface; ask them to confirm the cancellation status on the official page.
6. Explain that Google AI Pro subscription features are separate from Gemini API quota and API billing.

## Hard boundaries

- Do not ask for or save Google passwords, recovery codes, cookies, TOTP seeds, bank card numbers, CVC or billing secrets.
- Do not rewrite payment requests, inject offer tokens, stack invalid promotions, impersonate regions or bypass eligibility.
- Do not run purchases/cancellations without explicit user participation.
- Treat manually entered subscription notes as unverified until checked against an official Google page.
- Never commit the `data/` directory.

## UI / integration

The local web interface is served from `app.py`; no remote deployment is required. This document can be adapted to AI systems with local-tool support, but it is not installed merely by being present on GitHub.
