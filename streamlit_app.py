# import streamlit as st
# from streamlit_folium import folium_static
# import folium

# "# streamlit-folium"

# # with st.echo():
# import streamlit as st
# from streamlit_folium import folium_static
# import folium

# # center on Liberty Bell
# m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)

# # add marker for Liberty Bell
# tooltip = "Liberty Bell"
# folium.Marker(
#     [39.949610, -75.150282], popup="Liberty Bell", tooltip=tooltip
# ).add_to(m)

# # call to render Folium map in Streamlit
# folium_static(m)
from datetime import date, timedelta, datetime
import streamlit as st
from streamlit_folium import folium_static
import geemap.foliumap as geemap
import ee
import os
st.write(
    "Has environment variables been set:",
    os.environ["EARTHENGINE_TOKEN"] == st.secrets["EARTHENGINE_TOKEN"],
)

os.environ["EARTHENGINE_TOKEN"] == st.secrets["EARTHENGINE_TOKEN"]
def maskCloudAndShadows(image):
  cloudProb = image.select('MSK_CLDPRB')
  snowProb = image.select('MSK_SNWPRB')
  cloud = cloudProb.lt(5)
  snow = snowProb.lt(5)
  scl = image.select('SCL')
  shadow = scl.eq(3); # 3 = cloud shadow
  cirrus = scl.eq(10); # 10 = cirrus
  # Cloud probability less than 5% or cloud shadow classification
  mask = (cloud.And(snow)).And(cirrus.neq(1)).And(shadow.neq(1))
  return image.updateMask(mask).divide(10000)

def ee_authenticate(token_name="EARTHENGINE_TOKEN"):
    geemap.ee_initialize(token_name=token_name)

ee_authenticate(token_name=os.environ["EARTHENGINE_TOKEN"])   

m = geemap.Map()
# dem = ee.Image('USGS/SRTMGL1_003')
ed = date.today()
sd = ed - timedelta(days=30)

palette = ['FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163', '99B718', '74A901', '66A000', '529400', '3E8601', '207401', '056201', '004C00', '023B01', '012E01', '011D01', '011301']
# vis_params = {
#   'min': 0,
#   'max': 1,
#   'palette': palette}

band = ['B4','B3','B2']
rgbViza = {"min":0.0, "max":0.7,"bands":band}
titlemap = "Sentinel 2 - Natural Color"


startDate = sd.strftime("%Y-%m-%d") + "T" 
endDate = ed.strftime("%Y-%m-%d") + "T"

se2 = ee.ImageCollection('COPERNICUS/S2_SR').filterDate(
            startDate,endDate).filter(
            ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE",80)).map(maskCloudAndShadows).median()
m.addLayer(se2, rgbViza, titlemap)


vis_params = {
'min': 0,
'max': 4000,
'palette': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5']}

# m.addLayer(dem, vis_params, 'SRTM DEM', True, 1)
m.addLayerControl()

# call to render Folium map in Streamlit
folium_static(m)
