import pandas as pd
import numpy as np


def load_data():
    df_crime = pd.read_csv("data/crime_data.csv")
    df_police = pd.read_csv("data/Police_Stations.csv")

    # Keep necessary columns
    df_crime = df_crime[
        ["latitude", "longitude", "offense_group", "neighborhood_cluster"]
    ]

    df_crime = df_crime.dropna(subset=["latitude", "longitude"])
    df_crime = df_crime.dropna(subset=["neighborhood_cluster"])

    # Filter police stations
    df_police = df_police[df_police["TYPE"] == "Station"]
    df_police = df_police[["NAME", "LATITUDE", "LONGITUDE"]]

    return df_crime, df_police


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km

    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))

    return R * c


def compute_nearest_distance(crime_df, police_df):
    distances = []

    for _, crime in crime_df.iterrows():
        lat1 = crime["latitude"]
        lon1 = crime["longitude"]

        min_dist = float("inf")

        for _, station in police_df.iterrows():
            lat2 = station["LATITUDE"]
            lon2 = station["LONGITUDE"]

            dist = haversine(lat1, lon1, lat2, lon2)

            if dist < min_dist:
                min_dist = dist

        distances.append(min_dist)

    return distances


def calculate_safety_index():
    df_crime, df_police = load_data()

    # Limit rows for performance (optional)
    # df_crime = df_crime.head(5000)

    df_crime["nearest_police_km"] = compute_nearest_distance(df_crime, df_police)

    severity_map = {
        "violent": 5,
        "property": 2
    }

    df_crime["crime_weight"] = df_crime["offense_group"].map(severity_map)

    max_dist = df_crime["nearest_police_km"].max()
    df_crime["distance_factor"] = df_crime["nearest_police_km"] / max_dist

    df_crime["incident_risk"] = df_crime["crime_weight"] * (
        1 + df_crime["distance_factor"]
    )

    area_scores = df_crime.groupby("neighborhood_cluster")[
        "incident_risk"
    ].mean()

    min_score = area_scores.min()
    max_score = area_scores.max()

    safety_index = 100 * (
        1 - (area_scores - min_score) / (max_score - min_score)
    )

    return safety_index.sort_values(ascending=False)
