"""
D.A.T.A. - Dashboard & Analytics Tool for Accounting
Upload → Clean → Analyze → Visualize → Export
"""

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import os
from io import BytesIO

# SVG logos are now embedded directly in HTML for better Streamlit compatibility

try:
    from styles import CUSTOM_CSS
    from utils import (
        detect_column_types,
        clean_data,
        calculate_kpis,
        get_summary_stats,
        create_trend_chart,
        create_category_chart,
        create_entity_chart,
        create_monthly_comparison_chart,
        format_currency,
        generate_summary_report,
    )
except ImportError:
    from app.styles import CUSTOM_CSS
    from app.utils import (
        detect_column_types,
        clean_data,
        calculate_kpis,
        get_summary_stats,
        create_trend_chart,
        create_category_chart,
        create_entity_chart,
        create_monthly_comparison_chart,
        format_currency,
        generate_summary_report,
    )

# Page configuration
st.set_page_config(
    page_title="D.A.T.A.",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Inject custom CSS for V0-inspired styling
# Extract just the CSS content (without <style> tags) for st.html
CSS_CONTENT = CUSTOM_CSS.replace("<style>", "").replace("</style>", "").strip()

# Use st.html for more reliable CSS injection on Railway
st.html(f"""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
{CSS_CONTENT}
</style>
""")


def check_password() -> bool:
    """Simple password protection using environment variable."""
    correct_password = os.environ.get("APP_PASSWORD", "demo2024")

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    # Full page login with centered card (matching V0 design)
    st.markdown("""
    <style>
    .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 80vh;
    }
    .login-card {
        background: rgba(240, 253, 250, 0.5);
        border: 1px solid #e7e5e4;
        border-radius: 0.75rem;
        padding: 2.5rem;
        max-width: 28rem;
        width: 100%;
        box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
    }
    .login-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
    }
    .login-icon {
        width: 3rem;
        height: 3rem;
        border-radius: 0.5rem;
        background-color: rgba(13, 148, 136, 0.1);
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .login-icon svg {
        width: 1.5rem;
        height: 1.5rem;
        color: #0d9488;
    }
    .login-title {
        font-size: 1.875rem;
        font-weight: 700;
        color: #0f172a;
        letter-spacing: -0.025em;
        margin: 0;
    }
    .login-subtitle {
        font-size: 0.875rem;
        color: #64748b;
        margin: 0;
    }
    .login-tagline {
        text-align: center;
        color: #64748b;
        font-size: 0.875rem;
        margin-bottom: 1.5rem;
    }
    .login-footer {
        text-align: center;
        font-size: 0.75rem;
        color: #64748b;
        margin-top: 1.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

    # Center the login card
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Login card with V0 styling - Database cylinder icon (Lucide style)
        st.markdown("""
        <div class="login-header">
            <div class="login-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#0d9488" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <ellipse cx="12" cy="5" rx="9" ry="3"/>
                    <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>
                    <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>
                </svg>
            </div>
            <div>
                <h1 class="login-title">D.A.T.A.</h1>
                <p class="login-subtitle"><strong>D</strong>ashboard & <strong>A</strong>nalytics <strong>T</strong>ool for <strong>A</strong>ccounting</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Password form
        st.markdown("**🔒 Password**")
        password = st.text_input("Password", type="password", key="password_input", label_visibility="collapsed", placeholder="Enter your password")

        if st.button("Access Dashboard", use_container_width=True, type="primary"):
            if password == correct_password:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password. Please try again.")

        st.markdown('<p class="login-footer">Professional financial data analysis platform</p>', unsafe_allow_html=True)

    return False


def render_header():
    """Render the app header with database icon."""
    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <div style="width: 2.5rem; height: 2.5rem; border-radius: 0.5rem; background-color: rgba(13, 148, 136, 0.1); display: flex; align-items: center; justify-content: center;">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#0d9488" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <ellipse cx="12" cy="5" rx="9" ry="3"/>
                    <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>
                    <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>
                </svg>
            </div>
            <div>
                <h1 style="margin: 0; font-size: 1.5rem; font-weight: 700; color: #0f172a; letter-spacing: -0.025em;">D.A.T.A.</h1>
                <p style="margin: 0; font-size: 0.75rem; color: #64748b;"><strong>D</strong>ashboard & <strong>A</strong>nalytics <strong>T</strong>ool for <strong>A</strong>ccounting</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 0.5rem; padding: 0.375rem 0.75rem; background-color: #f0fdfa; border: 1px solid #99f6e4; border-radius: 9999px; width: fit-content; float: right;">
            <div style="width: 0.5rem; height: 0.5rem; border-radius: 50%; background-color: #14b8a6; animation: pulse 2s infinite;"></div>
            <span style="font-size: 0.75rem; color: #0f766e; font-weight: 500;">Ready to Analyze</span>
        </div>
        <style>
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        </style>
        """, unsafe_allow_html=True)


def render_upload_section():
    """Render the file upload section."""
    st.markdown("## Data Import")

    uploaded_file = st.file_uploader(
        "Drop your CSV or Excel file here",
        type=["csv", "xlsx", "xls"],
        help="Supported formats: CSV, Excel (.xlsx, .xls)",
        label_visibility="collapsed"
    )

    return uploaded_file


def render_column_mapping(df: pd.DataFrame, detected: dict):
    """Render column type mapping interface."""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        date_options = ["Select column"] + list(df.columns)
        default_date = detected['date'][0] if detected['date'] else "Select column"
        date_idx = date_options.index(default_date) if default_date in date_options else 0

        date_col = st.selectbox(
            "Date Column",
            options=date_options,
            index=date_idx,
        )

    with col2:
        amount_options = list(df.columns)
        default_amount = detected['amount'][0] if detected['amount'] else amount_options[0]
        amount_idx = amount_options.index(default_amount) if default_amount in amount_options else 0

        amount_col = st.selectbox(
            "Amount Column",
            options=amount_options,
            index=amount_idx,
        )

    with col3:
        category_options = ["Select column"] + list(df.columns)
        default_cat = detected['category'][0] if detected['category'] else "Select column"
        cat_idx = category_options.index(default_cat) if default_cat in category_options else 0

        category_col = st.selectbox(
            "Category Column",
            options=category_options,
            index=cat_idx,
        )

    with col4:
        entity_options = ["Select column"] + list(df.columns)
        default_entity = detected['entity'][0] if detected['entity'] else "Select column"
        entity_idx = entity_options.index(default_entity) if default_entity in entity_options else 0

        entity_col = st.selectbox(
            "Entity Column",
            options=entity_options,
            index=entity_idx,
        )

    return {
        'date': date_col if date_col != "Select column" else None,
        'amount': amount_col,
        'category': category_col if category_col != "Select column" else None,
        'entity': entity_col if entity_col != "Select column" else None,
    }


def render_kpi_card(label: str, value: str, change: str = None, is_positive: bool = True, mono: bool = False):
    """Render a single KPI card using Streamlit's native metric component."""
    delta_value = None
    if change:
        delta_value = f"{'↑' if is_positive else '↓'} {change}"

    st.metric(
        label=label,
        value=value,
        delta=delta_value if change else None
    )


def render_kpis(kpis: dict):
    """Render KPI cards."""
    # Row 1: Main KPIs (removed hardcoded percentage changes for accuracy)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_kpi_card("Total Amount", format_currency(kpis['total']))
    with col2:
        render_kpi_card("Revenue (Positive)", format_currency(kpis['total_positive']))
    with col3:
        render_kpi_card("Expenses (Negative)", format_currency(kpis['total_negative']))
    with col4:
        render_kpi_card("Transaction Count", f"{kpis['count']:,}")

    st.markdown("")  # Spacing

    # Row 2: Stats (mono font)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_kpi_card("Average", format_currency(kpis['average']), mono=True)
    with col2:
        render_kpi_card("Median", format_currency(kpis['median']), mono=True)
    with col3:
        render_kpi_card("Minimum", format_currency(kpis['min']), mono=True)
    with col4:
        render_kpi_card("Maximum", format_currency(kpis['max']), mono=True)


def render_charts(df: pd.DataFrame, columns: dict):
    """Render visualization charts."""
    # Validate data before rendering charts
    if len(df) == 0:
        st.warning("⚠️ No data available to display charts.")
        return

    tab1, tab2, tab3 = st.tabs(["Trends", "Breakdown", "Top Entities"])

    with tab1:
        if columns['date']:
            try:
                trend_chart = create_trend_chart(df, columns['date'], columns['amount'])
                if trend_chart:
                    st.plotly_chart(trend_chart, use_container_width=True)
                else:
                    st.info("⚠️ Unable to create trend chart. Ensure date column has valid dates.")

                comparison_chart = create_monthly_comparison_chart(
                    df, columns['date'], columns['amount']
                )
                if comparison_chart:
                    st.plotly_chart(comparison_chart, use_container_width=True)
                else:
                    st.info("⚠️ Unable to create comparison chart. Ensure date column has valid dates.")
            except Exception as e:
                st.error(f"⚠️ Error creating trend charts: {str(e)}")
        else:
            st.info("Select a date column to see trend analysis")

    with tab2:
        if columns['category']:
            try:
                col1, col2 = st.columns([1, 4])
                with col1:
                    chart_type = st.radio(
                        "Chart Type",
                        options=["pie", "bar"],
                        format_func=lambda x: "Pie Chart" if x == "pie" else "Bar Chart",
                        label_visibility="collapsed"
                    )

                category_chart = create_category_chart(
                    df, columns['category'], columns['amount'], chart_type
                )
                if category_chart:
                    st.plotly_chart(category_chart, use_container_width=True)
                else:
                    st.warning("⚠️ Unable to create category chart. Check your category column.")
            except Exception as e:
                st.error(f"⚠️ Error creating category chart: {str(e)}")
        else:
            st.info("Select a category column to see breakdown analysis")

    with tab3:
        if columns['entity']:
            try:
                col1, col2 = st.columns([1, 4])
                with col1:
                    top_n = st.slider("Show top N", min_value=5, max_value=20, value=10)

                entity_chart = create_entity_chart(
                    df, columns['entity'], columns['amount'], top_n
                )
                if entity_chart:
                    st.plotly_chart(entity_chart, use_container_width=True)
                else:
                    st.warning("⚠️ Unable to create entity chart. Check your entity column.")
            except Exception as e:
                st.error(f"⚠️ Error creating entity chart: {str(e)}")
        else:
            st.info("Select an entity column to see top performers")


def render_data_preview(df: pd.DataFrame):
    """Render data preview section."""
    with st.expander("📋 Data Preview", expanded=False):
        st.dataframe(df.head(100), use_container_width=True)
        st.caption(f"Showing first 100 of {len(df):,} rows")


def render_export_section(df: pd.DataFrame, columns: dict):
    """Render export/download section."""
    st.markdown("## Export Options")

    col1, col2, col3 = st.columns(3)

    with col1:
        csv_buffer = BytesIO()
        df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)

        st.download_button(
            label="Download CSV",
            data=csv_buffer,
            file_name="processed_data.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with col2:
        summary_df = generate_summary_report(df, columns['amount'], columns['category'])
        summary_buffer = BytesIO()
        summary_df.to_csv(summary_buffer, index=False)
        summary_buffer.seek(0)

        st.download_button(
            label="Export Summary",
            data=summary_buffer,
            file_name="summary_report.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with col3:
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Data', index=False)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)

            if columns['category']:
                by_cat = df.groupby(columns['category'])[columns['amount']].agg(
                    ['sum', 'count', 'mean']
                ).reset_index()
                by_cat.columns = [columns['category'], 'Total', 'Count', 'Average']
                by_cat.to_excel(writer, sheet_name='By Category', index=False)

        excel_buffer.seek(0)

        st.download_button(
            label="Excel Report",
            data=excel_buffer,
            file_name="finance_analysis.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )


def generate_sample_data() -> pd.DataFrame:
    """Generate realistic sample financial transaction data."""
    np.random.seed(42)
    n_records = 500

    # Date range: last 12 months
    dates = pd.date_range(end=pd.Timestamp.now(), periods=n_records, freq='D')
    dates = np.random.choice(dates, n_records)

    categories = ['Payroll', 'Software', 'Marketing', 'Operations', 'Travel',
                  'Utilities', 'Supplies', 'Professional Services']

    vendors = ['Acme Corp', 'TechStart Inc', 'Global Services', 'Data Systems',
               'Cloud Nine', 'Prime Solutions', 'NetWorks LLC', 'Digital First',
               'Summit Group', 'Alpha Tech']

    # Generate amounts - mix of expenses (negative) and revenue (positive)
    amounts = []
    for _ in range(n_records):
        if np.random.random() < 0.3:  # 30% revenue
            amounts.append(np.random.uniform(5000, 50000))
        else:  # 70% expenses
            amounts.append(-np.random.uniform(100, 15000))

    df = pd.DataFrame({
        'Transaction Date': dates,
        'Amount': amounts,
        'Category': np.random.choice(categories, n_records),
        'Vendor': np.random.choice(vendors, n_records),
        'Description': [f'Transaction #{i+1000}' for i in range(n_records)]
    })

    return df.sort_values('Transaction Date').reset_index(drop=True)


def render_footer():
    """Render the app footer."""
    st.markdown("---")
    st.caption("D.A.T.A. • Built with Streamlit • Part of [Financial Analytics Portfolio](https://github.com/jkatz015)")


def main():
    """Main application entry point."""

    # Check authentication
    if not check_password():
        return

    # Render header
    render_header()

    st.markdown("---")

    # File upload section
    st.markdown("## Data Import")

    col_upload, col_sample = st.columns([3, 1])

    with col_upload:
        uploaded_file = st.file_uploader(
            "Drop your CSV or Excel file here",
            type=["csv", "xlsx", "xls"],
            help="Supported formats: CSV, Excel (.xlsx, .xls)"
        )

    with col_sample:
        st.markdown("")  # Spacing
        if st.button("Load Sample Data", use_container_width=True):
            st.session_state.sample_data = generate_sample_data()
            st.session_state.using_sample = True

    # Check if we have data (uploaded or sample)
    df = None
    data_source = None

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            data_source = "uploaded"
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
            st.info("Please ensure your file is a valid CSV or Excel format.")

    elif st.session_state.get('using_sample', False):
        df = st.session_state.sample_data
        data_source = "sample"

    if df is not None:
        # Validate data
        if len(df) == 0:
            st.error("⚠️ The uploaded file is empty. Please upload a file with data.")
            return

        # Status badge update - use native Streamlit components
        badge_text = f"{len(df):,} rows loaded" if data_source == "uploaded" else "Sample Data Loaded"
        st.success(f"✅ {badge_text}")

        # Auto-detect column types
        detected = detect_column_types(df)

        # Column mapping
        columns = render_column_mapping(df, detected)

        st.markdown("")  # Spacing
        st.markdown("")  # Spacing

        # Action buttons row
        col_analyze, col_clear = st.columns([3, 1])
        with col_analyze:
            if st.button("Analyze Data", use_container_width=True, type="primary"):
                # Validate required columns
                if not columns['amount']:
                    st.error("⚠️ Please select an Amount column to proceed with analysis.")
                else:
                    try:
                        with st.spinner("Processing your data..."):
                            df_clean = clean_data(df, columns['date'], columns['amount'])

                            # Validate cleaned data
                            if len(df_clean) == 0:
                                st.error("⚠️ No valid data remaining after cleaning. Please check your date and amount columns.")
                            else:
                                st.session_state.df_clean = df_clean
                                st.session_state.columns = columns
                                st.session_state.analyzed = True
                                st.success("✅ Data analyzed successfully!")
                                st.rerun()
                    except Exception as e:
                        st.error(f"⚠️ Error during analysis: {str(e)}")
                        st.info("Please check your column selections and data format.")

        with col_clear:
            if st.button("Clear Data", use_container_width=True):
                # Clear session state
                for key in ['df_clean', 'columns', 'analyzed', 'sample_data', 'using_sample']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()

        # Show results if analyzed
        if st.session_state.get('analyzed', False):
            df_clean = st.session_state.df_clean
            columns = st.session_state.columns

            st.markdown("---")

            # KPIs
            kpis = calculate_kpis(df_clean, columns['amount'])
            render_kpis(kpis)

            st.markdown("---")

            # Charts
            render_charts(df_clean, columns)

            st.markdown("---")

            # Data preview
            render_data_preview(df_clean)

            # Export
            render_export_section(df_clean, columns)

    else:
        # Show helpful info when no file uploaded - use native Streamlit components
        st.markdown("---")
        st.info("📊 Drop a CSV or Excel file to get started")
        st.caption("Or click 'Load Sample Data' to explore with demo transactions")

    # Footer
    render_footer()


if __name__ == "__main__":
    main()
