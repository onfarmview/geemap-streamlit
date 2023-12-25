from datetime import date, timedelta
import streamlit as st
from streamlit_folium import folium_static
import geemap.foliumap as geemap
import ee
import os

st.write(
    "Has environment variables been set:",
    os.environ["EARTHENGINE_TOKEN"] == st.secrets["EARTHENGINE_TOKEN"],
)

# os.environ["EARTHENGINE_TOKEN"] == st.secrets["EARTHENGINE_TOKEN"]

def maskCloudAndShadows(image):
    cloudProb = image.select('MSK_CLDPRB')
    snowProb = image.select('MSK_SNWPRB')
    cloud = cloudProb.lt(5)
    snow = snowProb.lt(5)
    scl = image.select('SCL')
    shadow = scl.eq(3)  # 3 = cloud shadow
    cirrus = scl.eq(10)  # 10 = cirrus
    mask = (cloud.And(snow)).And(cirrus.neq(1)).And(shadow.neq(1))
    return image.updateMask(mask).divide(10000)

def ee_authenticate(token_name):
    geemap.ee_initialize(token_name=token_name)

ee_authenticate(token_name=os.environ["EARTHENGINE_TOKEN"])   
# st.write(
#     os.environ["EARTHENGINE_TOKEN"]
# )
m = geemap.Map()

ed = date.today()
sd = ed - timedelta(days=30)

startDate = sd.strftime("%Y-%m-%d") + "T" 
endDate = ed.strftime("%Y-%m-%d") + "T"

se2 = ee.ImageCollection('COPERNICUS/S2_SR').filterDate(
    startDate, endDate).filter(
    ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 80)).median()

band = ['B4', 'B3', 'B2']
rgbViza = {"min": 0.0, "max": 0.7, "bands": band}
titlemap = "Sentinel 2 - Natural Color"

m.addLayer(se2, rgbViza, titlemap)

vis_params = {
    'min': 0,
    'max': 4000,
    'palette': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5']
}

m.addLayerControl()

# call to render Folium map in Streamlit
folium_static(m)
