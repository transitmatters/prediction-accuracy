import matplotlib.pyplot as plt
import pandas as pd
import os

csv_url = "https://opendata.arcgis.com/api/v3/datasets/d126b4ce6d764493a8ddd7b30822fa8d_0/downloads/data?format=csv&spatialRefId=4326&where=1%3D1"

route_ids = ("Red", "Orange", "Blue", "Green-B", "Green-C", "Green-D", "Green-E")

colors_by_line = {
    "Blue": ["#0000FF", "#0000CC", "#000099", "#000066"],
    "Red": ["#FF0000", "#CC0000", "#990000", "#660000"],
    "Green": ["#00FF00", "#00CC00", "#009900", "#006600"],
    "Orange": ["#FFA500", "#CC8400", "#996300", "#664200"],
    "Fallback": ["#000000", "#000000", "#000000", "#000000"],
}


def read_predictions_file():
    df = pd.read_csv(csv_url)
    df = df[df["mode"] == "subway"]
    df = df.sort_values(by=["weekly"])
    # Ignore the time string
    df["weekly"] = df["weekly"].apply(lambda x: x.split(" ")[0])
    df["accuracy"] = df["num_accurate_predictions"] / df["num_predictions"]
    return df


def plot_accuracy_for_route_and_bucket(
    df: pd.DataFrame,
    route_id: str,
    bin_id: str,
    color: str,
):
    df = df[(df["route_id"] == route_id) & (df["bin"] == bin_id)]
    if not df.empty:
        plt.plot(
            df["weekly"],
            df["accuracy"],
            label=f"{route_id} {bin_id}",
            color=color,
        )


def bin_to_int(bin_id: str) -> int:
    return int(bin_id.split("-")[0])


def make_plot_for_route_id(df: pd.DataFrame, route_id: str):
    bin_ids = df["bin"].unique()
    plt.title(f"Prediction accuracy for {route_id} by week")
    plt.xticks(rotation=45)
    plt.ylim(0, 1)
    plt.gcf().set_size_inches(15, 7.5)
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(10))
    line = route_id.split("-")[0]
    colors = colors_by_line.get(line, colors_by_line["Fallback"])
    for idx, bin_id in enumerate(sorted(bin_ids, key=bin_to_int)):
        plot_accuracy_for_route_and_bucket(df, route_id, bin_id, colors[idx])
    plt.legend(loc="lower left")
    plt.savefig(f"output/{route_id}.png")
    plt.clf()


if __name__ == "__main__":
    if not os.path.exists("output"):
        os.mkdir("output")
    df = read_predictions_file()
    for route_id in route_ids:
        make_plot_for_route_id(df, route_id)
