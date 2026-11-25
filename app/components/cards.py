from html import escape

import streamlit as st

from components.render import show_html


def page_header(eyebrow: str, title: str, description: str) -> None:
    show_html(
        f"""
        <div class="mp-pagehead">
            <div class="mp-eyebrow">{escape(eyebrow)}</div>
            <h1 class="mp-h1">{escape(title)}</h1>
            <p class="mp-lede">{escape(description)}</p>
        </div>
        """
    )


def section_heading(title: str, caption: str = "") -> None:
    caption_html = f'<p class="mp-caption">{escape(caption)}</p>' if caption else ""
    show_html(
        f"""
        <div class="mp-section">
            <h2>{escape(title)}</h2>
            {caption_html}
        </div>
        """
    )


def kpi_row(items: list[tuple[str, str, str]]) -> None:
    columns = st.columns(len(items), gap="small")
    for column, (label, value, note) in zip(columns, items, strict=False):
        with column:
            show_html(
                f"""
                <div class="mp-kpi">
                    <div class="mp-kpi-label">{escape(label)}</div>
                    <div class="mp-kpi-value">{escape(value)}</div>
                    <div class="mp-kpi-note">{escape(note)}</div>
                </div>
                """
            )


def callout(title: str, body: str) -> None:
    show_html(
        f"""
        <div class="mp-callout">
            <div class="mp-kicker">{escape(title)}</div>
            <p>{escape(body)}</p>
        </div>
        """
    )


def finding(kind: str, title: str, body: str) -> None:
    label = {
        "observed": "OBSERVED FINDING",
        "statistical": "STATISTICAL FINDING",
        "recommendation": "RECOMMENDATION",
        "limitation": "LIMITATION",
    }[kind]
    show_html(
        f"""
        <div class="mp-finding mp-{kind}">
            <div class="mp-kicker">{label}</div>
            <h3>{escape(title)}</h3>
            <p>{escape(body)}</p>
        </div>
        """
    )


def stat_grid(items: list[tuple[str, str]]) -> None:
    cells = "".join(
        f"<div class='mp-stat'><span>{escape(label)}</span><strong>{escape(value)}</strong></div>"
        for label, value in items
    )
    show_html(f"<div class='mp-statgrid'>{cells}</div>")


def page_footer() -> None:
    show_html(
        """
        <div class="mp-foot">
            ChronoTunnel · Urban Mobility Intelligence · Historical records, 2020–2024.
            Transfers are included in ridership and are not added again.
        </div>
        """
    )
