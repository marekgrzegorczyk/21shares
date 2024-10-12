import streamlit as st

logo_path = "static/21co.png"

# results_data = {
#     "KPI": ["startDate", "EndDate", "cumulativeRet", "annRet",
#             "sharpeRatio",
#             "sortinoRatio", "infoRatio", "TrackingError",
#             "maxDrawdown",
#             "VaR95 (monthly)",
#             "VaR95 (annually)", "1Y", "3Y", "5Y", "alpha (vs SP500)",
#             "beta (vs SP500)", "turnover (ann)"],
#     "Benchmark": ["12/13/2016", "3/13/2022", "170.7%", "10.9%", "0.94",
#                   "1.91", "1.14", "-", "-11.2%", "-4.2%",
#                   "-1.2%", "-14.8%", "3.8%", "5.7%", "0.0%", "0.62%",
#                   "9.9%"]
# }


equity_data = {
    "Asset": ["AAPL", "NVDA", "GOOG"],
    "Type": ["Stock", "Stock", "Stock"],
    "Allocation": [32.43, 0.0, 0.0]
}
fixed_income_data = {
    "Asset": ["TLT", "JNK", "GOOG"],
    "Type": ["Fixed Income", "Fixed Income", "Fixed Income"],
    "Allocation": [20.00, 12.00, 2.00]
}
commodities_data = {
    "Asset": ["GLD", "USOIL", "XAG"],
    "Type": ["Commodity", "Commodity", "Commodity"],
    "Allocation": [0.00, 3.00, 0.00]
}
crypto_data = {
    "Asset": ["BTC", "ETH", "STX"],
    "Type": ["Crypto", "Crypto", "Crypto"],
    "Allocation": [0.00, 0.00, 0.00]
}

asset_options = {
    "Equity": ["AAPL", "NVDA", "GOOG"],
    "Fixed Income": ["US Bonds", "Corporate Bonds"],
    "Commodities": ["Gold", "Oil", "Silver"],
    "Crypto": ["Bitcoin", "Ethereum", "Litecoin"]
}

st.set_page_config(layout="wide", page_title="Portfolio Simulator",
                   page_icon=":chart_with_upwards_trend:",
                   initial_sidebar_state="collapsed")


@st.dialog(title="Add Asset", width="large")
def add_asset_dialog(dialog_selectbox_data):
    category_select = st.multiselect(
        label="Select Category",
        label_visibility="collapsed",
        placeholder="Select Category",
        options=["Equity", "Fixed Income", "Commodities", "Crypto"],
        help="Select the category of the asset you want to add.",
        key="category_select"
    )

    if category_select:
        for category in category_select:
            st.divider()
            with st.container(border=True):
                category_lower = category.title().replace(" ", "_").lower()
                st.subheader(f"{category} Assets")
                st.multiselect(
                    label=f"Select {category} Asset",
                    options=asset_options.get(category, []),
                    key=f"{category_lower}_asset_select"
                )
            dialog_selectbox_data.append((category_select, category))
    with st.form(key="add_asset_form"):
        st.form_submit_button("Save")


def df_in_container(data, subheader_text):
    with st.container(border=True):
        col1, col2, col3 = st.columns([3, 1, 1], vertical_alignment="bottom")

        with col1:
            st.write(subheader_text)

        with col2:
            st.number_input(label="", value=0.1, min_value=0.1,
                            max_value=100.0,
                            step=0.1, format="%0.1f",
                            key=f"input_{subheader_text}",
                            disabled=True,
                            )
        with col3:
            st.info(body="", icon="➕")

        st.dataframe(data, hide_index=True, use_container_width=True,
                     selection_mode="single")


def dashboard():
    dialog_selectbox_data = []
    header_col1, header_col2 = st.columns([1, 10], vertical_alignment="center")
    with header_col1:
        st.image(logo_path, )
    with header_col2:
        st.header("Portfolio Simulator")

    col1, col2 = st.columns([1, 3])

    with col1:
        with st.container(border=True):
            header_col1, header_col2 = st.columns(
                [2, 1], vertical_alignment="center")
            with header_col1:
                st.write("Portfolio composition")
            with header_col2:
                if st.button("\+ Add Asset", key="add_asset"):
                    add_asset_dialog(dialog_selectbox_data)

            button_col1, button_col2 = st.columns([1, 1])
            with button_col1:
                # weighted_value = st.session_state.get(
                #     "absolute")
                # absolute_value = st.session_state.get(
                #     "weighted")
                st.checkbox("Weighted", key="weighted", value=True,
                            )
            with button_col2:
                st.checkbox("Absolute", key="absolute",
                            )
            df_in_container(data=equity_data, subheader_text="🍧 Equity")

            df_in_container(data=fixed_income_data,
                            subheader_text="🍺 Fixed Income")

            df_in_container(data=commodities_data,
                            subheader_text="🍊 Commodities")

            df_in_container(data=crypto_data, subheader_text="⭐ Crypto")

            st.button("Save as benchmark portfolio", use_container_width=True)

    with col2:
        st.write("col2")
        st.write(dialog_selectbox_data)
        #
        # dates = pd.date_range(start="2023-01-01", periods=365)
        # spx_data = np.random.normal(loc=0.1, scale=0.05, size=365).cumsum()
        # benchmark_data = np.random.normal(loc=0.05, scale=0.03,
        #                                   size=365).cumsum()
        #
        # performance_data = pd.DataFrame({
        #     "Date": dates,
        #     "SPX": spx_data,
        #     "Benchmark": benchmark_data
        # })
        #
        # date_options = ["1D", "1W", "1M", "6M", "YTD", "1Y", "Max"]
        # selected_range = st.selectbox("Select Time Range", date_options)
        #
        # if selected_range == "1D":
        #     filtered_data = performance_data.tail(1)
        # elif selected_range == "1W":
        #     filtered_data = performance_data.tail(7)
        # elif selected_range == "1M":
        #     filtered_data = performance_data.tail(30)
        # elif selected_range == "6M":
        #     filtered_data = performance_data.tail(180)
        # elif selected_range == "YTD":
        #     filtered_data = performance_data[
        #         performance_data["Date"] >= pd.to_datetime("2023-01-01")]
        # elif selected_range == "1Y":
        #     filtered_data = performance_data.tail(365)
        # else:  # "Max"
        #     filtered_data = performance_data
        #
        # # Rysowanie wykresu po filtrowaniu
        # st.line_chart(filtered_data.set_index("Date"))
        #
        # st.header("Results")
        #
        # # Wyświetlenie tabeli bez numeracji (index=False)
        # st.table(pd.DataFrame(results_data).style.hide(axis='index'))


if __name__ == "__main__":
    dashboard()
