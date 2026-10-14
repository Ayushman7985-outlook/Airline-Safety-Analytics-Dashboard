
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="AeroInsight | Airline Safety",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# PROFESSIONAL THEME
# --------------------------------------------------
st.markdown(
    """
    <style>
    :root {
        --navy: #142B4A;
        --blue: #3977D5;
        --teal: #13A89E;
        --background: #F5F7FB;
        --text: #23344D;
        --muted: #718096;
    }

    .stApp {
        background-color: var(--background);
        color: var(--text);
    }

    [data-testid="stHeader"] {
        background-color: rgba(245, 247, 251, 0.95);
    }

    [data-testid="stSidebar"] {
        background-color: #142B4A;
        border-right: 1px solid #233E60;
    }

    [data-testid="stSidebar"] * {
        color: #F4F7FC;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        padding: 9px 10px;
        border-radius: 8px;
    }

    .brand {
        font-size: 25px;
        font-weight: 800;
        letter-spacing: -0.7px;
        color: #FFFFFF;
        margin: 5px 0 2px 0;
    }

    .brand-subtitle {
        color: #B9C9DF;
        font-size: 12px;
        margin-bottom: 24px;
    }

    .page-title {
        font-size: clamp(25px, 3vw, 34px);
        font-weight: 800;
        letter-spacing: -0.8px;
        color: #142B4A;
        margin-bottom: 4px;
    }

    .page-description {
        color: #718096;
        font-size: 14px;
        margin-bottom: 22px;
    }

    .section-heading {
        font-size: 18px;
        font-weight: 700;
        color: #142B4A;
        margin: 8px 0 12px 0;
    }

    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E4EAF2;
        border-radius: 13px;
        padding: 17px 18px;
        min-height: 112px;
        box-shadow: 0 3px 12px rgba(20, 43, 74, 0.035);
        overflow-wrap: anywhere;
    }

    div[data-testid="stMetricLabel"] {
        color: #718096;
        font-size: 13px;
    }

    div[data-testid="stMetricValue"] {
        color: #142B4A;
        font-size: clamp(20px, 2vw, 29px);
        font-weight: 750;
        white-space: normal;
        overflow-wrap: anywhere;
    }

    div[data-testid="stPlotlyChart"] {
        background: #FFFFFF;
        border: 1px solid #E4EAF2;
        border-radius: 13px;
        padding: 8px;
        overflow: hidden;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #E4EAF2;
        border-radius: 10px;
        overflow: hidden;
    }

    .info-note {
        background: #EAF1FC;
        border-left: 4px solid #3977D5;
        padding: 12px 15px;
        border-radius: 6px;
        color: #23344D;
        font-size: 13px;
        margin: 10px 0 18px 0;
    }

    .footer {
        color: #718096;
        font-size: 12px;
        text-align: center;
        padding: 25px 0 10px 0;
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    @media (max-width: 700px) {
        .page-title {
            font-size: 25px;
        }

        div[data-testid="stMetric"] {
            padding: 12px;
            min-height: 95px;
        }

        div[data-testid="stPlotlyChart"] {
            padding: 2px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# CONSTANTS AND DATA
# --------------------------------------------------
DATA_PATH = Path(__file__).parent / "data" / "airline-safety.csv"

REQUIRED_COLUMNS = [
    "airline",
    "avail_seat_km_per_week",
    "incidents_85_99",
    "fatal_accidents_85_99",
    "fatalities_85_99",
    "incidents_00_14",
    "fatal_accidents_00_14",
    "fatalities_00_14",
]

METRICS = {
    "Incidents": ("incidents_85_99", "incidents_00_14"),
    "Fatal accidents": (
        "fatal_accidents_85_99",
        "fatal_accidents_00_14",
    ),
    "Fatalities": ("fatalities_85_99", "fatalities_00_14"),
}

COLORS = {
    "navy": "#142B4A",
    "blue": "#3977D5",
    "teal": "#13A89E",
    "amber": "#E9A23B",
    "red": "#D95757",
    "grey": "#93A4BA",
}


@st.cache_data
def load_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {DATA_PATH}"
        )

    data = pd.read_csv(DATA_PATH)

    missing = [c for c in REQUIRED_COLUMNS if c not in data.columns]
    if missing:
        raise ValueError(
            "The dataset is missing these columns: "
            + ", ".join(missing)
        )

    data = data[REQUIRED_COLUMNS].copy()
    data["airline"] = data["airline"].astype(str).str.strip()

    numeric_columns = [
        c for c in REQUIRED_COLUMNS if c != "airline"
    ]

    for column in numeric_columns:
        data[column] = pd.to_numeric(
            data[column], errors="coerce"
        )

    data = data.dropna(subset=["airline"])
    data = data[data["airline"] != ""]

    return data


try:
    df = load_data()
except Exception as error:
    st.error(f"Unable to load the dataset: {error}")
    st.info(
        "Check that data/airline-safety.csv exists "
        "and contains the expected columns."
    )
    st.stop()


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------
def format_number(value):
    return f"{value:,.0f}"


def get_metric_column(metric, period):
    index = 0 if period == "1985–1999" else 1
    return METRICS[metric][index]


def style_chart(fig, height=360):
    fig.update_layout(
        height=height,
        autosize=True,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(
            family="Arial, sans-serif",
            color=COLORS["navy"],
            size=12,
        ),
        margin=dict(l=18, r=18, t=48, b=25),
        title=dict(
            font=dict(size=16, color=COLORS["navy"]),
            x=0.03,
            xanchor="left",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
        ),
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        automargin=True,
    )

    fig.update_yaxes(
        gridcolor="#EDF1F7",
        zeroline=False,
        automargin=True,
    )

    return fig


def show_header(title, description):
    st.markdown(
        f'<div class="page-title">{title}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="page-description">{description}</div>',
        unsafe_allow_html=True,
    )


def show_kpis(data, metric, period):
    metric_col = get_metric_column(metric, period)
    total_events = data[metric_col].fillna(0).sum()
    total_airlines = data["airline"].nunique()
    exposure = data["avail_seat_km_per_week"].fillna(0).sum()
    average_events = (
        data[metric_col].fillna(0).mean() if len(data) else 0
    )

    k1, k2, k3, k4 = st.columns(4, gap="medium")

    with k1:
        st.metric("Airlines", format_number(total_airlines))

    with k2:
        st.metric(f"Total {metric.lower()}", format_number(total_events))

    with k3:
        st.metric("Average per airline", format_number(average_events))

    with k4:
        st.metric("Seat-km exposure", format_number(exposure))


# --------------------------------------------------
# LEFT NAVIGATION
# --------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div class="brand">✈ AeroInsight</div>
        <div class="brand-subtitle">
            AIRLINE SAFETY ANALYTICS
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Navigation")

    page = st.radio(
        "Choose a page",
        [
            "Overview",
            "Period Comparison",
            "Exposure Analysis",
            "Data Explorer",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown("### Dashboard Filters")

    period = st.selectbox(
        "Analysis period",
        ["2000–2014", "1985–1999"],
        help="Select the historical period for the main charts.",
    )

    metric = st.selectbox(
        "Safety metric",
        ["Incidents", "Fatal accidents", "Fatalities"],
    )

    search_text = st.text_input(
        "Search airline",
        placeholder="Type an airline name...",
    )

    airline_options = sorted(df["airline"].unique().tolist())

    selected_airlines = st.multiselect(
        "Select airlines",
        options=airline_options,
        default=[],
        help="Leave empty to include all matching airlines.",
    )

    top_n = st.slider(
        "Airlines in ranking charts",
        min_value=5,
        max_value=min(30, max(5, len(airline_options))),
        value=min(10, max(5, len(airline_options))),
        step=1,
    )

    if st.button("Reset filters", use_container_width=True):
        st.session_state["Analysis period"] = "2000–2014"
        st.session_state["Safety metric"] = "Incidents"
        st.session_state["Search airline"] = ""
        st.session_state["Select airlines"] = []
        st.rerun()

    st.divider()

    st.caption("DATASET")
    st.markdown("Airline Safety · 1985–2014")
    st.caption(f"{len(df)} airline records loaded")


# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------
filtered = df.copy()

if search_text.strip():
    filtered = filtered[
        filtered["airline"].str.contains(
            search_text.strip(),
            case=False,
            na=False,
        )
    ]

if selected_airlines:
    filtered = filtered[
        filtered["airline"].isin(selected_airlines)
    ]

if filtered.empty:
    show_header("No matching airlines", "Adjust the filters in the left sidebar.")
    st.warning("No records match the current filters.")
    st.stop()


metric_col = get_metric_column(metric, period)
old_col, new_col = METRICS[metric]


# --------------------------------------------------
# PAGE 1: OVERVIEW
# --------------------------------------------------
if page == "Overview":
    show_header(
        "Airline Safety Overview",
        "A clear summary of historical airline safety statistics.",
    )

    st.markdown(
        f"""
        <div class="info-note">
        <b>Current view:</b> {period} &nbsp; | &nbsp;
        <b>Metric:</b> {metric} &nbsp; | &nbsp;
        <b>Airlines:</b> {len(filtered)}
        </div>
        """,
        unsafe_allow_html=True,
    )

    show_kpis(filtered, metric, period)

    st.markdown('<div class="section-heading">Safety Rankings</div>',
                unsafe_allow_html=True)

    ranking = (
        filtered.groupby("airline", as_index=False)[metric_col]
        .sum()
        .sort_values(metric_col, ascending=False)
        .head(top_n)
        .sort_values(metric_col, ascending=True)
    )

    chart1, chart2 = st.columns([1.6, 1], gap="large")

    with chart1:
        fig = px.bar(
            ranking,
            x=metric_col,
            y="airline",
            orientation="h",
            title=f"Top Airlines by {metric.lower()}",
            labels={
                metric_col: metric,
                "airline": "Airline",
            },
            color=metric_col,
            color_continuous_scale=["#B9D9F5", "#3977D5", "#142B4A"],
        )
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(
            style_chart(fig, 440),
            use_container_width=True,
            config={"responsive": True, "displaylogo": False},
        )

    with chart2:
        composition = (
            filtered[metric_col].fillna(0).clip(lower=0)
        )
        pie_df = pd.DataFrame({
            "Category": ["Selected airlines", "Remaining total"],
            "Value": [
                composition.sum(),
                max(0, df[metric_col].fillna(0).sum() - composition.sum()),
            ],
        })

        if pie_df["Value"].sum() == 0:
            st.info("No events are recorded for this metric.")
        else:
            fig = px.pie(
                pie_df,
                names="Category",
                values="Value",
                hole=0.65,
                title="Filtered vs. full dataset",
                color="Category",
                color_discrete_map={
                    "Selected airlines": COLORS["teal"],
                    "Remaining total": "#DCE5F0",
                },
            )
            fig.update_traces(
                textposition="inside",
                textinfo="percent",
                hovertemplate="%{label}<br>%{value:,.0f}<extra></extra>",
            )
            st.plotly_chart(
                style_chart(fig, 440),
                use_container_width=True,
                config={"responsive": True, "displaylogo": False},
            )

    st.markdown(
        '<div class="section-heading">Metric Breakdown</div>',
        unsafe_allow_html=True,
    )

    totals = pd.DataFrame({
        "Metric": list(METRICS.keys()),
        "Total": [
            filtered[get_metric_column(name, period)]
            .fillna(0).sum()
            for name in METRICS
        ],
    })

    fig = px.bar(
        totals,
        x="Metric",
        y="Total",
        title=f"All safety metrics · {period}",
        color="Metric",
        color_discrete_sequence=[
            COLORS["blue"], COLORS["amber"], COLORS["red"]
        ],
        text_auto=True,
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(
        style_chart(fig, 320),
        use_container_width=True,
        config={"responsive": True, "displaylogo": False},
    )


# --------------------------------------------------
# PAGE 2: PERIOD COMPARISON
# --------------------------------------------------
elif page == "Period Comparison":
    show_header(
        "Period Comparison",
        "Compare airline safety statistics across two historical periods.",
    )

    st.markdown(
        '<div class="info-note">Compare recorded events from '
        '<b>1985–1999</b> and <b>2000–2014</b>. These are historical '
        'totals, not risk-adjusted rates.</div>',
        unsafe_allow_html=True,
    )

    show_kpis(filtered, metric, period)

    st.markdown(
        '<div class="section-heading">Compare the selected metric</div>',
        unsafe_allow_html=True,
    )

    comparison = filtered[["airline", old_col, new_col]].copy()
    comparison[[old_col, new_col]] = comparison[
        [old_col, new_col]
    ].fillna(0)

    comparison["Total"] = comparison[old_col] + comparison[new_col]
    comparison = (
        comparison.sort_values("Total", ascending=False)
        .head(top_n)
        .drop(columns="Total")
    )

    comparison_long = comparison.melt(
        id_vars="airline",
        value_vars=[old_col, new_col],
        var_name="Period",
        value_name=metric,
    )

    comparison_long["Period"] = comparison_long["Period"].map({
        old_col: "1985–1999",
        new_col: "2000–2014",
    })

    fig = px.bar(
        comparison_long,
        x="airline",
        y=metric,
        color="Period",
        barmode="group",
        title=f"{metric} by airline and period",
        labels={"airline": "Airline"},
        color_discrete_map={
            "1985–1999": COLORS["blue"],
            "2000–2014": COLORS["teal"],
        },
    )
    fig.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(
        style_chart(fig, 470),
        use_container_width=True,
        config={"responsive": True, "displaylogo": False},
    )

    old_total = filtered[old_col].fillna(0).sum()
    new_total = filtered[new_col].fillna(0).sum()

    left, right = st.columns(2, gap="large")

    with left:
        st.metric("1985–1999 total", format_number(old_total))

    with right:
        st.metric("2000–2014 total", format_number(new_total))

    st.markdown(
        '<div class="section-heading">Detailed Comparison</div>',
        unsafe_allow_html=True,
    )

    st.dataframe(
        comparison.rename(columns={
            old_col: "1985–1999",
            new_col: "2000–2014",
            "airline": "Airline",
        }),
        use_container_width=True,
        hide_index=True,
    )


# --------------------------------------------------
# PAGE 3: EXPOSURE ANALYSIS
# --------------------------------------------------
elif page == "Exposure Analysis":
    show_header(
        "Exposure Analysis",
        "Explore recorded safety events alongside airline operating exposure.",
    )

    st.markdown(
        '<div class="info-note">Available seat-kilometres provide an '
        'exposure measure. This dashboard does not calculate a formal '
        'causal or standardized safety rate.</div>',
        unsafe_allow_html=True,
    )

    show_kpis(filtered, metric, period)

    exposure_data = filtered[
        ["airline", "avail_seat_km_per_week", metric_col]
    ].copy()

    exposure_data = exposure_data.rename(columns={
        "avail_seat_km_per_week": "Available seat-km per week",
        metric_col: metric,
    }).dropna()

    chart1, chart2 = st.columns(2, gap="large")

    with chart1:
        fig = px.scatter(
            exposure_data,
            x="Available seat-km per week",
            y=metric,
            hover_name="airline",
            size="Available seat-km per week",
            color=metric,
            title=f"Exposure vs. {metric.lower()}",
            color_continuous_scale=["#A9DCD7", "#13A89E", "#142B4A"],
        )
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(
            style_chart(fig, 410),
            use_container_width=True,
            config={"responsive": True, "displaylogo": False},
        )

    with chart2:
        fig = px.histogram(
            exposure_data,
            x=metric,
            nbins=15,
            title=f"Distribution of {metric.lower()}",
            labels={metric: metric},
            color_discrete_sequence=[COLORS["blue"]],
        )
        st.plotly_chart(
            style_chart(fig, 410),
            use_container_width=True,
            config={"responsive": True, "displaylogo": False},
        )

    st.markdown(
        '<div class="section-heading">Exposure Data</div>',
        unsafe_allow_html=True,
    )

    st.dataframe(
        exposure_data.sort_values(metric, ascending=False),
        use_container_width=True,
        hide_index=True,
    )


# --------------------------------------------------
# PAGE 4: DATA EXPLORER
# --------------------------------------------------
elif page == "Data Explorer":
    show_header(
        "Data Explorer",
        "Inspect, sort, and export the airline safety dataset.",
    )

    st.markdown(
        '<div class="info-note">Use the sidebar to narrow the records. '
        'The table and CSV export below reflect your selected airlines '
        'and search term.</div>',
        unsafe_allow_html=True,
    )

    k1, k2, k3 = st.columns(3, gap="medium")

    with k1:
        st.metric("Visible records", format_number(len(filtered)))

    with k2:
        st.metric("Unique airlines", format_number(filtered["airline"].nunique()))

    with k3:
        missing_count = int(filtered.isna().sum().sum())
        st.metric("Missing values", format_number(missing_count))

    st.markdown(
        '<div class="section-heading">Airline Records</div>',
        unsafe_allow_html=True,
    )

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True,
        height=460,
    )

    csv_data = filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇ Download filtered data (CSV)",
        data=csv_data,
        file_name="airline_safety_filtered.csv",
        mime="text/csv",
        use_container_width=True,
    )

    with st.expander("Dataset information"):
        st.write("**Dataset:** Airline Safety")
        st.write(f"**Original rows loaded:** {len(df)}")
        st.write(f"**Rows currently displayed:** {len(filtered)}")
        st.write("**Columns:**")
        st.write(", ".join(filtered.columns.tolist()))
        st.write(
            "**Note:** Missing numeric values are ignored in totals "
            "and omitted from exposure charts where required."
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown(
    """
    <div class="footer">
        AeroInsight · Airline Safety Analytics<br>
        Historical data for analysis and educational use.
        Historical event counts alone do not establish which airline
        is safest today.
    </div>
    """,
    unsafe_allow_html=True,
)
