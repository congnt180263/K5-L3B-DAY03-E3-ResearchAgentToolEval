# Team

## Thông tin nhóm

- Tên nhóm:E3
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-E3-ResearchAgentToolEval`
- URL repo, nhánh nộp, commit chốt: https://github.com/congnt180263/K5-L3B-DAY03-E3-ResearchAgentToolEval, nhánh main (commit chốt: xem git HEAD) 

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Nguyễn Thành Công | 2A202603789 | 26ai.congnt3@vinuni.edu.vn | congnt180263 | Quản lý System Prompt, Tool Declaration & Vòng lặp tối ưu v0 -> v3. Xây dựng UI, live chat và báo cáo |
|   2 | Mai Xuân Khang | 2A202603722 | 26ai.khangmx@vinuni.edu.vn | KhangMai123 | CP3 — New Tool & Unit Tests |
|   3 | Đồng Văn Quyến | 2A202603769 | 26ai.quyendv2@vinuni.edu.vn | dvquyen2609 | CP1 — Setup & Baseline v0, CP4 — Eval nhóm 10 case |
## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## Nguyễn Thành Công — 2A202603789

### Phần việc phụ trách

- Quản lý System Prompt, Tool Declaration & Vòng lặp tối ưu v0 -> v3 (CP2).
- Xây dựng giao diện UI (Streamlit), thực hiện phiên kiểm thử Live Chat thực tế và lập báo cáo nhóm / cá nhân (CP5).

### Đóng góp cụ thể

- Phân tích nguyên nhân lỗi ở baseline v0, loại bỏ triệt để các hướng dẫn xấu của starter prompt, thiết lập guardrail yêu cầu `clarify` khi thiếu thông tin hoặc xin xác nhận trước khi thực hiện hành động ghi/gửi (`send`).
- Viết lại toàn bộ mô tả trong `tools.yaml` (nêu rõ khi nào nên/không nên dùng), chuẩn hóa quy ước tham số (`query` chỉ lấy từ khóa chính, `screenname` không chứa ký tự `@`).
- Tối ưu hóa phản hồi xác nhận với `response_type="yes_no"` và khả năng carryover ngữ cảnh đa lượt (multi-turn), giúp agent đạt độ chính xác tuyệt đối 20/20 (1.00) ở phiên bản v3.
- Xây dựng giao diện web tương tác `starter_v0/app.py` bằng Streamlit hỗ trợ gọi tool đa vòng, giao diện chat thân thiện và export transcript JSON. Thực hiện phiên live chat thực tế kiểm chứng rào chắn an toàn.
- Tổng hợp và hoàn thiện báo cáo nhóm `group_report.md` và báo cáo cá nhân.

### Bằng chứng

- [Báo cáo cá nhân](report/team/2A202603789_NguyenThanhCong.md)
- [Báo cáo nhóm](report/team/group_report.md)
- Các file cấu hình: [system_prompt.md](starter_v0/artifacts/system_prompt.md), [tools.yaml](starter_v0/artifacts/tools.yaml), [version_log.csv](starter_v0/artifacts/version_log.csv)
- Các run logs: `starter_v0/runs/v0_...json` đến `starter_v0/runs/v3_...json`
- Ứng dụng UI [app.py](starter_v0/app.py) và [transcript live session](starter_v0/transcripts/ui_session_20261110T195845233289.transcript.json)

## Mai Xuân Khang — 2A202603722

### Phần việc phụ trách

- **CP3 — Tool mới và unit test:** Thiết kế, triển khai tool offline `dedupe_sources` để loại nguồn nghiên cứu trùng URL; viết hợp đồng `TOOL.md`, đăng ký trong `tools/__init__.py` và bổ sung declaration vào `artifacts/tools.yaml`.
- Viết ba unit test cho tool mới, kiểm tra contract và khả năng thực thi qua `ResearchAgent`; tổng hợp bằng chứng CP3 trong bảng B5a và báo cáo cá nhân.
- Chuẩn bị case định tuyến G01 để bàn giao cho CP4, phối hợp đối chiếu kết quả G01/G09 trong run nhóm và rà soát tính nhất quán của báo cáo, version log.

### Đóng góp cụ thể

- **Thiết kế và triển khai tool `dedupe_sources` (CP3).** Rà soát các tool có sẵn và bổ sung bước lọc nguồn trùng cho danh sách đã thu thập trước khi tổng hợp hoặc trích dẫn. Tool nhận danh sách đối tượng JSON chứa URL HTTP(S) tuyệt đối, trả các mục được giữ và số nguồn trùng `duplicate_count`. Khi so sánh, tool chuẩn hóa host, cổng mặc định và fragment; giữ nguyên URL, metadata của bản xuất hiện đầu tiên cùng thứ tự tương đối của các nguồn. Tool chạy bằng Python standard library, không cần API key, không gọi mạng và không ghi file.
- **Xây dựng hợp đồng và đăng ký tool.** Hoàn thiện `tools/dedupe_sources/TOOL.md` với frontmatter, mục đích, điều kiện sử dụng, tham số, ví dụ input/output và giới hạn. Import hàm, đăng ký đúng tên trong `TOOL_FUNCTIONS` và thêm JSON Schema vào `tools.yaml`. Phần tích hợp trên nền CP2 v3 giữ các khai báo tool cũ và cho phép Agent thực thi tool mới qua registry có sẵn.
- **Kiểm tra dữ liệu đầu vào và xử lý lỗi.** Kiểm tra kiểu danh sách, dữ liệu JSON, trường URL và cổng HTTP(S). Trường hợp sai dữ liệu trả error dict với `tool`, `error` và `message`. Nếu lỗi xuất hiện sau một mục hợp lệ, tool trả lỗi thay vì trả danh sách lọc dở dang. Giới hạn được ghi rõ gồm giữ nguyên query, không theo redirect và coi các URL chỉ khác fragment là cùng nguồn.
- **Viết ba unit test thực tế.** Thay ba stub dành cho tool mới trong `tests/test_tools_todo.py` bằng test chạy qua registry. Happy path kiểm tra loại URL trùng, giữ bản đầu tiên và thứ tự, bảo toàn đầu vào và giữ nguồn có query khác. Test sai kiểu kiểm tra chuỗi thay cho danh sách trả `TypeError` dạng dict. Test nhánh lỗi kiểm tra URL thứ hai có cổng `99999` trả `ValueError` đúng vị trí, không làm crash lời gọi.
- **Thực hiện kiểm thử và nghiệm thu CP3.** Contract tests đạt 60 PASS. Ba test mới đạt 3 PASS, 0 FAIL, 0 SKIP. Toàn suite đạt 70 PASS, 0 FAIL và 14 SKIP ở các stub tool cũ. Kiểm tra offline qua `ResearchAgent` với provider thử xác nhận lời gọi `dedupe_sources` đi qua registry, nhận 3 nguồn, giữ 2 và đếm 1 nguồn trùng.
- **Phối hợp tích hợp vào CP4.** Chuẩn bị case single-turn `G01_dedupe_research_sources` và bàn giao để thành viên phụ trách CP4 tích hợp vào bộ 10 case. Đối chiếu run nhóm `v3_B_group_gemini_20261110T224831464473.json` trên Gemini `gemini-3.5-flash-lite`, đo đủ 10/10 case và không lỗi provider. G01 giữ 2 trong 3 nguồn; G09 do CP4 bổ sung giữ 3 trong 4 nguồn. Hai case đều PASS và có `duplicate_count=1`.
- **Hoàn thiện báo cáo và bằng chứng đóng góp.** Viết báo cáo cá nhân đúng mẫu, bổ sung danh mục tool ở A2, mô tả giải pháp và bảng B5a trong báo cáo nhóm. Tích hợp CP3 lên nền `main` có CP2 v3, đối chiếu đường dẫn run, hash artifact và kết quả thực tế để đồng bộ version log cùng các nhận xét báo cáo. Nội dung còn thiếu phiên chạy được ghi rõ trạng thái chờ kiểm chứng.

### Bằng chứng

- [Báo cáo cá nhân CP3](report/team/2A202603722_MaiXuanKhang.md) và [bảng B5a trong báo cáo nhóm](report/team/group_report.md#b5a-required-evidence--tool-mới-unit-test-ui).
- Mã nguồn và hợp đồng tool mới [tool.py](starter_v0/tools/dedupe_sources/tool.py), [TOOL.md](starter_v0/tools/dedupe_sources/TOOL.md).
- Khai báo và đăng ký [tools.yaml](starter_v0/artifacts/tools.yaml), [tools/__init__.py](starter_v0/tools/__init__.py).
- [Ba unit test CP3](starter_v0/tests/test_tools_todo.py) và [contract tests](starter_v0/tests/test_tool_contract.py).
- [Bộ eval nhóm](starter_v0/data/eval_group.json) và [run G01/G09](starter_v0/runs/v3_B_group_gemini_20261110T224831464473.json).
- Commit triển khai trên nhánh cá nhân [b66657a](https://github.com/congnt180263/K5-L3B-DAY03-E3-ResearchAgentToolEval/commit/b66657a6ac9f11aa5a73b079d27d3a06799369b4), commit tích hợp CP3 vào main [515b40f](https://github.com/congnt180263/K5-L3B-DAY03-E3-ResearchAgentToolEval/commit/515b40fd9de1aaba9eb4a733e45de0fef412ad92) và commit đồng bộ bằng chứng [8774f5b](https://github.com/congnt180263/K5-L3B-DAY03-E3-ResearchAgentToolEval/commit/8774f5b519e7dec3c246a646223ec78fed4a62be).

## Đồng Văn Quyến — 2A202603769

### Phần việc phụ trách

- **CP1 — Setup và baseline v0:** thực thi kiểm thử baseline v0 (`runs/v0_...json`); tổng hợp và phân loại chi tiết 7 ca thất bại ban đầu để xây dựng Bảng B2 (Failure Analysis) trong Báo cáo nhóm.
- **CP4 — Eval nhóm 10 case:** Thiết kế, xây dựng và chuẩn hóa bộ đánh giá nhóm `starter_v0/data/eval_group.json` gồm đúng 10 case (5 single-turn và 5 multi-turn) bao phủ các trường hợp mà bộ base chưa có; kiểm thử định tuyến tới tool mới `dedupe_sources`; thực thi suite eval nhóm đạt độ chính xác 10/10 (1.00) và tổng hợp Bảng B3 trong `report/team/group_report.md`.

### Đóng góp cụ thể

- **Setup môi trường và phân tích Baseline v0 (CP1):**
  - Cấu hình môi trường `.env`, kiểm tra preflight và contract test (`pytest tests/test_tool_contract.py` pass 60/60).
  - Chạy baseline v0 đạt 13/20 (0.65), `provider_error_cases == 0`.
  - Phân loại chi tiết 7 ca thất bại (lỗi ranh giới an toàn R12, thiếu thông tin R10/R11, sai tham số R03/M02/M06, sai tool R13) và tổng hợp vào Bảng B2 (Failure Analysis) của `group_report.md`.
- **Thiết kế và đánh giá bộ Test Cases nhóm (CP4):**
  - Thiết kế đủ 10 case trong `starter_v0/data/eval_group.json` (5 single-turn, 5 multi-turn) mở rộng các khía cạnh: định tuyến tool mới `dedupe_sources` (G01, G09), xử lý tiền tố `@` trong handle (G02), mở rộng timeframe `month`/`year` (G03, G10), câu hỏi kiến thức nền tảng topic `general` (G04), nhận diện câu xã giao không gọi tool (G05), và kiểm tra rào chắn gửi/hủy sau xác nhận (G06, G07).
  - Chạy nghiệm thu chính thức với kết quả tuyệt đối 10/10 PASS (1.00) và lập Bảng B3 (Team Eval Cases) trong `group_report.md`.

### Bằng chứng

- [Báo cáo cá nhân](report/team/2A202603769_DongVanQuyen.md)
- [Bộ test case nhóm 10 case](starter_v0/data/eval_group.json)
- Run baseline v0: [`runs/v0_B_base_gemini_20261110T180435443105.json`](starter_v0/runs/v0_B_base_gemini_20261110T180435443105.json)
- Run eval nhóm CP4: [`runs/v3_B_group_gemini_20261110T224831464473.json`](starter_v0/runs/v3_B_group_gemini_20261110T224831464473.json)
- Báo cáo nhóm: [Bảng B2](report/team/group_report.md#b2-failure-analysis) và [Bảng B3](report/team/group_report.md#b3-team-eval-cases)


