import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dash_table as dtb
import pandas as pd
import openpyxl
from datetime import datetime as dt
from datetime import date, timedelta

# To create meta tag for each page, define the title, image, and description.
dash.register_page(__name__,
                   path='/time',  # '/' is home page and it represents the url
                   name='Time',  # name of page, commonly used as name of link
                   title='time',  # title that appears on browser's tab
                   image='crossist_logo.png',  # image in the assets folder
                   description='Data over time'
)


# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB])
# server = app.server

# df = pd.read_csv("data/2022_otc.csv")
df = pd.read_csv("data/otc_total.csv", low_memory=False)
df.rename(columns = {'KAT':'Kat'}, inplace = True)

# display_choice = "Ana Kategori"
# ecz = pd.read_excel("data/Eczaneler.xlsx")
# firma = pd.read_excel("data/OTC_FIRMA2.xlsx")
df_copy =df
layout = dbc.Container(
    [
        dcc.Markdown('#### Daily Sales', style={"textAlign": "center"}, className="my-1"),
        dbc.Row(
                [dbc.Col(
                    [
                        dcc.DatePickerRange(
                            id="datepicker",
                            min_date_allowed="2022-02-14 00:00:00",
                            max_date_allowed="2023-06-15 23:59:59",
                            end_date=max(df["created_at"]),
                            start_date=min(df["created_at"]),
                            clearable=True,
                            day_size=50,
                            end_date_placeholder_text="Enter End Date",
                            first_day_of_week=1,
                            number_of_months_shown=1,
                            initial_visible_month = "2023-01-01"

                                            ),
                    ],
                    width=4, align="start",
                        ),
                dbc.Col(
                    [
                        dcc.RadioItems(
                            id="display_dpdn",
                            options=[{'label': " Category", 'value': "Ana Kategori"},
                            {'label': " Manufacturer", 'value': "Firma"},
                            {'label': " City", 'value': "boro"},
                            {'label': " District", 'value': "İlçe"},
                            {'label': " Pharmacy", 'value': "Eczane adı"},
                            {'label': " Team Member", 'value': "kalfaad"},
                            {'label': " Consultant", 'value': "Danısman X (devIr)"},
                            {'label': " Product", 'value': "barcode"},
                            {'label': " Campaign Pro.", "campaignpr": "KAT"}],
                            value="Ana Kategori",
                            inline=True,
                            inputStyle={"margin-left": "20px"},
                            style={'padding-bottom': 10},
                                    ),
                    ], align="end", width=6,
                        ),
                ],
                ),
        dbc.Row(
            [dbc.Col(
                     [
                         dbc.Checklist(
                            id="per_choice",
                            options=[{'label': "Previous Period", 'value': 1},
                                     {'label': "Previous Year", 'value': 2}],
                            value=[],
                            inline=True,
                            switch=True,
                            # inputStyle={"margin-left": "5px"},
                            style={'padding-top': 10},
                                           ),

                     ], width=4, align="start",
                        ),
            dbc.Col(
                    [
                        dcc.Dropdown(id='Kat_choice', multi=False, value="Anne Bebek",
                        options=[{"label": x, "value": x} for x in sorted(df["Ana Kategori"].unique())],
                        clearable=False,
                        )
                    ],  lg={'size': 6, 'offset': 4   }, align="start",
                ),
            ],
                ),
        dbc.Row(
                [dbc.Col(
                    [
                        dcc.Dropdown(options=[], id='dyn_dropdown', value=None, multi=False),
                    ], lg={'size': 6, 'offset': 4   }
                        ),
                ],
                ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Tabs(
                            id="tabs",
                            value="tab-1",
                            children=[
                                dcc.Tab(
                                    label="Graph",
                                    value="tab-1",
                                    children=[dcc.Graph(id="line")],
                                ),
                                dcc.Tab(
                                    label="Data",
                                    value="tab-2",
                                    children=[
                                        html.Div([
                                            dbc.Card(
                                                id='datatable_id'
                                                    ),
                                                ]),
                                              ],
                                        ),
                    ],
                        ),
                    ],
                    align="center", class_name="m-3"
                        ),
            ]
                ),
    ]
)

@callback(
    Output('dyn_dropdown', 'options'),
    Input("display_dpdn", "value")
        )

def update_choice(chosen_radioitem):
     if chosen_radioitem == "Ana Kategori":
        dff = df[["Ana Kategori"]]
     elif chosen_radioitem == "Firma":
        dff = df[["Firma"]]
     elif chosen_radioitem == "boro":
        dff = df[["boro"]]
     elif chosen_radioitem == "İlçe":
        dff = df[["İlçe"]]
     elif chosen_radioitem == "Eczane adı":
        dff = df[["Eczane adı"]]
     elif chosen_radioitem == "kalfaad":
        dff = df[["kalfaad"]]
     elif chosen_radioitem == "Danısman X (devIr)":
        dff = df[["Danısman X (devIr)"]]
     elif chosen_radioitem == "barcode":
        dff = df[["barcode"]]
     elif chosen_radioitem == "KAT":
        dff = df[["KAT"]]
        # print(display_choice, choice)
     return  [{'label': c, 'value': c} for c in sorted(dff[chosen_radioitem].unique())]


@callback(
    Output('line', 'figure'),
    Output('datatable_id', 'children'),
    Input("datepicker", "start_date"),
    Input("datepicker", "end_date"),
    Input("per_choice", "value"),
    Input("display_dpdn", "value"),
    Input('dyn_dropdown', 'value'),
    Input('Kat_choice', 'value'),
    Input('tabs', 'value')
         )
def update_time(start_date, end_date, per_choice, display_dpdn, dyn_dropdown, Kat_choice, tabs_choice):
    print(f"display_choice is: {display_dpdn}")
    print(f"dyn_dropdown is: {dyn_dropdown}")
    print(f"Kat_choice is: {Kat_choice}")

    df["created_at"] = pd.to_datetime(df["created_at"]).dt.normalize()
    end = pd.to_datetime(end_date)
    start = pd.to_datetime(start_date)
    end = end.replace(hour=23, minute=59, second=59)
    mask = (df['created_at'] >= start) & (df['created_at'] <= end)
    # dfanaliz dfs between start and end date
    dfanaliz = df.loc[mask]
    # Choose category from dropdown
    dfgraph = dfanaliz[dfanaliz['Ana Kategori'].isin([Kat_choice])]
    # Group chosen category for each day
    # dfgraph2 = dfgraph1[dfgraph1["display_choice"].isin([choice])]
    # dfgraph = dfgraph2.groupby(by=["created_at"]).count().reset_index()
    # group chosen category by companies
    ###dfbarcode = df.loc[: , ['barcode', display_choice]]
    if not display_dpdn:
        fig = {}
    else:
        df["created_at"] = pd.to_datetime(df["created_at"]).dt.normalize()
        end = end.replace(hour=23, minute=59, second=59)
        mask = (df['created_at'] >= start) & (df['created_at'] <= end)
        # dfanaliz dfs between start and end date
        dfanaliz = df.loc[mask]
        dfgraph = dfanaliz[dfanaliz['Ana Kategori'].isin([Kat_choice])]
        analiz = dfgraph[dfgraph[display_dpdn].isin([dyn_dropdown])]
        # dfgraph2 = analiz.groupby(by=[display_choice]).size().to_frame().sort_values([0], ascending=False).reset_index()
        # dfgraph2 = dfgraph2.rename(columns={0: "Total Count"})
        # new df for chosen companies
        # dfgraph3 = pd.merge(analiz, dfgraph2, how="inner", on=display_choice)
        # count daily sales by company
        dftopcomp = analiz.groupby(by=["created_at"]).count().reset_index()
        dftopcomp.rename(columns={"Unnamed: 0": "Total Count", "created_at": "date"}, inplace=True)
        dftop = dftopcomp.loc[:, ["date", "Total Count"]]
        # Create company figure
        # end = pd.to_datetime(end_date)
        # start = pd.to_datetime(start_date)
        ddays = pd.Timedelta((end-start), "d").days
        print(F"ddays are {ddays}")
        ts= start
        te = end
        # Previous Period and Previous Year
        pyrs = ts.replace(year=ts.year-1)
        pyre = te.replace(year=te.year-1, hour=23, minute=59, second=59)
        if ddays <= 30:
          if ts.is_month_start and te.is_month_end:
            pts = (ts - timedelta(days=1)).replace(day=1, hour=0, minute=0, second=0)
            pte = (ts - timedelta(days=1)).replace(hour=23, minute=59, second=59)
            print(ddays, ts, te, pts, pte, pyrs, pyre)
          else:
            if ts.is_month_start and not te.is_month_end:
              pts = (ts - timedelta(days=ts.day)).replace(day=1, hour=0, minute=0, second=0)
              prv_month, prv_year = (te.month-1, te.year) if te.month != 1 else (12, te.year-1)
              pte = te.replace(month=prv_month, year=prv_year)
              print(f"previous period {pts, pte}")
            else:
              prv_month, prv_year = (ts.month-1, ts.year) if ts.month != 1 else (12, ts.year-1)
              pts = ts.replace(month=prv_month, year=prv_year)
              prve_month, prve_year = (te.month-1, te.year) if ts.month != 1 else (12, te.year-1)
              pte = te.replace(month=prve_month, year=prve_year)
              print(f"flex period {pts, pte}")
        else:
          if ddays <= 61:
            if ts.is_month_start and te.is_month_end:
              pts = (ts - timedelta(days=58)).replace(day=1, hour=0, minute=0, second=0)
              pte = (te - timedelta(days=63)) + pd.offsets.MonthEnd()
              print(f"previos quarter or 2mths {pts, pte}")
            else:
              if ts.is_month_start and not te.is_month_end:
                pts = (ts - timedelta(days=58)).replace(day=1, hour=0, minute=0, second=0)
                if te.month == 1:
                  prve_month, prve_year = (11, te.year-1)
                elif te.month == 2:
                  prve_month, prve_year = (12, te.year-1)
                else:
                  prve_month, prve_year = (te.month-2, te.year)
                pte = te.replace(month=prve_month, year=prve_year)
                print(f"previous 2x period {pts, pte}")
              else:
                if ts.month == 1:
                    if ts.day == 31:
                        pts = ts.replace(day=30, month =11, year=ts.year-1)
                        pte = te.replace(month = te.month-2)
                    else:
                        pts = ts.replace(month = 11, year=ts.year-1)
                        pte = te.replace(month = 11, year=ts.year-1 )
                elif ts.month == 2:
                    pts = ts.replace(month = 12, year=ts.year-1)
                    pte = te.replace(month = te.month-2)
                else:
                    pts = ts.replace(month = ts.month-2)
                    pte = te.replace(month = te.month-2)
                print(f"flex 2x period {pts, pte}")
          else:
            if ddays <= 91:
              if ts.is_month_start and te.is_month_end:
                pts = (ts - timedelta(days=88)).replace(day=1, hour=0, minute=0, second=0)
                pte = (te - timedelta(days=93)) + pd.offsets.MonthEnd()
                print(f"This is a quarter {pts,pte}")
              else:
                if ts.is_month_start and not te.is_month_end:
                  pts = (ts - timedelta(days=88)).replace(day=1, hour=0, minute=0, second=0)
                  if te.month == 1:
                    prve_month, prve_year = (10, te.year-1)
                  elif te.month == 2:
                    prve_month, prve_year = (11, te.year-1)
                  elif te.month == 3:
                    prve_month, prve_year = (12, te.year-1)
                  else:
                    prve_month, prve_year = (te.month-3, te.year)
                  pte = te.replace(month=prve_month, year=prve_year)
                else:
                  pts = (ts - timedelta(days=88)).replace(day=ts.day, hour=0, minute=0, second=0)
                  if te.month == 1:
                    prve_month, prve_year = (10, te.year-1)
                  elif te.month == 2:
                    prve_month, prve_year = (11, te.year-1)
                  elif te.month == 3:
                    prve_month, prve_year = (12, te.year-1)
                  else:
                    prve_month, prve_year = (te.month-3, te.year)
                  pte = te.replace(month=prve_month, year=prve_year)
                print(f"flex under 3 months{pts,pte}")
            else:
                pts = (ts - timedelta(days=ddays)).replace(day=ts.day, hour=0, minute=0, second=0)
                pte = (pts + timedelta(days=ddays)).replace(day=te.day, hour=23, minute=59, second=59)
                print(f"flex over 3 months {pts, pte}")
    print("prperiod")
    mask2 = (df['created_at'] >= pts) & (df['created_at'] <= pte)
    mask4 = (df['created_at'] >= pyrs) & (df['created_at'] <= pyre)
    # dfanaliz df between start and end date
    dfanaliz2 = df.loc[mask2]
    dfanaliz4 = df.loc[mask4]
    # Choose category from dropdown
    dfgraph_prev = dfanaliz2[dfanaliz2['Ana Kategori'].isin([Kat_choice])]
    dfgraph_pyear = dfanaliz4[dfanaliz4['Ana Kategori'].isin([Kat_choice])]
    analiz_prev = dfgraph_prev[dfgraph_prev[display_dpdn].isin([dyn_dropdown])]
    analiz_pyear = dfgraph_pyear[dfgraph_pyear[display_dpdn].isin([dyn_dropdown])]
    dftopcomp_prev = analiz_prev.groupby(by=["created_at"]).count().reset_index()
    dftopcomp_pyear = analiz_pyear.groupby(by=["created_at"]).count().reset_index()
    dftopcomp_prev.rename(columns={"Unnamed: 0": "Total Count"}, inplace=True)
    dftopcomp_pyear.rename(columns={"Unnamed: 0": "Total Count"}, inplace=True)
    dftop_prev = dftopcomp_prev.loc[:, ["created_at", "Total Count"]]
    dftop_pyear = dftopcomp_pyear.loc[:, ["created_at", "Total Count"]]
    # fig.update_traces(dftopcomp_prev, x="created_at", y='Total Count', color="green", mode="markers+lines", hovertemplate=None)
    print(f"previous df {dfgraph_prev.shape}")
    dftop_prev['created_at'] = pd.to_datetime(dftop_prev['created_at'])
    dftop_pyear['created_at'] = pd.to_datetime(dftop_pyear['created_at'])
    dftop_prev['date']=dftop_prev['created_at']+timedelta(days=ddays)
    print(f" min.: {dftop_pyear['created_at'].min()}")
    print(f" max.: {dftop_pyear['created_at'].max()}")
    dftop_pyear['date']=dftop_pyear['created_at']+timedelta(days=365)
    dftop = dftop.rename(columns={'created_at': 'date'})
    dftop_prev = dftop_prev.rename(columns={'Total Count': 'Prev. Period'})
    dftop_pyear = dftop_pyear.rename(columns={'Total Count': 'Prev. Year'})
         #Graph Update Previous Period or Previous Year
    if tabs_choice == "tab-1":
        if per_choice == []:
            fig = px.line(dftop, x="date", y='Total Count') #, color=display_choice, symbol=display_choice
            fig.update_traces(mode="markers+lines", hovertemplate=None)
        else:
            fig = {}
            if len(per_choice) == 2:
                print(f"prperiod and pryear {pyrs, pyre}")
                newtop2 = pd.merge(dftop, dftop_prev, how='outer', on="date")
                newtop = pd.merge(newtop2, dftop_pyear, how='outer', on='date')
                fig = px.line(newtop, x="date", y=['Total Count', 'Prev. Period', 'Prev. Year'], hover_data=["created_at_x","created_at_y", "date"],
                        color_discrete_sequence=["blue", "red", "green"])
                fig.update_traces(mode="markers+lines", hovertemplate=None)
                fig.update_layout(hovermode="x unified")
            else:
                if per_choice == [1]:
                   newtop = pd.merge(dftop, dftop_prev, how='outer', on="date")
                   fig = px.line(newtop, x="date", y=['Total Count', 'Prev. Period'], hover_data=["created_at", "date"])
                   fig.update_traces(mode="markers+lines", hovertemplate=None)
                   fig.update_layout(hovermode="x unified")

                elif per_choice == [2]:
                    print(f"pryear{pyrs, pyre}")
                    newtop = pd.merge(dftop, dftop_pyear, how='outer', on='date')
                    fig = px.line(newtop, x="date", y=['Total Count', 'Prev. Year'], hover_data=["created_at", "date"], color_discrete_sequence=["blue", "green"])
                    fig.update_traces(mode="markers+lines", hovertemplate=None)
                    fig.update_layout(hovermode="x unified")
        print("figure prepared")
        dempty = {}
        return fig, dempty

    # print DataTable
    elif tabs_choice =='tab-2':
        dftable = dfgraph[dfgraph[display_dpdn].isin([dyn_dropdown])]
        dftable = dftable.loc[:,['created_at','barcode']]
        dftable_copy =dftable
        dftable = dftable.reset_index()
        dftable = dftable.assign(Weeks =dftable['created_at']).drop(columns='created_at', axis=1)
        dftable = dftable.set_index('Weeks')
        dftable = dftable.resample('W-mon', label='left', closed = 'left').count()
        dftable["Week Number"] = pd.to_datetime(dftable.index)
        dftable["Week Number"] = pd.to_datetime(dftable['Week Number']).apply(lambda x: x.date().isocalendar().week)
        dftable = dftable[["Week Number", "barcode"]]
        # Add previous week numbers to table
        start_week = dftable["Week Number"].min()
        end_week = dftable["Week Number"].max()
        current_period_weeks = end_week - start_week +1
        dftable["Previous Period (Week Nr.)"] = dftable["Week Number"] - current_period_weeks
        dftable["Previous Period (Week Nr.)"] = dftable["Previous Period (Week Nr.)"].apply(lambda x: x+52 if x <=0 else x)
        # Calculate previous period data
        pr_start_date = dftable_copy["created_at"].min() - timedelta(days=7*current_period_weeks.item())
        pr_end_date = dftable_copy["created_at"].max() - timedelta(days=7*current_period_weeks.item())
        print(f"end date is: {pr_end_date}")
        print(f"start date is: {pr_start_date}")
        print(type(pr_start_date), type(pr_end_date))
        print(dftable_copy["created_at"].min(), type(dftable_copy["created_at"].min()))
        if pr_start_date < df["created_at"].min():
            pr_start_date = df["created_at"].min()
        print(pr_start_date, pr_end_date)
        mask3 = (df_copy['created_at'] >= pr_start_date) & (df_copy['created_at'] <= pr_end_date)
        print(f"mask3: {mask3}")
        dfanaliz3 = df.loc[mask3]
        print(0, dfanaliz3.head())
        dfdata_prev = dfanaliz3[dfanaliz3['Ana Kategori'].isin([Kat_choice])]
        data_prev = dfdata_prev[dfdata_prev[display_dpdn].isin([dyn_dropdown])]
        data_prev = data_prev.loc[:,['created_at','barcode']]
        dftable_copy = data_prev.reset_index()
        print(1, dftable_copy.head())
        dftable_copy = dftable_copy.assign(Weeks =dftable_copy['created_at']).drop(columns='created_at', axis=1)
        print(2, dftable_copy.head())
        dftable_copy = dftable_copy.set_index('Weeks')
        print(3, dftable_copy.head())
        dftable_copy = dftable_copy.resample('W-mon', label='left', closed = 'left').count()
        print(4, dftable_copy.head())
        dftable_copy = dftable_copy[["barcode"]]
        print(5, dftable_copy.head())
        dftable_copy.rename(columns={"barcode": "Pr. Period Sale"}, inplace=True)
        print(6, dftable_copy.head())
        # Add previous week data to table
        dffinal = dftable[["Previous Period (Week Nr.)", "Week Number", "barcode"]]
        dffinal = dffinal.rename(columns={"barcode": "Weekly Sale", "Week Number": "Current Period (Week Nr.)"})
        dffinal = pd.concat([dffinal, dftable_copy.set_index(dffinal.index)], axis=1)
        dffinal["Growth vs. prev. Period"] = ((dffinal["Weekly Sale"]/dffinal["Pr. Period Sale"] -1)*100).map('{:,.2f}'.format).add('%')
        datatbl = dffinal.to_dict('records')
        columnstbl = [{'name': i, 'id': i} for i in dffinal.columns]
        fig = {}
    return fig, [dtb.DataTable(data=datatbl, columns=columnstbl, style_cell={'textAlign': 'left', 'padding': '5px'},
                        style_header={'backgroundColor': 'hotpink', 'color': 'white', 'fontWeight': 'bold'})]