# Báo cáo cá nhân — Mai Xuân Khang-2A202603722

## 1. Thông tin thành viên

- Họ tên: Mai Xuân Khang
- MSSV: 2A202603722
- Email: 26ai.khangmx@vinuni.edu.vn
- GitHub: KhangMai123
- Nhóm và lớp: E3 — L3B, VinUni AI20K K5

## 2. Phần việc phụ trách

- CP3 — Thiết kế và triển khai `dedupe_sources`, khai báo contract, đăng ký tool và viết unit test offline. Phần bàn giao cho CP4 là một case kiểm tra model có chọn tool khi đã có sẵn danh sách nguồn.

## 3. Đóng góp cụ thể

### Bài toán và thiết kế

Một trang có thể xuất hiện nhiều lần khi gộp kết quả từ các nguồn tìm kiếm. `dedupe_sources` lọc các bản trùng URL trước khi lập danh sách trích dẫn hoặc làm digest. Agent gọi tool khi đã có URL và người dùng cần loại nguồn trùng. Các bước tìm nguồn, đọc trang và trình bày nội dung vẫn do các tool tương ứng đảm nhiệm.

Tool nhận `items`, một danh sách đối tượng JSON có trường `url` là địa chỉ HTTP(S) tuyệt đối. Để so sánh, code chuẩn hóa chữ hoa/thường của host, bỏ cổng mặc định và fragment. Tập hợp URL đã gặp giúp nhận ra bản trùng khi duyệt từ đầu đến cuối. Tool trả `items` và `duplicate_count`, giữ nguyên URL, metadata và thứ tự của các mục được giữ. Ví dụ, `https://Example.com:443/report#intro` và `https://example.com/report#summary` được tính là một nguồn. Nếu gặp kiểu dữ liệu sai, URL lỗi hoặc giá trị không thể mã hóa JSON, tool trả `tool`, `error` và `message`. Tool không trả danh sách lọc dở dang và không dùng mạng, key hay thư viện mới.

### Kiểm thử và tích hợp

| Kiểm tra | Kết quả | Điều được xác minh |
|---|---|---|
| Happy path | PASS | Hai bản cùng URL được gộp, bản đầu tiên giữ metadata, bản có query khác được giữ, đầu vào giữ nguyên. |
| Sai kiểu `items` | PASS | Chuỗi thay cho danh sách trả `TypeError` dưới dạng dict. |
| URL có cổng `99999` | PASS | Mục thứ hai trả `ValueError` với chỉ số 1. Mục hợp lệ đứng trước không trở thành kết quả dở dang. |
| Contract và toàn suite | 60 contract PASS. Toàn suite 70 PASS, 0 FAIL, 14 SKIP. | Registry, schema và hợp đồng tool khớp nhau. Ba test mới đều chạy. Các skip là stub cũ. |
| ResearchAgent với provider thử offline | PASS, 3 nguồn vào, giữ 2, loại 1. | ResearchAgent nhận khai báo và thực thi đúng tool qua registry khi nhận một lời gọi có sẵn. |

Kiểm tra tích hợp dùng `main` tại `740cdca`. Các mô tả CP2 trong `tools.yaml`, prompt v3, version log và run v0–v3 được giữ nguyên. Hai nhánh cùng sửa thông tin nhóm và báo cáo, nên phần CP3 được đưa vào đúng các mục trên bản mới của `main`. Số liệu v3 20/20 của nhóm là số đo trước khi thêm `dedupe_sources`.

### Giới hạn và bàn giao

Tool giữ nguyên query và không theo redirect. Do đó hai URL khác query hoặc qua redirect vẫn có thể cùng trỏ đến một bài. Hai địa chỉ chỉ khác fragment được coi là trùng, kể cả trang dùng fragment để phân biệt nội dung.

CP4 đã tích hợp case G01 do CP3 bàn giao và bổ sung G09 để đo ngữ cảnh nhiều lượt. [Run nhóm](../../starter_v0/runs/v3_B_group_gemini_20261110T224831464473.json) đạt 10/10, measured_cases=10 và provider_error_cases=0 trên Gemini gemini-3.5-flash-lite. G01 giữ 2 trong 3 nguồn, G09 giữ 3 trong 4 nguồn; cả hai có duplicate_count=1. Unit test đo logic lọc và nhánh lỗi, còn run nhóm bổ sung bằng chứng model tự chọn và thực thi đúng tool.

## 4. Bằng chứng

- File/commit/PR: [Tool](../../starter_v0/tools/dedupe_sources/tool.py), [contract](../../starter_v0/tools/dedupe_sources/TOOL.md), [unit test](../../starter_v0/tests/test_tools_todo.py), [case nhóm](../../starter_v0/data/eval_group.json) và [kết quả B5a](group_report.md#b5a-required-evidence--tool-mới-unit-test-ui).
- Commit đưa CP3 vào main: [515b40f](https://github.com/congnt180263/K5-L3B-DAY03-E3-ResearchAgentToolEval/commit/515b40fd9de1aaba9eb4a733e45de0fef412ad92).
- Commit triển khai CP3 đã push trên nhánh cá nhân: [b66657a](https://github.com/congnt180263/K5-L3B-DAY03-E3-ResearchAgentToolEval/commit/b66657a6ac9f11aa5a73b079d27d3a06799369b4).
- Rà soát đồng bộ báo cáo nhóm và metadata version log bằng các run JSON đã lưu. Các mục còn thiếu bằng chứng runtime được ghi rõ trong phần chờ kiểm chứng của báo cáo nhóm.
- AI/công cụ đã dùng và cách tự kiểm tra kết quả: Codex hỗ trợ triển khai, viết test và soạn báo cáo. Đối chiếu ví dụ trong TOOL.md với các assert đầu ra, kiểm tra đăng ký và chạy lại `python -m pytest -v` từ `starter_v0`.

## 5. Tự đánh giá

Phần triển khai CP3 đạt mục tiêu loại URL trùng mà vẫn giữ dữ liệu và thứ tự của các nguồn được chọn. Ba unit test đều PASS, gồm một trường hợp loại trùng và hai trường hợp lỗi đầu vào. Kiểm tra offline qua ResearchAgent xác nhận lời gọi đi qua registry và trả đúng kết quả cho ví dụ ba nguồn.

Giới hạn cần lưu ý là tool chỉ so sánh URL theo các quy tắc đã công bố. Hai URL khác query hoặc qua redirect vẫn có thể trỏ tới cùng nội dung. Các kiểm tra offline xác nhận logic xử lý và nhánh lỗi. Hai case G01/G09 trong run nhóm bổ sung bằng chứng định tuyến thành công trên Gemini. Phạm vi này chưa đo các URL redirect, nguồn có query khác nhau nhưng cùng nội dung hoặc trang phân biệt nội dung bằng fragment.
