from ntpath import join
from flask import Flask, send_from_directory, render_template
import pandas as pd
import yaml

app = Flask(__name__)

def _check(v):
    if v:
        return "green"
    else:
        return "red"


def status():
    """ create list of timestamps used for jinja """

    df = pd.read_csv("status.csv", sep=";", header=None)

    retval = []
    print(df)

    for idx, row in df.iterrows():
        tmp = {}
        tmp["url"] = row[0]
        tmp["light"] = _check(row[1])

        retval.append(tmp)

    return retval


@app.route('/sitemonitor')
def check():
    return render_template("check.html", table=status())

if __name__ == "__main__":
    app.run(debug=True, port=8000)
