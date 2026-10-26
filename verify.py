"""Compare real HTTP endpoints against shared fixtures. No third-party libraries."""
import json, sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
fixtures=json.loads((Path(__file__).parent/"fixtures.json").read_text())
if len(sys.argv)<2: raise SystemExit("Usage: python3 verify.py http://127.0.0.1:1881 [http://127.0.0.1:1882 http://127.0.0.1:8001]")
for base in sys.argv[1:]:
    for i,case in enumerate(fixtures,1):
        request=Request(base.rstrip("/")+"/evaluate", json.dumps(case["input"]).encode(), {"Content-Type":"application/json"})
        try: response=urlopen(request,timeout=5)
        except HTTPError as error: response=error
        with response:
            raw=response.read()
            try: actual=json.loads(raw)
            except ValueError: raise AssertionError((base,i,response.status,raw[:300]))
            assert response.status==case["status"],(base,i,response.status,actual)
            if case["status"]==200:
                assert actual=={"decision":case["decision"],"policy_version":1,"currency":"VND"},(base,i,actual)
            else: assert actual=={"error":case["error"]},(base,i,actual)
    print(f"PASS {base}: {len(fixtures)} HTTP fixtures")
