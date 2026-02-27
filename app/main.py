import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import asyncio
import threading
from queue import Queue
from src.bridge import start_browser_bridge
from src.config_loader import get_config

config = get_config()

st.set_page_config(page_title="Hardcore Plus Dashboard", layout="wide")
st.title("Hardcore Plus Monitor")

if "logs" not in st.session_state:
    st.session_state.logs = []
if "cmd_queue" not in st.session_state:
    st.session_state.cmd_queue = asyncio.Queue()

# Plain thread-safe queue — no Streamlit context needed
log_queue: Queue = Queue()
log_area = st.empty()


def run_bridge(cmd_queue):
    """Run the async bridge in a separate thread."""
    async def log_to_queue(text: str):
        log_queue.put(text)          # just put to queue, no Streamlit calls

    asyncio.run(start_browser_bridge(log_to_queue, cmd_queue))


with st.sidebar:
    st.info(f"Target: {config.server.url}")
    if st.button("Start Live Feed"):
        thread = threading.Thread(
            target=run_bridge,
            args=(st.session_state.cmd_queue,),
            daemon=True              # dies when app dies
        )
        thread.start()
        st.success("Bridge started!")

# Drain the log queue and update UI
while not log_queue.empty():
    text = log_queue.get_nowait()
    st.session_state.logs.append(text)
    if len(st.session_state.logs) > config.hardcore_plus.max_logs:
        st.session_state.logs.pop(0)

log_area.code("\n".join(st.session_state.logs))

# Auto refresh every second to pick up new logs
st.rerun() if st.button("Refresh logs") else None
