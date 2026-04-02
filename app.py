import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Set the pag and title layout
st.set_page_config(page_title = "Stock Data Extraction App", layout = "wide")

#Main title of the app
st.title("Stock Data Extraction App")

#Short Description under the title
st.write("Extract stocl ,market data from yahoo Finance using ticker symbol")
# sidebar Header
st.sidebar.header("User Input")

#input box for ticker
ticker = st.sidebar.text_input("Enter Ticker", "AAPL")

#input for start date
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"))

#input for end date
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

#download button
if st.sidebar.button("Get Data"):

  #create ticker object
  stock= yf.Ticker(ticker)

  #Dowmload historical price data
  df = stock.history(start=start_date, end=end_date)
  #Check if data exists
  if df.empty:
    st.error("No data found. Please check the ticker symbol or date range.")
  else:
    #show success message
    st.success(f"Data successfully extracted for {ticker}")

    # Display company information
    st.subheader("Company Information")
    info = stock.info

    company_name = info.get("longName", "N/A")
    sector = info.get("sector", "N/A")
    industry = info.get("industry", "N/A")
    market_cap = info.get("marketCap", "N/A")
    website = info.get("website", "N/A")

    st.write(f"**Company Name:** {company_name}")
    st.write(f"**Sector:** {sector}")
    st.write(f"**Industry:** {industry}")
    st.write(f"**Market Cap:** {market_cap}")
    st.write(f"**Website:** {website}")

    #Display Sock data
    st.subheader("Historical Stock Data")
    st.dataframe(df)

    # Plot closing price
    st.subheader("Closing Price Chart")
    fig,ax = plt.subplots()
    ax.plot(df.index, df["Close"])
    ax.set_xlabel("Date")
    ax.set_ylabel("Closing Price")
    ax.set_title(f"{ticker} Closing Price")
    st.pyplot(fig)

    #Convert dataframe to CSV for download
    csv = df.to_csv().encode("utf-8")

    #download button for CSV
    st.download_button(
        label= "Download Data as CSV",
        data= csv,
        file_name= f"{ticker}_stock_data.csv",
        mime="text/csv"
    )
