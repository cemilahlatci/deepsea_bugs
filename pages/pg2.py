import dash
from dash import dcc, html, callback, Output, Input, State
from dash import dash_table as dt
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import openpyxl
# To create meta tag for each page, define the title, image, and description.
dash.register_page(__name__,
                   path='/manufacturer',  # '/' is home page and it represents the url
                   name='Manufacturer',  # name of page, commonly used as name of link
                   title='manufacturer',  # title that appears on browser's tab
                   image='crossist_logo.png',  # image in the assets folder
                   description='Manufacturer Data'
)

dff = pd.read_csv("data/otc_total.csv", low_memory=False)
firma = pd.read_excel("data/OTC_FIRMA2.xlsx")

# top10 = pd.DataFrame()

layout = html.Div(
                    [
                        dcc.Markdown('## OTC Sales by Manufacturer 2022 (Feb - Sep)', style={'textAlign':'center'}),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(id='cat_choice', multi=False, value="Anne Bebek",
                        options=[{"label": x, "value": x} for x in sorted(dff["Ana Kategori"].unique())],
                                     )
                    ], xs=10, sm=10, md=8, lg=2, xl=2, xxl=2
                ),

                dbc.Col(
                    [
                        dcc.Dropdown(options=sorted(firma["Firma"].unique()),
                                    id='firma_choice', value=None, multi=True)
                    ], xs=10, sm=10, md=8, lg=6, xl=6, xxl=6
                ),
                dbc.Col(
                    [
                        dbc.Button(
                            f"Open TOP10",
                            id="Top10_Button",
                            className="mb-3",
                            color="primary",
                            )
                    ], xs=10, sm=10, md=8, lg=2, xl=2, xxl=2
                )
            ]
                ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='hist_fig')
                    ], width=6,
                        ),
                dbc.Col(
                        dbc.Collapse(
                            dbc.Card(
                                id="collapse_tbl",
                                    ), is_open=False, id='collapse',
                                    ), width=4, className="mt-5"
                        )
            ]
                )
        ]
)

@callback(
    Output("collapse", "is_open"),
    [Input("Top10_Button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
[Output('hist_fig', 'figure')],
[Input('cat_choice', 'value'),
 Input('firma_choice', 'value')]
)

def update_graph(cat_choice, firma_choice):

    df1 = dff[dff["Ana Kategori"].isin([cat_choice])]
    # top10 = df1.groupby(['Firma']).size().reset_index(name="counts").sort_values(by="counts", ascending=False)
    # firma1 = firma[firma["Firma"].isin([firma_choice[0]])]
    dffirma = pd.DataFrame(columns=['barcode', 'Firma'])  #Create empty Dataframe
    if not firma_choice:
        fig = {}
    elif len(firma_choice)>5:
        pass
    else:
         for x in range (0, len(firma_choice)):
            firma2 = firma[firma["Firma"].isin([firma_choice[x]])]
            dffirma = pd.concat([dffirma, firma2])

    analiz = pd.merge(df1, dffirma, how="inner", on="barcode")
    fig = px.histogram(analiz, x='Firma_x', histfunc="count")
    return [fig]

@callback(
[Output('collapse_tbl', 'children')],
[Input('cat_choice', 'value')]
        )

def update_table(cat_choice):
    df1 = dff[dff["Ana Kategori"].isin([cat_choice])]
    top10 = df1.groupby(['Firma']).size().reset_index(name="counts").sort_values(by="counts", ascending=False)[:10]
    data = top10.to_dict('records')
    columns =  [{"name": i, "id": i,} for i in (top10.columns)]
    return [dt.DataTable(data=data, columns=columns, style_cell={'textAlign': 'left', 'padding': '5px'},
                        style_header={'backgroundColor': 'hotpink', 'color': 'white', 'fontWeight': 'bold'})]
