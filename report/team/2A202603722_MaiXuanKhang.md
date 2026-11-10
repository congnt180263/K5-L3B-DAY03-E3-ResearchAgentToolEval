# Báo cáo cá nhân — Mai Xuân Khang-2A202603722

## 1. Thông tin thành viên

- Họ tên: Mai Xuân Khang
- MSSV: 2A202603722
- Email: Chờ Khang bổ sung.
- GitHub: KhangMai123
- Nhóm và lớp: E3 — L3B, VinUni AI20K K5

## 2. Phần việc phụ trách

- CP3 — Tool mới và unit test. Phần việc gồm contract, đăng ký tool, kiểm thử offline và một case định tuyến để nhóm dùng trong CP4.

## 3. Đóng góp cụ thể

- `dedupe_sources` xử lý danh sách đã thu thập trước khi làm digest hoặc trích dẫn. Khi cùng một trang xuất hiện ở nhiều kết quả, tool giữ bản đầu tiên, URL và metadata gốc, cùng thứ tự tương đối của các mục được giữ.
- Tool nhận `items` là danh sách đối tượng JSON có URL HTTP(S) tuyệt đối. Code chuẩn hóa host và cổng mặc định, bỏ fragment rồi dùng tập hợp URL đã gặp. Kết quả trả về gồm danh sách `items` và `duplicate_count`. Sai kiểu, URL không hợp lệ hoặc dữ liệu không thể mã hóa JSON trả error dict thay cho danh sách một phần. Không cần mạng, key hay thư viện mới.
- Ba unit test kiểm tra việc loại bản trùng mà vẫn giữ dữ liệu và thứ tự, lỗi khi `items` sai kiểu, và lỗi khi URL thứ hai có cổng `99999`. Ở ca cuối, test kiểm tra tool trả lỗi thay vì ném exception hoặc chỉ trả nguồn đầu tiên.
- Kết quả thật gồm contract **60 passed**. File TODO có **3 passed, 14 skipped**. Toàn bộ suite có **70 passed, 14 skipped, 0 failed**. Ba test mới đều chạy. Không ghi nhận lần test thất bại trong quá trình triển khai CP3.
- Tool giữ nguyên query và không theo redirect, nên URL khác query hoặc redirect vẫn có thể cùng trỏ đến một bài. Các URL chỉ khác fragment được tính là trùng, kể cả trang dùng fragment để phân biệt nội dung.
- Đã thêm case single-turn `G01_dedupe_research_sources` vào bộ nhóm đang trống. Case đo việc chọn tool. CP4 cần giữ case này trong 5 single-turn, bổ sung 4 single-turn và 5 multi-turn còn lại rồi chạy eval nhóm.

## 4. Bằng chứng

- File/commit/PR: [Tool](../../starter_v0/tools/dedupe_sources/tool.py), [contract](../../starter_v0/tools/dedupe_sources/TOOL.md), [unit tests](../../starter_v0/tests/test_tools_todo.py), [case nhóm](../../starter_v0/data/eval_group.json) và [kết quả B5a](group_report.md#b5a-required-evidence--tool-mới-unit-test-ui).
- AI/công cụ đã dùng và cách tự kiểm tra kết quả: Codex hỗ trợ triển khai, viết test và soạn báo cáo. Khang có thể đối chiếu ví dụ trong TOOL.md với ba assert đầu ra, đọc phần đăng ký và chạy lại `python -m pytest -v` từ `starter_v0`.

## 5. Tự đánh giá

Khang tự đánh giá sau khi chạy lại test và đối chiếu hành vi với contract.
