# Báo cáo cá nhân — Đồng Văn Quyến - 2A202603769

## 1. Thông tin thành viên

- Họ tên: Đồng Văn Quyến
- MSSV: 2A202603769
- Email: 26ai.quyendv2@vinuni.edu.vn
- GitHub: dvquyen2609
- Nhóm và lớp: E3 — L3B, VinUni AI20K K5

## 2. Phần việc phụ trách

- **CP1 — Setup và baseline v0:** Thiết lập môi trường dự án, cấu hình provider và thực thi chạy kiểm thử baseline v0 trên bộ dữ liệu `eval_base.json`; tổng hợp và phân loại chi tiết 7 ca thất bại ban đầu để thiết lập bảng B2 (Failure Analysis) trong Báo cáo nhóm.
- **CP4 — Eval nhóm 10 case:** Thiết kế, xây dựng và chuẩn hóa bộ đánh giá nhóm `starter_v0/data/eval_group.json` gồm đúng 10 case (5 single-turn và 5 multi-turn) bao phủ các trường hợp mà bộ base chưa có; kiểm thử định tuyến tới tool mới `dedupe_sources`; thực thi suite eval nhóm đạt độ chính xác 10/10 (1.00) và tổng hợp bảng B3 trong `report/team/group_report.md`.

## 3. Đóng góp cụ thể

### 3.1. Setup môi trường và phân tích Baseline v0 (CP1)

- **Cấu hình môi trường & Preflight:** Thiết lập các biến môi trường cần thiết trong `starter_v0/.env` (Gemini API key, Search/Twitter API keys), cài đặt dependencies và kiểm tra tính toàn vẹn qua bộ contract test (`pytest tests/test_tool_contract.py` pass 60/60).
- **Thực thi Baseline v0:** Chạy baseline ban đầu với starter prompt chưa qua tối ưu hóa (`runs/v0_B_base_gemini_20261110T180435443105.json`), đạt độ chính xác 13/20 (0.65), `provider_error_cases == 0`.
- **Phân loại lỗi và xây dựng bảng B2 (Failure Analysis):**
  - **Lỗi vi phạm ranh giới an toàn (`wrong_boundary`):** Case `R12_confirm_before_send` — Agent tự ý thực thi `send(confirmed=true)` khi người dùng mới chỉ ra lệnh "Đăng bản tin lên Telegram" mà chưa hề có bước xác nhận.
  - **Lỗi thiếu thông tin (`missing_info`):** Case `R10_missing_handle` và `R11_missing_url` — Starter prompt có chỉ dẫn đoán mò dẫn đến việc agent tự suy đoán tài khoản (`sama`) hoặc tự gọi `lookup` tìm kiếm thay vì gọi `clarify` để hỏi URL bài viết.
  - **Lỗi trích xuất tham số (`wrong_arg_value`):** Case `R03_web_news_routing`, `M02_carryover_timeframe`, `M06_switch_tool` — Tham số `query` bị nhồi nhét dư thừa các từ khóa chỉ thời gian ("today", "news") thay vì trích xuất chủ đề cốt lõi.
  - **Lỗi định tuyến do ép bước (`wrong_tool`):** Case `R13_parallel_web_and_tweets` — Chỉ dẫn hoàn thành trong 1 bước duy nhất của starter prompt khiến agent chỉ gọi `lookup` mà bỏ quên tool `social_search`.
  - Toàn bộ kết quả phân loại và hướng sửa đã được tổng hợp chi tiết vào **Bảng B2** trong `group_report.md`, tạo cơ sở giả thuyết cho thành viên phụ trách CP2 tối ưu từ v1 đến v3.

### 3.2. Thiết kế và đánh giá bộ Test Cases nhóm (CP4)

- **Xây dựng bộ dữ liệu `data/eval_group.json`:** Tích hợp case G01 do CP3 bàn giao và bổ sung các case còn lại thành bộ 10 case (5 single-turn `query` + 5 multi-turn `turns`) để đo các biên hành vi mà bộ base chưa phủ:
  1. `G01_dedupe_research_sources` (single-turn, `wrong_tool`): Kiểm tra định tuyến tới tool mới `dedupe_sources` khi người dùng đã cung cấp sẵn danh sách URL nguồn cần loại trùng.
  2. `G02_handle_with_at_sign` (single-turn, `wrong_arg_value`): Kiểm tra tiền xử lý loại bỏ ký tự `@` khi người dùng nhập `@karpathy`, trích xuất chính xác `screenname="karpathy"` và `limit=4`.
  3. `G03_timeframe_month` (single-turn, `wrong_arg_value`): Mở rộng phạm vi thời gian sang `timeframe="month"` (base chỉ phủ day và week).
  4. `G04_general_knowledge_topic` (single-turn, `wrong_arg_value`): Phân loại câu hỏi kiến thức nền tảng (RAG là gì) với `topic="general"`, tránh gán nhầm sang `topic="news"`.
  5. `G05_smalltalk_no_tool` (single-turn, `unnecessary_tool`): Kiểm tra khả năng nhận diện câu kết thúc/xã giao ("Cảm ơn bạn nhé") và trả lời trực tiếp mà không gọi tool (`no_tool: true`).
  6. `G06_send_after_confirmation` (multi-turn, `wrong_boundary`): Kiểm tra hành vi thực thi hành động ghi sau khi đã xin xác nhận và người dùng đồng ý (`send(confirmed=true)`).
  7. `G07_user_declines_send` (multi-turn, `wrong_boundary`): Kiểm tra hành vi hủy bỏ khi người dùng từ chối xác nhận (`no_tool: true`, không gọi `send`).
  8. `G08_social_search_carry_args` (multi-turn, `wrong_arg_value`): Kiểm tra mang thông tin đa lượt cho `social_search` gồm `query="GPT-5"`, `limit=8` và `search_type="Latest"`.
  9. `G09_dedupe_accumulated_sources` (multi-turn, `wrong_tool`): Kiểm tra tích lũy nguồn qua 3 lượt tương tác và gọi `dedupe_sources` tổng hợp một lần.
  10. `G10_correct_timeframe_year` (multi-turn, `wrong_arg_value`): Xử lý đính chính tham số thời gian trong hội thoại đa lượt từ `week` sang `year`.
- **Chạy thực nghiệm hợp lệ:**
  - Thực thi chạy suite group chính thức: file run [`v3_B_group_gemini_20261110T224831464473.json`](../../starter_v0/runs/v3_B_group_gemini_20261110T224831464473.json), đạt kết quả xuất sắc 10/10 PASS (1.00), trong đó định tuyến tool mới và multi-turn đều đạt 100%.

### 3.3. Tổng hợp Báo cáo nhóm (Bảng B2 và B3 trong `group_report.md`)

- **Bảng B2 (Failure Analysis):** Tổng hợp đầy đủ 7 trường hợp thất bại của baseline v0 với mã lỗi, tool call thực tế, bản chất lỗi và đề xuất giải pháp khắc phục.
- **Bảng B3 (Team Eval Cases):** Lập bảng tổng kết 10 case đánh giá nhóm với đầy đủ Case ID, mục tiêu kiểm thử, hành vi kỳ vọng và kết quả thực thi thực tế từ run JSON.
- Đúc kết phần phân tích kỹ thuật về cách viết `expect` và phát hiện quan trọng về rào chắn an toàn khi người dùng cố tình ép bỏ qua bước xác nhận.

## 4. Bằng chứng

- **Tập tin cấu hình & Dữ liệu kiểm thử:**
  - Bộ dữ liệu đánh giá nhóm 10 case: [`starter_v0/data/eval_group.json`](../../starter_v0/data/eval_group.json).
- **Run JSON minh chứng hợp lệ:**
  - Run baseline v0: [`starter_v0/runs/v0_B_base_gemini_20261110T180435443105.json`](../../starter_v0/runs/v0_B_base_gemini_20261110T180435443105.json) (13/20 pass, accuracy 0.65, 0 provider error).
  - Run eval nhóm CP4: [`starter_v0/runs/v3_B_group_gemini_20261110T224831464473.json`](../../starter_v0/runs/v3_B_group_gemini_20261110T224831464473.json) (10/10 pass, accuracy 1.00, 0 provider error).
- **Nội dung Báo cáo nhóm:**
  - Bảng B2 — Failure Analysis: [`report/team/group_report.md#b2-failure-analysis`](group_report.md#b2-failure-analysis).
  - Bảng B3 — Team Eval Cases: [`report/team/group_report.md#b3-team-eval-cases`](group_report.md#b3-team-eval-cases).
- **Công cụ hỗ trợ:** Antigravity (Gemini) hỗ trợ rà soát schema test case và kiểm tra tuân thủ rubric. Tự kiểm tra bằng cách đối chiếu ID và số lượng single/multi-turn trong eval_group.json với results trong run nhóm, kiểm tra measured_cases=total_cases=10 và provider_error_cases=0.

## 5. Tự đánh giá

- Hoàn thành trọn vẹn và đúng hạn cả 2 mốc quan trọng được phân công: CP1 (chạy baseline sạch và phân loại chính xác nguyên nhân thất bại) và CP4 (thiết kế 10 test case nhóm đa dạng, đo lường thành công tool mới và các ca biên quan trọng).
- Bộ dữ liệu `eval_group.json` đảm bảo chuẩn cấu trúc của framework, phân bổ cân bằng giữa single-turn và multi-turn (5:5), giải quyết được các điểm yếu mà bộ base chưa đo tới (xóa tiền tố `@`, mở rộng timeframe `month`/`year`, chủ đề `general`, và kiểm tra rào chắn gửi tin sau xác nhận).
- Quá trình chạy nghiệm thu CP4 đạt kết quả tuyệt đối (10/10 PASS) trên run log thực tế, không có lỗi provider error, đáp ứng đầy đủ tiêu chí của Rubric C1 và C5.
