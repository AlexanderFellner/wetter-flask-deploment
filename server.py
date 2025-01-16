from flask import Flask, render_template
import requests
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sb

app = Flask(__name__)


@app.get("/index")
@app.get("/")
def index():
    return render_template("index.html", title="index")


# https://dataset.api.hub.geosphere.at/v1/station/historical/tawes-v1-10min?parameters=TL&station_ids=11035&start=2024-12-01&end=2025-01-01
@app.post("/wetter")
def wetter_abfragen():
    response = requests.get(
        "https://dataset.api.hub.geosphere.at/v1/station/historical/tawes-v1-10min?parameters=TL&station_ids=11035&start=2024-11-01&end=2024-12-01")
    TL_list = response.json()["features"][0]["properties"]["parameters"]["TL"]["data"]
    timestamps_list = response.json()["timestamps"]
    dict_daten = {"timestamp": timestamps_list, "TL": TL_list}
    df = pd.DataFrame(data=dict_daten)
    """
    plt.title("wetterdaten")
    plt.xlabel("timestamps")
    plt.ylabel("Lufttemperatur")
    plt.plot(df["timestamp"], df["TL"])
    plt.show()
    
    """
    sb.lineplot(x="timestamp", y="TL", data=df)

    plt.xticks([])
    plt.savefig("static/img/wetter.jpg")
   # plt.show()

    return render_template("wetter.html")


if __name__ == "__main__":
    app.run(host="localhost", port=8000)
