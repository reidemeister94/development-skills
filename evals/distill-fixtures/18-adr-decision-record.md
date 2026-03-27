# ADR-017: Message Queue Selection

## Status

Accepted (2026-02-20)

## Context

It's important to note that our order processing pipeline currently handles events synchronously. Moreover, this means that a failure in the notification service blocks order completion. Furthermore, during peak hours (Black Friday 2025), we observed 340ms p99 latency on the order endpoint, with 12% of that time spent waiting for downstream services.

Additionally, we evaluated three message queue options:

### RabbitMQ
- AMQP protocol, mature, well-understood
- Supports complex routing (topic, fanout, headers exchanges)
- Single-node throughput: ~50,000 msg/s
- Clustering requires careful network partition handling
- Team has 3 years of production experience

### Apache Kafka
- Log-based, append-only, high throughput
- Single-broker throughput: ~200,000 msg/s
- Built-in retention and replay (7-day default)
- Requires ZooKeeper (or KRaft in newer versions)
- Steeper learning curve, no team experience
- Overkill for our current volume (~2M messages/day)

### AWS SQS
- Fully managed, no infrastructure
- Standard queue: unlimited throughput, at-least-once delivery
- FIFO queue: 3,000 msg/s with deduplication
- No message replay capability
- Vendor lock-in to AWS
- $0.40 per million requests

## Decision

We chose **RabbitMQ** because:
1. Team expertise reduces operational risk
2. Our volume (2M msg/day = ~23 msg/s average, ~200 msg/s peak) is well within RabbitMQ's capacity
3. Complex routing (order events fan out to 4 consumers: inventory, notifications, analytics, billing) maps naturally to RabbitMQ exchanges
4. We don't need Kafka's replay capability — failed messages retry via dead-letter queues

## Consequences

- Positive: 3-week implementation timeline (vs. estimated 8 weeks for Kafka)
- Positive: team can own operations from day one
- Negative: if volume grows 100x, we'll need to revisit (Kafka or SQS)
- Negative: no built-in message replay for debugging — mitigated by logging all messages to S3
