#!/usr/bin/env python3
import folium
import pandas as pd


if __name__ == '__main__':
    # Create map
    map_osm = folium.Map(location=[35.9589, -83.9338])

    # Get data
    data = pd.read_csv('battles.csv', sep=',', header=0)

    # Add markers to map
    data.apply(lambda row:folium.Marker(location=[row["Lat"],
                                        row['Lon']], popup=row['Battle']
                                       ).add_to(map_osm),
               axis=1)

    # Save js to html
    map_osm.save('map.html')

