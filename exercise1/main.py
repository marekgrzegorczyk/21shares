import streamlit as st

from fig import (
    placeholder_chart,
    plot_cumulative_returns,
    display_metrics_table,
)
from processing import calculate_metrics, calculate_weighted_returns
from query import fetch_asset_data, fetch_benchmark_data

logo_path = "static/21co.png"

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


# The main function that runs the dashboard.
def dashboard():
    """
    This is the main logic for the portfolio simulator. It handles rendering the UI for adding/removing assets
    and allocating portfolio weights.
    """
    # Check if the session state needs to be initialized
    if "generate_chart" not in st.session_state:
        st.session_state.generate_chart = False

    if "total_allocation" not in st.session_state:
        st.session_state.total_allocation = 0.0

    if "grand_total_allocation" not in st.session_state:
        st.session_state.grand_total_allocation = 0.0

    # Render header with the logo and title
    header_col1, header_col2 = st.columns([1, 10], vertical_alignment="center")
    with header_col1:
        st.image(logo_path)
    with header_col2:
        st.header("Portfolio Simulator")

    # Main layout with two columns: one for input and one for visualization
    main_col1, main_col2, main_col3 = st.columns([3, 6, 2])

    # Left Column: Handle asset input and portfolio management
    with main_col1:
        # If assets aren't initialized in the session state, create an empty dictionary
        if "assets" not in st.session_state:
            st.session_state.assets = {}

        # This will store the user's allocations for each asset category (e.g., stock, ETF, etc.)
        user_allocations = {category: {} for category in st.session_state.assets}

        # Form to manage portfolio assets
        with st.container(border=True):
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

                    if st.button(label="Add Asset", type="secondary"):
                        if not new_asset:
                            st.error("Please enter a ticker symbol.")
                        elif any(
                            new_asset in assets
                            for assets in st.session_state.assets.values()
                        ):
                            st.error(
                                f"{new_asset.upper()} is already in the portfolio!"
                            )
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
                                st.session_state.generate_chart = False
                                st.rerun()
            st.divider()

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

                # Initialize grand total allocation at the beginning of every render cycle
                st.session_state.grand_total_allocation = 0.0
                # Store user-selected assets for later use
                selected_assets = []
                # Store corresponding allocations for later use
                allocations = []

                # Iterate through each asset category and render its assets
                for category in st.session_state.assets:
                    with st.container(border=True):
                        col1, col2 = st.columns([2, 1], vertical_alignment="bottom")

                        with st.container(border=True):
                            with col1:
                                st.write(f"#### {category}")
                            with col2:
                                # Sum up total allocation per category
                                total_allocation_input = st.empty()

                            # Display assets within the category
                            for asset in st.session_state.assets[category]:
                                name, symbol, quote_type = fetch_asset_data(asset)

                                # Display asset information in json format
                                # st.write(yf.Ticker(asset).info)

                                if (
                                    name and symbol
                                ):  # Only display if data fetch is successful

                                    # Initialize session state for each asset's allocation if not already set
                                    if f"allocation_{asset}" not in st.session_state:
                                        st.session_state[f"allocation_{asset}"] = 0.0

                                    col1, col2 = st.columns(
                                        [3, 2], vertical_alignment="bottom"
                                    )
                                    with col1:
                                        # Use the value from st.session_state to initialize the widget
                                        allocation = st.number_input(
                                            f"{name} ({symbol})",
                                            min_value=0.0,
                                            max_value=100.0,
                                            value=st.session_state[
                                                f"allocation_{asset}"
                                            ],
                                            key=f"allocation_{asset}",
                                        )
                                        user_allocations[category][asset] = allocation
                                        selected_assets.append(asset)
                                        # Convert percentage to a fraction
                                        allocations.append(allocation / 100.0)

                                    with col2:
                                        # Button to remove asset
                                        if st.button(
                                            label=f"Remove {asset.upper()}",
                                            type="secondary",
                                            use_container_width=True,
                                        ):
                                            st.session_state.assets[category].remove(
                                                asset
                                            )
                                            # Clean up empty categories
                                            if not st.session_state.assets[category]:
                                                st.session_state.assets[
                                                    category
                                                ].clear()
                                            st.rerun()

                        # Calculate total allocation for the category
                        # with st.container(border=True):
                        col1, col2 = st.columns([2, 1], vertical_alignment="bottom")
                        with col1:
                            st.write(f"Total Allocation in {category}")
                        with col2:
                            st.session_state.total_allocation = sum(
                                user_allocations[category].values()
                            )
                            total_allocation_input = st.text_input(
                                label="",
                                value=f"{st.session_state.total_allocation:.2f}%",
                                disabled=True,
                                key=f"total_{category}",
                            )

                        # Add this category's total allocation to the grand total
                        st.session_state.grand_total_allocation += (
                            st.session_state.total_allocation
                        )
                grand_total_exceeded = st.session_state.grand_total_allocation > 100.0
                grand_total_low = st.session_state.grand_total_allocation < 100.0
                # Remove all assets or submit the portfolio
                remove_all_assets = st.button(
                    label="Remove All Assets", type="primary", use_container_width=True
                )
                submitted = st.button(
                    label="Save as benchmark portfolio",
                    type="primary",
                    use_container_width=True,
                    disabled=grand_total_exceeded
                    or grand_total_low
                    or st.session_state.grand_total_allocation == 0.0,
                    key="submit_portfolio",
                )
                if grand_total_exceeded:
                    st.error(
                        "Total allocation across all assets exceeds 100%. Please adjust to continue."
                    )
                if grand_total_low:
                    st.error(
                        "Total allocation across all assets is less than 100%. Please adjust to continue."
                    )

                if st.session_state.grand_total_allocation == 0.0:
                    st.error("Total allocation is 0%. Please adjust to continue.")

                # Clear the portfolio
                if remove_all_assets:
                    st.session_state.generate_chart = False
                    st.session_state.assets.clear()
                    st.rerun()

                # Show the simulator if the user submits the portfolio
                if submitted:
                    st.session_state.generate_chart = True

            else:
                # If no assets added, prompt the user to add some
                st.info("No assets added. Click '+ Add Asset' to build your portfolio.")

    with main_col2:
        with st.container(border=True, key="performance_chart"):
            st.write("#### Performance")
            st.divider()

            if st.session_state.generate_chart:
                perf_col1, perf_col2 = st.columns(spec=2)
                with perf_col1:
                    benchmark_index = st.selectbox(
                        label="Select Benchmark Index",
                        options=["^GSPC", "^IXIC", "^DJI", "^RUT"],
                        index=0,
                        format_func=lambda x: {
                            "^GSPC": "S&P 500",
                            "^IXIC": "Nasdaq Composite",
                            "^DJI": "Dow Jones Industrial Average",
                            "^RUT": "Russell 2000",
                        }.get(x, x),
                    )
                with perf_col2:
                    period = st.radio(
                        label="Select period",
                        options=[
                            "1mo",
                            "6mo",
                            "1y",
                            "5y",
                            "10y",
                            "ytd",
                            "max",
                        ],
                        index=6,
                        horizontal=True,
                    )
            chart = st.empty()
            chart2 = st.empty()
            chart3 = st.empty()
            if not st.session_state.generate_chart:
                chart = placeholder_chart()
            else:
                # Get the submitted portfolio and calculate performance
                benchmark_data = fetch_benchmark_data(
                    benchmark_index,
                    period,
                )
                portfolio_returns = calculate_weighted_returns(
                    selected_assets, allocations, period
                )

                # Generate and display the cumulative returns plot
                chart = plot_cumulative_returns(
                    portfolio_returns=portfolio_returns,
                    benchmark_returns=benchmark_data.pct_change(),
                    benchmark_name=benchmark_index,
                )

    with main_col3:
        with st.container(border=True, key="metrics_table"):
            st.write("#### Results")
            st.divider()

            # Calculate and display the metrics table
            if not st.session_state.generate_chart:
                st.info("Add and save assets to view performance metrics.")
            else:
                portfolio_returns = calculate_weighted_returns(
                    selected_assets, allocations, period
                )
                metrics = calculate_metrics(
                    portfolio_returns, benchmark_data.pct_change()
                )
                display_metrics_table(metrics)


# Run the app
if __name__ == "__main__":
    dashboard()
