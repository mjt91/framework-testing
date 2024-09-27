"""Simple FastApi Forecasting App."""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
import pandas as pd

from statsforecast.models import AutoARIMA
from statsforecast import StatsForecast

# Init FastApi
app = FastAPI()

# Access templates
templates = Jinja2Templates(directory="templates")

dataf = pd.read_parquet("data/AirPassengers.parquet")


# Define a request model for the forecast endpoint
class ForecastRequest(BaseModel):
    periods: int  # Number of months to forecast


# Define an API endpoint for forecasting
@app.post("/forecast/")
async def forecast(request: ForecastRequest):
    # Use StatsForecast with AutoARIMA model
    model = StatsForecast(models=[AutoARIMA()], freq="MS")

    # Fit the model on the AirPassengers data
    model.fit(dataf)

    # Generate forecast for the specified number of periods
    forecast_df = model.predict(h=request.periods)

    # Return forecast as JSON
    return forecast_df.to_dict(orient="records")


# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
