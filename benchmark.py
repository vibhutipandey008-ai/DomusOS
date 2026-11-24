"""Small repeatable local API timing benchmark; reports measurements from this machine."""
import time, statistics
from app import app, init_db
init_db(); client=app.test_client()
email='benchmark_user@domusos.local'; password='BenchmarkPass123'
r=client.post('/api/register',json={'name':'Benchmark User','email':email,'password':password})
if r.status_code not in (201,409): raise SystemExit(r.json)
if r.status_code==409: client.post('/api/login',json={'email':email,'password':password})
for _ in range(3): client.get('/api/health')
for endpoint in ['/api/health','/api/me','/api/state']:
 samples=[]
 for _ in range(100):
  t=time.perf_counter(); client.get(endpoint); samples.append((time.perf_counter()-t)*1000)
 print(f'{endpoint}: mean={statistics.mean(samples):.3f} ms; p95={sorted(samples)[94]:.3f} ms; n={len(samples)}')
