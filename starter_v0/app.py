from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st

from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from chat import (
    run_model_tool_loop,
    trim_history,
    write_transcript,
    safe_slug,
    now_iso,
)
from versioning import artifact_version_dict, build_artifact_version

ROOT = Path(__file__).parent
ARTIFACTS_DIR = ROOT / "artifacts"
TRANSCRIPTS_DIR = ROOT / "transcripts"
load_lab_env(ROOT)

st.set_page_config(page_title="Research Agent UI", page_icon="🤖", layout="wide")


def init_session_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "raw_history" not in st.session_state:
        st.session_state.raw_history = []
    if "transcript_id" not in st.session_state:
        timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
        st.session_state.transcript_id = f"ui_session_{timestamp}"
    if "transcript_path" not in st.session_state:
        st.session_state.transcript_path = TRANSCRIPTS_DIR / f"{st.session_state.transcript_id}.transcript.json"
    if "turn_index" not in st.session_state:
        st.session_state.turn_index = 0
    if "transcript_data" not in st.session_state:
        st.session_state.transcript_data = None


init_session_state()

# --- Sidebar Controls ---
st.sidebar.title("⚙️ Cấu hình Agent")
provider_name = st.sidebar.selectbox(
    "Provider",
    ["openrouter", "openai", "anthropic", "gemini", "ollama"],
    index=0,
    help="Provider LLM được chọn để hoàn thành task.",
)
model_name = st.sidebar.text_input(
    "Model (Optional / để trống lấy mặc định)",
    value="",
    placeholder="e.g. meta-llama/llama-3.1-70b-instruct",
)
version_label = st.sidebar.text_input(
    "Version Artifact Label",
    value="v3",
    help="Phiên bản artifact đang test (v0, v1, v2, v3, ...)",
)
history_window = st.sidebar.slider("History Window (lượt)", min_value=1, max_value=10, value=5)
max_tool_rounds = st.sidebar.slider("Max Tool Rounds", min_value=1, max_value=8, value=4)

if st.sidebar.button("🧹 Xoá lịch sử chat", use_container_width=True):
    st.session_state.messages = []
    st.session_state.raw_history = []
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    st.session_state.transcript_id = f"ui_{safe_slug(version_label)}_{safe_slug(provider_name)}_{timestamp}"
    st.session_state.transcript_path = TRANSCRIPTS_DIR / f"{st.session_state.transcript_id}.transcript.json"
    st.session_state.turn_index = 0
    st.session_state.transcript_data = None
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 Thông tin bài lab")
st.sidebar.markdown(
    "- **Artifacts:** `system_prompt.md`, `tools.yaml`\n"
    "- **Transcripts:** Tự động ghi vào `transcripts/*.transcript.json`\n"
    "- **Hỗ trợ:** Clarification, multi-turn, tool execution"
)

# --- Title and Header ---
st.title("🤖 Research Agent Tool Eval — Live Demo")
st.caption(f"Đang chạy phiên bản **{version_label}** với Provider: `{provider_name}`")

# Load artifacts
prompt_path = ARTIFACTS_DIR / "system_prompt.md"
tools_path = ARTIFACTS_DIR / "tools.yaml"

if not prompt_path.exists() or not tools_path.exists():
    st.error("Không tìm thấy `artifacts/system_prompt.md` hoặc `artifacts/tools.yaml`!")
    st.stop()

system_prompt = prompt_path.read_text(encoding="utf-8")
tool_declarations = load_tool_declarations(tools_path)
openai_tools = to_openai_tools(tool_declarations)

try:
    provider = make_provider(provider_name)
except Exception as e:
    st.error(f"Lỗi khởi tạo provider `{provider_name}`: {e}")
    st.stop()

selected_model = model_name.strip() or getattr(provider, "default_model", None)
artifact_version = build_artifact_version(version_label, prompt_path, tools_path)

# Initialize transcript if not yet created
if st.session_state.transcript_data is None:
    st.session_state.transcript_data = {
        "transcript_id": st.session_state.transcript_id,
        **artifact_version_dict(artifact_version),
        "provider": provider_name,
        "model": selected_model,
        "system_prompt": str(prompt_path),
        "tools": str(tools_path),
        "history_window": history_window,
        "max_tool_rounds": max_tool_rounds,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "turns": [],
    }

# --- Hiển thị lịch sử chat ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("tool_events"):
            with st.expander("🛠️ Chi tiết Tool Calls & Kết quả", expanded=False):
                st.json(msg["tool_events"])

# --- Chat Input ---
if user_input := st.chat_input("Nhập câu hỏi hoặc yêu cầu research..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.turn_index += 1
    turn_record: dict[str, Any] = {
        "turn_index": st.session_state.turn_index,
        "started_at": now_iso(),
        "user": user_input,
        "status": "started",
        "assistant_text": None,
        "rounds": [],
        "tool_events": [],
    }

    messages = [
        {"role": "system", "content": system_prompt},
        *trim_history(st.session_state.raw_history, history_window),
        {"role": "user", "content": user_input},
    ]

    with st.chat_message("assistant"):
        with st.spinner("Agent đang suy nghĩ và thực thi tools..."):
            try:
                result = run_model_tool_loop(
                    provider=provider,
                    messages=messages,
                    tools=openai_tools,
                    model=selected_model,
                    max_tool_rounds=max_tool_rounds,
                )
                turn_record.update(result)
                assistant_text = result.get("assistant_text", "")
                st.markdown(assistant_text)

                tool_events = result.get("tool_events", [])
                if tool_events:
                    with st.expander("🛠️ Chi tiết Tool Calls & Kết quả", expanded=True):
                        st.json(tool_events)

                st.session_state.raw_history.append({"role": "user", "content": user_input})
                st.session_state.raw_history.append({"role": "assistant", "content": assistant_text})
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_text,
                    "tool_events": tool_events,
                })

            except Exception as exc:
                err_msg = f"{type(exc).__name__}: {str(exc)}"
                turn_record.update({"status": "provider_error", "error": err_msg})
                st.error(f"Lỗi: {err_msg}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"⚠️ Đã xảy ra lỗi: {err_msg}",
                })

        turn_record["ended_at"] = now_iso()
        st.session_state.transcript_data["turns"].append(turn_record)
        write_transcript(st.session_state.transcript_path, st.session_state.transcript_data)
        st.toast(f"Đã lưu transcript vào: {st.session_state.transcript_path.name}")

