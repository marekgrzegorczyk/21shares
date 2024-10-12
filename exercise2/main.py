import time

import streamlit as st

from data import fetch_binance_ohlcv
from fig import create_large_data_chart, create_random_chart, create_figure
from processing import calculate_indicators

# User Experience: Added st.set_page_config to set the page title, icon, layout, initial_sidebar_state, and menu items
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


# Added st.fragment decorator to generate_large_chart function to improve the performance of the application.
@st.fragment
def generate_large_chart(title: str):
    """
    Generate a large data chart with the given title.
    """
    return create_large_data_chart(title=title)


# Added st.fragment decorator to generate_random_chart function to improve the performance of the application.
@st.fragment
def generate_random_chart(title: str):
    """
    Generate a random chart with the given title.
    """
    return create_random_chart(title=title)


#
def dashboard():
    """
    Main dashboard function to display the Streamlit application.
    """
    st.title("21.co Streamlit Test - Optimization Exercise")

    # Added sidebar context manager to improve readability and organization of the code
    with st.sidebar:
        st.title("Filters")
        coin = st.selectbox("Select Coin", ["BTC/USDT", "ETH/USDT", "LTC/USDT"])
        frequency = st.selectbox(
            "Select Update Frequency", ["1 second", "5 seconds", "10 seconds"]
        )
        frequency_map = {"1 second": 1, "5 seconds": 5, "10 seconds": 10}
        st.title("Indicators")
        show_ema_12 = st.checkbox("Show EMA 12", value=True)
        show_ema_26 = st.checkbox("Show EMA 26", value=True)
        show_bollinger = st.checkbox("Show Bollinger Bands", value=True)
        bollinger_window = st.slider("Bollinger Bands Window", 10, 50, 10)

        # User Experience: Added about popover  to provide information about the filters
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

    # Added main content context manager to improve readability and organization of the code
    with st.container():
        plot_placeholder = st.empty()
        update_data_toggle = st.toggle(
            "Stop/Start Data Update", key="update_data_toggle", value=True
        )
        fetch_info_placeholder = st.empty()
        message_placeholder = st.empty()

        # Display a warning about the calculation time
        message_placeholder.warning(
            "Please wait, the initial calculations may take some time..."
        )

        # Display the large data chart first
        large_data_fig = generate_large_chart(title="Complex Calculation Result (FFT)")
        plot_placeholder.plotly_chart(large_data_fig)
        # time.sleep(5)  # Simulate loading time

        # Display additional random charts
        random_chart_1 = generate_random_chart(title="Random Chart 1")
        plot_placeholder.plotly_chart(random_chart_1, key="random_chart_1")
        # time.sleep(3)  # Simulate loading time

        random_chart_2 = generate_random_chart(title="Random Chart 2")
        plot_placeholder.plotly_chart(random_chart_2, key="random_chart_2")
        # time.sleep(3)  # Simulate loading time

        # Update the message to indicate heavy processing is finished
        message_placeholder.success(
            "Finished heavy processing charts. Now displaying real-time OHLCV chart."
        )

        while True:
            # User Experience: spinner was added in data.py in fetch_binance_ohlcv function to show the spinner while the data is being fetched
            data = fetch_binance_ohlcv(coin)
            data = calculate_indicators(
                data,
                ema_12=show_ema_12,
                ema_26=show_ema_26,
                bollinger=show_bollinger,
                window=bollinger_window,
            )
            fig = create_figure(
                data, ema_12=show_ema_12, ema_26=show_ema_26, bollinger=show_bollinger
            )

            # Added uuid to the key to avoid StreamlitDuplicateElementKey error
            # Key handling does not allow manipulation of the dashboarded because it creates a new version every selected frequency
            plot_placeholder.plotly_chart(fig, key=f"real_time_chart")
            # User Experience: Display the last updated time
            fetch_info_placeholder.info(
                f"Chart updated at {time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}"
            )
            time.sleep(frequency_map[frequency])


if __name__ == "__main__":
    dashboard()
