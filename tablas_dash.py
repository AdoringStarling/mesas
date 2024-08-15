###########################################################################################################
##################OBTENER COPIAS AUTOMATICAS DE LAS FICHAS DE LA ESTRATEGIA TERRITORIAL####################
###########################################################################################################
##Elborado por: Danys Ortiz#

#Este script obtiene copias de las ficha de Comunidades energéticas en el marco de la construcción de la PP
#de Com. Energéticas, además genera copias de seguridad en el disco D del computador (por defecto)#

###Librerias
from koboextractor import KoboExtractor
import pandas as pd
import json
import plotly.express as px
import dash_bootstrap_components as dbc
import numpy as np

#Funciones
def dict_to_text(x):
    tx=''
    try:
        for i in x:
            i = list(i.values())[0]
            tx=tx+i+'\n'
        return tx
    except:
        return tx

def change_names(x):
    try:
        names=str(x).split(' ')
        namesx=[replace_dict[letter] for letter in names]
        namx=''
        for stringss in namesx:
            try:
                stringss.replace('<br>','')
            except:
                pass
            namx=namx+'\n'+stringss
        return namx
    except:
        return(str(x))

#Fin funciones

#Replace start
replace=pd.read_excel('aux1/diccionario_mesas.xlsx',sheet_name='choices') #Palabras de reemplazo
replace_1=replace[np.isin(replace['list_name'],replace['list_name'].unique()[0:5])]# Palabras de reemplazo iniciales
values=replace['label'].values
values_1=replace_1['label'].values
replace_dict = dict(zip(replace['name'].values, [values for values in values]))
replace_dict_1 = dict(zip(replace_1['name'].values, [values_1 for values_1 in values_1]))
#Replace end


###configuración del token
your_token = '3d81f96d16fbc8adc419e90fd5e5684bc58445ff' #replace token by the generated token
kobo = KoboExtractor(your_token, 'https://kf.kobotoolbox.org/api/v2')

form_id = 'aPc8FSwJ3eu9j7KJDPWr2f' # aPc8FSwJ3eu9j7KJDPWr2f aPc8FSwJ3eu9j7KJDPWr2f

data = kobo.get_data(form_id, query=None, start=None, limit=None, submitted_after=None)

#convert your data from json to a pd dataframe
df = pd.json_normalize(data['results'])
# preview your data -- this step is not compulsory 
#df.head()
#print(df.columns)
df=df.replace(replace_dict)
df_esp=df[df['Tipo_Reporte/Tipo_de_Reporte']=='Espacios de Diálogo Social']
df_mes=df[df['Tipo_Reporte/Tipo_de_Reporte']!='Espacios de Diálogo Social']
df_esp = df_esp[['Tipo_Reporte/Tipo_de_Reporte',
         'Tipo_Reporte/Subsector_que_genera_el_tipo_d',
         'Tipo_Reporte/Fecha_de_Registro_Seguimiento',
         'Tipo_Reporte/Nombre_de_quien_diligencia_el_reporte',
         'Tipo_Reporte/Correo_electr_nico_d_iligencia_el_reporte',
         'group_ke65b09/departamento',
         'group_ke65b09/Municipio',
         'group_ke65b09/Objetivo_del_Espacio',
         'group_ke65b09/Breve_descripci_n_de_l_espacio_de_di_logo',
         'group_ke65b09/Esta_espacio_de_di_logo_se_rea',
         'group_ke65b09/Relaci_n_el_c_digo_idad_alerta_temprana',
         'group_ke65b09/Actores_Sociales_Econ_micos_qu',
         'group_ke65b09/Nombre_de_las_organi_ciones_participantes',
         'group_ke65b09/Entidades_participantes',
         'group_ke65b09/Temas_abordados',
         'group_ke65b09/Durante_el_espacio_se_adquirie',
         'group_ke65b09/Principales_Compromisos_y_Responsables',
         ]]
df_esp.columns = ('Tipo de Reporte',
                'Sector del reporte',
                'Fecha de ocurrencia',
                'Nombre de quien diligenció',
                'Correo electrónico de quien reporta',
                'Departamento',
                'Municipio',
                'Objetivo del espacio',
                'Breve descripción del espacio de diálogo',
                '¿El espacio se realiza con ocasión de una conflictividad?',
                'Código de la alerta',
                'Actores Sociales y Económicos',
                'Nombre de las organizaciones asistentes',
                'Entidades Participantes',
                'Temas Abordados',
                '¿Se adquirieron compromisos?',
                'Principales compromisos y Responsables')

df_mes = df_mes[[
    'Tipo_Reporte/Tipo_de_Reporte',
    'Tipo_Reporte/Subsector_que_genera_el_tipo_d',
    'Tipo_Reporte/Fecha_de_Registro_Seguimiento',
    'Tipo_Reporte/Nombre_de_quien_diligencia_el_reporte',
    'Tipo_Reporte/Correo_electr_nico_d_iligencia_el_reporte',
    'Mesas/Nombre_de_la_Mesa',
    'Mesas/Tipo_de_Mesa',
    'Mesas/departamento_L',
    'Mesas/municipio_L',
    'Mesas/Objetivo_de_la_Mesa',
    'Mesas/Instituciones_Entidades_que_pa',
    'Mesas/Datos_de_Contacto_de_delegados_al_espacio',
    'Mesas/Compromisos_mesas',
    'Mesas/Observaciones_001',
    'Mesas/Entidad_l_der_de_la_mesa',
    'Mesas/Compromisos',
    'Mesas/Actores_Sociales_Econ_micos_qu_001'
         ]]
df_mes.columns = (
    'Tipo de Reporte',
    'Sector del reporte',
    'Fecha de ocurrencia',
    'Nombre de quien diligenció',
    'Correo electrónico de quien reporta',
    'Nombre de la Mesa',
    'Tipo de Mesa',
    'Departamento',
    'Municipio',
    'Objetivo',
    'Instituciones/Entidades que participan',
    'Datos de Contacto de delegados al espacio',
    'Compromisos 1',
    'Observaciones',
    'Entidad líder de la mesa',
    'Compromisos 2',
    'Actores Sociales/Económicos que participan')

df_esp['Actores Sociales y Económicos']=df_esp['Actores Sociales y Económicos'].apply(lambda x:change_names(x))
df_mes['Instituciones/Entidades que participan']=df_mes['Instituciones/Entidades que participan'].apply(lambda x:change_names(x))
df_mes['Actores Sociales/Económicos que participan']=df_mes['Actores Sociales/Económicos que participan'].apply(lambda x:change_names(x))
df_mes['Compromisos 1']=df_mes['Compromisos 1'].apply(lambda x:dict_to_text(x))
    
from dash import Dash, dash_table, dcc, html, Input, Output, callback, State
import pandas as pd

card_function=dbc.Card(
    dbc.CardBody([
        html.H6("La Oficina de Asuntos Ambientales y Sociales busca potenciar de manera significativa el desarrollo sostenible en armonía y respeto de los diferentes territorios del país donde existe presencia del sector minero-energético, de manera que se consolide como un aliado de los territorios.",
            className="card-text"),
        html.H6("Por ello, trabajamos en:", 
            className="card-text"),
        html.H6("   -El fortalecimiento de un buen relacionamiento del sector minero-energético con las autoridades ambientales, locales y las comunidades, promoviendo espacios de diálogo y concertación social.", 
            className="card-text"),
        html.H6("   -La definición de políticas y lineamientos que posicionen los subsectores de minería, energía e hidrocarburos con los más altos estándares, garantizando su sostenibilidad, articulando el sector en las diferentes etapas de planeación de los procesos de Ordenamiento Territorial de las regiones de manera articulada con el sector ambiental del país.", 
            className="card-text"),
        html.H6("   -La construcción de políticas de adaptación, mitigación y gobernanza del cambio climático, derechos humanos y gestión del riesgo de desastres del sector minero energética, así como estrategias de desarrollo y relacionamiento territorial y la articulación de una agenda de relacionamiento interministerial con el Ministerio de Ambiente y Desarrollo Sostenible.", 
            className="card-text"),
        html.Div(
        html.Img(

                            src="assets\OAAS_cut.png",

                            id="Tabla7a-image",

                            style={

                                "height": "auto",
                                #"max-width": "750x",
                                "margin-top": "5px",
                                "display":"block",
                                'textAlign': 'center',
                                "margin-left": "15%",
                                "width": "70%",
                                # "margin-bottom": "5px",

                            },

                        )),
    ]))

card_references=dbc.Card(
    dbc.CardBody([
        html.H6("Oliver H. Lowry, Nira J. Rosenbrough, A. Lewis Farr, Rose J. Randall, “Protein Measurement with the Folin Phenol Reagent,” The Journal of Biological Chemistry (JBC) 193: 265-275, 1951",
            className="card-text"),
    ]))

card_explication_sem=dbc.Card(
    dbc.CardBody([
        html.H6("[Descripción provisional hecha por IA] Este visor de datos es una herramienta poderosa que permite a los usuarios explorar y comprender la dinámica de los conflictos en el sector mineroenergético. Funciona a través de un tablero de control intuitivo que facilita la navegación y el análisis de la información. Aquí tienes una descripción detallada de su funcionamiento:",
            className="card-text"),
        html.H6("Filtrado por múltiples variables: Los usuarios pueden filtrar los datos por departamento, gerencia, fecha y subsector. Esto les permite enfocarse en áreas específicas de interés y obtener información relevante para sus necesidades de análisis.",
            className="card-text"),
        html.H6("Tablero de control interactivo: El tablero de control proporciona una interfaz interactiva donde los usuarios pueden seleccionar fácilmente las variables de interés y ver los resultados de forma dinámica. Pueden explorar diferentes combinaciones de filtros para obtener una visión más completa de los datos.", 
            className="card-text"),
        html.H6("Modelado de resultados en gráficas: Los resultados de los filtros se representan visualmente a través de diversas gráficas y visualizaciones. Estas gráficas pueden incluir histogramas, gráficos de barras, gráficos de líneas, entre otros, dependiendo de la naturaleza de los datos y las preferencias del usuario. Además, el usuario puede ajustar la categorización de fecha y conteo para adaptarse a sus necesidades analíticas específicas.", 
            className="card-text"),
        html.H6("Mapa interactivo: El visor también incluye un mapa interactivo que muestra la ubicación geográfica de los conflictos mineroenergéticos reportados. Al hacer clic en un lugar específico en el mapa, los usuarios pueden acceder a información detallada sobre los informes de conflictos en esa ubicación particular, como la fecha del informe, el tipo de conflicto, las partes involucradas, entre otros detalles relevantes.", 
            className="card-text"),
        html.H6("En resumen, este visor de datos ofrece una experiencia de usuario completa y dinámica para explorar y comprender los conflictos en el sector mineroenergético. Con su capacidad de filtrado, modelado de resultados y visualización interactiva, los usuarios pueden obtener información valiosa para la toma de decisiones y la formulación de políticas.", 
            className="card-text"),
    ]))
# App layout
app = Dash(__name__, prevent_initial_callbacks=True) # this was introduced in Dash version 1.12.0
server = app.server
# Sorting operators (https://dash.plotly.com/datatable/filtering)
header=     html.Div(

            [    
                html.Img(
                    src="assets\gobierno_1.png",
                    id="plotly-image",
                    className="logo-vida"
                ),                   
                 html.Div([
                html.H4(

                    "Buscador de Mesas de Concertación y Espacios de Diálogo",
                    style={'color':'black'},
                    className="model-title"

                    # style={"margin-bottom": "0px", 'textAlign': 'center','font-weight':'bold'},
                ),
                html.H6(

                    "Observatorio de la Oficina de Asuntos Ambientales y Sociales",
                    style={'color':'black'},
                    className="model-title"

                    # style={"margin-bottom": "0px", 'textAlign': 'center','font-weight':'bold'},
                )
                ],className="model-title"), 
                html.Img(
                    src="assets\OAAS_cut.png",
                    id="plotly-image3",
                    className="logo-oaas"
                ), 
                html.Img(
                    src="assets\ENERGÍA@4x.png",
                    id="plotly-image1",
                    className="logo-energia"
                ), 

            ], className="header", id='header')
app.layout = html.Div([
    header,
    html.H6(' Usted está accediendo a los registros de las mesas de concertación y espacios de diálogo adelantados por el Ministerio de Minas y Energía. Aquí podrá encontrar información territorializada a nivel departamental y municipal sobre los compromisos adquiridos por el sector en el marco del relacionamiento territorial y social, así como las temáticas relevantes en la agenda mineroenergética.',
    style={
        'font-family':'Nunito Sans',
        'color':'black',}),
    dcc.Markdown('''
        * Este instrumento es para uso interno de los funcionarios y contratistas del Ministerio y sus entidades adscritas; se prohíbe su divulgación a personas o entidades ajenas al Ministerio.
    ''',
    style={
        "fontSize": "1.2em",
        'font-family':'Nunito Sans',
        'color':'black',}),
    html.H1('Espacios de Dialogo',
                style={
                        "fontSize": "3em",
                        'font-family':'Nunito Sans',
                        'color':'black',}
            ),
    html.Div([
    dash_table.DataTable(

        id='datatable-interactivity1',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True, "hideable": True}
            if i == "iso_alpha3" or i == "year" or i == "id"
            else {"name": i, "id": i, "deletable": True, "selectable": True}
            for i in df_esp.columns
        ],
        data=df_esp.to_dict('records'),  # the contents of the table
        editable=True,              # allow editing of data inside all cells
        filter_action="native",     # allow filtering of data by user ('native') or not ('none')
        sort_action="native",       # enables data to be sorted per-column by user or not ('none')
        sort_mode="single",         # sort across 'multi' or 'single' columns
        column_selectable="multi",  # allow users to select 'multi' or 'single' columns
        row_selectable="multi",     # allow users to select 'multi' or 'single' rows
        row_deletable=True,         # choose if user can delete a row (True) or not (False)
        selected_columns=[],        # ids of columns that user selects
        selected_rows=[],           # indices of rows that user selects
        page_action="native",       # all data is passed to the table up-front or not ('none')
        page_current=0,             # page number that user is on
        page_size=150,               # number of rows visible per page

        style_table={
                    'overflowY': 'scroll',
                    'overflowX': 'scroll',
                    'maxWidth':'99%',
                },
        style_cell={                # ensure adequate header width when text is shorter than cell's text
            # 'minWidth': 70, 
            # 'maxWidth': 500, 
            # 'width': 70,
            'textAlign': 'left',
            # 'backgroundColor': 'rgb(30, 30, 30)',
            'color': 'white',
            'font-family':'Nunito Sans',
            'font-size': '13px',
            "whiteSpace": "pre-line",
            'maxWidth': '600px',
            'minWidth': '180px',
        },
        style_cell_conditional=[    # align text columns to left. By default they are aligned to right
            {
                'if': {'column_id': c},
                'textAlign': 'center'
            } for c in ['Nombre de quien diligenció', 'Departamento']
        ],
        style_header={
            'backgroundColor': '#edb600',
            'fontWeight': 'bold',
            'color': 'black',
        },
        style_data={                # overflow cells' content into multiple lines
            'whiteSpace': 'normal',
            'height': 'auto',
            'color': 'black',
            'backgroundColor': '#DDD0B4'
        },
        fixed_rows={'headers': True},
    ),

    # html.Br(),
    # html.Br(),
    # html.Div(id='bar-container'),
    # html.Div(id='choromap-container'),

],className="model_table_search"),
    
    html.H1('Mesas',
            style={
        "fontSize": "3em",
        'font-family':'Nunito Sans',
        'color':'black',}),
    html.Div([
    dash_table.DataTable(

        id='datatable-interactivity2',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True, "hideable": True}
            if i == "iso_alpha3" or i == "year" or i == "id"
            else {"name": i, "id": i, "deletable": True, "selectable": True}
            for i in df_mes.columns
        ],
        data=df_mes.to_dict('records'),  # the contents of the table
        editable=True,              # allow editing of data inside all cells
        filter_action="native",     # allow filtering of data by user ('native') or not ('none')
        sort_action="native",       # enables data to be sorted per-column by user or not ('none')
        sort_mode="single",         # sort across 'multi' or 'single' columns
        column_selectable="multi",  # allow users to select 'multi' or 'single' columns
        row_selectable="multi",     # allow users to select 'multi' or 'single' rows
        row_deletable=True,         # choose if user can delete a row (True) or not (False)
        selected_columns=[],        # ids of columns that user selects
        selected_rows=[],           # indices of rows that user selects
        page_action="native",       # all data is passed to the table up-front or not ('none')
        page_current=0,             # page number that user is on
        page_size=150,               # number of rows visible per page

        style_table={
                    'overflowY': 'scroll',
                    'overflowX': 'scroll',
                    'maxWidth':'99%',
                },
        style_cell={                # ensure adequate header width when text is shorter than cell's text
            # 'minWidth': 70, 
            # 'maxWidth': 500, 
            # 'width': 70,
            'textAlign': 'left',
            # 'backgroundColor': 'rgb(30, 30, 30)',
            'color': 'white',
            'font-family':'Nunito Sans',
            'font-size': '13px',
            "whiteSpace": "pre-line",
            'maxWidth': '600px',
            'minWidth': '180px',
        },
        style_cell_conditional=[    # align text columns to left. By default they are aligned to right
            {
                'if': {'column_id': c},
                'textAlign': 'center'
            } for c in ['Nombre de quien diligenció', 'Departamento']
        ],
        style_header={
            'backgroundColor': '#edb600',
            'fontWeight': 'bold',
            'color': 'black',
        },
        style_data={                # overflow cells' content into multiple lines
            'whiteSpace': 'normal',
            'height': 'auto',
            'color': 'black',
            'backgroundColor': '#DDD0B4'
        },
        fixed_rows={'headers': True},
    ),

    # html.Br(),
    # html.Br(),
    # html.Div(id='bar-container'),
    # html.Div(id='choromap-container'),

],className="model_table_search"),
        html.Div([
                    html.Div(
                        [     
        dbc.Button("¿Qué es el Observatorio de la Oficina de Asuntos Sociales y Ambientales (OAAS)?", 
                color='#DDD0B4',id="function_but_xl",className="me-1", n_clicks=0),
        dbc.Button("¿Como funciona el buscador?",
                color='#DDD0B4', id="semaforo_but_xl",size="sm", className="me-1", n_clicks=0),
        dbc.Button("Referencias",
                color='#DDD0B4', id="references_but_xl",size="sm", className="me-1", n_clicks=0)
        # html.Button("¿Cómo funciona?", id="function_but_xl",  className="footerButtons", n_clicks=0),
        # html.Button("¿Semáforo sísmico?", id="semaforo_but_xl", className="footerButtons", n_clicks=0),
        # html.Button("Referencias", id="references_but_xl", className="footerButtons", n_clicks=0)
        ], className='helpButtons'
        ),
                    # html.Hr(),
                    # html.Img(
                    # src="assets\OAAS_cut.png",
                    # id="logos-image"),
            ],id='footer'),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle(html.H2("¿Qué es el Observatorio de la Oficina de Asuntos Sociales y Ambientales (OAAS)?")), close_button=True),
                dbc.ModalBody(card_function),
            ],
            id="function_mod_xl",
            # fullscreen=True,
            is_open=False,
            size="xl",
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(html.H2(html.H2("Referencias"))),
                dbc.ModalBody(card_references),
            ],
            id="references_mod_xl",
            fullscreen=True,
            is_open=False,
            size="xl",
        ),
                dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle(html.H2("¿Como funciona el visor?"))),
                dbc.ModalBody(card_explication_sem),
            ],
            id="semaforo_mod_xl",
            fullscreen=True,
            is_open=False,
            size="xl",
        ),])


# -------------------------------------------------------------------------------------
# Create bar chart
# @app.callback(
#     Output(component_id='bar-container', component_property='children'),
#     [Input(component_id='datatable-interactivity', component_property="derived_virtual_data"),
#      Input(component_id='datatable-interactivity', component_property='derived_virtual_selected_rows'),
#      Input(component_id='datatable-interactivity', component_property='derived_virtual_selected_row_ids'),
#      Input(component_id='datatable-interactivity', component_property='selected_rows'),
#      Input(component_id='datatable-interactivity', component_property='derived_virtual_indices'),
#      Input(component_id='datatable-interactivity', component_property='derived_virtual_row_ids'),
#      Input(component_id='datatable-interactivity', component_property='active_cell'),
#      Input(component_id='datatable-interactivity', component_property='selected_cells')]
# )
# def update_bar(all_rows_data, slctd_row_indices, slct_rows_names, slctd_rows,
#                order_of_rows_indices, order_of_rows_names, actv_cell, slctd_cell):
#     # print('***************************************************************************')
#     # print('Data across all pages pre or post filtering: {}'.format(all_rows_data))
#     # print('---------------------------------------------')
#     # print("Indices of selected rows if part of table after filtering:{}".format(slctd_row_indices))
#     # print("Names of selected rows if part of table after filtering: {}".format(slct_rows_names))
#     # print("Indices of selected rows regardless of filtering results: {}".format(slctd_rows))
#     # print('---------------------------------------------')
#     # print("Indices of all rows pre or post filtering: {}".format(order_of_rows_indices))
#     # print("Names of all rows pre or post filtering: {}".format(order_of_rows_names))
#     # print("---------------------------------------------")
#     # print("Complete data of active cell: {}".format(actv_cell))
#     # print("Complete data of all selected cells: {}".format(slctd_cell))

#     dff = pd.DataFrame(all_rows_data)

#     # used to highlight selected countries on bar chart
#     colors = ['#7FDBFF' if i in slctd_row_indices else '#0074D9'
#               for i in range(len(dff))]

#     if "country" in dff and "did online course" in dff:
#         return [
#             dcc.Graph(id='bar-chart',
#                       figure=px.bar(
#                           data_frame=dff,
#                           x="country",
#                           y='did online course',
#                           labels={"did online course": "% of Pop took online course"}
#                       ).update_layout(showlegend=False, xaxis={'categoryorder': 'total ascending'})
#                       .update_traces(marker_color=colors, hovertemplate="<b>%{y}%</b><extra></extra>")
#                       )
#         ]


# -------------------------------------------------------------------------------------
# Create choropleth map
# @app.callback(
#     Output(component_id='choromap-container', component_property='children'),
#     [Input(component_id='datatable-interactivity', component_property="derived_virtual_data"),
#      Input(component_id='datatable-interactivity', component_property='derived_virtual_selected_rows')]
# )
# def update_map(all_rows_data, slctd_row_indices):
#     dff = pd.DataFrame(all_rows_data)

#     # highlight selected countries on map
#     borders = [5 if i in slctd_row_indices else 1
#                for i in range(len(dff))]

#     if "iso_alpha3" in dff and "internet daily" in dff and "country" in dff:
#         return [
#             dcc.Graph(id='choropleth',
#                       style={'height': 700},
#                       figure=px.choropleth(
#                           data_frame=dff,
#                           locations="iso_alpha3",
#                           scope="europe",
#                           color="internet daily",
#                           title="% of Pop that Uses Internet Daily",
#                           template='plotly_dark',
#                           hover_data=['country', 'internet daily'],
#                       ).update_layout(showlegend=False, title=dict(font=dict(size=28), x=0.5, xanchor='center'))
#                       .update_traces(marker_line_width=borders, hovertemplate="<b>%{customdata[0]}</b><br><br>" +
#                                                                               "%{customdata[1]}" + "%")
#                       )
#         ]

def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open

app.callback(
    Output("function_mod_xl", "is_open"),
    Input("function_but_xl", "n_clicks"),
    State("function_mod_xl", "is_open"),
)(toggle_modal)

app.callback(
    Output("references_mod_xl", "is_open"),
    Input("references_but_xl", "n_clicks"),
    State("references_mod_xl", "is_open"),
)(toggle_modal)

app.callback(
    Output("semaforo_mod_xl", "is_open"),
    Input("semaforo_but_xl", "n_clicks"),
    State("semaforo_mod_xl", "is_open"),
)(toggle_modal)
# -------------------------------------------------------------------------------------
# Highlight selected column
@app.callback(
    Output('datatable-interactivity1', 'style_data_conditional'),
    [Input('datatable-interactivity1', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': {'column_id': i},
        'background_color': '#D2F3FF'
    } for i in selected_columns]

@app.callback(
    Output('datatable-interactivity2', 'style_data_conditional'),
    [Input('datatable-interactivity2', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': {'column_id': i},
        'background_color': '#D2F3FF'
    } for i in selected_columns]


# -------------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run_server(debug=True)


#app = Dash(__name__)

#app.layout = html.Div([
#    dash_table.DataTable
#])

#dash_table.DataTable(df.to_dict('records'),[{"name":i, "id":i} for i in df.columns])

#if __name__ == '__main__':
#    app.run(debug=True)
