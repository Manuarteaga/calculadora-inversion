import os
import streamlit as st

st.set_page_config(
    page_title="AssetAllocation Planner", page_icon="📈", layout="wide"
)

html_file_path = os.path.join(os.path.dirname(__file__), "index.html")
if os.path.exists(html_file_path):
    with open(html_file_path, "r", encoding="utf-8") as f:
        st.components.v1.html(f.read(), height=950, scrolling=True)
