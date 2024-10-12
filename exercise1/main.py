import matplotlib.pyplot as plt
import streamlit as st
import yfinance as yf

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


# Function to fetch data from yfinance
@st.cache_data(show_spinner=True)
def fetch_asset_data(ticker):
    try:
        asset = yf.Ticker(ticker)
        return asset.info["longName"], asset.info["symbol"], asset.info["quoteType"]
    except Exception as e:
        st.error(body=f"Error fetching data for {ticker}: {e}")
        return None, None, None


# Define the main dashboard function
def dashboard():
    header_col1, header_col2 = st.columns([1, 10], vertical_alignment="center")
    with header_col1:
        st.image(logo_path)
    with header_col2:
        st.header(body="Portfolio Simulator")

    main_col1, main_col2 = st.columns([2, 5])

    # Initialize session state to hold dynamic assets and allocations
    with main_col1:
        if "assets" not in st.session_state:
            st.session_state.assets = {}

        user_allocations = {category: {} for category in st.session_state.assets}

        # Create a form for portfolio inputs
        with st.form(key="portfolio_form", enter_to_submit=False):
            form_header_col1, form_header_col2 = st.columns(
                [2, 1], vertical_alignment="center"
            )
            with form_header_col1:
                st.write("#### Portfolio Composition")

            with form_header_col2:
                with st.popover(label="\+ Add Asset"):
                    st.write("#### Add Asset to Portfolio")
                    new_asset = st.text_input(
                        label="Add new asset (ticker symbol)", key="new_asset_ticker"
                    )
                    if st.form_submit_button(label="Add Asset", type="secondary"):
                        if new_asset:
                            # Check if the asset is already in any category
                            asset_exists = any(
                                new_asset in assets
                                for assets in st.session_state.assets.values()
                            )
                            if asset_exists:
                                st.error(
                                    f"Asset {new_asset} already exists in the portfolio!"
                                )
                            else:
                                name, symbol, quote_type = fetch_asset_data(new_asset)
                                if name and quote_type:
                                    # Add asset under the correct quoteType (category)
                                    if quote_type not in st.session_state.assets:
                                        st.session_state.assets[quote_type] = []
                                    st.session_state.assets[quote_type].append(
                                        new_asset
                                    )
                                    st.success(body=f"Added {new_asset} ({quote_type})")
                                    st.rerun()
                                else:
                                    st.error(
                                        body=f"Asset {new_asset} is invalid or could not be fetched!"
                                    )

            for category in st.session_state.assets:
                col1, col2 = st.columns(spec=[2, 1], vertical_alignment="bottom")
                with col1:
                    st.write(f"#### {category}")
                with col2:
                    total_allocation = sum(user_allocations[category].values())
                    st.text_input(
                        label="",
                        disabled=True,
                        value=f"{total_allocation:.2f}%",
                        key=f"total_{category}",
                    )

                # Display current assets in the category
                if st.session_state.assets[category]:
                    for asset in st.session_state.assets[category]:
                        name, symbol, quote_type = fetch_asset_data(asset)
                        if name and symbol:
                            col1, col2 = st.columns(
                                spec=[3, 2], vertical_alignment="bottom"
                            )
                            with col1:
                                # Input for allocation
                                allocation = st.number_input(
                                    f"{name} ({symbol})",
                                    min_value=0.0,
                                    max_value=100.0,
                                    key=f"allocation_{asset}",
                                )
                                user_allocations[category][asset] = allocation
                            with col2:
                                if st.form_submit_button(
                                    label=f"Remove {asset}",
                                    type="secondary",
                                    use_container_width=True,
                                ):
                                    # Remove the asset from the category after submission
                                    st.session_state.assets[category].remove(asset)
                                    # Remove the category if empty after removal of asset
                                    if len(st.session_state.assets[category]) == 0:
                                        del st.session_state.assets[category]
                                    st.rerun()

            if "show_main_col" not in st.session_state:
                st.session_state.show_main_col = False

            submitted = st.empty()
            if len(st.session_state.assets) == 0:
                st.info(
                    body="No assets added. Click '+ Add Asset' to add assets to your portfolio."
                )
            else:
                submitted = st.form_submit_button(
                    label="Save as benchmark portfolio", type="primary"
                )
                if submitted:
                    st.session_state.show_main_col = True

    with main_col2:
        st.write("Main column")
        if st.session_state.show_main_col:
            # Generate and display a bar chart of portfolio composition
            fig, ax = plt.subplots()
            category_allocations = {
                category: sum(user_allocations[category].values())
                for category in st.session_state.assets
            }
            ax.bar(category_allocations.keys(), category_allocations.values())
            ax.set_xlabel("Category")
            ax.set_ylabel("Allocation (%)")
            ax.set_title("Benchmark Portfolio Allocation")

            st.pyplot(fig)

            # Optionally show raw data (for reference)
            st.write("## Portfolio Allocations")
            for category, assets in user_allocations.items():
                for asset, allocation in assets.items():
                    st.write(f"{category} - {asset}: {allocation}%")


# Main entry point
if __name__ == "__main__":
    dashboard()
