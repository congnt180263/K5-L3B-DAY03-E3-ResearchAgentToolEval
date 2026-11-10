# Team

## Thông tin nhóm

- Tên nhóm:E3
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-E3-ResearchAgentToolEval`
- URL repo, nhánh nộp, commit chốt: https://github.com/congnt180263/K5-L3B-DAY03-E3-ResearchAgentToolEval, nhánh main (commit chốt: xem git HEAD) 

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Nguyễn Thành Công | 2A202603789 | congc3c1@gmail.com | congnt180263 | Quản lý System Prompt, Tool Declaration & Vòng lặp tối ưu v0 -> v3. Xây dựng UI, live chat và báo cáo |
|   2 | Mai Xuân Khang | 2A202603722 | maixkhang2004@gmail.com | KhangMai123 | CP3 — New Tool & Unit Tests |
|   3 |        | 2A202603769 |       | dvquyen2609 | CP1 — Setup & Baseline v0, CP4 — Eval nhóm 10 case |
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
