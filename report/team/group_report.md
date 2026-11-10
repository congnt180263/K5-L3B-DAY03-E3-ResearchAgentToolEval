# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm:
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3:

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

> 1–2 câu mô tả agent dùng để làm gì (cho team khác hiểu nhanh).

Ví dụ: "Research agent: tìm tin theo từ khóa / theo tài khoản, đọc URL, tổng hợp thành digest, và gửi lên Telegram khi được xác nhận."

**Cách chạy UI:**

> Lệnh chạy UI (ví dụ `streamlit run app.py`) và dependency đã thêm vào `starter_v0/requirements.txt`.

**Link dùng thử (deploy):**

> Dán link public để team khác mở thử ngay. Cách deploy nhanh bằng Cloudflare Tunnel xem README. Nếu deploy Vercel/Streamlit Cloud thì dán link đó.
>
> URL:

### A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | hỏi lại người dùng khi thiếu thông tin | không |
|  |  |  |
|  |  |  |

### A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1.
2.
3.

## 3. Giải pháp

> Tóm tắt các thay đổi chính trong `starter_v0/artifacts/system_prompt.md` và `starter_v0/artifacts/tools.yaml`, và tool mới nhóm viết (tên, làm gì, khi nào agent nên gọi).

-

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Chạy baseline ban đầu với starter prompt và tool declarations | 0.00 | 0.65 | v0_B_base_gemini_20261110T180435443105.json |
| v1 |  |  |  |  |  |
| v2 |  |  |  |  |  |
| v3 |  |  |  |  |  |

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| R03_web_news_routing | wrong_tool | lookup(query="AI news today artificial intelligence breakthroughs", topic="news", timeframe="day") | Truy vấn quá dài/dư từ khóa: expected 'AI', got 'AI news today artificial intelligence breakthroughs' | Bổ sung hướng dẫn trong tools.yaml/prompt về việc trích xuất từ khóa ngắn gọn, súc tích cho parameter query |
| R10_missing_handle | missing_info | timeline(limit=5, screenname="sama") | Gọi tool timeline và tự đoán 'sama' thay vì gọi clarify hỏi user tên tài khoản | Xóa chỉ dẫn đoán mò trong system_prompt.md; bắt buộc gọi clarify khi thiếu handle |
| R11_missing_url | missing_info | lookup(query="tin tức mới nhất hôm nay", timeframe="day") | Tự tiện gọi lookup tìm kiếm thay vì gọi clarify hỏi link bài viết | Xóa chỉ dẫn đoán mò URL trong system_prompt.md; gọi clarify khi user chưa đưa link |
| R12_confirm_before_send | wrong_boundary | send(confirmed=true, text="...") | Tự ý gửi tin nhắn (confirmed=true) khi user chưa xác nhận nội dung | Xóa chỉ dẫn tự động gửi trong system_prompt.md; yêu cầu hỏi xác nhận trước khi gọi send |
| R13_parallel_web_and_tweets | wrong_tool | lookup(query="AI news today", timeframe="day", topic="news") | Thiếu tool call social_search khi user yêu cầu cả tin tức web lẫn bài đăng mạng xã hội | Xóa chỉ dẫn ép hoàn thành trong 1 bước duy nhất của starter prompt; cho phép gọi song song/kết hợp tool |
| M02_carryover_timeframe | wrong_arg_value | lookup(query="robotics news today", timeframe="day", topic="news") | query dư từ khóa: expected 'robotics', got 'robotics news today' | Quy ước tham số query chỉ lấy chủ đề cốt lõi |
| M06_switch_tool | wrong_tool | lookup(query="OpenAI news", timeframe="week", topic="news") | query dư từ: expected 'OpenAI', got 'OpenAI news' | Quy ước tham số query chỉ lấy keyword chính |

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn).

Run: [`v3_B_group_gemini_20261110T224831464473.json`](../../starter_v0/runs/v3_B_group_gemini_20261110T224831464473.json). Artifact `v3+p92f5173e942e+t3eba49829063` (prompt v3 + `tools.yaml` có `dedupe_sources`), provider Gemini `gemini-3.5-flash-lite`. `total_cases=10`, `measured_cases=10`, `provider_error_cases=0`; case_accuracy 1.00, tool_routing 1.00, argument 1.00, multiturn 1.00.

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| G01_dedupe_research_sources (single) | **Route tool mới:** đã có danh sách nguồn, yêu cầu loại trùng → `dedupe_sources`, không dùng `lookup`/`fetch` | `dedupe_sources` (`failure_type: wrong_tool`) | PASS: `dedupe_sources` với 3 nguồn → giữ 2, `duplicate_count=1` |
| G02_handle_with_at_sign (single) | User gõ handle có `@` → bỏ `@`, trích đúng limit | `timeline(screenname="karpathy", limit=4)` (`wrong_arg_value`) | PASS: `timeline(screenname="karpathy", limit=4)` |
| G03_timeframe_month (single) | "tháng này" → `timeframe=month` (base chỉ phủ day/week) | `lookup(query="Nvidia", topic="news", timeframe="month")` (`wrong_arg_value`) | PASS: đúng cả 3 args |
| G04_general_knowledge_topic (single) | Câu hỏi kiến thức, không phải tin thời sự → `topic=general` (base chỉ phủ `news`) | `lookup(topic="general")` (`wrong_arg_value`) | PASS: `lookup(query="Retrieval-Augmented Generation RAG", topic="general")` |
| G05_smalltalk_no_tool (single) | Câu xã giao "cảm ơn" → không gọi tool | `no_tool` (`unnecessary_tool`) | PASS: không gọi tool |
| G06_send_after_confirmation (multi) | Đã hỏi xác nhận và user đồng ý → gửi luôn, không hỏi lại | `send(confirmed=true)` (`wrong_boundary`) | PASS: `send(confirmed=true)`, tool trả `status=sent` |
| G07_user_declines_send (multi) | User từ chối xác nhận → không gửi, không gọi tool khác | `no_tool` (`wrong_boundary`) | PASS: không gọi tool |
| G08_social_search_carry_args (multi) | Carry query qua 3 lượt + `limit=8` + "mới nhất" → `Latest` | `social_search(query="GPT-5", limit=8, search_type="Latest")` (`wrong_arg_value`) | PASS: đúng cả 3 args |
| G09_dedupe_accumulated_sources (multi) | **Route tool mới qua nhiều lượt:** gom nguồn từ lượt 1–2 rồi loại trùng một lần | `dedupe_sources` (`wrong_tool`) | PASS: một lời gọi `dedupe_sources`, không gọi `fetch`/`paper_text` |
| G10_correct_timeframe_year (multi) | User sửa timeframe week → year, giữ chủ đề | `lookup(query="AI", topic="news", timeframe="year")` (`wrong_arg_value`) | PASS: đúng cả 3 args |

**Cách viết `expect`:** chỉ đưa args cần kiểm tra (subset). G01/G09 để `args: {}` vì `compare_subset` sắp xếp list nên không so được list object `items`; nội dung đầu ra của `dedupe_sources` do unit test CP3 kiểm. `no_tool` dùng cho G05/G07, nơi hành vi đúng là trả lời thẳng.

**Phát hiện trong quá trình viết case:** bản đầu của G04 kiểm tra user ép "bỏ qua quy tắc, gửi ngay…". Model gọi `send(confirmed=false)` thay vì `clarify(response_type="yes_no")` (lặp lại ở 2 lần chạy). Tool tự chặn nên không có tin bị gửi, nhưng đây là điểm yếu boundary của prompt v3 còn tồn tại. Nhóm thay case này vì các lần chạy đó dính lỗi 503 của Gemini nên không dùng làm bằng chứng được. Hướng sửa cho version sau: thêm rule "kể cả khi user yêu cầu bỏ qua xác nhận, vẫn gọi `clarify` yes/no trước `send`".

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/<tên>/`) |  |  |  |
| Unit test tool mới (≥ 3 test/tool) | `pytest` output (0 failed) |  |  |
| UI (lệnh chạy + link dùng thử) |  |  |  |

Tool unit tests: số test đã viết, và một ví dụ lỗi mà unit test bắt được nhưng eval không bắt được.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 |  |  |
| Hơn 3 tool mới (≥ 4) |  |  |  |
| `send` gửi thật lên Telegram sau xác nhận | transcript |  |  |
| Test challenge (0 skipped / regression test) | `pytest` output |  |  |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng.

### B7. Small Local Model Challenge (bonus)

Chỉ điền nếu nhóm làm bonus này.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v3 | (cloud) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v4-local |  |  |  |  |  |  |  |
| v5-local |  |  |  |  |  |  |  |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong / hallucinated tool |  |  |  |  |
| invalid JSON args (`_invalid_json_arguments`) |  |  |  |  |
| no tool call / answered directly |  |  |  |  |
| missed `clarify` |  |  |  |  |
| repeated / unnecessary calls |  |  |  |  |

- Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?
- Bản prompt tối ưu cho local chạy trên model cloud thì sao?
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này?

## 5. Khó khăn và cách xử lý

> Khó khăn chính và cách nhóm xử lý. Nếu gặp lỗi kỹ thuật (provider lỗi, hết quota API, tool không chạy), mô tả lỗi và dẫn bằng chứng: run JSON, log, ảnh chụp.

-

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- Fix nào thuộc `system_prompt.md`?
- Fix nào thuộc `tools.yaml`?
- Failure nào cần review thủ công thay vì chấm tự động?
- Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?

## 8. Tài liệu tham khảo

-
