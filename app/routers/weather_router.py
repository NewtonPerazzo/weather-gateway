from typing import Annotated
from datetime import date

from fastapi import APIRouter, Depends, Response

from app.dependency import WeatherServiceDependency
from app.models.weather_analysis.weather_model import (
    CityForecastAnalysisResponseModel,
    CityHourAnalysisResponseModel,
    FilterTime,
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
    current_user: Annotated[
        UsersModel,
        Depends(get_current_user),
    ],
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
    current_user: Annotated[
        UsersModel,
        Depends(get_current_user),
    ],
    weather_service: WeatherServiceDependency,
    city: str,
    country_code: str,
    day: date | None = None,
    filter: FilterTime | None = None,
) -> CityHourAnalysisResponseModel:
    return await weather_service.get_forecast_hour_analysis(
        city=city,
        country_code=country_code,
        day=day,
        filter_time=filter,
    )


@weather_router.post("/reports")
async def create_report(
    current_user: Annotated[UsersModel, Depends(get_current_user)],
    weather_service: WeatherServiceDependency,
    city_key: str,
    city_name: str | None = None,
    day: date | None = None,
    filter: FilterTime | None = None,
) -> dict:
    return await weather_service.create_report(
        city_key=city_key,
        city_name=city_name,
        day=day,
        filter_time=filter,
    )


@weather_router.get("/reports", response_model=None)
async def get_report(
    current_user: Annotated[UsersModel, Depends(get_current_user)],
    weather_service: WeatherServiceDependency,
    task_id: str,
):
    content, status, content_disposition, content_type = await weather_service.get_report(task_id)
    if content is None:
        return status or {"task_id": task_id, "status": "processing"}
    headers = {"Content-Disposition": content_disposition} if content_disposition else {}
    return Response(
        content=content,
        media_type=content_type or "application/octet-stream",
        headers=headers,
    )
