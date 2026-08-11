from fastapi import APIRouter
from app.models.weather_analysis.weather_model import (
    ForecastResponseModel,
    CityForecastAnalysisResponseModel,CityHourAnalysisResponseModel
)
from datetime import date
from fastapi import APIRouter, HTTPException


weather_router = APIRouter(tags=["Weather"])

@weather_router.get(
    "/search-city",
)
async def get_forecast(
    name: str,
    country_code: str,
    count: int = 1,
    language: str = 'en',
    format: str = 'json',
    forecast_days: int = 1
) -> ForecastResponseModel:

    # response = await integration_weather_service.get_city_forecast_info(
    #     name=name, 
    #     country_code=country_code,
    #     count=count,
    #     language=language,
    #     format=format,
    #     forecast_days=forecast_days
    # )
    # return response
    pass

@weather_router.get(
    "/get-forecast-analysis",
)
async def get_forecast_analysis(
    city: str, 
    country_code: str,
) -> CityForecastAnalysisResponseModel:

    # if not city or not country_code:
    #     raise HTTPException(status_code=400, detail="City and country code are required parameters.")
    
    # response = await analysis_weather_service.get_forecast_analysis(
    #     city=city, 
    #     country_code=country_code,
    # )
    # return response
    pass

@weather_router.get(
    "/get-forecast-hourly-analysis",
)
async def get_forecast_hour_analysis(
    city: str, 
    country_code: str,
    day: date | None = None,
) -> CityHourAnalysisResponseModel:

    # response = await analysis_weather_service.get_forecast_hour_analysis(
    #     city=city, 
    #     country_code=country_code,
    #     day=day
    # )
    # return response
    pass
