import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import openpyxl

# To create meta tag for each page, define the title, image, and description.
dash.register_page(__name__,
                   path='/barcode',  # '/' is home page and it represents the url
                   name='Barcode',  # name of page, commonly used as name of link
                   title='barcode',  # title that appears on browser's tab
                   image='crossist_logo.png',  # image in the assets folder
                   description='Barcode Data'
)

# To create meta tag for each page, define the title, image, and description.
# app = dash.Dash(__name__, use_pages=False, external_stylesheets=[dbc.themes.SPACELAB])
# server = app.server

df = pd.read_csv("data/otc_total.csv", low_memory=False)

layout = dbc.Container(
    [
        dcc.Markdown('## Compare your product to TOP10', style={'textAlign':'center'}),
        html.P("Choose One, Barcode or Product"),
        dbc.Accordion(
        [
            dbc.AccordionItem(
                dcc.Dropdown(id='bar_choice', multi=False, value="33984008663",
                        options=[{"label": x, "value": x} for x in sorted(df["barcode"].unique())],
                                     ),
                title="Barcode", item_id="item-0", style={"width": 600}
            ),
            dbc.AccordionItem(
                dcc.Dropdown(id='bop_choice', multi=False, value="4 HEPA 30 KAPSUL",
                        options=[{"label": x, "value": x} for x in sorted(df["Ürün Adı"].unique())],
                                     ),
                title="Product", item_id="item-1", style={"width": 600}
            ),
         ],
        start_collapsed=False, flush=True,
        id="acc_id",
        active_item="item-0",
                      ),
        html.Br(),
        dbc.Row([
            dbc.Col([
                html.P(f"Product chosen: ")
                    ], width={'size': 1}),
            dbc.Col([
                html.P(id='product_id')
                    ], width={'size': 2})
                ]),
        dbc.Row([
            dbc.Col([
                html.P(f"Subcategory shown: ")
                    ], width={'size': 1}),
            dbc.Col([
                html.P(id='cat_id')
                    ], width={'size': 2}),
            dbc.Col([
                dcc.Graph(id='pie-graph', figure={}, className='six columns',),
                    ], xs=10, sm=10, md=8, lg=8, xl=8, xxl=8)
                ])
])

@callback(Output("product_id", "children"),
          Output("cat_id", "children"),
          Output(component_id='pie-graph', component_property='figure'),
          Input("acc_id", "active_item"),
          Input("bop_choice", "value"),
          Input("bar_choice", "value"),
          )
def choose_product(active_item,  bop_choice, bar_choice):
    if active_item == "item-0":
        item_choice = 0
    elif active_item == "item-1":
        item_choice = 1
    print(f"itemchoice is {item_choice}")
    print(bar_choice, bop_choice)
    if item_choice == 1:
        barcode_chosen = df[df['Ürün Adı'] == bop_choice].iloc[0]['barcode']
        print(f"barcode1 is {barcode_chosen}")
    else:
        barcode_chosen = bar_choice
        print(f"barcode0 is {barcode_chosen}")

    dff = df[df['barcode'] == barcode_chosen]
    print(dff.shape)
    if dff.shape[0] > 0:
        product_name = dff.iloc[0]['Ürün Adı']
        dfcat = df[df['KAT'] == dff.iloc[0]['KAT']]
        analiz = dfcat.groupby(['Ürün Adı']).size().to_frame().sort_values([0], ascending=False).reset_index()
        analiz = analiz.rename(columns={0: "count"})
        top10 = analiz.head(10)
        summe = top10["count"].sum()
        if product_name in top10['Ürün Adı'].unique():
            rest = dfcat.shape[0] - summe
            data = {'Ürün Adı': "Diğer", 'count': [rest]}
            diger = pd.DataFrame.from_dict(data)
            top12 = pd.concat([top10, diger], ignore_index=True)
        else:
            rest = dfcat.shape[0] - summe - dff.shape[0]
            data = {'Ürün Adı': "Diğer", 'count': [rest]}
            diger = pd.DataFrame.from_dict(data)
            udata = {'Ürün Adı': [product_name], 'count': [dff.shape[0]]}
            udatadf = pd.DataFrame.from_dict(udata)
            top11 = pd.concat([top10, udatadf], ignore_index=True)
            diger = pd.DataFrame.from_dict(data)
            top12 = pd.concat([top11, diger], ignore_index=True)
        cat_name = dfcat.iloc[0]['Alt Kategori 2']
        #print(cat_name)
        fig = px.pie(top12, values='count', names='Ürün Adı', hole=0.3)
    else:
        product_name = "Product not found"
        cat_name = ""
        fig = {}
    return product_name, cat_name, fig

