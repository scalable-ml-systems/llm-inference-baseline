What does it mean for a vLLM backend to be alive?
What does it mean for it to be ready?
What does it mean for it to be safe to receive more traffic?

## Health Semantics 
Liveness answers: should Kubernetes restart this process?

Readiness answers: should this pod receive generic traffic?

Traffic readiness answers: should this backend receive more work right now?

Workload-specific readiness answers: should this backend receive this specific request, given prompt shape, adapter need, queue state, and cache locality?

## Readiness Contract 
traffic-ready = model loaded
              + GPU available
              + num_requests_waiting below threshold
              + KV cache usage below threshold
              + not draining