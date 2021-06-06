from flask import Flask, send_from_directory, render_template
import pandas as pd
import yaml

def _load_cfg():
    with open("monitor.yml", "r") as _yml:
        cfg = yaml.load(_yml, Loader=yaml.FullLoader)
    return cfg

app = Flask(__name__)

def _check(ts, limit):
    """ check how old ts is compared to utcnow """
    now = pd.Timestamp.utcnow()
    now = now.tz_localize(None)

    if now - ts > pd.Timedelta(limit): 
        return "red"
    else:
        return "green"

def _get_ts(path):
    """ read csv file at path and return its basetime """
    ts = pd.Timestamp(pd.read_csv(path, ",", header=None).iloc[0][0])
    return ts

def _timestamps():
    """ create list of timestamps used for jinja """
    cfg = _load_cfg()

    retval = []
    for plant in cfg["plants"]:
        for source in cfg["plants"][plant]:
            ts = _get_ts(cfg["plants"][plant][source])
            _tmp = {
                "id": plant,
                "source": source,
                "basetime": ts.strftime("%Y-%m-%dT%H:%M:%S"),
                "light": _check(ts, cfg["limits"][source])}
            retval.append(_tmp)

    return retval

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
