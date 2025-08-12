# Predictive Demand Analytics for Metals (Prophet Future-Only Dashboard)

## Overview
This project provides a scalable, production-ready dashboard for forecasting and comparing the **future prices** of multiple key metals (lithium, copper, nickel, aluminum, cobalt) using Prophet. The dashboard is now focused on displaying **only future predictions** (next 6 months) for each metal—no actuals, no test set, no overlap. It is designed for easy integration into larger analytics or business intelligence products.

## Features
- **Prophet modeling** for robust time series forecasting
- **Multi-metal support**: lithium, copper, nickel, aluminum, cobalt (easily extendable)
- **Interactive Streamlit dashboard**
- **Comparison and highlighting** of the most valuable metal in the future
- **Synthetic data generation** (no real data required, but can be adapted)
- **Future-focused**: Only the next 6 months of predicted prices are displayed—in both the chart and the table. No actuals or historical predictions are shown.

## Quick Start

### 1. Python Version & Virtual Environment
- **Recommended Python version:** 3.11 (Prophet does NOT support Python 3.12+ as of mid-2024)
- **Set up a virtual environment** (recommended):

```bash
# Install Python 3.11 if not already installed
# Download from https://www.python.org/downloads/release/python-3119/

# Create and activate a virtual environment (Windows example)
python -m venv venv
venv\Scripts\activate

# On macOS/Linux:
# python3.11 -m venv venv
# source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

If you see errors about `prophet`, double-check you are using Python 3.11.

### 3. Run the Dashboard

```bash
streamlit run src/dashboard.py
```

- The dashboard will open in your browser (usually at http://localhost:8501).
- You can compare metals, see future price forecasts (next 6 months), and highlight the most valuable one.

## Project Structure
```
predictive_demand_analytics/
├── data/                # (Not used in current dashboard, for future real data)
├── notebooks/           # (Jupyter notebooks for EDA, not required for dashboard)
├── src/
│   └── dashboard.py     # Main Streamlit dashboard (entry point)
├── requirements.txt     # All dependencies
├── README.md            # This file
```

## Troubleshooting
- **Prophet install errors:**
  - Ensure you are using Python 3.11 (not 3.12+).
  - On Windows, you may need to install build tools for Prophet. See [Prophet install docs](https://facebook.github.io/prophet/docs/installation.html).
- **Plotly warning:**
  - The dashboard uses matplotlib, but if you want interactive plots, install plotly: `pip install plotly`.
- **Virtual environment not activating:**
  - Double-check your shell and Python version. Use `python --version` to confirm.

## Extending/Integrating
- **To use real data:**
  - Replace the synthetic data generation in `dashboard.py` with your own data loading logic (e.g., from CSV or database).
- **To add more metals:**
  - Add to the `metals` list and provide a base price in the code.
- **To integrate into a larger product:**
  - The dashboard is modular and can be imported as a Streamlit app or the modeling logic can be refactored into a package.

## Contact
For questions or integration support, contact the project maintainer or open an issue in your main product repository. 