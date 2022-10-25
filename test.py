import folium
import pyproj
def tranform(x,y):
    inProj = pyproj.Proj(init='epsg:2154')
    outProj = pyproj.Proj(init='epsg:4326')
    x2, y2 = pyproj.transform(inProj, outProj, x, y)
    return [x2, y2]
coord =tranform(612061.7502,6875832.0686)
print(coord)
map = folium.Map(location=coord, tiles='OpenStreetMap', zoom_start=2)
folium.Marker(location=coord, tiles='OpenStreetMap', zoom_start=2).add_to(map)
map.save(outfile='map.html')