import streamlit as st


def show_html(fragment: str) -> None:
    """Render an HTML fragment without Markdown inserting extra blocks."""

    compact = "\n".join(line.strip() for line in fragment.splitlines() if line.strip())

    st.markdown(compact, unsafe_allow_html=True)
