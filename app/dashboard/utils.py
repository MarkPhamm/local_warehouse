import duckdb
import pandas as pd
import streamlit as st

DB_PATH = "database/cfpb_complaints.duckdb"


# --- ENHANCED DESIGN SYSTEM ---
def apply_styling():
    st.markdown(
        """
        <style>
            /* 1. MAIN BACKGROUND (Tối giản, bớt rực) */
            [data-testid="stAppViewContainer"] {
                /* Chuyển từ Đen than (020617) sang Xám đen (1E293B).
                   Không còn màu xanh rực ở dưới đáy nữa. */
                background: linear-gradient(to bottom, #020617 0%, #0F172A 50%, #1E293B 100%);
                background-attachment: fixed;
                color: #F1F5F9; /* Chữ màu trắng xám sáng, dễ đọc hơn */
                font-family: 'Inter', sans-serif;
            }

            /* 2. REMOVE HEADER BG */
            [data-testid="stHeader"] {
                background-color: rgba(0,0,0,0);
            }

            /* IMPORT FONT */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            font-family: 'Inter', sans-serif;

            html, body, [class*="css"] {
                font-family: 'Roboto', sans-serif;
                background: linear-gradient(135deg, #E8EEF2 0%, #F4F7F9 50%, #EDF1F5 100%);
                color: #1F2937;
            }

            /* SIDEBAR STYLING WITH ENHANCED GRADIENT */
            section[data-testid="stSidebar"] {
                background: linear-gradient(180deg, #00395D 0%, #002B4A 50%, #001F35 100%);
                box-shadow: 4px 0 20px rgba(0, 57, 93, 0.15);
            }

            section[data-testid="stSidebar"] h1,
            section[data-testid="stSidebar"] h2,
            section[data-testid="stSidebar"] h3,
            section[data-testid="stSidebar"] span,
            section[data-testid="stSidebar"] label {
                color: #FFFFFF !important;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            }

            /* Sidebar widgets styling */
            section[data-testid="stSidebar"] .stMultiSelect,
            section[data-testid="stSidebar"] .stDateInput {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 5px;
                backdrop-filter: blur(10px);
            }

            /* HEADERS WITH GRADIENT UNDERLINE */
            h1, h2, h3 {
                color: #00395D;
                font-weight: 700;
                letter-spacing: -0.5px;
            }
            h1 {
                background: linear-gradient(90deg, #00AEEF 0%, #0090C8 100%);
                background-size: 100% 4px;
                background-repeat: no-repeat;
                background-position: left bottom;
                padding-bottom: 12px;
                display: inline-block;
                text-shadow: 0 2px 4px rgba(0, 57, 93, 0.1);
            }

            h2 {
                border-left: 4px solid #00AEEF;
                padding-left: 12px;
                margin-left: -12px;
            }

            /* ENHANCED 3D CARDS WITH LAYERED SHADOWS */
            div.css-card {
                background: linear-gradient(145deg, #FFFFFF 0%, #F8FAFB 100%);
                border-radius: 16px;
                padding: 24px 20px;
                box-shadow:
                    0 2px 4px rgba(0, 57, 93, 0.05),
                    0 8px 16px rgba(0, 57, 93, 0.08),
                    0 16px 32px rgba(0, 57, 93, 0.06);
                border: 1px solid rgba(0, 174, 239, 0.1);
                border-left: 5px solid #00AEEF;
                position: relative;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                overflow: hidden;
            }

            /* Subtle gradient overlay on cards */
            div.css-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, #00AEEF 0%, #00C9FF 100%);
                opacity: 0;
                transition: opacity 0.3s ease;
            }

            div.css-card:hover {
                transform: translateY(-6px) scale(1.02);
                box-shadow:
                    0 4px 8px rgba(0, 57, 93, 0.08),
                    0 12px 24px rgba(0, 57, 93, 0.12),
                    0 24px 48px rgba(0, 57, 93, 0.1),
                    0 0 0 1px rgba(0, 174, 239, 0.3);
                border-left-width: 6px;
            }

            div.css-card:hover::before {
                opacity: 1;
            }

            /* ENHANCED METRIC TEXT WITH ANIMATIONS */
            .metric-label {
                font-size: 0.85rem;
                color: #6B7280;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                font-weight: 600;
                margin-bottom: 8px;
                display: block;
            }

            .metric-value {
                font-size: 1.8rem;                /* slightly smaller for text KPIs */
                font-weight: 800;
                background: linear-gradient(135deg, #00395D 0%, #005A8C 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                white-space: normal;
                overflow: hidden;
                display: -webkit-box;
                -webkit-line-clamp: 2;             /* max 2 lines */
                -webkit-box-orient: vertical;

                line-height: 1.25;
                max-width: 100%;
            }

            /* Icon decoration for cards */
            .metric-icon {
                position: absolute;
                top: 20px;
                right: 20px;
                width: 48px;
                height: 48px;
                background: linear-gradient(135deg, rgba(0, 174, 239, 0.1) 0%, rgba(0, 174, 239, 0.05) 100%);
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 24px;
                opacity: 0.6;
                transition: all 0.3s ease;
            }

            div.css-card:hover .metric-icon {
                opacity: 1;
                transform: rotate(10deg) scale(1.1);
                background: linear-gradient(135deg, rgba(0, 174, 239, 0.2) 0%, rgba(0, 174, 239, 0.1) 100%);
            }

            /* ENHANCED PLOTLY CHART CONTAINER */
            .js-plotly-plot {
                border-radius: 16px;
                box-shadow:
                    0 2px 4px rgba(0, 57, 93, 0.04),
                    0 8px 16px rgba(0, 57, 93, 0.06),
                    0 16px 32px rgba(0, 57, 93, 0.04);
                background: linear-gradient(145deg, #FFFFFF 0%, #FAFBFC 100%);
                padding: 16px;
                border: 1px solid rgba(0, 57, 93, 0.06);
                transition: all 0.3s ease;
            }

            .js-plotly-plot:hover {
                box-shadow:
                    0 4px 8px rgba(0, 57, 93, 0.06),
                    0 12px 24px rgba(0, 57, 93, 0.08),
                    0 24px 48px rgba(0, 57, 93, 0.06);
                transform: translateY(-2px);
            }

            /* ENHANCED DATAFRAME STYLING */
            .stDataFrame {
                border-radius: 12px;
                overflow: hidden;
                box-shadow:
                    0 2px 8px rgba(0, 57, 93, 0.06),
                    0 8px 16px rgba(0, 57, 93, 0.04);
            }

            /* INFO/WARNING BOXES WITH DEPTH */
            .stAlert {
                border-radius: 12px;
                border: none;
                box-shadow:
                    0 2px 8px rgba(0, 57, 93, 0.08),
                    0 4px 16px rgba(0, 57, 93, 0.04);
                background: linear-gradient(145deg, #FFFFFF 0%, #F8FAFB 100%);
            }

            /* BUTTON ENHANCEMENTS */
            .stButton > button {
                border-radius: 10px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                transition: all 0.3s ease;
                box-shadow: 0 4px 12px rgba(0, 57, 93, 0.15);
            }

            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(0, 57, 93, 0.25);
            }

            /* SUBTLE ANIMATIONS */
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            .css-card {
                animation: fadeInUp 0.6s ease-out;
            }

            /* Stagger animation for multiple cards */
            .css-card:nth-child(1) { animation-delay: 0.1s; }
            .css-card:nth-child(2) { animation-delay: 0.2s; }
            .css-card:nth-child(3) { animation-delay: 0.3s; }
            .css-card:nth-child(4) { animation-delay: 0.4s; }
        </style>
    """,
        unsafe_allow_html=True,
    )


def metric_card(label, value, help_text="", icon="📊"):
    """
    Renders an enhanced 3D HTML card with icon decoration.
    """
    html_code = f"""
    <div class="css-card" title="{help_text}">
        <div class="metric-icon">{icon}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)


# --- DATA LOADING ---
@st.cache_data(ttl=3600)
def load_data():
    try:
        # Connect to DuckDB
        con = duckdb.connect(DB_PATH, read_only=True)

        # Query specific columns
        query = """
            select
                date_received,
                product,
                sub_product,
                issue,
                company,
                state,
                submitted_via,
                company_response,
                timely,
                consumer_disputed
            from raw.cfpb_complaints
            where company IN (
                select company
                from raw.cfpb_complaints
                group by company
                having count(*) >= 10000
                order by count(*) DESC
            )
        """
        df = con.execute(query).df()
        con.close()

        # --- PREPROCESSING ---
        df["date_received"] = pd.to_datetime(df["date_received"])
        df["timely"] = df["timely"].apply(lambda x: 1 if x == "Yes" else 0)
        return df
    except Exception:
        return pd.DataFrame()  # Return empty if DB not found for safety


# --- SHARED SIDEBAR FILTERS ---
def render_sidebar(df):
    # Ensure styling is applied on every page load
    apply_styling()

    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    st.sidebar.header("🔍 Filter Data")

    if df.empty:
        return df

    # 1. Date Range
    min_date = df["date_received"].min()
    max_date = df["date_received"].max()

    st.sidebar.subheader("📅 Date Range")

    col1, col2 = st.sidebar.columns(2)

    with col1:
        start_date = st.date_input(
            "Start Date", value=min_date, min_value=min_date, max_value=max_date
        )

    with col2:
        end_date = st.date_input("End Date", value=max_date, min_value=min_date, max_value=max_date)

    # 2. Company Filter
    st.sidebar.subheader("🏢 Select Company")
    top_companies = df["company"].value_counts().nlargest(50).index.tolist()
    selected_companies = st.sidebar.multiselect(
        "Select Company", options=top_companies, label_visibility="collapsed"
    )

    # 3. Product Filter
    st.sidebar.subheader("📦 Select Product")
    all_products = df["product"].unique().tolist()
    selected_products = st.sidebar.multiselect(
        "Select Product", options=all_products, label_visibility="collapsed"
    )

    # --- APPLY FILTERS ---
    mask = (
        (df["date_received"].dt.date >= start_date)
        & (df["date_received"].dt.date <= end_date)
        & (df["company"].isin(selected_companies) if selected_companies else True)
        & (df["product"].isin(selected_products) if selected_products else True)
    )

    return df[mask]
