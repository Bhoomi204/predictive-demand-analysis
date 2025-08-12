import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from prophet import Prophet


st.title("Multi-Metal Future Price Forecast")

# List of metals
metals = ['lithium', 'copper', 'nickel', 'aluminum', 'cobalt']
results = {}

# Generate synthetic data and fit Prophet for each metal
for metal in metals:
    np.random.seed(hash(metal) % 2**32)
    dates = pd.date_range(start='2022-01-01', periods=36, freq='M')
    base_price = {
        'lithium': 18000, 'copper': 9000, 'nickel': 20000, 'aluminum': 2500, 'cobalt': 35000
    }[metal]
    price = base_price + np.cumsum(np.random.normal(300, 200, 36))
    df = pd.DataFrame({'date': dates, 'price_usd_per_ton': price})

    # Prepare data for Prophet
    prophet_df = df.rename(columns={'date': 'ds', 'price_usd_per_ton': 'y'})[['ds', 'y']]

    # Fit Prophet on all available data
    model_prophet = Prophet()
    model_prophet.fit(prophet_df)

    # Forecast next 6 months
    future = model_prophet.make_future_dataframe(periods=6, freq='M')
    forecast = model_prophet.predict(future)

    # Only keep future predictions (dates after last actual)
    last_actual_date = df['date'].max()
    future_only = forecast[forecast['ds'] > last_actual_date].copy()

    # Store results
    results[metal] = {
        'future_only': future_only,
        'future_price': float(future_only['yhat'].iloc[-1]) if not future_only.empty else np.nan
    }

# Display table of future prices (last forecasted value for each metal)
future_prices = {metal: results[metal]['future_price'] for metal in metals}
st.write("## Predicted Price (6 Months Ahead, USD/ton)")
st.table(pd.DataFrame.from_dict(future_prices, orient='index', columns=['Predicted Price']).style.format("{:,.2f}"))

# Highlight the highest value metal
max_metal = max(future_prices, key=future_prices.get)
st.success(f"The predicted highest value metal in 6 months is: **{max_metal.capitalize()}** at ${future_prices[max_metal]:,.2f} per ton")

# 🔗 Add button to view hotspot map for the predicted top metal
if st.button("Show Hotspots for Highest Value Metal"):
    st.session_state['selected_metal'] = max_metal
    st.switch_page("pages/hotspot_map.py")

# Let user select a metal to view details
selected_metal = st.selectbox("Select a metal to view future forecast:", metals)
future_only = results[selected_metal]['future_only']

# Plot only future predictions
st.subheader(f"{selected_metal.capitalize()}: Future Price Forecast (Next 6 Months)")

# Color scheme
primary_color = '#90D26D'   # green
secondary_color = '#459D72' # teal
background_color = '#342B2B' # dark brown

fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor(background_color)
ax.set_facecolor(background_color)
ax.plot(future_only['ds'], future_only['yhat'], label='Predicted Price (Future)', marker='o', color=primary_color, markerfacecolor=secondary_color)
ax.fill_between(future_only['ds'], future_only['yhat_lower'], future_only['yhat_upper'], color=secondary_color, alpha=0.2, label='Confidence Interval')
ax.set_xlabel('Date', color=primary_color)
ax.set_ylabel('Price (USD/ton)', color=primary_color)
ax.set_title(f"{selected_metal.capitalize()} Price Forecast: Next 6 Months", color=primary_color)
ax.tick_params(axis='x', colors=primary_color)
ax.tick_params(axis='y', colors=primary_color)
legend = ax.legend()
for text in legend.get_texts():
    text.set_color(primary_color)
st.pyplot(fig)

# Show only the future forecast table
st.write(f"Prophet Forecast for {selected_metal.capitalize()} (Next 6 Months):")
st.dataframe(
    future_only[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].reset_index(drop=True)
    .rename(columns={'ds': 'Date', 'yhat': 'Predicted Price', 'yhat_lower': 'Lower Bound', 'yhat_upper': 'Upper Bound'})
) 