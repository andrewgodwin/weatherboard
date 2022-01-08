import datetime

holidays = {
    'us': {
        datetime.date(2021, 9, 6): "Labor Day",
        datetime.date(2021, 10, 11): "Columbus Day",
        datetime.date(2021, 11, 11): "Veterans Day",
        datetime.date(2021, 11, 25): "Thanksgiving",
        datetime.date(2021, 12, 25): "Christmas",
        datetime.date(2022, 1, 1): "New Year",
        datetime.date(2022, 1, 17): "MLK Day",
        datetime.date(2022, 2, 21): "Presidents' Day",
        datetime.date(2022, 3, 27): "Mothers' Day UK",
        datetime.date(2022, 5, 9): "Mothers' Day US",
        datetime.date(2022, 5, 30): "Memorial Day",
        datetime.date(2022, 6, 19): "Fathers' Day",
        datetime.date(2022, 6, 20): "Juneteenth",
        datetime.date(2022, 7, 4): "Independence Day",
        datetime.date(2022, 9, 5): "Labor Day",
        datetime.date(2022, 10, 10): "Columbus Day",
        datetime.date(2022, 11, 11): "Veterans Day",
        datetime.date(2022, 11, 24): "Thanksgiving",
        datetime.date(2022, 12, 25): "Christmas",
        datetime.date(2023, 1, 1): "New Year",
    },
    'gb': {
        datetime.date(2022, 1, 1): "New Year",
        datetime.date(2023, 1, 3): "New Year’s Day (substitute)",
        datetime.date(2022, 3, 27): "Mothers’ Day",
        datetime.date(2022, 4, 15): "Good Friday",
        datetime.date(2022, 4, 18): "Easter Monday",
        datetime.date(2022, 6, 2): "Spring bank holiday",
        datetime.date(2022, 6, 3): "Platinum Jubilee",
        datetime.date(2022, 6, 19): "Fathers’ Day",
        datetime.date(2022, 8, 29): "Summer bank holiday",
        datetime.date(2022, 12, 25): "Christmas",
        datetime.date(2022, 12, 26): "Boxing Day",
        datetime.date(2022, 12, 27): "Christmas Day (substitute)",
        datetime.date(2023, 1, 1): "New Year’s Day",
        datetime.date(2023, 1, 2): "New Year’s Day (substitute)",
    }
}
holidays['uk'] = holidays['gb']

def holidays_by_country(country):
    return holidays.get(country, {})
