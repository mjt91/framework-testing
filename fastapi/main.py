"""Simple FastApi Forecasting App."""
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

from statsforecast.models import AutoARIMA
from statsforecast import StatsForecast

# Init FastApi
app = FastAPI()

dataf = pd.read_parquet("data/AirPassengers.parquet")


# Define a request model for the forecast endpoint
class ForecastRequest(BaseModel):
    periods: int  # Number of months to forecast


# Define an API endpoint for forecasting
@app.post("/forecast/")
async def forecast(request: ForecastRequest):
    # Use StatsForecast with AutoARIMA model
    model = StatsForecast(models=[AutoARIMA()], freq='MS')

    # Fit the model on the AirPassengers data
    model.fit(dataf)

    # Generate forecast for the specified number of periods
    forecast_df = model.predict(h=request.periods)
    
    # Return forecast as JSON
    return forecast_df.to_dict(orient="records")


# Root endpoint
@app.get("/")
async def home():
    return {"message": "Welcome to the AirPassengers Forecast API!"}
