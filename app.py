import streamlit as st
import plotly.graph_objects as go

from data_loader import get_stock_data


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Stock Market Analysis",
    page_icon="📈",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("📈 Stock Market Analysis and Visualization")

st.write(
    "An interactive stock market analysis dashboard "
    "using Python, Streamlit, Yahoo Finance and Plotly."
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("📊 Stock Selection")

ticker = st.sidebar.text_input(
    "Enter Stock Symbol",
    value="AAPL"
).strip().upper()

period = st.sidebar.selectbox(
    "Select Analysis Period",
    ["1mo", "3mo", "6mo", "1y", "2y", "5y"]
)


# ============================================================
# ANALYZE BUTTON
# ============================================================

analyze_button = st.sidebar.button(
    "🔍 Analyze Stock"
)


# ============================================================
# MAIN APPLICATION
# ============================================================

if analyze_button:

    if not ticker:

        st.error("Please enter a stock symbol.")

        st.stop()


    try:

        # ----------------------------------------------------
        # LOAD DATA
        # ----------------------------------------------------

        data = get_stock_data(
            ticker,
            period
        )


        # ----------------------------------------------------
        # CHECK DATA
        # ----------------------------------------------------

        if data.empty:

            st.error(
                f"No stock data found for {ticker}. "
                "Please check the stock symbol."
            )

            st.stop()


        # ----------------------------------------------------
        # GET CLOSE AND VOLUME
        # ----------------------------------------------------

        close_prices = data["Close"]
        volume_data = data["Volume"]


        # ----------------------------------------------------
        # MAKE SURE VALUES ARE SIMPLE SERIES
        # ----------------------------------------------------

        if hasattr(close_prices, "columns"):

            close_prices = close_prices.iloc[:, 0]


        if hasattr(volume_data, "columns"):

            volume_data = volume_data.iloc[:, 0]


        # Convert to numeric values
        close_prices = close_prices.astype(float)
        volume_data = volume_data.astype(float)


        # Remove missing values
        close_prices = close_prices.dropna()
        volume_data = volume_data.dropna()


        # ----------------------------------------------------
        # KPI VALUES
        # ----------------------------------------------------

        current_price = float(
            close_prices.iloc[-1]
        )

        highest_price = float(
            close_prices.max()
        )

        lowest_price = float(
            close_prices.min()
        )

        latest_volume = int(
            volume_data.iloc[-1]
        )


        # ----------------------------------------------------
        # SUCCESS MESSAGE
        # ----------------------------------------------------

        st.success(
            f"✅ Data loaded successfully for {ticker}"
        )


        # ====================================================
        # MARKET OVERVIEW
        # ====================================================

        st.subheader("📊 Market Overview")


        col1, col2, col3, col4 = st.columns(4)


        col1.metric(
            "Current Price",
            f"${current_price:,.2f}"
        )


        col2.metric(
            "Highest Price",
            f"${highest_price:,.2f}"
        )


        col3.metric(
            "Lowest Price",
            f"${lowest_price:,.2f}"
        )


        col4.metric(
            "Latest Volume",
            f"{latest_volume:,}"
        )


        # ====================================================
        # HISTORICAL PRICE CHART
        # ====================================================

        st.subheader("📈 Historical Stock Price")


        fig = go.Figure()


        fig.add_trace(
            go.Scatter(
                x=close_prices.index,
                y=close_prices.values,
                mode="lines",
                name="Closing Price"
            )
        )


        fig.update_layout(
            title=f"{ticker} Closing Price",
            xaxis_title="Date",
            yaxis_title="Price",
            height=500,
            hovermode="x unified"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


        # ====================================================
        # TRADING VOLUME
        # ====================================================

        st.subheader("📊 Trading Volume")


        volume_fig = go.Figure()


        volume_fig.add_trace(
            go.Bar(
                x=volume_data.index,
                y=volume_data.values,
                name="Trading Volume"
            )
        )


        volume_fig.update_layout(
            title=f"{ticker} Trading Volume",
            xaxis_title="Date",
            yaxis_title="Volume",
            height=400,
            hovermode="x unified"
        )


        st.plotly_chart(
            volume_fig,
            use_container_width=True
        )


        # ====================================================
        # HISTORICAL DATA
        # ====================================================

        st.subheader("📋 Historical Data")


        st.dataframe(
            data.tail(20),
            use_container_width=True
        )


    except Exception as e:

        st.error(
            f"❌ Error while analyzing {ticker}: {e}"
        )


# ============================================================
# INITIAL SCREEN
# ============================================================

else:

    st.info(
        "👈 Enter a stock symbol from the sidebar "
        "and click 'Analyze Stock' to begin."
    )