Prefix cache benefit is workload-dependent.
If future routing distributes shared-prefix requests randomly across backends, it may destroy locality and increase prefill work.
Therefore, request routing should eventually consider prefix locality, not only backend load.