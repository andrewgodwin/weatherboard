import time
import pytz
import requests
from datetime import datetime


class WeatherClient:
    def __init__(self, latitude, longitude):
        self.latitude = float(latitude)
        self.longitude = float(longitude)

    def load(self, api_key):
        self.data = requests.get(
            f"https://api.openweathermap.org/data/2.5/onecall?lat={self.latitude}&lon={self.longitude}&exclude=minutely&units=metric&appid={api_key}"
        ).json()
        self.current_time = self.data["current"]["dt"]

    def temp_current(self):
        return self.data["current"]["temp"]

    def temp_range_24hr(self):
        temps = [
            hour["temp"]
            for hour in self.data["hourly"]
            if hour["dt"] - self.current_time < 86400
        ]
        return min(temps), max(temps)

    def humidity_current(self):
        return self.data["current"]["humidity"]

    def sunrise(self):
        return datetime.utcfromtimestamp(self.data["current"]["sunrise"]).replace(
            tzinfo=pytz.utc
        )

    def sunset(self):
        return datetime.utcfromtimestamp(self.data["current"]["sunset"]).replace(
            tzinfo=pytz.utc
        )

    def hourly_summary(self, time_offset):
        # Find the right hour
        target = time.time() + time_offset
        for d1, d2 in zip(self.data["hourly"], self.data["hourly"][1:]):
            if d1["dt"] < target < d2["dt"]:
                break
        data = d1
        # Format a summary
        return {
            "time": datetime.utcfromtimestamp(data["dt"]).replace(tzinfo=pytz.utc),
            "icon": self.code_to_icon(data["weather"][0]["id"]),
            "description": data["weather"][0]["main"].title(),
            "temperature": data["temp"],
            "wind": data["wind_speed"] * 2.2,
            "rain": 2,  # data.get("rain", {}).get("1h", 0),
            "snow": 4,  # data.get("snow", {}).get("1h", 0),
            "uv": data["uvi"],
        }

    def daily_summary(self, day_offset):
        data = self.data["daily"][day_offset]
        # Format a summary
        return {
            "date": datetime.utcfromtimestamp(data["dt"]).replace(tzinfo=pytz.utc),
            "icon": self.code_to_icon(data["weather"][0]["id"]),
            "description": data["weather"][0]["main"].title(),
            "temperature_range": (data["temp"]["min"], data["temp"]["max"]),
            "wind": data["wind_speed"] * 2.2,
        }

    def code_to_icon(self, code):
        if code == 511:
            return "snow"
        elif code == 771:
            return "thunderstorm"
        elif 200 <= code < 300:
            return "thunderstorm"
        elif 300 <= code < 400:
            return "showers"
        elif 500 <= code < 505:
            return "rain"
        elif 520 <= code < 600:
            return "showers"
        elif 611 <= code < 620:
            return "sleet"
        elif 600 <= code < 700:
            return "snow"
        elif 700 <= code < 800:
            return "fog"
        elif code == 800:
            return "clear-day"
        elif code == 801:
            return "clouds-few-day"
        elif code == 802:
            return "clouds-scattered"
        else:
            return "clouds-broken"
