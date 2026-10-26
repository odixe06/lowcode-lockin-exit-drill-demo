import json, subprocess, unittest
from pathlib import Path
from engine import evaluate
ROOT=Path(__file__).parent
class ParityTest(unittest.TestCase):
    def test_python_and_exact_nodered_function(self):
        cases=json.loads((ROOT/"fixtures.json").read_text())
        flow=json.loads((ROOT/"nodered/flows.json").read_text())
        source=(ROOT/"nodered/evaluate.function.js").read_text()
        self.assertEqual(next(n["func"] for n in flow if n["id"]=="decision-fn"),source)
        runner="""const fs=require('fs'),vm=require('vm');
const cases=JSON.parse(fs.readFileSync('fixtures.json'));
const policy=JSON.parse(fs.readFileSync('policy.json'));
const source=fs.readFileSync('nodered/evaluate.function.js','utf8');
const output=cases.map(c=>{const context={msg:{payload:c.input},global:{get:()=>policy}};vm.runInNewContext('(function(){'+source+'})()',context);return [context.msg.statusCode,context.msg.payload];});
console.log(JSON.stringify(output));"""
        actual=json.loads(subprocess.check_output(["node","-e",runner],cwd=ROOT,text=True))
        for case,js_result in zip(cases,actual):
            py_status,py_body=evaluate(case["input"])
            self.assertEqual([py_status,py_body],js_result)
            self.assertEqual(py_status,case["status"])
            self.assertEqual(py_body.get("decision",py_body.get("error")),case.get("decision",case.get("error")))
if __name__=="__main__": unittest.main()
