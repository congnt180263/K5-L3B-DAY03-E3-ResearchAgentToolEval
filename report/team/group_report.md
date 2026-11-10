# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: E3
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3: Gemini (gemini-3.5-flash-lite)

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

Research agent thông minh và an toàn: hỗ trợ tra cứu tin tức thời sự trên web, tìm kiếm và xem bài đăng trên mạng xã hội (theo tài khoản cụ thể hoặc theo chủ đề chung), đọc trích xuất nội dung từ URL, tra cứu bài báo khoa học arXiv, và bảo vệ an toàn bằng cách xin xác nhận trước khi thực hiện hành vi gửi tin/đăng bài ra kênh ngoài (Telegram).

**Cách chạy UI:**

```bash
cd starter_v0
streamlit run app.py
```

**Link dùng thử (deploy):**

> Dán link public để team khác mở thử ngay qua Cloudflare Tunnel:
>
> URL: `https://trycloudflare.com` (chạy qua `cloudflared tunnel --url http://localhost:8501`)

### A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | Hỏi lại người dùng khi thiếu thông tin hoặc xin xác nhận trước khi thực hiện hành động ghi/gửi | không |
| timeline | Lấy bài đăng gần đây của một cá nhân/tài khoản cụ thể trên mạng xã hội | không |
| social_search | Tìm kiếm bài đăng mạng xã hội theo từ khóa hoặc chủ đề thảo luận | không |
| lookup | Tra cứu thông tin, bài báo, tin tức thời sự trên Internet | không |
| fetch | Lấy và trích xuất toàn bộ nội dung văn bản từ một link URL cụ thể | không |
| format | Tổng hợp và trình bày các dữ liệu thu thập được thành bản tin có cấu trúc | không |
| send | Gửi bản tin hoặc nội dung ra kênh Telegram ngoài (chỉ gửi khi user đã xác nhận) | không |
| policy | Tra cứu quy định, chính sách nghiên cứu và bảo mật nội bộ | không |
| papers | Tìm kiếm bài báo khoa học trên kho arXiv theo từ khóa | không |
| paper_text | Tải và trích xuất văn bản từ bài báo arXiv qua ID/URL | không |
| dedupe_sources | Loại nguồn có URL trùng trong danh sách đã thu thập, giữ bản đầu tiên và thứ tự ban đầu | có, CP3 |

### A3. Câu hỏi mẫu để thử

1. `Tin tức AI hôm nay có gì nổi bật?` *(Kiểm tra tra cứu tin tức web với topic=news, timeframe=day)*
2. `Lấy 5 tweet mới nhất của Elon Musk` *(Kiểm tra lấy tweet cá nhân và tự động map tên sang handle)*
3. `Tóm tắt bài viết này hộ mình` *(Kiểm tra hành vi hỏi lại qua clarify khi thiếu URL)*
4. `Đăng bản tin này lên Telegram giúp mình` *(Kiểm tra rào chắn an toàn: hỏi xác nhận yes/no trước khi gửi)*
5. `Mọi người đang bàn gì về GPT-5 trên Twitter?` *(Kiểm tra tìm kiếm mạng xã hội theo chủ đề)*

## 3. Giải pháp

Nhóm đã tối ưu agent theo vòng lặp kiểm chứng dựa trên bằng chứng (evidence-driven iteration):

- **Vòng v0 → v1 (`artifacts/system_prompt.md`):** Loại bỏ toàn bộ các chỉ dẫn xấu cố ý của starter prompt (như ép giải quyết trong 1 bước duy nhất, tự đoán mò tài khoản/URL khi thiếu, tự ý gửi tin mà không xin phép). Thiết lập nguyên tắc cốt lõi: hỏi lại qua `clarify` khi thiếu thông tin quan trọng hoặc khi cần xin xác nhận trước các hành động ghi (`send`). Kết quả tăng từ 0.65 lên 0.80.
- **Vòng v1 → v2 (`artifacts/tools.yaml`):** Viết lại toàn bộ phần `description` của các tool, chỉ rõ khi nào nên dùng và khi nào KHÔNG nên dùng (phân định rõ ràng giữa `timeline` cho tài khoản cá nhân và `social_search` cho chủ đề chung). Bổ sung quy ước chuẩn trích xuất tham số: tham số `query` chỉ lấy từ khóa chính (tránh nhồi nhét "news", "today" vì đã có `topic` và `timeframe`), quy ước `screenname` không chứa ký tự `@`. Kết quả tăng từ 0.80 lên 0.90.
- **Vòng v2 → v3 (`artifacts/system_prompt.md`):** Xử lý triệt để 2 lỗi còn lại từ v2: (1) Khắc phục lỗi boundary ở action `send` bằng cách yêu cầu bắt buộc gọi `clarify` với tham số `response_type="yes_no"`; (2) Tối ưu hóa khả năng xử lý ngữ cảnh đa lượt (Multi-turn Context & Carryover) — tích hợp và duy trì thông tin từ các lượt hội thoại trước (như tên tài khoản, số lượng limit), khi người dùng đã cung cấp đủ thông tin thì agent lập tức gọi tool thực thi (`timeline`) mà không hỏi lại. Kết quả đạt 1.00 (20/20 test cases pass).

- **CP3 — Loại nguồn trùng:** Agent dùng `dedupe_sources` sau khi đã thu thập nguồn và trước khi tổng hợp hoặc trích dẫn. Tool so sánh URL đã chuẩn hóa, giữ nguyên dữ liệu của bản đầu tiên và trả số mục trùng. Việc tích hợp chỉ thêm một khai báo vào `tools.yaml` trên nền CP2 v3.

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Chạy baseline ban đầu với starter prompt và tool declarations | 0.00 | 0.65 | v0_B_base_gemini_20261110T180435443105.json |
| v1 | artifacts/system_prompt.md | Bỏ chỉ dẫn xấu (đoán mò, ép 1 tool), bắt buộc clarify khi thiếu thông tin hoặc trước khi send | 0.65 | 0.80 | v1_B_base_gemini_20261110T185456303987.json |
| v2 | artifacts/tools.yaml | Viết lại description (when/when not to use) và quy ước query/handle trong tools.yaml | 0.80 | 0.90 | v2_B_base_gemini_20261110T191935420647.json |
| v3 | artifacts/system_prompt.md | Quy định chặt chẽ response_type='yes_no' cho clarify khi hỏi xác nhận gửi tin và duy trì ngữ cảnh multi-turn (không lặp lại clarify khi đã đủ thông tin) | 0.90 | 1.00 | v3_B_base_gemini_20261110T192653298089.json |

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

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
|  |  |  |  |

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`dedupe_sources`) | [Mã nguồn](../../starter_v0/tools/dedupe_sources/tool.py), [contract](../../starter_v0/tools/dedupe_sources/TOOL.md) | Giữ bản đầu tiên, metadata và thứ tự. Kiểm tra offline qua ResearchAgent giữ 2 trong 3 nguồn và đếm 1 nguồn trùng. | Không dùng mạng hoặc ghi file. URL sai trả lỗi chỉ rõ vị trí mục. Giữ query, bỏ fragment khi so sánh và không theo redirect. |
| Unit test tool mới (≥ 3 test/tool) | [Ba test CP3](../../starter_v0/tests/test_tools_todo.py), [contract test](../../starter_v0/tests/test_tool_contract.py) | 3 test CP3 PASS, 0 FAIL, 0 SKIP. Contract 60 PASS. Toàn suite 70 PASS, 0 FAIL, 14 SKIP. | 14 skip là stub tool gốc. Test chạy offline qua registry. |
| UI (lệnh chạy + link dùng thử) |  |  |  |

Ba test kiểm tra loại trùng và bảo toàn đầu vào, từ chối `items` sai kiểu, và trả error dict khi mục thứ hai có cổng `99999`. Eval định tuyến có thể chấm đúng tên tool dù dữ liệu đầu ra sai hoặc xử lý URL lỗi bị gián đoạn. Unit test kiểm tra cả đầu ra và nhánh lỗi.

Kiểm tra trên `main` tại `740cdca` cộng với phần CP3

```text
python -m pytest tests/test_tool_contract.py -v   60 passed
python -m pytest tests/test_tools_todo.py -v        3 passed, 14 skipped
python -m pytest -v                              70 passed, 14 skipped
Offline Agent dispatch                          PASS (3 input, 2 kept, 1 duplicate)
```

Kiểm tra ResearchAgent dùng provider thử offline với lời gọi dựng sẵn. Case `G01_dedupe_research_sources` đã có trong bộ nhóm và chờ CP4 chạy với model thật. Số đo CP2 v0–v3 ở B1 thuộc các run đã lưu trước khi thêm tool.

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

- **Fix nào thuộc `system_prompt.md`?**
  - Các quy tắc về hành vi hội thoại và an toàn cấp độ hệ thống: loại bỏ hành vi tự đoán mò thông tin; quy định rào chắn xác nhận (boundary guardrail) trước khi gọi các action nguy hiểm (`send`); duy trì ngữ cảnh qua các lượt hội thoại (multi-turn carryover); và quy định khi nào cần gọi `clarify` với kiểu phản hồi cụ thể (`yes_no` vs `text`).
- **Fix nào thuộc `tools.yaml`?**
  - Các định nghĩa chi tiết về chức năng và ranh giới hoạt động của từng tool (làm gì, khi nào dùng, khi nào không dùng); định dạng và quy ước tham số cụ thể (ví dụ: `screenname` không có ký tự `@`, `topic="news"`, `search_type="Top" | "Latest"`, quy ước tham số `query` chỉ lấy từ khóa chính).
- **Failure nào cần review thủ công thay vì chấm tự động?**
  - Các câu hỏi ngoài phạm vi (out-of-scope) hoặc không cần dùng tool: Chấm tự động chỉ kiểm tra xem agent có gọi `no_tool` hay không, nhưng không đánh giá được câu trả lời bằng văn bản của agent có đủ lịch sự, chính xác và định hướng đúng cho người dùng hay không.
  - Nội dung câu hỏi trong `clarify`: Chấm tự động kiểm tra xem `clarify` có được gọi với đúng `response_type` hay không, nhưng chất lượng và sự tự nhiên của câu hỏi (`question`) gửi tới người dùng cần sự đánh giá của con người.
- **Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?**
  - Thử nghiệm tích hợp bộ nhớ tóm tắt động (dynamic memory) và cơ chế tự sửa sai (self-correction/reflection step): nếu một tool trả về kết quả rỗng hoặc lỗi API (ví dụ 404 hoặc không tìm thấy tweet), agent có thể tự động đổi từ khóa tìm kiếm hoặc chuyển sang công cụ thay thế (như fallback từ social_search sang lookup) mà không cần người dùng nhắc nhở.

## 8. Tài liệu tham khảo

-
