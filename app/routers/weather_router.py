from typing import Annotated
from datetime import date

from fastapi import APIRouter, Depends

from app.dependency import WeatherServiceDependency
from app.models.weather_analysis.weather_model import (
    CityForecastAnalysisResponseModel,
    CityHourAnalysisResponseModel,
    ForecastResponseModel,
    SearchCityRequest,
)
from app.models.authentication.users_model import UsersModel
from app.authentication_dependency import get_current_user

weather_router = APIRouter(tags=["Weather"])


@weather_router.post("/search-city")
async def get_forecast(
    current_user: Annotated[
        UsersModel,
        Depends(get_current_user),
    ],
    weather_service: WeatherServiceDependency,
    city_request: SearchCityRequest
) -> ForecastResponseModel:
    return await weather_service.get_city_forecast_info(city_request=city_request)


@weather_router.get("/get-forecast-analysis")
async def get_forecast_analysis(
    weather_service: WeatherServiceDependency,
    city: str,
    country_code: str,
) -> CityForecastAnalysisResponseModel:
    return await weather_service.get_forecast_analysis(
        city=city,
        country_code=country_code,
    )


@weather_router.get("/get-forecast-hourly-analysis")
async def get_forecast_hour_analysis(
    weather_service: WeatherServiceDependency,
    city: str,
    country_code: str,
    day: date | None = None,
) -> CityHourAnalysisResponseModel:
    return await weather_service.get_forecast_hour_analysis(
        city=city,
        country_code=country_code,
        day=day,
    )
