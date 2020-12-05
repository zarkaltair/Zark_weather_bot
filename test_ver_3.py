from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
from pyowm.utils import timestamps

config_dict = get_default_config()
config_dict['language'] = 'ru'

# owm = OWM('e7bb679b81c3710fc4192bcc1018a907')
owm = OWM('70732ac514bf006244ac74c5f31de5aa', config_dict)
mgr = owm.weather_manager()
# daily_forecast = mgr.forecast_at_place('Berlin,DE', 'daily').forecast
three_h_forecast = mgr.forecast_at_place('Moscow,RU', '3h').forecast

# print(daily_forecast)
# print(three_h_forecast)

# nr_of_weathers = len()


three_forecaster = mgr.forecast_at_place('Moscow,RU', '3h')
tomorrow_at_five = timestamps.tomorrow(17, 0)
weather = three_forecaster.get_weather_at(tomorrow_at_five)

# print(weather.status)
# print(weather.detailed_status)
# print(weather.status)

print(dir(mgr.forecast_at_place('Moscow,RU', 'daily')))