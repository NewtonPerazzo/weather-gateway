from datetime import date

import httpx

from app.integrations.APIIntegration import APIIntegration
from app.models.weather_analysis.weather_model import CityForecastAnalysisResponseModel, CityHourAnalysisResponseModel, FilterTime, ForecastResponseModel, SearchCityRequest
import logging

logger = logging.getLogger(__name__)


WEATHER_ANALYSIS_URI = '/get-forecast-analysis'
WEATHER_HOURLY_ANALYSIS_URI = '/get-forecast-hourly-analysis'
SEARCH_CITY_URI = '/search-city'

class WeatherService():
    def __init__(
        self,
        api_integrations: APIIntegration,
    ) -> None:
        self.__api_integrations = api_integrations

    async def get_forecast_analysis(self, city: str, country_code: str) -> CityForecastAnalysisResponseModel:
        url = self.get_url(WEATHER_ANALYSIS_URI)
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params={ 'city': city , 'country_code': country_code })
            response.raise_for_status()
            return response.json()

    async def get_city_forecast_info(
            self, 
            city_request: SearchCityRequest
        ) -> ForecastResponseModel:
        url = self.get_url(SEARCH_CITY_URI)
        city_request_data = SearchCityRequest.model_dump(city_request)

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=city_request_data)
            logger.info(
                "Weather response: status=%s body=%s",
                response.status_code,
                response.text,
            )
            response.raise_for_status()
            return response.json()

    async def get_forecast_hour_analysis(
        self,
        city: str,
        country_code: str,
        day: date | None = None,
        filter_time: FilterTime | None = None,
    ) -> CityHourAnalysisResponseModel:
        url = self.get_url(WEATHER_HOURLY_ANALYSIS_URI)
        params = {
            'city': city,
            'country_code': country_code,
        }
        if day is not None:
            params['day'] = day.isoformat()
        if filter_time is not None:
            params['filter'] = filter_time

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()

    def get_url(self, uri: str) -> str:
        return f'{self.__api_integrations.weather_url}{uri}'
