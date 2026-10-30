import time, requests, statistics

URL = 'http://127.0.0.1:8000/predict'
PAYLOAD = {'features': [0.5]*20}  # List[float] - matches your schema!

print(f'Testing {URL} with payload {PAYLOAD}')
latencies = []
ok = 0
for i in range(100):
    start = time.time()
    try:
        r = requests.post(URL, json=PAYLOAD, timeout=5)
        ms = (time.time()-start)*1000
        latencies.append(ms)
        if r.status_code == 200:
            ok += 1
        if i < 3:
            print(f"{i}: {r.status_code} {r.json()} {ms:.1f}ms")
    except Exception as e:
        print(f"{i}: ERROR {e}")

if latencies:
    latencies.sort()
    p50 = statistics.median(latencies)
    p95 = latencies[int(len(latencies)*0.95)]
    print(f"\n✅ SUCCESS: {ok}/100 ok")
    print(f"p50: {p50:.1f}ms")
    print(f"p95: {p95:.1f}ms")
    print(f"p99: {latencies[int(len(latencies)*0.99)]:.1f}ms")
    print(f"Fail: {(100-ok)}%")
else:
    print("No response!")
