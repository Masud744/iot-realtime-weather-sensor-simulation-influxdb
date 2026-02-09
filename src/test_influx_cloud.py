from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

url = "https://us-east-1-1.aws.cloud2.influxdata.com"
token = "YOUR_TOKEN_HERE"
org = "IoT Frontier"
bucket = "weather_bucket" 

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

point = (
    Point("weather")
    .tag("city", "Dhaka")
    .field("temperature", 30.8)
    .field("humidity", 74)
)

write_api.write(bucket=bucket, org=org, record=point)

print("Data written to InfluxDB Cloud successfully")


client.close()
