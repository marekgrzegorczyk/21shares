# Exercise 1 - Build a Portfolio Allocation Dashboard

In this exercise, you will build a portfolio allocation dashboard using Streamlit. The goal is to create a functional and interactive dashboard that allows users to select various assets, assign weights to them, and visualize the portfolio's cumulative returns and risk metrics.

## Exercise Instructions

The purpose of this exercise is to develop a dashboard that allows users to build and analyze a portfolio consisting of different asset classes such as stocks, bonds, and cryptocurrencies. Users will be able to fetch daily prices or OHLCV data for any ticker supported by Yahoo Finance, assign weights to the selected assets, and visualize the portfolio's performance and risk metrics.

### Focus Areas

The purpose of this exercise is not to implement all metrics but to focus on the following aspects:
- **Dashboard Functionality**: Ensure the dashboard is fully functional and interactive.
- **Performance**: Optimize the dashboard for speed and efficiency.
- **User Experience**: Provide a smooth user journey through intuitive filters and meaningful visualizations.
- **Visualizations**: Add charts and visualizations that enhance the interpretability of the data. Feel free to include any additional charts that you find meaningful and helpful for the analysis.

### Tasks

1. **Fetch Data**
   - Use the Yahoo Finance API to fetch daily prices or OHLCV data for any supported ticker. You can refer to the [yfinance package](https://pypi.org/project/yfinance/) for this purpose.
   
2. **User Input for Portfolio Allocation**
   - Implement filters in the left sidebar to allow users to choose assets (stocks, bonds, crypto).
   - Allow users to assign weights to each selected asset. Ensure the sum of the weights is always 100%.

3. **Calculate Cumulative Returns**
   - Calculate and display the cumulative returns chart for the portfolio in the center of the dashboard.

4. **Display Performance & Risk Metrics Table**
   - Display risk metrics and performance metrics in a table as shown in the Figma design. Metrics can include (as shown in the figma design):
     - **Risk Metrics**:
       - **Value at Risk (VaR 95%)**: Estimates the maximum loss a portfolio could face over a given period with 95% confidence.
       - **Annual Volatility**: Measures the annualized standard deviation of portfolio returns, indicating the risk level.
       - **Maximum Drawdown**: The largest peak-to-trough decline in the portfolio's value, representing the worst loss.
       - **Tracking Ratio**: Measures the standard deviation of the difference between portfolio returns and benchmark returns.
       - **Information Ratio**: Compares portfolio returns above the benchmark to the volatility of those returns.
       - **Hit Ratio**: The percentage of periods where the portfolio outperforms the benchmark.
       - **Rolling Hit Ratio**: Similar to Hit Ratio but calculated over rolling periods.
       - **Relative Drawdown**: Measures the drawdown relative to the benchmark's performance.
     - **Performance Metrics**:
       - **Cumulative Returns**: The total return of the portfolio over the period.
       - **Annual Returns**: The yearly return of the portfolio.
       - **Sharpe Ratio**: Measures the portfolio's risk-adjusted return, calculated as the return above the risk-free rate divided by the portfolio's standard deviation.
       - **Sortino Ratio**: Similar to Sharpe Ratio but only considers downside risk.
       - **Alpha**: The excess return of the portfolio relative to the benchmark.
       - **Beta**: Measures the portfolio's sensitivity to market movements.
       - **Turnover Rate**: The percentage of the portfolio's holdings that have been replaced over a period.

     The default benchmark can be the S&P 500. However, you may add the ability for users to choose which benchmark to use and fetch its data from Yahoo Finance.

5. **Enhancements**
   - The exercise is open-ended. You are encouraged to add more advanced charts and analyses if needed. The Figma design is a starting point, but feel free to enhance the functionality.

### Project Structure

Your project should follow this structure:

```
/project-directory
    /data.py
    /fig.py
    /processing.py
    /query.py
    /main.py
    requirements.txt
    Dockerfile
```

### Implementation Notes

- **Data Fetching**: Use `query.py` to handle all data fetching operations. Implement functions to call the Yahoo Finance API and retrieve the necessary data.
- **Data Processing**: Use `processing.py` for data processing tasks such as calculating returns, aggregating data, and preparing it for visualization.
- **Figure Generation**: Use `fig.py` to create all charts and visualizations. This includes the cumulative returns chart and any additional charts you decide to implement.
- **Main Application**: Implement the Streamlit application in `main.py`. This file will handle the layout of the dashboard, user inputs, and the integration of various components.
- **Dependencies**: List all dependencies in `requirements.txt`. Ensure that the project can be easily set up by installing these dependencies.
- **Containerization**: Provide a `Dockerfile` to allow the project to be containerized and run in any environment.

### Dashboard Performance and Optimization

- **Efficiency**: Ensure that your code runs efficiently and can handle large datasets without significant delays.
- **Caching**: Implement caching mechanisms where appropriate to reduce redundant data fetching and processing.
- **Interactivity**: Make sure the dashboard is interactive and responsive to user inputs.

---

By completing this exercise, you will demonstrate your ability to build a functional and interactive data visualization dashboard, handle API integrations, perform data processing, and optimize the performance of your application. Good luck!

---

## Contributing

Feel free to submit issues or pull requests if you find any bugs or have suggestions for improvements.

## License

This project is licensed under the MIT License.
