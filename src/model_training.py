import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from data_preprocessing import load_and_merge

# XGBoost Regression
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

df = load_and_merge()
df['month'] = df['date'].dt.month

X = df[['ev_units', 'month']]
y = df['price_usd_per_ton']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

model = xgb.XGBRegressor(objective='reg:squarederror')
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print('XGBoost MAE:', mean_absolute_error(y_test, y_pred))

# LSTM Time-Series Forecasting
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
price_scaled = scaler.fit_transform(df[['price_usd_per_ton']])

def create_sequences(data, seq_length):
    xs, ys = [], []
    for i in range(len(data) - seq_length):
        xs.append(data[i:i+seq_length])
        ys.append(data[i+seq_length])
    return np.array(xs), np.array(ys)

seq_length = 3
X_lstm, y_lstm = create_sequences(price_scaled, seq_length)

split = int(0.8 * len(X_lstm))
X_train_lstm, X_test_lstm = X_lstm[:split], X_lstm[split:]
y_train_lstm, y_test_lstm = y_lstm[:split], y_lstm[split:]

model_lstm = Sequential([
    LSTM(50, activation='relu', input_shape=(seq_length, 1)),
    Dropout(0.2),
    Dense(1)
])
model_lstm.compile(optimizer='adam', loss='mse')
model_lstm.fit(X_train_lstm, y_train_lstm, epochs=50, batch_size=1, verbose=1)

y_pred_lstm = model_lstm.predict(X_test_lstm)
y_pred_inv = scaler.inverse_transform(y_pred_lstm)
y_test_inv = scaler.inverse_transform(y_test_lstm)

print('LSTM MAE:', np.mean(np.abs(y_test_inv - y_pred_inv))) 