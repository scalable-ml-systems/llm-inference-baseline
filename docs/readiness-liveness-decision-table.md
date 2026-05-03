| Condition                         | Liveness | Readiness  | Traffic-ready | Why                                 
| --------------------------------- | -------- | ---------- | ------------- | ---------------------------------|
| Process running, model not loaded | pass     | fail       | fail          | backend cannot serve             |
| Model loaded, queue empty         | pass     | pass       | pass          | safe                             |
| Model loaded, queue very high     | pass     | pass maybe | fail          | alive but overloaded             |  
| GPU memory near limit             | pass     | pass maybe | fail          | risk of OOM                      |  
| draining for shutdown             | pass     | fail       | fail          | should not receive new traffic   |   
| adapter not loaded                | pass     | pass       | depends       | base traffic okay, LoRA risky    |
