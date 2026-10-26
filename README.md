# Demo 2: self hosting và diễn tập rời runtime

Seminar **Low code and no code development: Vendor lock in low code**.
Sinh viên trình bày: **Trương Nguyễn Thùy Anh**.

Mục tiêu gồm hai phần khác nhau: di chuyển flow giữa hai instance Node-RED và thay hẳn runtime bằng Python. Đây là demo giáo dục tự xây dựng. JSON của Node-RED không phải định dạng workflow trung lập giữa các sản phẩm.

## Bài toán

Xét duyệt yêu cầu có số tiền nguyên không âm theo VND. Số tiền tối đa 1.000.000 được `approved`, lớn hơn chuyển `manual_review`. Đây là ngưỡng giả định cho demo, không phải quy định tài chính thực tế. Giá trị đầu vào phải là safe integer trong phạm vi JavaScript, không chấp nhận boolean, chuỗi, số âm hoặc số thập phân.

`policy.json` giữ ngưỡng và version. `nodered/evaluate.function.js` là code dùng nguyên văn trong Function node. `engine.py` thực thi lại quy tắc trong Python. Định dạng policy này do demo tự định nghĩa, chỉ bao phủ quy tắc đơn giản. Nó không phải tiêu chuẩn chung hoặc bộ chuyển đổi mọi workflow.

## Chuẩn bị và chạy

Cần Docker Engine, Docker Compose plugin, Python 3.10 trở lên. Node.js 18 trở lên chỉ cần cho test parity cục bộ.

```bash
git clone https://github.com/odixe06/lowcode-lockin-exit-drill-demo.git
cd lowcode-lockin-exit-drill-demo
docker compose up -d
```

* Runtime A có sẵn flow tại http://127.0.0.1:1881
* Runtime B ban đầu trống tại http://127.0.0.1:1882

Chỉ bind localhost. Editor chưa bật authentication, không dùng để triển khai Internet. Runtime A dùng flow chỉ đọc, runtime B lưu các thay đổi vào named volume.

## Phần 1: chuyển instance khoảng 2 phút

1. Mở editor A, xem flow `Portable approval demo`.
2. Menu góc phải, chọn Export, chọn current flow, tải file JSON.
3. Mở editor B, chọn Import, tải file JSON vừa export, chọn new flow rồi bấm Deploy.
4. Chạy kiểm tra bằng HTTP thật:

```bash
python3 verify.py http://127.0.0.1:1881 http://127.0.0.1:1882
```

Kết quả mong đợi là `PASS` cho 10 fixtures ở mỗi endpoint. Đây là migration cùng engine. `policy.json` và `settings` đã được cấu hình ở cả hai instance qua Compose. Chỉ có flow export không đủ để tái dựng mọi dependency.

## Phần 2: thay runtime khoảng 2 phút

Mở terminal thứ hai:

```bash
python3 engine.py
```

Tại terminal ban đầu:

```bash
python3 verify.py http://127.0.0.1:1882 http://127.0.0.1:8001
docker compose stop runtime_a runtime_b
python3 verify.py http://127.0.0.1:8001
```

Kết quả Python vẫn giống fixtures khi cả hai Node-RED instance đã dừng. Python không chạy flow JSON của Node-RED, người phát triển đã viết một adapter thực thi quy tắc tương đương. Công sức viết adapter chính là một phần chi phí thoát nền tảng.

## Test parity không cần Docker

```bash
python3 -m unittest discover -p 'test_*.py' -v
```

Cần `node` trong PATH. Test thực thi chính Function JavaScript trong Node VM và đối chiếu Python trên các mốc 0, ngưỡng, vượt ngưỡng và đầu vào không hợp lệ. Test này không thay cho HTTP integration. `verify.py` kiểm thử HTTP thật và trả mã lỗi khi bất kỳ kết quả nào khác fixtures.

## Chạy Node-RED bằng npm thay Docker

```bash
npm install --prefix .runtime node-red@4.1.0
```

Tạo settings cục bộ trỏ `functionGlobalContext.policy` tới đường dẫn tuyệt đối của `policy.json`, dùng `require('/duong/dan/tuyet/doi/policy.json')`. Trong settings, đặt `flowFile` là đường dẫn tuyệt đối của `nodered/flows.json` cho A. Với B dùng `flowFile: 'flows.json'` trong một `--userDir` riêng. Chạy mỗi instance với `--userDir` và `-p` riêng. Xem [hướng dẫn kỹ thuật](docs/architecture.md).

## Bằng chứng cần ghi trong seminar

* Lưu JSON export A và đối chiếu flow sau import B.
* 10 fixtures cùng cho đúng HTTP status và payload.
* Python vẫn trả kết quả đúng sau khi dừng A và B.
* Tự đo thời gian export, import, test. Không dùng thời gian mẫu như số liệu thực nghiệm.

## Giới hạn

Demo không có workflow đang chạy dở, dữ liệu giao dịch, queue, timer, retry hay side effect. Migration production phải xử lý thêm trạng thái, idempotency, credentials, plugin, authentication, authorization, timezone, rounding và rollback. Self hosting chuyển trách nhiệm vận hành sang nhóm sở hữu, không tự xóa phụ thuộc runtime.

Dừng container bằng `docker compose down`, dữ liệu editor B vẫn nằm trong volume. Không dùng `down -v` nếu muốn giữ flow đã import. Quy tắc policy thay đổi yêu cầu restart runtime và cập nhật fixtures có chủ đích.

Nguồn: [Node-RED import/export](https://nodered.org/docs/user-guide/editor/workspace/import-export), [Docker](https://nodered.org/docs/getting-started/docker), [security](https://nodered.org/docs/user-guide/runtime/securing-node-red).
