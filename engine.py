"""Replacement engine with no Node-RED dependency."""
import argparse, json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
ROOT = Path(__file__).resolve().parent
POLICY = json.loads((ROOT/"policy.json").read_text())

def evaluate(data, policy=POLICY):
    amount = data.get("amount") if isinstance(data,dict) else None
    if isinstance(amount,bool) or not isinstance(amount,(int,float)) or not 0 <= amount <= 9007199254740991 or amount != int(amount):
        return 400, {"error":"amount must be a non-negative safe integer"}
    return 200, {"decision":"approved" if amount <= policy["auto_approve_limit"] else policy["otherwise"], "policy_version":policy["version"], "currency":policy["currency"]}

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/evaluate":
            status,result=404,{"error":"not found"}
        else:
            try:
                length=int(self.headers.get("Content-Length",0))
                if not 0 < length <= 8192: raise ValueError("invalid body size")
                data=json.loads(self.rfile.read(length), parse_constant=lambda v: (_ for _ in ()).throw(ValueError("invalid JSON constant")))
                status,result=evaluate(data)
            except (ValueError, UnicodeError, OverflowError): status,result=400,{"error":"invalid JSON"}
        body=json.dumps(result).encode()
        self.send_response(status); self.send_header("Content-Type","application/json")
        self.send_header("Content-Length",str(len(body))); self.end_headers(); self.wfile.write(body)

if __name__ == "__main__":
    parser=argparse.ArgumentParser(); parser.add_argument("--host",default="127.0.0.1"); parser.add_argument("--port",type=int,default=8001)
    args=parser.parse_args(); print(f"Replacement engine on {args.host}:{args.port}",flush=True)
    ThreadingHTTPServer((args.host,args.port),Handler).serve_forever()
