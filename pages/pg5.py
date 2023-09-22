import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

# To create meta tag for each page, define the title, image, and description.
dash.register_page(__name__,
                   path='/geographical',  # '/' is home page and it represents the url
                   name='Geographical',  # name of page, commonly used as name of link
                   title='geographical',  # title that appears on browser's tab
                   image='crossist_logo.png',  # image in the assets folder
                   description='Geographical Data'
)

alldf = pd.read_csv("data/otc_total.csv", low_memory=False)

layout = dbc.Container(
    [
        dbc.Row([
            dcc.Markdown('Geographical Layout of OTC Sales', style={'textAlign':'center'}),
            ]),
        dbc.Row([
            dcc.RadioItems(
            id="reg_choice",
            options=[{'label': "City", 'value': "boro"},
                     {'label': "District", 'value': "İlçe"},
                     {'label': "Pharmacy", 'value': "glnno"}],
            value="İlçe",
            inline=True,
            inputStyle={"margin-left": "5px"},
            style={'padding-bottom': 10}               ),
            ]),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id='cat_choice', multi=False, value="Anne Bebek",
                    options=[{"label": x, "value": x} for x in sorted(alldf["Ana Kategori"].unique())],
                             )
                    ], xs=10, sm=10, md=8, lg=2, xl=2, xxl=2
                    ),
            dbc.Col([
                    dcc.Graph(id='map_fig', figure={})
                    ], width=9,
                        ),
                ])
])


@callback(
    Output('map_fig', 'figure'),
    Input('reg_choice', 'value'),
    Input('cat_choice', 'value'),
           )
def update_graph(reg_choice, cat_choice):
    df = alldf[['glnno','boro', 'İlçe', 'latitude', 'longitude','Ana Kategori']]
    df1 = df[df["Ana Kategori"].isin([cat_choice])]
    dfs = df1.groupby(by=reg_choice).count().reset_index()
    dfsn = dfs.rename(columns={'latitude': 'lati', 'longitude': 'long'})
    if reg_choice == 'glnno':
        df2 = alldf[['glnno','latitude', 'longitude', 'Eczane adı']]
        df3 = dfsn.merge(df2, on='glnno')
        dfecza = df3.drop_duplicates(subset='glnno')
        fig = px.scatter_mapbox(dfecza, lat='latitude', lon='longitude', zoom=5, height=650,
                            center=dict(lat=38.000, lon=32.00), mapbox_style="carto-positron",
                            size='Ana Kategori', color="Ana Kategori", labels= {"Ana Kategori": "Adet", "boro": "City"},
                            hover_data={reg_choice: True, 'Ana Kategori': True, 'latitude': False,
                            'longitude': False, 'Eczane adı': True})
    else:
        dflong = df1.groupby(by=reg_choice)['longitude'].mean().to_frame("avg_long")
        dflati = df1.groupby(by=reg_choice)['latitude'].mean().to_frame("avg_lati")
        dffinal = dfsn.merge(dflati, on=reg_choice).merge(dflong, on=reg_choice)
        fig = px.scatter_mapbox(dffinal, lat='avg_lati', lon='avg_long', zoom=5, height=650,
                            center=dict(lat=38.000, lon=32.00), mapbox_style="carto-positron",
                            size='Ana Kategori', color="Ana Kategori", labels= {"Ana Kategori": "Adet", "boro": "City"},
                            hover_data={reg_choice: True, 'Ana Kategori': True, 'lati': False, 'long': False,
                            'avg_long': False, 'avg_lati': False })
    return fig