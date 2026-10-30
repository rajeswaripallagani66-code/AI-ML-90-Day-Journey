import time, requests, statistics
URL = "http://localhost:8000/predict"
payload = {"data": [0.1]*20}

latencies = []
for i in range(50):
    start = time.time()
    try:
        r = requests.post(URL, json=payload, timeout=5)
        latencies.append((time.time()-start)*1000)
    except:
        pass

print(f"p50: {statistics.median(latencies):.1f}ms")
print(f"p95: {sorted(latencies)[int(len(latencies)*0.95)]:.1f}ms" if latencies else "no data")
print(f"Success: {len(latencies)}/50")