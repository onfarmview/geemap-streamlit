# from datetime import date, timedelta
# import streamlit as st
# from streamlit_folium import folium_static
# import geemap.foliumap as geemap
# import ee
# import os

# st.write(
#     "Has environment variables been set:",
#     os.environ["EARTHENGINE_TOKEN"] == st.secrets["EARTHENGINE_TOKEN"],
# )

# # os.environ["EARTHENGINE_TOKEN"] == st.secrets["EARTHENGINE_TOKEN"]

# def maskCloudAndShadows(image):
#     cloudProb = image.select('MSK_CLDPRB')
#     snowProb = image.select('MSK_SNWPRB')
#     cloud = cloudProb.lt(5)
#     snow = snowProb.lt(5)
#     scl = image.select('SCL')
#     shadow = scl.eq(3)  # 3 = cloud shadow
#     cirrus = scl.eq(10)  # 10 = cirrus
#     mask = (cloud.And(snow)).And(cirrus.neq(1)).And(shadow.neq(1))
#     return image.updateMask(mask).divide(10000)

# def ee_authenticate(token_name):
#     geemap.ee_initialize(token_name=token_name)

# ee_authenticate(token_name=os.environ["EARTHENGINE_TOKEN"])   
# # st.write(
# #     os.environ["EARTHENGINE_TOKEN"]
# # )
# # m = geemap.Map()

# ed = date.today()
# sd = ed - timedelta(days=30)

# startDate = sd.strftime("%Y-%m-%d") + "T" 
# endDate = ed.strftime("%Y-%m-%d") + "T"

# # se2 = ee.ImageCollection('COPERNICUS/S2_SR').filterDate(
# #     startDate, endDate).filter(
# #     ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 80)).median()

# # band = ['B4', 'B3', 'B2']
# # rgbViza = {"min": 0.0, "max": 0.7, "bands": band}
# # titlemap = "Sentinel 2 - Natural Color"

# # m.addLayer(se2, rgbViza, titlemap)
# map_center=(-43.525650, 172.639847)

# m = geemap.Map(
#     basemap="HYBRID",
#     plugin_Draw=True,
#     Draw_export=True,
#     locate_control=True,
#     plugin_LatLngPopup=True, 
#     center=map_center, zoom=15,
# )

# vis_params = {
#     'min': 0,
#     'max': 4000,
#     'palette': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5']
# }

# m.addLayerControl()

# # call to render Folium map in Streamlit
# folium_static(m)
import streamlit as st
# import leafmap.foliumap as geemap
import geemap.foliumap as geemap
from streamlit.components.v1 import html
import ee
import folium
import pandas
# import geemap.foliumap as geemap
# import ee
from datetime import date, timedelta, datetime
from streamlit_folium import folium_static
import os
st.set_page_config(layout="wide")
st.write(
    "Has environment variables been set:",
    os.environ["EARTHENGINE_TOKEN"] == st.secrets["EARTHENGINE_TOKEN"],
)
st.sidebar.info(
    """
    URL: <https://onfarmview.com>
    
    """
)

st.sidebar.title("Contact")

st.sidebar.markdown('<a href="mailto:admin@onfarmview.com">Contact Us</a>', unsafe_allow_html=True)

st.title("On Farm View")

footer_content = """
 
    <p>&copy; 2023 On Farm View. </p>

    """

st.sidebar.markdown(footer_content, unsafe_allow_html=True)


def ee_authenticate(token_name="EARTHENGINE_TOKEN"):
    geemap.ee_initialize(token_name=token_name)

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

map_center=(-43.525650, 172.639847)
ee_authenticate(token_name= os.environ["EARTHENGINE_TOKEN"])

m = geemap.Map(
    basemap="HYBRID",
    plugin_Draw=True,
    Draw_export=True,
    locate_control=True,
    plugin_LatLngPopup=True, 
    center=map_center, zoom=15,
)

ed = date.today()
sd = ed - timedelta(days=30)


startDate = sd.strftime("%Y-%m-%d") + "T" 
endDate = ed.strftime("%Y-%m-%d") + "T"


se2 = ee.ImageCollection('COPERNICUS/S2_SR').filterDate(
            startDate,endDate).filter(
            ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE",80)).map(maskCloudAndShadows).median()
band = ['B4','B3','B2']
rgbViza = {"min":0.0, "max":0.7,"bands":band}
titlemap = "Sentinel 2 - Natural Color"
m.addLayer(se2, rgbViza, titlemap)

# m.to_streamlit(height=650)
folium_static(m)
