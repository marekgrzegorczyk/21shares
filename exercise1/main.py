import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Set up the page configuration for the Streamlit app
st.set_page_config(
    page_title="21Shares Streamlit Exercise",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://www.linkedin.com/in/marek-grzegorczyk-a2b8a420a/",
        "Report a bug": "mailto:marekgrzegorczykk93@gmail.com",
        "About": "# 21Shares Streamlit Exercise by Marek Grzegorczyk",
    },
)

logo_path = "static/21co.png"


# Fetch asset data from yfinance. Cached to avoid re-fetching the same data repeatedly.
@st.cache_data(show_spinner=True)
def fetch_asset_data(ticker):
    """
    Fetch asset data using the yfinance API. Returns the long name, symbol, and type of the asset.
    """
    try:
        asset = yf.Ticker(ticker)
        return (
            asset.info.get("longName"),
            asset.info.get("symbol"),
            asset.info.get("quoteType"),
        )
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return None, None, None


# The main function that runs the dashboard.
def dashboard():
    """
    This is the main logic for the portfolio simulator. It handles rendering the UI for adding/removing assets
    and allocating portfolio weights.
    """
    # Check if the session state needs to be initialized
    if "show_main_col" not in st.session_state:
        st.session_state.show_main_col = False

    # Render header with the logo and title
    header_col1, header_col2 = st.columns([1, 10], vertical_alignment="center")
    with header_col1:
        st.image(logo_path)
    with header_col2:
        st.header("Portfolio Simulator")

    # Main layout with two columns: one for input and one for visualization
    main_col1, main_col2 = st.columns([2, 5])

    # Left Column: Handle asset input and portfolio management
    with main_col1:
        # If assets aren't initialized in the session state, create an empty dictionary
        if "assets" not in st.session_state:
            st.session_state.assets = {}

        # This will store the user's allocations for each asset category (e.g., stock, ETF, etc.)
        user_allocations = {category: {} for category in st.session_state.assets}

        # Form to manage portfolio assets
        with st.form(key="portfolio_form", enter_to_submit=False):
            # Header for portfolio form
            form_header_col1, form_header_col2 = st.columns(
                [2, 1], vertical_alignment="center"
            )
            with form_header_col1:
                st.write("#### Portfolio Composition")

            # Add Asset functionality inside a popover
            with form_header_col2:
                with st.popover(label="+ Add Asset"):
                    st.write("#### Add Asset to Portfolio")
                    new_asset = st.text_input(
                        "Add new asset (ticker symbol)", key="new_asset_ticker"
                    )

                    if st.form_submit_button(label="Add Asset", type="secondary"):
                        if not new_asset:
                            st.error("Please enter a ticker symbol.")
                        elif any(
                            new_asset in assets
                            for assets in st.session_state.assets.values()
                        ):
                            st.error(f"Asset {new_asset} is already in the portfolio!")
                        else:
                            name, symbol, quote_type = fetch_asset_data(new_asset)
                            if not name or not quote_type:
                                st.error(f"Asset {new_asset} could not be found.")
                            else:
                                # Add the asset under the correct category (e.g., Stock, ETF)
                                if quote_type not in st.session_state.assets:
                                    st.session_state.assets[quote_type] = []
                                st.session_state.assets[quote_type].append(new_asset)
                                st.success(f"Added {new_asset} ({quote_type})")
                                st.rerun()

            # If there are assets in the portfolio, show the allocation inputs
            if st.session_state.assets:
                # Let the user choose how they want to allocate (percentage or absolute value)
                with st.container(border=True):
                    allocation_type = st.radio(
                        label="",
                        options=["% Weighted", "$ Absolute"],
                        horizontal=True,
                        key="allocation_type",
                    )

                # Iterate through each asset category and render its assets
                for category in st.session_state.assets:
                    with st.container(border=True):
                        col1, col2 = st.columns([2, 1], vertical_alignment="bottom")
                        with st.container(border=True):
                            with col1:
                                st.write(f"#### {category}")
                            with col2:
                                # Sum up total allocation per category
                                total_allocation = sum(
                                    user_allocations[category].values()
                                )
                                st.text_input(
                                    "",
                                    value=f"{total_allocation:.2f}%",
                                    disabled=True,
                                    key=f"total_{category}",
                                )

                            # Display assets within the category
                            for asset in st.session_state.assets[category]:
                                name, symbol, quote_type = fetch_asset_data(asset)
                                if (
                                    name and symbol
                                ):  # Only display if data fetch is successful
                                    col1, col2 = st.columns(
                                        [3, 2], vertical_alignment="bottom"
                                    )
                                    with col1:
                                        # User input for asset allocation
                                        allocation = st.number_input(
                                            f"{name} ({symbol})",
                                            min_value=0.0,
                                            max_value=100.0,
                                            key=f"allocation_{asset}",
                                        )
                                        user_allocations[category][asset] = allocation
                                    with col2:
                                        # Button to remove asset
                                        if st.form_submit_button(
                                            label=f"Remove {asset.upper()}",
                                            type="secondary",
                                            use_container_width=True,
                                        ):
                                            st.session_state.assets[category].remove(
                                                asset
                                            )
                                            # Clean up empty categories
                                            if not st.session_state.assets[category]:
                                                del st.session_state.assets[category]
                                            st.rerun()

                # Remove all assets or submit the portfolio
                remove_all_assets = st.form_submit_button(
                    label="Remove All Assets", type="primary", use_container_width=True
                )
                submitted = st.form_submit_button(
                    label="Save as benchmark portfolio",
                    type="primary",
                    use_container_width=True,
                )

                # Clear the portfolio
                if remove_all_assets:
                    st.session_state.show_main_col = False
                    st.session_state.assets.clear()
                    st.rerun()

                # Show the simulator if the user submits the portfolio
                if submitted:
                    st.session_state.show_main_col = True
            else:
                # No assets yet, prompt the user to add some
                st.info("No assets added. Click '+ Add Asset' to build your portfolio.")

    # Right Column: This will eventually show the portfolio simulator once the user has added assets
    with main_col2:
        with st.container(border=True):

            # if st.session_state.show_main_col:
            st.write("#### Performance")

            # Create a placeholder chart
            dates = pd.date_range(start="2023-01-01", periods=12, freq="M")
            placeholder_performance = np.zeros(len(dates))

            # Create Plotly figure
            fig = go.Figure()

            # Add a line that remains at zero
            fig.add_trace(
                go.Scatter(
                    x=dates,
                    y=placeholder_performance,
                    mode="lines",
                    name="Performance",
                    line=dict(color="grey", width=2, dash="dash"),
                )
            )

            # Add annotation to inform the user
            fig.add_annotation(
                text="Add assets to generate the chart",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=True,
                font=dict(size=16, color="grey"),
            )

            # Update layout to match the clean style
            fig.update_layout(
                # title="Performance",
                xaxis_title="Date",
                yaxis_title="Performance (%)",
                template="simple_white",
                showlegend=False,
                margin=dict(l=20, r=20, t=40, b=20),
                height=400,
            )

            # Update the x-axis to show date formatting
            fig.update_xaxes(
                tickformat="%b %Y",
                showgrid=False,
            )

            # Update y-axis for percentages
            fig.update_yaxes(
                ticksuffix="%",
                showgrid=True,
                gridcolor="lightgrey",
            )

            # Display chart in Streamlit
            st.plotly_chart(fig, use_container_width=True)

        with st.container(border=True):
            st.write("#### Results ")


# Run the app
if __name__ == "__main__":
    dashboard()
