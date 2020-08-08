import folium
import pandas as pd 

data = pd.read_csv("Volcanoes.txt") 
#read the volcano coordinates and elevation for popup
latitudes_list=data["LAT"]
longitudes_list=data["LON"]
elevations_list=data["ELEV"]
names_list=data["NAME"]
html = """ <h4>Volcano Info:</h4> 
Elevation: %s m<br>
<a href="https://www.google.com/search?q=%s" target="_blank">%s</a><br>"""  #html that will be used in popup window

def color_decider(elevation): #decide marker colors according to their elevations
    if elevation< 1000:
        return "green"
    elif 1000 <= elevation <3000:
        return "orange"
    else:
        return "red"

#adding a base layer
basemap=folium.Map(location = [30.80,75.78], zoom_start=2,tiles="Stamen Terrain") # define a physical/political map
fgv=folium.FeatureGroup("Volcanoes") # define a feature group to add properties to map
for lat, lon, el, name in zip(latitudes_list, longitudes_list, elevations_list, names_list):
    iframe = folium.IFrame(html = html %(el,name,name), height = 100 ,width = 200 ) # iframe used in popup of marker
    fgv.add_child(folium.Marker(location=[lat,lon], popup=folium.Popup(iframe),icon=folium.Icon(color=color_decider(el)))) #adding markers
    #fg.add_child(folium.CircleMarker(location=[lat,lon],popup=folium.Popup(iframe),radius = 6,fill_color=color_decider(el),color="black",fill_opacity=0.7))#code to use circle markers

#adding a polygon layer
#adding geojson data to form polygons aroung country boundaries and color legend them according to their population size
fgp= folium.FeatureGroup(name="Population")
fgp.add_child(folium.GeoJson(data=open('world.json','r',encoding='utf-8-sig').read(), #encoding since whole html doc has to be in a single encoding
style_function = lambda x: {"fillColor":"green" if x['properties']['POP2005']< 10000000 # style_function maps the polygon(geojson objects) to their style dicts
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red' }, tooltip="bosdk"))

basemap.add_child(fgp)
basemap.add_child(fgv)
basemap.add_child(folium.LayerControl()) #Adding a layer control panel
basemap.save("basemap.html")


