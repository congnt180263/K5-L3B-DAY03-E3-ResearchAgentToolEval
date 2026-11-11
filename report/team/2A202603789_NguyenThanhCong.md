# Báo cáo cá nhân — Nguyễn Thành Công - 2A202603789

## 1. Thông tin thành viên

- Họ tên: Nguyễn Thành Công
- MSSV: 2A202603789
- Email: congc3c1@gmail.com
- GitHub: congnt180263
- Nhóm và lớp: E3 — L3B, VinUni AI20K K5

## 2. Phần việc phụ trách

- **CP2 — Tối ưu prompt và tool declaration v1–v3:** Quản lý `artifacts/system_prompt.md`, `artifacts/tools.yaml` và `artifacts/version_log.csv`. Thiết kế các giả thuyết cải tiến theo chu trình kiểm chứng khoa học, chạy base eval kiểm nghiệm qua từng vòng v0 → v1 → v2 → v3, đưa độ chính xác từ 0.65 lên 1.00 (20/20 test cases pass).
- **CP5 — UI, live chat và báo cáo:** Xây dựng giao diện web người dùng bằng Streamlit (`starter_v0/app.py`), thực hiện phiên tương tác trực tiếp (live chat) với agent để thu thập transcript quan sát hành vi hỏi xác nhận, và chủ trì biên soạn nội dung Báo cáo nhóm (`group_report.md`).

## 3. Đóng góp cụ thể

### Tối ưu prompt và tool declaration v1–v3 (CP2)
- **Phân tích lỗi baseline v0:** Dựa trên kết quả chạy baseline v0 (`runs/v0_...json`), phân loại và xác định nguyên nhân cốt lõi của 7 ca thất bại:
  - Lỗi vi phạm boundary: Agent tự ý gọi `send(confirmed=true)` khi người dùng chưa xác nhận (R12).
  - Lỗi thiếu thông tin: Tự suy đoán tài khoản (`sama`) hoặc URL tìm kiếm thay vì hỏi lại người dùng bằng `clarify` (R10, R11).
  - Lỗi trích xuất tham số: Điền dư thừa từ ngữ ("news", "today") vào tham số `query` của tool `lookup` (R03, M02, M06).
  - Lỗi định tuyến: Ép chạy trong 1 bước duy nhất của starter prompt dẫn đến thiếu tool gọi kèm (R13).
- **Vòng v0 → v1 (`artifacts/system_prompt.md`):** Loại bỏ toàn bộ các chỉ dẫn xấu cố ý trong starter prompt (ép giải quyết 1 bước, tự đoán mò URL/handle khi thiếu, tự gửi tin). Thiết lập quy tắc cốt lõi: bắt buộc gọi `clarify` khi thiếu thông tin quan trọng hoặc khi người dùng yêu cầu hành động ghi/gửi (`send`). Kết quả: độ chính xác tăng từ 0.65 lên 0.80 (16/20 pass).
- **Vòng v1 → v2 (`artifacts/tools.yaml`):** Viết lại chi tiết mô tả (`description`) cho từng tool, chỉ rõ khi nào nên dùng và khi nào KHÔNG nên dùng (phân định rõ ràng giữa `timeline` cho tài khoản cá nhân và `social_search` cho chủ đề thảo luận chung). Chuẩn hóa quy ước tham số: `query` chỉ lấy từ khóa chính (tránh thừa từ chỉ thời gian hay tính chất tin tức vì đã có `timeframe` và `topic`), `screenname` không chứa ký tự `@`. Kết quả: độ chính xác tăng từ 0.80 lên 0.90 (18/20 pass).
- **Vòng v2 → v3 (`artifacts/system_prompt.md`):** Khắc phục triệt để 2 lỗi còn lại từ v2:
  1. Quy định bắt buộc gọi `clarify` với tham số `response_type="yes_no"` khi xin xác nhận gửi/đăng nội dung ra kênh ngoài (`send`).
  2. Tối ưu hóa khả năng duy trì ngữ cảnh đa lượt (Multi-turn Context & Carryover): ghi nhớ thông tin từ các lượt trước (handle, limit, topic); khi người dùng đã cung cấp đủ thông tin thì lập tức gọi tool thực thi mà không lặp lại câu hỏi clarify. Kết quả: đạt độ chính xác tuyệt đối 20/20 (1.00).

### Xây dựng UI, Live Chat và Báo cáo (CP5)
- **Phát triển giao diện UI (`starter_v0/app.py`):** Xây dựng ứng dụng web tương tác bằng Streamlit:
  - Thiết kế luồng xử lý agent đa vòng, mặc định 4 vòng gọi tool mỗi lượt và cho phép chọn từ 1 đến 8 vòng trong sidebar.
  - Hiển thị trực quan từng bước gọi tool, tham số và kết quả phản hồi trung gian của tool.
  - Liệt kê câu hỏi mẫu trong A3 của báo cáo nhóm để người ngoài dùng thử qua ô nhập chat của UI.
  - Tích hợp cơ chế tự động ghi và xuất transcript JSON theo đúng cấu trúc tiêu chuẩn của bài lab.
- **Thực hiện phiên Live Chat thực tế:** Chạy phiên tương tác 4 lượt trực tiếp trên giao diện UI (`starter_v0/transcripts/ui_session_20261110T195845233289.transcript.json`), ghi nhận các hành vi sau:
  - Turn 1: Tra cứu tin tức AI hôm nay và tự động format thành bản tin chuyên mục.
  - Turn 2: Lấy tweet mới nhất của Elon Musk (tự động map tên sang handle).
  - Turn 3: Người dùng yêu cầu đăng Telegram → Agent kích hoạt guardrail, gọi `clarify(response_type="yes_no")` xin xác nhận.
  - Turn 4: Người dùng đồng ý → Agent gọi `send(confirmed=true)` kèm nội dung bản tin; tool trả RuntimeError do thiếu cấu hình Telegram.
  - C6 còn thiếu phiên thiếu thông tin nghiên cứu rồi người dùng bổ sung, cùng link UI đang hoạt động. Các mục này chờ bằng chứng thật.
- **Biên soạn Báo cáo nhóm (`group_report.md`):**
  - Trình bày Phần A (giới thiệu agent, danh mục tool, câu hỏi mẫu).
  - Lập bảng bằng chứng version B1, phân tích lỗi baseline B2, bằng chứng live chat B4, bảng nghiệm thu B5a.
  - Viết phần phản biện B6 (phân định phạm vi sửa giữa prompt và tools.yaml, các case cần con người đánh giá) và đúc kết các khó khăn kỹ thuật trong quá trình thực hiện.

## 4. Bằng chứng

- **Commits cá nhân trong lịch sử Git:**
  - `7c3f550`: baseeval v1 — tối ưu system_prompt.md lần đầu (v1).
  - `534ef4d`: baseline v2 — viết lại mô tả và quy ước tham số trong tools.yaml (v2).
  - `d259e4b`: baseline v3 — hoàn thiện quy tắc yes_no và multi-turn carryover (v3, đạt 20/20).
  - `fad5282` & `740cdca`: cập nhật log thử nghiệm và group_report.
  - `e194416`: xây dựng UI Streamlit `app.py`, thực hiện live chat session và trích xuất transcript JSON.
- **Tập tin bằng chứng:**
  - Prompt & tool configuration: [`starter_v0/artifacts/system_prompt.md`](../../starter_v0/artifacts/system_prompt.md), [`starter_v0/artifacts/tools.yaml`](../../starter_v0/artifacts/tools.yaml), [`starter_v0/artifacts/version_log.csv`](../../starter_v0/artifacts/version_log.csv).
  - Run JSON files: [`v0_...json`](../../starter_v0/runs/v0_B_base_gemini_20261110T180435443105.json), [`v1_...json`](../../starter_v0/runs/v1_B_base_gemini_20261110T185456303987.json), [`v2_...json`](../../starter_v0/runs/v2_B_base_gemini_20261110T191935420647.json), [`v3_...json`](../../starter_v0/runs/v3_B_base_gemini_20261110T192653298089.json).
  - Code UI và transcript: [`starter_v0/app.py`](../../starter_v0/app.py), [`starter_v0/transcripts/ui_session_20261110T195845233289.transcript.json`](../../starter_v0/transcripts/ui_session_20261110T195845233289.transcript.json).
  - Báo cáo nhóm: [`report/team/group_report.md`](group_report.md).
- **Công cụ hỗ trợ:** Antigravity (Gemini 3.8 Flash) hỗ trợ phân tích kết quả chạy và rà soát đối chiếu rubric.

## 5. Tự đánh giá

- CP2 có các run hợp lệ đạt 0.65 → 0.80 → 0.90 → 1.00. CP5 có code UI và transcript bốn lượt, còn chờ kịch bản thiếu thông tin rồi bổ sung và link UI để hoàn tất C6.
- Các vòng có log và bảng so sánh trước/sau. V3 cùng sửa boundary và carryover; run hiện tại đo tác động chung, nên chưa tách được đóng góp của từng sửa đổi theo yêu cầu một giả thuyết mỗi vòng.
- Giao diện UI trực quan, hoạt động ổn định và phục vụ tốt việc kiểm thử thực tế.
- Báo cáo nhóm và cá nhân được hoàn thiện đúng quy chuẩn, gắn liền với các bằng chứng kỹ thuật có thể kiểm chứng được trong repo.
