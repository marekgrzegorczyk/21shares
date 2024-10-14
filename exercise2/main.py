import time

import streamlit as st

from data import fetch_binance_ohlcv
from fig import create_large_data_chart, create_random_chart, create_figure
from processing import calculate_indicators

# User Experience: Set the page configuration to improve layout and add a favicon
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


# Cache the resource of the large data chart generation
@st.cache_resource
def generate_large_chart(title: str):
    """
    Generate a large data chart with the given title.
    Cached to improve performance for large data sets.
    """
    return create_large_data_chart(title=title)


# Cache the resource of random chart generation
@st.cache_resource
def generate_random_chart(title: str):
    """
    Generate a random chart with the given title.
    Cached for efficiency.
    """
    return create_random_chart(title=title)


def dashboard():
    """
    Main dashboard function to display the Streamlit application.
    """
    st.title("21.co Streamlit Test - Optimization Exercise")

    # Sidebar
    with st.sidebar:
        st.title("Filters")
        coin = st.selectbox(
            "Select Coin", ["BTC/USDT", "ETH/USDT", "LTC/USDT"], key="coin"
        )
        frequency = st.selectbox(
            "Select Update Frequency",
            ["1 second", "5 seconds", "10 seconds"],
            key="frequency",
        )
        frequency_map = {"1 second": 1, "5 seconds": 5, "10 seconds": 10}
        st.title("Indicators")
        show_ema_12 = st.checkbox("Show EMA 12", value=True, key="show_ema_12")
        show_ema_26 = st.checkbox("Show EMA 26", value=True, key="show_ema_26")
        show_bollinger = st.checkbox(
            "Show Bollinger Bands", value=True, key="show_bollinger"
        )
        bollinger_window = st.slider(
            "Bollinger Bands Window", 10, 50, 10, key="bollinger_window"
        )

        with st.popover(label="About", help="Information about filters"):
            st.write(
                """
                - **Select Coin**: Choose a coin pair to display the OHLCV chart.
                - **Select Update Frequency**: Choose the frequency to update the OHLCV chart.
                - **Show EMA 12**: Display the Exponential Moving Average with a window of 12.
                - **Show EMA 26**: Display the Exponential Moving Average with a window of 26.
                - **Show Bollinger Bands**: Display the Bollinger Bands.
                - **Bollinger Bands Window**: Choose the window size for the Bollinger Bands.
                """
            )

    # Main content
    with st.container():
        plot_placeholder = st.empty()
        fetch_info_placeholder = st.empty()
        message_placeholder = st.empty()

        # Display a warning about the calculation time
        message_placeholder.warning(
            "Please wait, the initial calculations may take some time..."
        )
        with st.spinner("Calculating..."):
            # Display the large data chart first (cached)
            large_data_fig = generate_large_chart(
                title="Complex Calculation Result (FFT)"
            )
            plot_placeholder.plotly_chart(large_data_fig)
            # time.sleep(3)

            # Display additional random charts (cached)
            random_chart_1 = generate_random_chart(title="Random Chart 1")
            plot_placeholder.plotly_chart(random_chart_1, key="random_chart_1")
            # time.sleep(3)

            random_chart_2 = generate_random_chart(title="Random Chart 2")
            plot_placeholder.plotly_chart(random_chart_2, key="random_chart_2")
            # time.sleep(3)

        # Update the message to indicate heavy processing is finished
        message_placeholder.success(
            "Finished heavy processing charts. Now displaying real-time OHLCV chart."
        )

        # Define the fragment function for real-time chart updates
        @st.fragment(run_every=f"{frequency_map[st.session_state['frequency']]}s")
        def update_real_time_chart():
            # Fetch OHLCV data
            data = fetch_binance_ohlcv(st.session_state["coin"])
            data = calculate_indicators(
                data,
                ema_12=st.session_state["show_ema_12"],
                ema_26=st.session_state["show_ema_26"],
                bollinger=st.session_state["show_bollinger"],
                window=st.session_state["bollinger_window"],
            )
            fig = create_figure(
                data,
                ema_12=st.session_state["show_ema_12"],
                ema_26=st.session_state["show_ema_26"],
                bollinger=st.session_state["show_bollinger"],
            )
            plot_placeholder.plotly_chart(fig)
            fetch_info_placeholder.info(f"Chart updated at {time.strftime('%H:%M:%S')}")

        # Call the fragment function
        update_real_time_chart()


if __name__ == "__main__":
    dashboard()
