# Kubernetes Pod Scheduling

Kubernetes schedules pods via kube-scheduler using a two-phase process: filtering and scoring.

**Filtering** eliminates nodes that can't run the pod. Checks include:
- Resource availability (CPU, memory requests fit within allocatable)
- Node selectors and affinity rules match
- Taints are tolerated
- PersistentVolume topology constraints satisfied

**Scoring** ranks remaining nodes 0-100. Default plugins:
- `NodeResourcesFit`: prefers nodes with balanced resource utilization
- `InterPodAffinity`: favors nodes satisfying soft affinity rules
- `ImageLocality`: prefers nodes that already have the container image

The highest-scoring node wins. Ties are broken randomly.

**Priority and preemption**: if no node passes filtering, the scheduler checks whether evicting lower-priority pods would free enough resources. If so, it evicts them and schedules the pending pod. Priority classes range from -2 billion to 1 billion; system-critical pods use values above 1 billion.

Pod Disruption Budgets (PDBs) limit how many pods in a set can be unavailable simultaneously. The scheduler respects PDBs during preemption — it won't evict pods if doing so violates the budget.

Configure scheduling constraints in the pod spec:

```yaml
spec:
  nodeSelector:
    disk: ssd
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
          - matchExpressions:
              - key: topology.kubernetes.io/zone
                operator: In
                values: [eu-west-1a, eu-west-1b]
  tolerations:
    - key: "dedicated"
      operator: "Equal"
      value: "gpu"
      effect: "NoSchedule"
  priorityClassName: high-priority
```
