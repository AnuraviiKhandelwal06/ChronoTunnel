import pandas as pd
import streamlit as st

from config import BOROUGH_ORDER, STUDY_END_YEAR, STUDY_START_YEAR


def year_selector(key: str = "year_filter") -> str | int:
    """Select a study year or all available years."""

    if STUDY_START_YEAR > STUDY_END_YEAR:
        raise ValueError("Invalid study period: start year exceeds end year.")

    options: list[str | int] = ["All years"] + list(
        range(STUDY_START_YEAR, STUDY_END_YEAR + 1)
    )

    return st.selectbox("Year", options, key=key)


def borough_selector(
    include_all: bool = True,
    key: str = "borough_filter",
) -> str:
    """Select a borough, optionally including all boroughs."""

    options = (["All boroughs"] if include_all else []) + list(BOROUGH_ORDER)

    if not options:
        st.warning("No borough options are available.")
        st.stop()

    return st.selectbox("Borough", options, key=key)


def mode_selector(
    modes: list[str],
    key: str = "mode_filter",
) -> str:
    """Select a transit mode or all available modes."""

    options = ["All modes"] + sorted(set(modes))

    return st.selectbox("Transit mode", options, key=key)


def station_selector(
    catalog: pd.DataFrame,
    key: str = "station_pick",
) -> str:
    """Select a station while preserving a valid session-state selection."""

    if not isinstance(catalog, pd.DataFrame):
        raise TypeError("Station catalog must be a pandas DataFrame.")

    if "label" not in catalog.columns:
        raise ValueError("Station catalog is missing the required 'label' column.")

    options = catalog["label"].dropna().astype(str).drop_duplicates().tolist()

    if not options:
        st.warning("No stations match the current filters.")
        st.stop()

    current = st.session_state.get(key)

    if current not in options:
        st.session_state[key] = options[0]

    return st.selectbox("Station", options, key=key)
