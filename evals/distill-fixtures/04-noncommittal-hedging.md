# Performance Investigation: Checkout Latency

The checkout endpoint can potentially be experiencing higher than expected latency. Some users could possibly be seeing response times that might exceed 3 seconds under certain conditions.

Our investigation suggests that the issue may be related to the payment gateway integration. It appears that the Stripe API calls could potentially take up to 2.5 seconds in some cases. This might possibly be caused by the fact that we're making sequential API calls where parallel calls could potentially be more efficient.

It depends on various factors, but the N+1 query pattern in the order line items loader may help explain part of the latency. The ORM is generating approximately 47 queries per checkout for an average cart of 8 items. This possibly accounts for roughly 800ms of the total response time.

There are potentially several approaches that could possibly help address these issues:

1. **Parallel Stripe calls**: The payment validation and fraud check can possibly be made in parallel, which might reduce Stripe latency by approximately 40%.
2. **Batch query**: The line items could potentially be loaded with a single `WHERE IN` query, which may reduce database time from 800ms to approximately 50ms.
3. **Response caching**: Product metadata, which doesn't change frequently, could possibly be cached with a 5-minute TTL.

It's worth considering that implementing all three changes could potentially bring checkout latency down to under 1 second for the vast majority of users.
