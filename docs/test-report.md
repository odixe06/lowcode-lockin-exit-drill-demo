# Báo cáo kiểm thử

Kiểm tra ngày 26/10/2026. Môi trường: Linux, Python 3.12.14, Node.js 24.22.1, Node-RED 4.1.0 cài bằng npm. Không có Docker trong môi trường kiểm thử.

## Đã chạy và đạt

* Test parity thực thi nguyên văn Function JavaScript của flow và engine Python trên 10 fixtures.
* Khởi chạy hai process Node-RED độc lập. Runtime B ban đầu trả 404 tại `/evaluate`.
* Export bằng Admin API từ A, import sang B thành công với HTTP 204. Flow có một tab và ba node nghiệp vụ.
* Mỗi endpoint A, B và Python đều đạt 10 HTTP fixtures, gồm status và payload.
* Dừng cả hai process Node-RED. Python vẫn đạt đủ 10 HTTP fixtures.

## Contract và giới hạn

Fixtures dùng body JSON object. Payload ngoài contract như JSON scalar có thể bị middleware Node-RED từ chối trước Function, với định dạng lỗi khác Python. Không tuyên bố parity ngoài contract.

Docker image, Compose và thao tác import bằng giao diện editor chưa chạy trong môi trường này. Test Admin API kiểm chứng cơ chế export/import thực, nhưng không thay kiểm tra thao tác UI trên máy trình bày. Chưa có state đang chạy, queue, timer, side effect hoặc transaction để migrate. Không có số liệu thời gian hoặc hiệu năng production.
