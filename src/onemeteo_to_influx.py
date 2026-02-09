import time
import requests
from datetime import datetime, timezone

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# =========================
# Open-Meteo Configuration
# =========================
API_URL = (
    "Your_Open_Meteo_API_Endpoint_Here"
)

CITY = "Dhaka"
SENSOR_ID = "OM-DHAKA-01"

# =========================
# InfluxDB Cloud Config
# =========================
INFLUX_URL = "https://us-east-1-1.aws.cloud2.influxdata.com"
INFLUX_TOKEN = "YOUR_TOKEN_HERE"
ORG = "IoT Frontier"
BUCKET = "weather_bucket"

client = InfluxDBClient(
    url=INFLUX_URL,
    token=INFLUX_TOKEN,
    org=ORG
)

write_api = client.write_api(write_options=SYNCHRONOUS)

print("Open-Meteo realtime sensor started...")

# =========================
# Realtime Sensor Loop
# =========================
while True:
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()

        temp = float(data["hourly"]["temperature_2m"][0])
        humidity = float(data["hourly"]["relative_humidity_2m"][0])

        point = (
            Point("weather")
            .tag("city", CITY)
            .tag("sensor_id", SENSOR_ID)
            .field("temperature", temp)
            .field("humidity_pct", humidity)
            .time(datetime.now(timezone.utc))
        )

        write_api.write(
            bucket=BUCKET,
            org=ORG,
            record=point
        )

        print(
            f"Data sent | City={CITY} | Temp={temp}C | Humidity={humidity}%"
        )

    except Exception as e:
        print("Error occurred, retrying in 60s:", str(e))
        time.sleep(60)
        continue

    # ⏱ Real sensor interval (1 minute)
    time.sleep(60)
