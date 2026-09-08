# TechNova — Incident Response Playbook

## Overview

This document defines how TechNova responds to production incidents.
An **incident** is any unplanned event that degrades service availability
or performance for users.

## Severity Levels

### P1 — Critical
- **Definition:** Complete service outage or data loss
- **Examples:** NovaCode API returning 500 errors, database corruption,
  security breach
- **Response time:** 15 minutes
- **Escalation:** VP Engineering + CEO notified immediately
- **Resolution target:** 2 hours

### P2 — Major
- **Definition:** Major feature broken, significant user impact
- **Examples:** Code review not working, NL2SQL returning wrong queries,
  authentication failures
- **Response time:** 30 minutes
- **Escalation:** Engineering leads notified
- **Resolution target:** 4 hours

### P3 — Minor
- **Definition:** Minor feature issue, workaround available
- **Examples:** Slow suggestion latency, UI glitch, non-critical error logs
- **Response time:** 2 hours
- **Escalation:** Team lead notified
- **Resolution target:** 24 hours

### P4 — Low
- **Definition:** Cosmetic issues, minor inconveniences
- **Examples:** Typo in error message, dark mode color issue
- **Response time:** Next business day
- **Resolution target:** Next sprint

## Incident Response Steps

### 1. Detect & Alert (0-5 minutes)
- Monitoring alerts fire via PagerDuty
- Or user reports via support ticket / Slack #incidents channel
- On-call engineer acknowledges the alert within 5 minutes

### 2. Assess & Triage (5-15 minutes)
- Determine severity level based on user impact
- Check monitoring dashboards (Grafana, Datadog)
- Check if recent deployments might have caused the issue
- Open an incident channel: #incident-YYYY-MM-DD-brief-description

### 3. Mitigate (15-60 minutes)
- **First priority:** Restore service, even if it means rolling back
- Rollback the most recent deployment if it's deployment-related
- If not deployment-related, investigate logs and metrics
- Communicate status in #incidents every 30 minutes for P1/P2

### 4. Resolve & Verify (varies)
- Fix the root cause
- Verify the fix in staging before production
- Monitor for 30 minutes after fix to ensure stability
- Close the incident channel

### 5. Post-Mortem (within 48 hours)
- Write a blameless post-mortem document
- Include: timeline, root cause, impact, resolution, action items
- Schedule a post-mortem review meeting with the team
- Track action items in Jira

## On-Call Rotation

- **Schedule:** Weekly rotation, Monday to Monday at 10am CT
- **Primary + Secondary:** Each rotation has two engineers
- **Compensation:** On-call engineers receive $500/week stipend
- **Handoff:** Primary on-call calls secondary at start of rotation
  to share context

## Escalation Contacts

| Role                  | Name            | Phone          | Slack             |
|-----------------------|-----------------|----------------|-------------------|
| VP Engineering        | Priya Sharma    | +1-512-555-0101| @priya.sharma     |
| Platform Lead         | James O'Brien   | +1-512-555-0102| @james.obrien     |
| CTO                   | Sarah Chen      | +1-512-555-0100| @sarah.chen       |
| Security Lead         | Marcus Rodriguez| +1-512-555-0103| @marcus.r         |

## Common Incidents & Resolutions

### NovaCode API High Latency
- **Symptom:** Suggestion latency > 200ms
- **Check:** GPU utilization on inference servers, request queue depth
- **Common fix:** Scale up inference replicas (currently 3 → 6)
- **Escalate if:** Latency persists after scaling

### Database Connection Pool Exhausted
- **Symptom:** "Connection pool exhausted" errors in logs
- **Check:** Active connections in PostgreSQL, slow queries
- **Common fix:** Kill long-running queries, restart connection pooler (PgBouncer)
- **Prevention:** Set query timeout to 30 seconds

### GitHub Webhook Failures
- **Symptom:** Code reviews not triggering on new PRs
- **Check:** GitHub webhook delivery logs, API rate limits
- **Common fix:** Re-deliver failed webhooks, check for IP allowlist changes
