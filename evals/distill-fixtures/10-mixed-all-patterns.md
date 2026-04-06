# Incident Postmortem: Payment Processing Outage

## Overview

It's important to note that on March 3, 2026, our payment processing system experienced a significant outage. This document provides a comprehensive and holistic overview of the incident.

## Timeline

Moreover, here is the detailed timeline of events:

- **14:02 UTC** — Monitoring alerts triggered for elevated error rates on the payment service
- **14:05 UTC** — On-call engineer acknowledged the alert
- **14:12 UTC** — Root cause identified: expired TLS certificate on the Stripe webhook endpoint
- **14:15 UTC** — Certificate renewed via Let's Encrypt
- **14:18 UTC** — Payment processing restored
- **14:30 UTC** — All queued payments processed successfully

## Impact

It's worth mentioning that the outage lasted 16 minutes. Furthermore, during this period, approximately 342 payment attempts failed. Additionally, it should be noted that all failed payments were automatically retried and completed successfully after the fix.

In terms of financial impact, no revenue was lost due to the fact that the retry mechanism handled all failed transactions. The vast majority of users (98.7%) did not notice the outage. In the event that a user did notice, they saw a "Payment processing, please wait" message.

Certainly, the customer support team reported that 4 users contacted support. Great question about the SLA impact — the outage brought our monthly uptime from 99.99% to 99.97%, which is still above our 99.95% SLA commitment.

## Root Cause

The root cause of this incident was an expired TLS certificate. The certificate was set to auto-renew, but the auto-renewal process failed because the DNS validation record had been accidentally deleted during a DNS migration on February 28. The DNS migration was part of our effort to leverage Cloudflare for enhanced performance.

In other words, the certificate expired because the DNS record needed for renewal was missing. The DNS record was missing because it was deleted during migration. The migration deleted it because the record wasn't tagged as system-managed.

## Action Items

In order to prevent this from happening again, the following action items have been identified:

1. **Tag all system-managed DNS records** with `managed-by: letsencrypt` — Owner: SRE team, Due: March 10
2. **Add certificate expiry monitoring** with 30-day, 7-day, and 1-day alerts — Owner: Platform team, Due: March 7
3. **Create runbook for certificate renewal failures** — Owner: On-call team, Due: March 14
4. **Audit all DNS records** for the purpose of identifying other system-managed records that might be at risk — Owner: SRE team, Due: March 15

## Lessons Learned

At the end of the day, this incident highlights the importance of monitoring certificate expiration. The bottom line is that automated renewal alone is not sufficient — monitoring is also needed. In conclusion, we need defense in depth for critical infrastructure like TLS certificates. To summarize, monitor what you automate.
