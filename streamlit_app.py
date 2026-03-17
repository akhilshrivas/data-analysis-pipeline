"""Streamlit UI for autonomous data analysis pipeline."""

import streamlit as st
import requests
import pandas as pd
import os

# Page configuration
st.set_page_config(
    page_title="Data Analysis Pipeline",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# API endpoint
API_URL = os.getenv("DATA_PIPELINE_API_URL", "http://localhost:8010")


def inject_custom_css():
    """Apply a more intentional visual system to the Streamlit app."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

        :root {
            --bg: #0f1417;
            --panel: rgba(22, 30, 35, 0.94);
            --panel-strong: #182127;
            --ink: #edf3ef;
            --muted: #9cadb0;
            --line: rgba(237, 243, 239, 0.10);
            --accent: #ff9347;
            --accent-deep: #ffc08f;
            --accent-soft: rgba(255, 147, 71, 0.12);
            --sage: rgba(93, 191, 140, 0.16);
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(255, 147, 71, 0.16), transparent 28%),
                radial-gradient(circle at top right, rgba(93, 191, 140, 0.12), transparent 24%),
                linear-gradient(180deg, #11181c 0%, var(--bg) 100%);
            color: var(--ink);
        }

        .stApp, .stApp * {
            color: var(--ink);
        }

        h1, h2, h3, h4 {
            font-family: "Space Grotesk", sans-serif;
            color: var(--ink);
            letter-spacing: -0.02em;
        }

        p, li, div, label, span {
            font-family: "Space Grotesk", sans-serif;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(17, 24, 28, 0.98), rgba(14, 20, 24, 0.98));
            border-right: 1px solid var(--line);
        }

        [data-testid="stSidebar"] * {
            color: var(--ink) !important;
        }

        [data-testid="stSidebar"] .stRadio label,
        [data-testid="stSidebar"] .stCheckbox label,
        [data-testid="stSidebar"] .stCaption,
        [data-testid="stSidebar"] p {
            color: var(--ink) !important;
        }

        .stRadio label, .stCheckbox label, .stSelectbox label, .stFileUploader label,
        .stTextInput label, .stTextArea label, .stMultiSelect label {
            color: var(--ink) !important;
            font-weight: 600;
        }

        .stRadio div[role="radiogroup"] label,
        .stCheckbox div[role="checkbox"] + label {
            color: var(--ink) !important;
        }

        .stRadio > div {
            background: rgba(28, 38, 44, 0.96);
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 0.45rem 0.55rem;
        }

        .stRadio [role="radiogroup"] > label {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(237, 243, 239, 0.08);
            border-radius: 12px;
            padding: 0.55rem 0.7rem;
            margin-bottom: 0.45rem;
        }

        .stRadio [role="radiogroup"] > label:hover {
            background: rgba(255, 147, 71, 0.08);
            border-color: rgba(255, 147, 71, 0.22);
        }

        .stRadio [role="radiogroup"] p {
            color: var(--ink) !important;
            font-weight: 600;
        }

        .stRadio input:checked + div p,
        .stRadio input:checked + div span {
            color: var(--accent) !important;
            font-weight: 700;
        }

        .stSelectbox > div[data-baseweb="select"] > div {
            background: rgba(28, 38, 44, 0.96) !important;
            border: 1px solid var(--line) !important;
            border-radius: 14px !important;
            color: var(--ink) !important;
        }

        .stSelectbox div[data-baseweb="select"] * {
            color: var(--ink) !important;
            fill: var(--ink) !important;
        }

        .stSelectbox input,
        .stSelectbox div[role="combobox"],
        .stSelectbox span,
        .stSelectbox p {
            color: var(--ink) !important;
            -webkit-text-fill-color: var(--ink) !important;
        }

        .stFileUploader > div {
            background: var(--panel) !important;
            border: 1px solid var(--line) !important;
            border-radius: 18px !important;
        }

        .stFileUploader [data-testid="stFileUploaderDropzone"] {
            background: var(--panel-strong) !important;
            border: 2px dashed rgba(255, 147, 71, 0.30) !important;
            color: var(--ink) !important;
        }

        .stFileUploader [data-testid="stFileUploaderDropzone"] * {
            color: var(--ink) !important;
        }

        .stFileUploader button,
        .stButton > button,
        .stDownloadButton > button {
            background: linear-gradient(180deg, var(--accent), var(--accent-deep)) !important;
            color: #101518 !important;
            border: none !important;
            border-radius: 14px !important;
            font-weight: 700 !important;
            box-shadow: 0 10px 18px rgba(0, 0, 0, 0.18);
        }

        .stFileUploader button:hover,
        .stButton > button:hover,
        .stDownloadButton > button:hover {
            background: linear-gradient(180deg, #ff9f61, #ffc08f) !important;
            color: #0f1417 !important;
        }

        .stButton > button:disabled {
            background: #b8ada4 !important;
            color: #f8f1ea !important;
        }

        [data-testid="stTabs"] button {
            color: var(--muted) !important;
            background: rgba(255, 255, 255, 0.03) !important;
            border-radius: 12px 12px 0 0 !important;
        }

        [data-testid="stTabs"] button[aria-selected="true"] {
            color: var(--accent) !important;
            background: rgba(255, 147, 71, 0.10) !important;
            font-weight: 700 !important;
        }

        .stAlert, .stInfo, .stSuccess, .stWarning, .stError {
            color: var(--ink) !important;
        }

        .stDataFrame, .stTable {
            color: var(--ink) !important;
        }

        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stMarkdownContainer"] span {
            color: var(--ink) !important;
        }

        code {
            font-family: "IBM Plex Mono", monospace !important;
            color: var(--accent-deep) !important;
            background: rgba(255, 147, 71, 0.12) !important;
            padding: 0.14rem 0.38rem !important;
            border-radius: 8px !important;
            border: 1px solid rgba(255, 147, 71, 0.14) !important;
        }

        .hero-panel {
            background: linear-gradient(135deg, rgba(24, 33, 38, 0.97), rgba(17, 24, 28, 0.95));
            border: 1px solid var(--line);
            border-radius: 24px;
            padding: 1.5rem 1.6rem;
            box-shadow: 0 18px 40px rgba(0, 0, 0, 0.22);
            margin-bottom: 1rem;
        }

        .hero-kicker {
            color: var(--accent-deep);
            text-transform: uppercase;
            letter-spacing: 0.14em;
            font-size: 0.78rem;
            font-weight: 700;
        }

        .hero-title {
            font-size: 2.55rem;
            line-height: 1.02;
            margin: 0.35rem 0 0.6rem 0;
            font-weight: 700;
        }

        .hero-copy {
            color: var(--muted);
            max-width: 56rem;
            font-size: 1rem;
        }

        .metric-card, .section-card {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 20px;
            padding: 1rem 1.1rem;
            box-shadow: 0 10px 24px rgba(0, 0, 0, 0.18);
        }

        .metric-label {
            color: var(--muted);
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.35rem;
        }

        .metric-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--ink);
            line-height: 1;
        }

        .metric-note {
            color: var(--muted);
            font-size: 0.88rem;
            margin-top: 0.45rem;
        }

        .chip-row {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin: 0.6rem 0 1rem 0;
        }

        .chip {
            background: rgba(255, 147, 71, 0.12);
            color: var(--ink);
            border: 1px solid rgba(255, 147, 71, 0.16);
            border-radius: 999px;
            padding: 0.35rem 0.72rem;
            font-size: 0.84rem;
            font-weight: 600;
        }

        .chip-success {
            background: rgba(93, 191, 140, 0.14);
            border-color: rgba(93, 191, 140, 0.16);
        }

        .sample-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 0.8rem;
        }

        .sample-pill {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(237, 243, 239, 0.09);
            color: var(--ink);
            border-radius: 999px;
            padding: 0.38rem 0.72rem;
            font-size: 0.82rem;
            font-weight: 600;
        }

        .section-title {
            font-size: 1.15rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
            color: var(--ink);
        }

        .section-copy {
            color: var(--muted);
            margin-bottom: 0.9rem;
        }

        .section-card code,
        .section-card span,
        .section-card p,
        .section-card div {
            color: var(--ink) !important;
        }

        .section-card code {
            color: var(--accent-deep) !important;
            background: rgba(255, 147, 71, 0.12) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def check_api_status() -> tuple[bool, str]:
    """Validate that the configured API URL points to this project backend."""
    try:
        health_response = requests.get(f"{API_URL}/health", timeout=2)
        if health_response.status_code != 200:
            return False, f"Health check failed with status {health_response.status_code}"

        root_response = requests.get(f"{API_URL}/", timeout=2)
        if root_response.status_code != 200:
            return False, "Root endpoint is unavailable"

        payload = root_response.json()
        service_name = payload.get("service")
        if service_name != "Data Analysis Pipeline API":
            return False, f"Connected to the wrong service at {API_URL}"

        return True, "API Connected"
    except Exception as exc:
        return False, str(exc)


def fetch_runs() -> list[dict]:
    """Fetch saved workspace runs from the backend."""
    try:
        response = requests.get(f"{API_URL}/runs", timeout=5)
        if response.status_code == 200:
            return response.json().get("runs", [])
    except Exception:
        return []
    return []


def fetch_run_details(run_id: str) -> dict | None:
    """Fetch one saved run."""
    try:
        response = requests.get(f"{API_URL}/runs/{run_id}", timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception:
        return None
    return None


def ask_copilot(question: str, run_id: str | None) -> dict | None:
    """Ask the analytics copilot about a selected run."""
    try:
        response = requests.post(
            f"{API_URL}/copilot/ask",
            json={"question": question, "run_id": run_id},
            timeout=30,
        )
        if response.status_code == 200:
            return response.json()
    except Exception:
        return None
    return None


def load_uploaded_dataframe(uploaded_file) -> pd.DataFrame:
    """Load an uploaded file into a dataframe for frontend chart rendering."""
    file_name = uploaded_file.name.lower()
    file_bytes = uploaded_file.getvalue()

    if file_name.endswith(".csv"):
        return pd.read_csv(pd.io.common.BytesIO(file_bytes))
    if file_name.endswith(".json"):
        try:
            return pd.read_json(pd.io.common.BytesIO(file_bytes))
        except ValueError:
            return pd.read_json(pd.io.common.BytesIO(file_bytes), lines=True)
    if file_name.endswith(".xlsx"):
        return pd.read_excel(pd.io.common.BytesIO(file_bytes))
    raise ValueError(f"Unsupported preview format: {uploaded_file.name}")


def render_histogram_like_chart(df: pd.DataFrame, column: str):
    """Render a histogram-like chart using binned counts."""
    series = pd.to_numeric(df[column], errors="coerce").dropna()
    if series.empty:
        st.info(f"No numeric data available for `{column}`.")
        return

    bins = min(20, max(5, int(series.nunique() ** 0.5)))
    bucketed = pd.cut(series, bins=bins)
    counts = bucketed.value_counts().sort_index()
    chart_df = pd.DataFrame(
        {
            "range": counts.index.astype(str),
            "count": counts.values,
        }
    ).set_index("range")
    st.bar_chart(chart_df)


def render_scatter_chart(df: pd.DataFrame, x_col: str, y_col: str):
    """Render a scatter chart for two numeric columns."""
    chart_df = df[[x_col, y_col]].copy()
    chart_df[x_col] = pd.to_numeric(chart_df[x_col], errors="coerce")
    chart_df[y_col] = pd.to_numeric(chart_df[y_col], errors="coerce")
    chart_df = chart_df.dropna().head(2000)

    if chart_df.empty:
        st.info(f"No usable rows found for `{x_col}` vs `{y_col}`.")
        return

    st.scatter_chart(chart_df, x=x_col, y=y_col)


def render_categorical_bar_chart(df: pd.DataFrame, column: str):
    """Render category frequencies."""
    counts = df[column].astype(str).fillna("Missing").value_counts().head(15)
    st.bar_chart(counts)


def render_missingness_chart(profile: dict):
    """Render missing-value percentages from profile output."""
    missing = profile.get("missing_percentage", {})
    if not missing:
        st.info("No missing-value summary available.")
        return

    chart_df = (
        pd.DataFrame(
            [{"column": column, "missing_pct": value} for column, value in missing.items()]
        )
        .sort_values("missing_pct", ascending=False)
        .set_index("column")
    )
    st.bar_chart(chart_df)


def render_metric_card(label: str, value: str, note: str = ""):
    """Render a styled metric summary card."""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_chip_row(items: list[str], success: bool = False):
    """Render rounded workflow chips."""
    chip_class = "chip chip-success" if success else "chip"
    chips = "".join([f'<span class="{chip_class}">{item}</span>' for item in items])
    st.markdown(f'<div class="chip-row">{chips}</div>', unsafe_allow_html=True)


def render_hero(api_connected: bool, api_message: str):
    """Render the app hero section."""
    status = "Connected" if api_connected else "Backend Needed"
    st.markdown(
        f"""
        <div class="hero-panel">
            <div class="hero-kicker">LangGraph Analysis Studio</div>
            <div class="hero-title">From raw file to routed multi-agent report.</div>
            <div class="hero-copy">
                Upload structured data, route it through a LangGraph workflow, inspect anomalies,
                generate LLM-backed insights, and review a saved markdown report. This frontend is
                designed to help you learn the pipeline while using it.
            </div>
            <div class="chip-row">
                <span class="chip">{status}</span>
                <span class="chip">API: {API_URL}</span>
                <span class="chip">{api_message}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main():
    inject_custom_css()
    if "copilot_messages" not in st.session_state:
        st.session_state.copilot_messages = []
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        st.caption(f"API URL: {API_URL}")
        
        analysis_type = st.radio(
            "Analysis Type",
            ["Quick Profile", "Deep Analysis", "Comparative Analysis"],
        )
        
        include_anomalies = st.checkbox("Detect Anomalies", value=True)
        include_insights = st.checkbox("Generate Insights", value=True)
        include_visualizations = st.checkbox("Create Visualizations", value=True)
        include_report = st.checkbox("Generate Report", value=True)
        
        st.divider()
        
        # API Status
        api_connected, api_message = check_api_status()
        if api_connected:
            st.success("✅ API Connected")
        else:
            st.error(f"❌ {api_message}")

        st.divider()
        st.subheader("Workspace Runs")
        runs = fetch_runs() if api_connected else []
        if runs:
            run_options = {
                f"{run['file_name']} | {run['created_at'][:19]}": run["run_id"]
                for run in runs[:15]
            }
            selected_run_label = st.selectbox(
                "Saved analyses",
                options=list(run_options.keys()),
                key="run_selector",
            )
            selected_run_id = run_options[selected_run_label]
            if st.button("Load Selected Run", use_container_width=True):
                run_record = fetch_run_details(selected_run_id)
                if run_record:
                    st.session_state.analysis_result = {
                        **run_record.get("result", {}),
                        "run_id": run_record.get("run_id"),
                        "workspace_summary": run_record.get("summary", {}),
                    }
                    st.session_state.last_uploaded_name = run_record.get("file_name")
                    st.session_state.selected_run_id = run_record.get("run_id")
                    st.session_state.copilot_messages = []
        else:
            st.caption("No saved runs yet. Upload data to create your first workspace.")

    render_hero(api_connected, api_message)

    top_metrics = st.columns(4)
    with top_metrics[0]:
        render_metric_card("Mode", analysis_type, "Choose the routing depth for this run")
    with top_metrics[1]:
        enabled_count = sum(
            [include_anomalies, include_insights, include_visualizations, include_report]
        )
        render_metric_card("Modules", str(enabled_count), "Enabled workflow modules")
    with top_metrics[2]:
        render_metric_card("Formats", "CSV / JSON / XLSX", "Frontend preview + backend upload")
    with top_metrics[3]:
        render_metric_card(
            "Learning Focus",
            "LangGraph",
            "Routing, retries, state transitions, and outputs",
        )
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">Upload Workspace</div>
                <div class="section-copy">
                    Bring in a dataset, preview its shape, and push it through the analysis graph.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        uploaded_file = st.file_uploader(
            "Choose a CSV, JSON, or XLSX file",
            type=["csv", "json", "xlsx"],
            help="Max 1024MB"
        )
        
        if uploaded_file:
            st.success(f"File selected: {uploaded_file.name}")
            
            # File preview
            with st.expander("Preview Data"):
                try:
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file, nrows=10)
                        st.dataframe(df, use_container_width=True)
                        st.caption(f"Showing 10 of {len(df)} rows")
                except Exception as e:
                    st.error(f"Cannot preview: {e}")
            
            # Analyze button
            if st.button(
                "Start Analysis",
                type="primary",
                use_container_width=True,
                disabled=not api_connected,
            ):
                with st.spinner("Analyzing data... This may take a moment."):
                    try:
                        response = requests.post(
                            f"{API_URL}/analyze",
                            files={"file": (uploaded_file.name, uploaded_file.getvalue())},
                            data={
                                "analysis_type": analysis_type,
                                "include_anomalies": str(include_anomalies).lower(),
                                "include_insights": str(include_insights).lower(),
                                "include_visualizations": str(include_visualizations).lower(),
                                "include_report": str(include_report).lower(),
                            },
                            timeout=30,
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.session_state.analysis_dataframe = load_uploaded_dataframe(uploaded_file)
                            st.session_state.analysis_result = result
                            st.session_state.last_uploaded_name = uploaded_file.name
                            st.session_state.selected_run_id = result.get("run_id")
                            st.session_state.copilot_messages = []
                            st.success("Analysis completed!")
                        else:
                            try:
                                error_payload = response.json()
                            except Exception:
                                error_payload = {"detail": response.text}
                            st.error(f"Analysis failed: {error_payload.get('detail', response.text)}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

            if not api_connected:
                st.warning("Start the FastAPI backend first, then retry.")
    
    with col2:
        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">Control Panel</div>
                <div class="section-copy">
                    Active analysis mode and enabled workflow modules.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        render_chip_row([analysis_type])
        selected_modules = []
        if include_anomalies:
            selected_modules.append("Anomaly Detection")
        if include_insights:
            selected_modules.append("Insight Generation")
        if include_visualizations:
            selected_modules.append("Visualizations")
        if include_report:
            selected_modules.append("Report Generation")
        render_chip_row(selected_modules or ["No modules enabled"])
    
    st.divider()
    
    # Results tabs
    if "analysis_result" in st.session_state:
        result = st.session_state.analysis_result
        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">Analysis Results</div>
                <div class="section-copy">
                    Review the routed graph output, the generated report, and the visual layer in one place.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        overview_cols = st.columns(4)
        profile = result.get("profile", {})
        anomalies = result.get("anomalies", {})
        report = result.get("report", {})
        with overview_cols[0]:
            render_metric_card(
                "Dataset",
                st.session_state.get("last_uploaded_name", "Current run"),
                "Source analyzed in the latest request",
            )
        with overview_cols[1]:
            render_metric_card(
                "Rows",
                f"{profile.get('shape', {}).get('rows', 0):,}",
                "Loaded into the workflow",
            )
        with overview_cols[2]:
            render_metric_card(
                "Flagged Rows",
                f"{anomalies.get('total_anomalous_rows', 0):,}",
                "Potential anomalies found",
            )
        with overview_cols[3]:
            render_metric_card(
                "Report Mode",
                report.get("generation_mode", "n/a"),
                "LLM-backed or fallback output",
            )
        workspace_summary = result.get("workspace_summary", {})
        if result.get("run_id"):
            st.markdown("**Workspace Summary**")
            render_chip_row(
                [
                    f"Run ID: {result['run_id']}",
                    f"Rows: {workspace_summary.get('rows', profile.get('shape', {}).get('rows', 0)):,}",
                    f"Flagged: {workspace_summary.get('flagged_rows', anomalies.get('total_anomalous_rows', 0)):,}",
                ]
            )
        if result.get("completed_steps"):
            st.markdown("**Executed Workflow Steps**")
            render_chip_row(result.get("completed_steps", []), success=True)
            with st.expander("Workflow Execution Trace", expanded=False):
                st.write("Messages:")
                for message in result.get("messages", []):
                    st.write(f"- {message}")

        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">Analytics Copilot</div>
                <div class="section-copy">
                    Ask follow-up questions about the selected run, such as what to clean first,
                    which anomalies matter, or what actions should come next.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        copilot_cols = st.columns([3, 1])
        with copilot_cols[0]:
            question = st.text_input(
                "Ask the copilot about this run",
                placeholder="What should I investigate first in this dataset?",
                key="copilot_question",
            )
        with copilot_cols[1]:
            if st.button("Ask Copilot", use_container_width=True):
                if question.strip():
                    reply = ask_copilot(question, result.get("run_id") or st.session_state.get("selected_run_id"))
                    if reply:
                        st.session_state.copilot_messages.append(
                            {"role": "user", "content": question}
                        )
                        st.session_state.copilot_messages.append(
                            {"role": "assistant", "content": reply.get("answer", ""), "mode": reply.get("mode", "")}
                        )
                    else:
                        st.error("Copilot request failed. Check that the backend is running.")

        for message in st.session_state.get("copilot_messages", []):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if message.get("mode"):
                    st.caption(f"Mode: {message['mode']}")
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["Profile", "Anomalies", "Insights", "Visualizations", "Report"]
        )
        
        with tab1:
            st.subheader("Data Profile")
            profile = result.get("profile", {})
            if profile:
                shape = profile.get("shape", {})
                metric_cols = st.columns(3)
                metric_cols[0].metric("Rows", f"{shape.get('rows', 0):,}")
                metric_cols[1].metric("Columns", f"{shape.get('columns', 0)}")
                metric_cols[2].metric("Duplicates", f"{profile.get('duplicate_rows', 0):,}")

                missing_pct = profile.get("missing_percentage", {})
                missing_df = pd.DataFrame(
                    [{"column": col, "missing_pct": pct} for col, pct in missing_pct.items()]
                ).sort_values("missing_pct", ascending=False)
                st.dataframe(missing_df, use_container_width=True)
            else:
                st.info("No profiling results returned.")
        
        with tab2:
            st.subheader("Anomaly Detection")
            anomalies = result.get("anomalies", {})
            if anomalies:
                metric_cols = st.columns(3)
                metric_cols[0].metric("Flagged Rows", f"{anomalies.get('total_anomalous_rows', 0):,}")
                metric_cols[1].metric("IQR Flags", f"{anomalies.get('methods', {}).get('iqr', {}).get('total_anomalies', 0):,}")
                metric_cols[2].metric("Z-score Flags", f"{anomalies.get('methods', {}).get('zscore', {}).get('total_anomalies', 0):,}")

                top_columns = anomalies.get("top_columns", [])
                if top_columns:
                    st.dataframe(pd.DataFrame(top_columns), use_container_width=True)
                st.text(anomalies.get("summary", ""))
            else:
                st.info("No anomaly results returned.")
        
        with tab3:
            st.subheader("Generated Insights")
            insights = result.get("insights", {})
            if insights:
                st.markdown(f"**Summary:** {insights.get('executive_summary', 'N/A')}")
                for finding in insights.get("key_findings", []):
                    st.write(f"- {finding}")

                if insights.get("risks"):
                    st.markdown("**Risks**")
                    for risk in insights.get("risks", []):
                        st.write(f"- {risk}")

                if insights.get("recommended_actions"):
                    st.markdown("**Recommended Actions**")
                    for action in insights.get("recommended_actions", []):
                        st.write(f"- {action}")
                st.caption(f"Generation mode: {insights.get('generation_mode', 'unknown')}")
            else:
                profiler_insights = result.get("profile", {}).get("insights", [])
                if profiler_insights:
                    for insight in profiler_insights:
                        st.write(f"- {insight}")
                else:
                    st.info("Insight generation is not implemented yet.")
        
        with tab4:
            st.subheader("Visualizations")
            visualizations = result.get("visualizations", {})
            completed_steps = result.get("completed_steps", [])
            analysis_df = st.session_state.get("analysis_dataframe")
            if visualizations:
                st.markdown(visualizations.get("dashboard_notes", ""))
                charts = visualizations.get("recommended_charts", [])
                if charts:
                    st.dataframe(pd.DataFrame(charts), use_container_width=True)
                    st.divider()
                    st.markdown("### Rendered Charts")

                    profile = result.get("profile", {})
                    for chart in charts:
                        chart_type = chart.get("chart_type")
                        columns = chart.get("columns", [])
                        st.markdown(f"**{chart_type.replace('_', ' ').title()}**")
                        st.caption(chart.get("reason", ""))

                        if chart_type == "summary_card":
                            metrics = st.columns(3)
                            metrics[0].metric("Rows", f"{profile.get('shape', {}).get('rows', 0):,}")
                            metrics[1].metric("Columns", f"{profile.get('shape', {}).get('columns', 0)}")
                            metrics[2].metric(
                                "Flagged Rows",
                                f"{result.get('anomalies', {}).get('total_anomalous_rows', 0):,}",
                            )
                        elif chart_type == "missingness_bar":
                            render_missingness_chart(profile)
                        elif analysis_df is None:
                            st.info("Uploaded dataframe is not available in session. Rerun the analysis to render charts.")
                        elif chart_type == "histogram" and columns:
                            render_histogram_like_chart(analysis_df, columns[0])
                        elif chart_type == "scatter" and len(columns) >= 2:
                            render_scatter_chart(analysis_df, columns[0], columns[1])
                        elif chart_type == "bar" and columns:
                            render_categorical_bar_chart(analysis_df, columns[0])
                        else:
                            st.info("No renderer implemented for this recommendation yet.")
                else:
                    st.info("No chart recommendations returned.")
            else:
                if "skip_visualizations" in completed_steps:
                    st.warning("Visualization generation was skipped for this run. Enable `Create Visualizations` and run the analysis again.")
                elif "create_visualizations" not in completed_steps:
                    st.warning("This result appears to come from an older backend response that did not execute the visualization node. Restart the FastAPI backend and rerun the analysis.")
                else:
                    st.warning("Visualization node ran but returned no recommendations. Check the workflow trace for details.")
        
        with tab5:
            st.subheader("Full Report")
            report = result.get("report", {})
            if report.get("content"):
                st.markdown(report["content"])
                st.caption(f"Saved at: {report.get('report_path', 'N/A')}")
                st.caption(f"Generation mode: {report.get('generation_mode', 'unknown')}")
            else:
                st.json(
                    {
                        "status": result.get("status"),
                        "messages": result.get("messages", []),
                        "error": result.get("error"),
                    }
                )


if __name__ == "__main__":
    main()
