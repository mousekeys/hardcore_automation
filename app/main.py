import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import asyncio
from src.bridge import start_browser_bridge
from src.config_loader import get_config

config = get_config()

st.set_page_config(page_title="Hardcore Plus Dashboard", layout="wide")
st.title("Hardcore Plus Monitor")

if "logs" not in st.session_state:
    st.session_state.logs = []
if "cmd_queue" not in st.session_state:
    st.session_state.cmd_queue = asyncio.Queue()

log_area = st.empty()


async def log_to_ui(text: str):
    st.session_state.logs.append(text)
    if len(st.session_state.logs) > config.hardcore_plus.max_logs:
        st.session_state.logs.pop(0)
    log_area.code("\n".join(st.session_state.logs))



st.info(f"Target: {config.server.url}")
if st.button("Start Live Feed"):
    asyncio.run(start_browser_bridge(log_to_ui, st.session_state.cmd_queue))

# cmd = st.text_input("Console Command")
# if st.button("Execute"):
#     st.session_state.cmd_queue.put_nowait(cmd)