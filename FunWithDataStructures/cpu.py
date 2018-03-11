import psutil
import time
from datetime import datetime, timedelta
from influxdb import InfluxDBClient

if __name__ == '__main__':
    client = InfluxDBClient(host='127.0.0.1', port=8086, database='cpu')

    while True:
        dt = datetime.now() - timedelta(hours=1)
        dts = dt.strftime('%Y-%m-%dT%H:%M:%SZ')
        cpup = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory()[2]
        print(dts, cpup, mem)
        json = [
                {
                    "measurement": "MS7758",
                    "time": "%s" % (dts),
                    "fields": {
                        "cpu_percent": cpup,
                        "virt_mem": mem
                    }
                }
        ]
        client.write_points(json)

        time.sleep(5)

