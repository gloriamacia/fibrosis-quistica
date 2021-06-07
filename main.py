from flask import Flask, render_template
import pandas as pd
import folium
from quickstart import get_gspread
import folium.plugins

app = Flask(__name__)


@app.route('/')
def index():
    start_coords = (-25.278055444434276, -57.58487367338524)
    folium_map = folium.Map(location=start_coords, zoom_start=3)
    fg = folium.FeatureGroup(control=False)
    #df = pd.read_csv('static/data/hco.csv')
    df_centers = get_gspread('centers')
    df_countries = get_gspread('countries')
    countries = df_centers['pais'].unique()
    g = {}
    for index, country in enumerate(countries):
        g[f'{country}'] = folium.plugins.FeatureGroupSubGroup(fg, f'{country}')  # First subgroup of fg
    folium_map.add_child(fg)
    for key in sorted(g.keys()):
        folium_map.add_child(g[key])

    for index, row in df_centers.iterrows():
        tooltip = row['nombre']
        lat = float(row['coordenadas'].split(',')[0])
        lon = float(row['coordenadas'].split(',')[1])
        color = df_countries[df_countries['pais']==row['pais']]['color'].item()
        popup_text = f"<b>{row['nombre']}</b><br><br>{row['direccion']}<br>{row['pais']}<br>telefono:{row['telefono']}"
        popup = folium.Popup(popup_text, max_width=500)
        country = row['pais']
        g[f'{country}'].add_child(folium.Marker([lat, lon], popup=popup, tooltip=tooltip, icon=folium.Icon(color=color, icon='h-square', prefix='fa'), parse_html=True))
    
    minimap = folium.plugins.MiniMap()
    folium_map.add_child(minimap)
    folium.LayerControl().add_to(folium_map)
    
    folium_map.save('templates/map.html')

    df_specialists = get_gspread('specialists')
    df_specialists = df_specialists.head()
    # https://stackoverflow.com/questions/61740225/bootstrap-css-and-pandas-dataframe-to-html-how-to-add-class-to-thead
    df_specialists.to_html(classes=['table'], buf=open('templates/df_specialists.html', 'w', encoding="utf-8"))
    
    df_associations = get_gspread('associations')
    # https://stackoverflow.com/questions/61740225/bootstrap-css-and-pandas-dataframe-to-html-how-to-add-class-to-thead
    df_associations.to_html(classes=['table'], buf=open('templates/df_associations.html', 'w', encoding="utf-8"))

    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)