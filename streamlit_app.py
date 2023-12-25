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

import streamlit as st
from streamlit_folium import folium_static
import geemap.foliumap as geemap
import ee
import os

os.environ["EARTHENGINE_TOKEN"] == st.secrets["EARTHENGINE_TOKEN"]

# with st.echo():
import streamlit as st
from streamlit_folium import folium_static
import geemap.foliumap as geemap
import ee

def ee_authenticate(token_name="EARTHENGINE_TOKEN"):
    geemap.ee_initialize(token_name=token_name)

ee_authenticate(token_name="EARTHENGINE_TOKEN")    
m = geemap.Map()
dem = ee.Image('USGS/SRTMGL1_003')

vis_params = {
'min': 0,
'max': 4000,
'palette': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5']}

m.addLayer(dem, vis_params, 'SRTM DEM', True, 1)
m.addLayerControl()

# call to render Folium map in Streamlit
folium_static(m)
