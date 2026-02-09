import time
import random
from datetime import datetime, timezone

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# ===============================
# InfluxDB Cloud Config
# ===============================
INFLUX_URL = "https://us-east-1-1.aws.cloud2.influxdata.com"
INFLUX_TOKEN = "YOUR_TOKEN_HERE"   
ORG = "64d08bf112f03d85"               
BUCKET = "weather_bucket"

# ===============================
# Sensor Metadata
# ===============================
CITY = "Dhaka"
SENSOR_ID = "SIM-DHAKA-01"

# ===============================
# Initial Sensor Values
# ===============================
temperature = 25.0
humidity = 65.0

# ===============================
# InfluxDB Client
# ===============================
client = InfluxDBClient(
    url=INFLUX_URL,
    token=INFLUX_TOKEN,
    org=ORG
)

write_api = client.write_api(write_options=SYNCHRONOUS)

print("Realtime simulated sensor started (1 second interval)...")

# ===============================
# Realtime Sensor Loop
# ===============================
try:
    while True:
        # generate smooth sensor-like variation
        temperature += random.uniform(-0.15, 0.15)
        humidity += random.uniform(-0.5, 0.5)

        # clamp to realistic range
        temperature = max(15.0, min(40.0, temperature))
        humidity = max(30.0, min(95.0, humidity))

        point = (
            Point("weather")
            .tag("city", CITY)
            .tag("sensor_id", SENSOR_ID)
            .field("temperature", round(temperature, 2))
            .field("humidity_pct", round(humidity, 2))
            .time(datetime.now(timezone.utc))
        )

        write_api.write(
            bucket=BUCKET,
            org=ORG,
            record=point
        )

        print(
            f"Data sent | City={CITY} | "
            f"Temp={temperature:.2f}C | "
            f"Humidity={humidity:.2f}%"
        )

        time.sleep(1)   # 1 second realtime

except KeyboardInterrupt:
    print("\nStopping realtime sensor...")
    client.close()
