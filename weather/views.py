from django.views.generic import TemplateView
import requests
from environs import Env

env = Env()
env.read_env()


class HomepageView(TemplateView):
    template_name = "home.html"

    def dispatch(self, request, *args, **kwargs):
        # retrieve remote ip address
        remote_addr = request.META["REMOTE_ADDR"]
        # Pass the IP to weather api and get weather info
        self.weather = self.ip_to_weather(remote_addr)

        return super().dispatch(request, *args, **kwargs)

    def ip_to_weather(self, IP):
        url = "https://api.weatherapi.com/v1/current.json"
        params = {
            "key": env("WEATHER_API_KEY"),
            "q": IP,
            "aqi": "yes",
        }

        response = requests.get(url, params)
        if "error" in response.json().keys():
            return {}
        return response.json()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["location_name"] = self.weather["location"]["name"]
        context["region"] = self.weather["location"]["region"]
        context["country"] = self.weather["location"]["country"]
        context["localtime"] = self.weather["location"]["localtime"]
        context["current_temp"] = self.weather["current"]["temp_c"]
        context["is_day"] = self.weather["current"]["is_day"]
        context["feelslike_temp"] = self.weather["current"]["feelslike_c"]
        context["weather"] = self.weather["current"]["condition"]["text"]
        context["w_icon"] = self.weather["current"]["condition"]["icon"]
        context["wind_kph"] = self.weather["current"]["wind_kph"]
        context["wind_dir"] = self.weather["current"]["wind_dir"]
        context["gust_kph"] = self.weather["current"]["gust_kph"]
        context["pressure_mb"] = self.weather["current"]["pressure_mb"]
        context["humidity"] = self.weather["current"]["humidity"]
        context["cloud"] = self.weather["current"]["cloud"]
        context["visibility"] = self.weather["current"]["vis_km"]
        return context


class DetailReportView(TemplateView):
    template_name = "detail_report.html"

    def ip_to_weather(self):
        url = "https://api.weatherapi.com/v1/current.json"
        params = {
            "key": env("WEATHER_API_KEY"),
            "q": self.get_location(),
            "aqi": "yes",
        }
        response = requests.get(url, params)
        if "error" in response.json().keys():
            return {}
        return response.json()

    def get_search(self):
        query = self.request.GET.get("search")
        return query

    def get_astronomy_data(self):
        url = "https://api.weatherapi.com/v1/astronomy.json"
        params = {
            "key": env("WEATHER_API_KEY"),
            "q": self.get_location(),
        }

        response = requests.get(url, params)
        return response.json()

    def get_location(self):
        if self.get_search():
            location = self.get_search()
        else:
            location = self.request.GET.get("param")
        return location

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        response = self.get_astronomy_data()

        self.weather = self.ip_to_weather()

        if "error" not in response.keys():
            context["location_name"] = self.weather["location"]["name"]
            context["region"] = self.weather["location"]["region"]
            context["country"] = self.weather["location"]["country"]
            context["localtime"] = self.weather["location"]["localtime"]
            context["current_temp"] = self.weather["current"]["temp_c"]
            context["is_day"] = self.weather["current"]["is_day"]
            context["feelslike_temp"] = self.weather["current"]["feelslike_c"]
            context["weather"] = self.weather["current"]["condition"]["text"]
            context["w_icon"] = self.weather["current"]["condition"]["icon"]
            context["wind_kph"] = self.weather["current"]["wind_kph"]
            context["wind_dir"] = self.weather["current"]["wind_dir"]
            context["gust_kph"] = self.weather["current"]["gust_kph"]
            context["pressure_mb"] = self.weather["current"]["pressure_mb"]
            context["humidity"] = self.weather["current"]["humidity"]
            context["cloud"] = self.weather["current"]["cloud"]
            context["visibility"] = self.weather["current"]["vis_km"]
            context["sunrise"] = response["astronomy"]["astro"]["sunrise"]
            context["sunset"] = response["astronomy"]["astro"]["sunset"]
            context["moonrise"] = response["astronomy"]["astro"]["moonrise"]
            context["moonset"] = response["astronomy"]["astro"]["moonset"]
            context["moon_phase"] = response["astronomy"]["astro"]["moon_phase"]
            return context
        else:
            context["error_code"] = True
        return context
