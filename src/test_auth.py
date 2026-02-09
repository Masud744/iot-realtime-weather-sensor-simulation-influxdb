from influxdb_client import InfluxDBClient

client = InfluxDBClient(
    url="https://us-east-1-1.aws.cloud2.influxdata.com",
    token="YOUR_TOKEN_HERE",
    org="64d08bf112f03d85"
)

print("Auth OK")
client.close()
