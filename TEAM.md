# Team

## Thông tin nhóm

- Tên nhóm:E3
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-E3-ResearchAgentToolEval`
- URL repo, nhánh nộp, commit chốt: URL(https://github.com/congnt180263/K5-L3B-DAY03-E3-ResearchAgentToolEval), nhánh main, 

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 |Nguyễn Thành Công | 2A202603789 |congc3c1@gmail.com|congnt180263 | Quản lý System Prompt, Tool Declaration & Vòng lặp tối ưu v0 -> v3. Xây dựng UI,live chat và báo cáo       |
|   2 | Mai Xuân Khang | 2A202603722 | maixkhang2004@gmail.com | KhangMai123 | CP3 — New Tool & Unit Tests |
|   3 | Đồng Văn Quyến | 2A202603769 | 26ai.quyendv2@vinuni.edu.vn | dvquyen2609 | CP1 — Setup & Baseline v0, CP4 — Eval nhóm 10 case |
## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## HoVaTen-MSSV

### Phần việc phụ trách

-

### Đóng góp cụ thể

-

### Bằng chứng

-

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


