

from django.conf import settings
from django.utils import timezone

from ..aquariums.models import Measurement, Parameter

from datetime import datetime
import time
from typing import List

from influxdb_client import InfluxDBClient, BucketRetentionRules, Point
from influxdb_client.rest import ApiException
from influxdb_client.client.write_api import SYNCHRONOUS

class TimeseriesDatabase():
    def __init__(self, name, id):
        # Initialize clients and apis
        self.client = InfluxDBClient(url=settings.INFLUX_URL, token=settings.INFLUX_TOKEN, org=settings.INFLUX_ORG)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()
        self.buckets_api = self.client.buckets_api()
        self.bucket = name + "-" + id

        # Try to find own bucket
        bucket = self.buckets_api.find_bucket_by_name(self.bucket)

        # If no bucket exists, create a new one
        if bucket == None:
            try:
                # 180 days retention
                retention = BucketRetentionRules(type="expires", every_seconds=15552000)
                self.buckets_api.create_bucket(bucket_name=self.bucket,
                                               retention_rules=retention,
                                               org=settings.INFLUX_ORG)
            except ApiException:
                # If we cant connect, we just pass 
                pass


    def AddMeasurement(self, measurement: Measurement):
        points = []
        for param in measurement.parameters.all():
            if param.value == '' or param.value == None:
                continue
            points.append(Point("Parameters").field(param.name, param.value).tag(
                "name", param.name).time(measurement.timestamp))

        for p in points:
            self.write_api.write(bucket=self.bucket, record=p,
                                 record_measurement_key="Parameters")


    def GetMeasurements(self, start_time, end_time):
        start = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        end = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")

        # Build query
        query = f"from(bucket:\"{self.bucket}\") |> range(start: {start}, stop: {end})"
        tables = self.query_api.query(query)

        # Parse to measurement object
        measurements = {}
        for table in tables:
            for row in table.records:
                if row["_field"] in measurements.keys():
                    measurements[row["_field"]].append({
                        "value": row["_value"],
                        "timestamp": timezone.localtime(row["_time"]).isoformat()
                    })
                else:
                    measurements[row["_field"]] = [{
                        "value": row["_value"],
                        "timestamp": timezone.localtime(row["_time"]).isoformat()
                    }]

        return measurements

    def GetLatestMeasurements(self) -> List[Measurement]:
        query = build_latest_query(self.bucket)
        tables = self.query_api.query(query)

        measurements = {}
        for table in tables:
            for row in table.records:
                measurements[row["_field"]] = {
                    "value": row["_value"],
                    "timestamp": timezone.localtime(row["_time"]).isoformat()
                }

        return measurements

    def DeleteDatabase(self):
        bucket = self.buckets_api.find_bucket_by_name(self.bucket)
        return self.buckets_api.delete_bucket(bucket)


def datetime_from_local_to_utc(naive_datetime):
    aware = timezone.make_aware(naive_datetime)
    return aware - aware.utcoffset()


def build_latest_query(bucket):
    params_string = ""
    for p in Parameter.Name.choices:
        if params_string == "":
            params_string = f"r[\"_field\"] == \"{p[0]}\""
        else:
            params_string = params_string + f" or r[\"_field\"] == \"{p[0]}\""

    query = f"from(bucket:\"{bucket}\") |> range(start: -90d, stop: now()) |> filter(fn: (r) => {params_string}) |> last()"
    return query
