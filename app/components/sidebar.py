import streamlit as st

from components.render import show_html
from config import NAV_ITEMS, STUDY_END_YEAR, STUDY_START_YEAR


def render_sidebar() -> None:
    with st.sidebar:
        # ChronoTunnel brand — native navigation to landing page
        st.page_link(
            "Landing.py",
            label="ChronoTunnel",
            icon=":material/graphic_eq:",
            width="stretch",
        )

        # Brand subtitle
        show_html(
            """
            <div class="side-sub" style="padding: 0 0.75rem 1rem;">
                URBAN MOBILITY
            </div>
            <div class="side-label">WORKSPACE</div>
            """
        )

        # Dashboard navigation
        for path, label, icon in NAV_ITEMS:
            st.page_link(
                path,
                label=label,
                icon=icon,
                width="stretch",
            )

        # Landing page navigation
        st.page_link(
            "Landing.py",
            label="Landing page",
            icon=":material/arrow_back:",
            width="stretch",
        )

        # Study information
        show_html(
            f"""
            <div class="side-note">
                <div class="side-label">STUDY PERIOD</div>
                <strong>{STUDY_START_YEAR}–{STUDY_END_YEAR}</strong>
                <p>
                    Historical MTA ridership records.
                    This is not a live operations feed.
                </p>
            </div>
            """
        )


def mount_dashboard() -> None:
    from components.styles import inject_dashboard_styles

    inject_dashboard_styles()
    render_sidebar()
