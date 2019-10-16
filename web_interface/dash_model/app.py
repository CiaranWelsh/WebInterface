import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import os
import numpy as np
import plotly.graph_objs as go
from collections import OrderedDict

from web_interface._simulator import TimeSeries
from web_interface._model_string import model_string

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
WD = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
WEB_INTERFACE_DIR = os.path.join(WD, 'web_interface')
APP_DIR = os.path.join(WEB_INTERFACE_DIR, 'dash_model')
ASSETS_DIR = os.path.join(APP_DIR, 'assets')

NETWORK_FNAME = os.path.join(WEB_INTERFACE_DIR, 'network.png')

# checks for directories
for i in [WD, WEB_INTERFACE_DIR, ASSETS_DIR, APP_DIR]:
    if not os.path.isdir(i):
        raise ValueError(i)


def get_model_inputs(model_string):
    """
    Return model inputs from the model string
    Args:
        model_string:

    Returns:

    """
    # modify this list to include all model inputs
    return ['AICAR_treatment']


def get_model_species(model_string):
    """
    Return model components from model string
    Args:
        model_string:

    Returns:

    """

    return ['AMPK', 'AMPK_P', 'PGC1a',
     'PGC1a_P', 'PGC1a_deacet', '$SIRT1_activity',
     'SIRT1', 'NAD', 'Delay_in_NAD_increase',
     'PARP', 'PGC1a_Deacetylation_Activity',
     'AICAR_Delay', 'AICAR_treatment', 'Glucose in compartment',
     'GlucoseDelay', 'NAD_NegReg', 'NR_NMN in compartment',
     'Damage', 'Mito_old', 'Mitophagy', 'Mito_new', 'Mito_turnover'
     ]


model_inputs = get_model_inputs(model_string)
model_species = get_model_species(model_string)

# dictionary to support the output buttons callback
NCLICKS_DCT = OrderedDict(
    all_output_btn={
        'n_clicks': 0,
        'output': model_species
    },
    clear_output_btn={
        'n_clicks': 0,
        'output': []
    },
    # The commented out section is taylored for my model. You can replace them if you like

    # all_pi3k_output_btn={
    #     'n_clicks': 0,
    #     'output': ['IRS1', 'IRS1a', 'pIRS1', 'PI3K',
    #                'pPI3K', 'PI3Ki', 'PIP2', 'PIP3',
    #                'PDK1', 'PDK1_PIP3', 'Akt', 'Akt_PIP3',
    #                'pAkt', 'Akt_PIP3', 'Akti', 'TSC2',
    #                'pTSC2', 'RagGDP', 'TSC2_Rag', 'RagGTP',
    #                'mTORC1cyt', 'mTORC1lys',
    #                'RhebGTP', 'pmTORC1', 'RhebGDP', 'mTORC1i',
    #                'mTORC1ii', 'mTORC1iii', 'FourEBP1',
    #                'pFourEBP1', 'S6K', 'pS6K', 'PTEN']
    # },
    # active_pi3k_output_btn={
    #     'n_clicks': 0,
    #     'output': ['IRS1a', 'pPI3K', 'pAkt', 'TSC2_Rag', 'RagGTP',
    #                'RhebGTP', 'pmTORC1', 'pFourEBP1', 'pS6K']
    # },
    # ampk_output_btn={
    #     'n_clicks': 0,
    #     'output': [
    #         'AMPK', 'AMPKi', 'pAMPK',
    #     ]
    # },
    # ampk_regulation_btn={
    #     'n_clicks': 0,
    #     'output': [
    #         'CaMKK2', 'CaMKK2a', 'Ca2', 'PKC', 'PKCa', 'LKB1', 'LKB1_nuc'
    #     ]
    # },
    # erk_output_btn={
    #     'n_clicks': 0,
    #     'output': ['RTK', 'pRTK', 'Sos', 'pRTKa', 'pSos',
    #                'RasGDP', 'RasGTP', 'Raf', 'pRaf', 'Mek',
    #                'pMek', 'Erk', 'pErk', 'Meki', 'DUSPmRNA', 'DUSP',
    #                ]
    # },
    # ip3_output_btn={
    #     'n_clicks': 0,
    #     'output': ['PLCeps', 'pPLCeps', 'IP3', 'DAG', 'IpR', 'IpRa', ]
    # },
    # e2_output_btn={
    #     'n_clicks': 0,
    #     'output': [
    #         'E2', 'E2_cyt', 'ERa_cyt', 'ERa_E2', 'ERa_dimer', 'ERa_dimer_nuc',
    #         'Greb1mRNA', 'Greb1', 'TFFmRNA', 'TFF', 'eIFa', 'ERa_cyti'
    #     ]
    # },
    # phenom_output_btn={
    #     'n_clicks': 0,
    #     'output': ['ProlifSignals', 'Growth', 'Immuno', 'Autophagy']
    # },
    # infg_output_btn={
    #     'n_clicks': 0,
    #     'output': ['pJak', 'Jak', 'Stat1', 'pStat1',
    #                'pStat1_dim_cyt', 'pStat1_dim_nuc', 'IDO1mRNA', 'IDO1']
    # },
    # trp_output_btn={
    #     'n_clicks': 0,
    #     'output': ['Kyn', 'GCN2', 'GCN2_a', 'eIFa',
    #                'peIFa']
    # },
)


def plot_graph(model_string, model_inputs, start, stop, step, outputs):
    """
    Plot the graph

    Args:
        model_string:
        model_inputs:
        start:
        stop:
        step:
        outputs:

    Returns:

    """
    model_inputs = {i: 1 for i in model_inputs}
    ts = TimeSeries(model_string, model_inputs, float(start), float(stop), int(step)).simulate()
    ts = ts[outputs]
    print('model inputs: ', model_inputs)
    print(ts.head())
    traces = []
    for i in ts:
        traces.append(
            go.Scatter(
                x=np.array(ts.index),
                y=ts[i],
                name=i,
                mode='lines'
            )
        )

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'Time (AU)'},
            yaxis={'title': '[AU]'},
            showlegend=True
        )
    }


app = dash.Dash(
    __name__,
    assets_folder=ASSETS_DIR,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    suppress_callback_exceptions=True
)

app.layout = html.Div([
    html.H1(children='NAD Model'),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Simulation', value='tab-1'),
        # dcc.Tab(label='Model Definition', value='tab-2'),
    ]),
    html.Div(id='tabs-content')
])

tab1 = html.Div([
    html.Div([

        # a left panel for inputs
        html.H2('Select Model Inputs'),
        html.Div([
            html.Div([
                dcc.Checklist(
                    id='model_inputs',
                    options=[
                        {'label': i, 'value': i} for i in model_inputs
                    ],
                    # multi=True,
                    value=['AICAR_treatment'],
                    labelStyle={"display": "inline-block"},
                    style={'text-align': 'center'}
                ),
                html.Label('(Inputs are constant throughout simulation. Checked=1, unchecked=0).',
                           style={'text-align': 'center'}),
            ]),

            html.Div([
                html.H2('Select Model Outputs'),
                dcc.Dropdown(
                    id='outputs',
                    options=[{'label': i, 'value': i} for i in model_species],
                    value=['AMPK'],#NCLICKS_DCT['active_pi3k_output_btn']['output'],
                    multi=True,
                    persistence=True,
                    style={'autocomplete': 'off'}
                ),
            ]),

            html.Div([
                html.Button(id='clear_output_btn', children='Clear'),
                html.Button(id='all_output_btn', children='All Outputs'),
                # html.Button(id='all_pi3k_output_btn', children='PI3K Outputs'),
                # html.Button(id='active_pi3k_output_btn', children='Active PI3K Outputs'),
                # html.Button(id='erk_output_btn', children='Erk Output'),
                # html.Button(id='ampk_output_btn', children='AMPK Output'),
                # html.Button(id='ampk_regulation_btn', children='AMPK Regulation Output'),
                # html.Button(id='ip3_output_btn', children='IP3 Output'),
                # html.Button(id='e2_output_btn', children='Estrogen Output'),
                # html.Button(id='phenom_output_btn', children='Phenomenological Output'),
                # html.Button(id='infg_output_btn', children='INFg Output'),
                # html.Button(id='trp_output_btn', children='Trp Output'),
            ]),

            html.H2('Integration Parameters'),
            html.Div([
                html.Form([
                    html.Label('Start'),
                    dcc.Input(placeholder='0', type='text', value=0, id='start'),
                    html.Label('Stop'),
                    dcc.Input(placeholder='100', type='text', value=100, id='stop'),
                    html.Label('Step'),
                    dcc.Input(placeholder='101', type='text', value=101, id='step'),
                ],
                    style={'display': 'flex',
                           'align': 'center'},
                )
            ], style={'align': 'center'}
            )
        ]),

        # graph
        html.Div([dcc.Graph(
            id='graph', figure=plot_graph(
                model_string,
                {i: 1 for i in model_inputs},
                0, 100, 101,
                ['AMPK']
                # NCLICKS_DCT['active_pi3k_output_btn']['output'],
            )
        )
        ]),
    ]),

    # for network image
    html.Div([
        html.Img(
            src='/assets/network.png',
            style={
                'width': '100%',
                'height': '100%',
            }
        ),
    ], style={
        'height': '100%',
        'width': '100%'
    }),

    html.Div(children=[
        html.Div([
            html.Label('If you modify the model definition below, the changes will be reflected '
                       'in the simulation output. For instance, to simulate TSC knockdown, '
                       'ensure all relevant TSC2 components start with an initial '
                       'amount of 0.'),
            dcc.Textarea(
                id='model_string',
                value=model_string,
                style={
                    'width': '100%',
                    'height': '100%',
                }
            ),
        ],
            style={'height': '1000px'})

    ], style={
        # 'background-color': 'coral',
        'width': '100%',
        'height': '100%'
    })
])


@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs', 'value')]
)
def render_content(tab):
    if tab == 'tab-1':
        return tab1
    # elif tab == 'tab-2':
    #     return tab2


@app.callback(
    Output(component_id='graph', component_property='figure'),
    [
        Input(component_id='model_string', component_property='value'),
        Input(component_id='model_inputs', component_property='value'),
        Input(component_id='start', component_property='value'),
        Input(component_id='stop', component_property='value'),
        Input(component_id='step', component_property='value'),
        Input(component_id='outputs', component_property='value'),
    ]
)
def update_inputs_callback(model_string, model_inputs, start, stop, step, outputs):
    """
    update graph
    Args:
        model_string:
        model_inputs:
        start:
        stop:
        step:
        outputs:

    Returns:

    """
    return plot_graph(model_string, model_inputs, start, stop, step, outputs)


# @app.callback(
#     Output('outputs', 'value'),
#     [Input(i, 'n_clicks') for i in list(NCLICKS_DCT.keys())]
# )
# def output_callbacks(*args):
#     # default return
#     to_return = NCLICKS_DCT['active_pi3k_output_btn']['output']
#     if all(args) is None:
#         raise dash.exceptions.PreventUpdate
#
#     for i in range(len(args)):
#         btn = list(NCLICKS_DCT.keys())[i]
#         nclick = args[i]
#         existing_nclick = NCLICKS_DCT[btn]['n_clicks']
#
#         if nclick is not None:
#             if nclick != existing_nclick:
#                 NCLICKS_DCT[btn]['n_clicks'] = nclick
#                 to_return = NCLICKS_DCT[btn]['output']
#             else:
#                 continue
#     return to_return


if __name__ == '__main__':
    app.run_server(debug=True)
