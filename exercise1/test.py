# with st.container(border=True):
#     col1, col2 = st.columns(spec=2, vertical_alignment="bottom")
#     with col1:
#         st.write("#### Performance")
#     with col2:
#         # yFinance does not support exact '1W', but '5d' covers the working week
#         filter_periods = {
#             "1D": "1d",
#             "1W": "5d",
#             "1M": "1mo",
#             "3M": "3mo",
#             "6M": "6mo",
#             "1Y": "1y",
#             "YTD": "ytd",
#             "MAX": "max",
#         }
#
#         selected_filter = st.radio(
#             label="",
#             options=filter_periods.keys(),
#             horizontal=True,
#             key="chart_date_filter",
#         )
#
#     with st.container(key="chart_container", border=True):
#         placeholder_chart()
#
# with st.container(border=True):
#     st.write("#### Results ")
#     if not st.session_state.assets:
#         st.info("Add assets to view risk metrics.")
#     else:
#         # Benchmark selection
#         benchmark_ticker = st.selectbox(
#             "Select Benchmark", options=["^GSPC", "^IXIC", "^DJI"], index=0
#         )
#
#         # Get selected period
#         period = filter_periods[selected_filter]
#
#         # Fetch benchmark data
#         benchmark_data = fetch_benchmark_data(benchmark_ticker, period)
#
#         # Fetch portfolio returns using the user-selected assets and allocations
#         portfolio_returns = calculate_weighted_returns(
#             selected_assets, allocations, period
#         )
#
#         # Calculate risk and performance metrics
#         metrics = calculate_metrics(portfolio_returns, benchmark_data)
#
#         # Display the metrics in a table
#         display_metrics_table(metrics)
