# SLA Comparison: Cloud Providers

It's important to note that when choosing a cloud provider, SLA guarantees are a crucial factor. Moreover, let me provide a comprehensive comparison.

## Compute SLAs

| Provider | Service | Monthly SLA | Credit at 99.0-99.9% | Credit below 99.0% |
|----------|---------|-------------|----------------------|---------------------|
| AWS | EC2 | 99.99% | 10% | 30% |
| GCP | Compute Engine | 99.99% | 10% | 25% |
| Azure | Virtual Machines | 99.99% | 10% | 25% |

## Database SLAs

| Provider | Service | Monthly SLA | RPO | RTO |
|----------|---------|-------------|-----|-----|
| AWS | RDS Multi-AZ | 99.95% | 0 (sync replication) | < 60s |
| GCP | Cloud SQL HA | 99.95% | 0 (sync replication) | < 120s |
| Azure | Azure SQL | 99.995% | 5s | < 30s |

## Storage SLAs

| Provider | Service | Durability | Availability |
|----------|---------|------------|--------------|
| AWS | S3 Standard | 99.999999999% (11 nines) | 99.99% |
| GCP | Cloud Storage | 99.999999999% (11 nines) | 99.95% |
| Azure | Blob Storage | 99.999999999999% (14 nines, LRS) | 99.9% |

It should be noted that Azure Blob Storage with LRS (Locally Redundant Storage) claims 14 nines of durability because data is written synchronously to 3 copies within a single datacenter. However, it's worth mentioning that this doesn't protect against datacenter-level failures. For geo-redundancy, Azure GRS provides 99.99999999999999% (16 nines) but with 99.9% availability.

## Our Decision

Based on our requirements (RPO=0, RTO < 60s, data in EU), we chose:
- **Compute**: AWS EC2 in `eu-west-1` (Ireland)
- **Database**: AWS RDS PostgreSQL Multi-AZ
- **Storage**: AWS S3 with cross-region replication to `eu-central-1` (Frankfurt)

Total cost: $14,200/month for our current scale (8 services, ~50K RPM, 2.1TB storage).
