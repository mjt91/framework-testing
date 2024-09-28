# Testing different frameworks

This repo is a playground for testing different frameworks to build (mostly data) applications.

For now I built these:
1. Time Series Forecasting App using fastapi + basic html templating
2. Time Series Anomalies Detection App using streamlit

## FastApi + Html templating

**Idea:** Create time series forecasting application. The user can decide about the horizon.
The model fitting and predicting happens on the client side for now.

At a later stage decide if model training happens beforehand and the model is served only.
Allowing the user to use different models may be an improvement too.

```console
cd fastapi
uv run uvicorn main:app --reload
```


## Streamlit Time Series Anomalies Detection App

**Idea:** Create an app that allows users to upload csv files and analyze it with regards to anomalies.

```console
cd streamlit
uv run streamlit run app.py
```
