# Cấu trúc và diễn tập

Luồng: HTTP POST `/evaluate`, Function đọc policy từ global context, HTTP response trả decision. Settings của mỗi runtime nạp policy từ file ngoài flow. Policy chỉ hỗ trợ một ngưỡng, không có vòng lặp hay biểu thức động.

Chạy npm cục bộ bằng Python để tạo settings với đường dẫn tuyệt đối:

```bash
python3 - <<'PYCODE'
import json
from pathlib import Path
root=Path.cwd()
for name,port in [('a',1881),('b',1882)]:
    user=root/'.runtime'/name
    user.mkdir(parents=True,exist_ok=True)
    flow=str(root/'nodered/flows.json') if name=='a' else 'flows.json'
    policy=str(root/'policy.json')
    config='module.exports={uiPort:'+str(port)+',flowFile:'+json.dumps(flow)+',functionGlobalContext:{policy:require('+json.dumps(policy)+')}};'
    (user/'settings.js').write_text(config)
PYCODE
```

Chạy trong hai terminal riêng:

```bash
./.runtime/node_modules/.bin/node-red --userDir .runtime/a
```

```bash
./.runtime/node_modules/.bin/node-red --userDir .runtime/b
```

Trước khi import, B trả 404 ở `/evaluate`. Sau khi import và Deploy, chạy `verify.py` cho hai runtime. Kiểm tra khi chuyển engine phải giữ cùng đơn vị, cùng biên inclusive tại 1.000.000, cùng kiểu dữ liệu và HTTP status. Phiên bản policy hiện là 1.

Trong production, danh sách bàn giao tối thiểu gồm flow, runtime version, dependency lockfile, credentials qua kênh bí mật riêng, cấu hình, schema, dữ liệu, state, lịch chạy, test và rollback. Export JSON chưa có nghĩa đã chuyển đủ tất cả.

Contract demo yêu cầu body JSON object. Các payload ngoài contract như JSON scalar hoặc JSON lỗi có thể bị middleware Node-RED từ chối trước Function, với dạng lỗi khác engine Python. Không tuyên bố tương đương các phản hồi ngoài contract.
