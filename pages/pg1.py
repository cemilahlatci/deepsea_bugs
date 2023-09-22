import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import openpyxl

# To create meta tag for each page, define the title, image, and description.
dash.register_page(__name__,
                   path='/',  # '/' is home page and it represents the url
                   name='Category',  # name of page, commonly used as name of link
                   title='index',  # title that appears on browser's tab
                   image='crossist_logo.png',  # image in the assets folder
                   description='Category Data'
)

df = pd.read_csv("data/otc_total.csv", low_memory=False)
analiz = df.groupby(by=['Ana Kategori',
                        'Alt Kategori 1',
                        'Alt Kategori 2'], as_index=False).agg({"created_at": pd.Series.count})
analiz =analiz.sort_values("created_at", ascending=False)


layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        # dcc.Dropdown(options=df["Ana Kategori"].unique(),
                                     html.Div(id='cat-choice', children=''),
                    ], xs=10, sm=10, md=8, lg=2, xl=2, xxl=2
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Markdown('## OTC Sales 2022 (Feb-Sep)', style={'textAlign':'center'}),

                    ], width=10
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id="sunburst1",
                        figure = {})
                    ], width=10
                )
            ]
        )
    ]
)

@callback(
    Output('sunburst1', 'figure'),
    [Input('cat-choice', 'value')]
)
def update_graph(value):
    if value is None:
        fig = px.sunburst(analiz,
                  path=['Ana Kategori', 'Alt Kategori 1', 'Alt Kategori 2'],
                  values='created_at',
                  maxdepth = 2,
                  labels = {"created_at": "Adet"}
                  ).update_traces(textinfo= 'label+percent entry')  # insidetextorientation='radial'
        fig.update_layout(margin=dict(t=15, l=0, r=0, b=0)) # uniformtext=dict(minsize=10, mode='show')


    else:

        fig = px.sunburst(analiz,
                  path=['cat-choice', 'Alt Kategori 1', 'Alt Kategori 2'],
                  values='created_at',
                  maxdepth = 2,
                  labels = {"created_at": "Adet"}
                  ).update_traces(textinfo= 'label+percent entry')  # insidetextorientation='radial'
        fig.update_layout(margin=dict(t=15, l=0, r=0, b=0)) # uniformtext=dict(minsize=10, mode='show')

    return fig

