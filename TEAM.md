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

- CP3 — Tool mới, hợp đồng và unit test offline.

### Đóng góp cụ thể

- Bổ sung `dedupe_sources`, đăng ký tool và viết ba unit test. Thêm một case định tuyến để bàn giao cho CP4.

### Bằng chứng

- [Báo cáo CP3](report/team/2A202603722_MaiXuanKhang.md) và [kết quả kiểm thử](report/team/group_report.md#b5a-required-evidence--tool-mới-unit-test-ui).

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


