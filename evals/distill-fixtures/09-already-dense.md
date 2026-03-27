# Backup Policy

Daily snapshots at 02:00 UTC. Retained 30 days. Stored in S3 `prod-backups-eu-west-1`.

WAL archiving enabled, continuous. Point-in-time recovery to any second within the 30-day window.

Weekly full backup (Sunday 03:00 UTC) to Glacier Deep Archive. Retained 1 year. Encrypted with AES-256, key in AWS KMS `arn:aws:kms:eu-west-1:123456:key/backup-key`.

Restore tested monthly. Last test: 2026-02-15, RTO achieved: 12 minutes. Target RTO: 15 minutes. Target RPO: 0 (WAL-based).

On-call runbook: `runbooks/restore-from-backup.md`.
