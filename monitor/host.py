from flask import Flask, send_from_directory, render_template
import pandas as pd

app = Flask(__name__)

def _check(ts):
    now = pd.Timestamp.utcnow()
    now = now.tz_localize(None)
    if now - ts > pd.Timedelta("1d"): 
        return "red"
    else:
        return "green"

def _timestamps():
    ts = pd.Timestamp("2021-06-04T12:00:00")
    ts2 = pd.Timestamp("2021-06-06T12:00:00")

    return [{"id": "p1",
             "source": "天气",
             "basetime": ts.strftime("%Y-%m-%dT%H:%M:%S"),
             "light": _check(ts)},
             {"id": "p1",
             "source": "卫星",
             "basetime": ts.strftime("%Y-%m-%dT%H:%M:%S"),
             "light": _check(ts2)}]

@app.route('/red.png')
def red():
    return send_from_directory("images", "red.png")

@app.route('/green.png')
def green():
    return send_from_directory("images", "green.png")

@app.route('/monitor')
def monitor():
    return render_template("monitor.html", timestamps=_timestamps())

if __name__ == "__main__":
    app.run(debug=True, port=8000)
