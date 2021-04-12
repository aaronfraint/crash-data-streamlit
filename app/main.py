import streamlit as st
import pydeck as pdk
import pandas as pd
import geopandas as gpd


def make_pydeck_map(gdf):

    view_args = {
        "latitude": 38.89829130763422,
        "longitude": -77.03660795919676,
        "zoom": 11,
        "bearing": 0,
        "pitch": 45,
    }

    view_state = pdk.ViewState(**view_args)

    layer = pdk.Layer(
        "GridLayer",
        gdf,
        pickable=True,
        extruded=True,
        cell_size=200,
        opacity=0.6,
        elevation_scale=4,
        get_position=["lon", "lat"],
    )

    return pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "{FROMDATE}\n{ADDRESS}"},
        map_style="road",
    )


@st.cache()
def load_initial_data():
    gdf = gpd.read_file("./app/data/dc_bike_crashes.geojson")

    gdf.rename(columns={"LATITUDE": "lat", "LONGITUDE": "lon"}, inplace=True)

    gdf["year"] = 0

    for idx, row in gdf.iterrows():
        year = row.FROMDATE.split("-")[0]
        gdf.at[idx, "year"] = year

    return gdf


def filter_data(gdf, start: int, end: int):

    return gdf[(gdf.year >= start) & (gdf.year <= end)]


gdf = load_initial_data()

st.markdown("# Bicycle Crashes in Washington DC")

start_year, end_year = st.slider("Select years to include on the map", 2011, 2021, (2016, 2021), 1)

filtered_df = filter_data(gdf, start_year, end_year)

st.markdown("## Map with `streamlit.map()`")
st.map(filtered_df)

st.markdown("## Map with `pydeck` and `streamlit.pydeck_chart()`")
st.pydeck_chart(make_pydeck_map(filtered_df))