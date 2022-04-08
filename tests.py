import unittest
from unittest import mock
from unittest.mock import MagicMock, patch
from openweather import get_weather
import json
import os

# testing the weather API response
class WeatherTest(unittest.TestCase):
    def test_get_weather(self):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "coord": {"lon": -84.388, "lat": 33.749},
            "weather": [
                {
                    "id": 803,
                    "main": "Clouds",
                    "description": "broken clouds",
                    "icon": "04n",
                }
            ],
            "base": "stations",
            "main": {
                "temp": 282.55,
                "feels_like": 280.89,
                "temp_min": 279.96,
                "temp_max": 284.11,
                "pressure": 1011,
                "humidity": 53,
            },
            "visibility": 10000,
            "wind": {"speed": 3.09, "deg": 270},
            "clouds": {"all": 75},
            "dt": 1649399895,
            "sys": {
                "type": 2,
                "id": 2006620,
                "country": "US",
                "sunrise": 1649416533,
                "sunset": 1649462566,
            },
            "timezone": -14400,
            "id": 4180439,
            "name": "Atlanta",
            "cod": 200,
        }

        with patch("openweather.requests.get") as mock_requests_get:
            mock_requests_get.return_value = mock_response

            self.assertEqual(
                get_weather(),
                {
                    "weather": "Clouds",
                    "city": "Atlanta",
                    "fahrenheit": "48.92 F°",
                    "country": "US",
                },
            )


if __name__ == "__main__":
    unittest.main()
