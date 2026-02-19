from flask import Flask, jsonify
from safety import calculate_safety_index, load_data
import folium
from folium.plugins import HeatMap

app = Flask(__name__)

print("Calculating safety index...")
SAFETY_SCORES = calculate_safety_index()
print("Safety index ready.")

df_crime, _ = load_data()


@app.route("/")
@app.route("/")
def home():
    m = folium.Map(
        location=[df_crime["latitude"].mean(),
                  df_crime["longitude"].mean()],
        zoom_start=12
    )

    # Downsample crime points
    df_sample = df_crime.sample(n=5000, random_state=42)
    heat_data = df_sample[["latitude", "longitude"]].values.tolist()
    HeatMap(heat_data).add_to(m)

    # Add police station markers
    _, df_police = load_data()

    for _, station in df_police.iterrows():
        folium.Marker(
            location=[station["LATITUDE"], station["LONGITUDE"]],
            popup=station["NAME"],
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

    return m._repr_html_()

@app.route("/safety/<cluster>")
def get_cluster_safety(cluster):
    score = SAFETY_SCORES.get(cluster)
    if score is None:
        return jsonify({"error": "Cluster not found"}), 404
    return jsonify({
        "cluster": cluster,
        "safety_score": round(score, 2)
    })

if __name__ == "__main__":
    app.run(debug=True)
