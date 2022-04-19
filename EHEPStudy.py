import pandas as pd
import numpy as np

#DASH
import dash
from dash import dcc
from dash import html
from dash import Input, Output
#PLOTLY
import plotly.express as px

####################################
##       READ THE DATA            ##
####################################

## Functions
def ReadFile(fname,CHUNKSIZE,Filter):
    df_chunk = pd.read_csv(fname,sep=' ',index_col=None, usecols=cols,names=col_names,chunksize=CHUNKSIZE,nrows=Filter)
    
    chunk_list=[]
    for chunk in df_chunk:
        chunk_list.append(chunk)
    
    #Concat
    df_concat = pd.concat(chunk_list)
    
    return df_concat
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

col_names=["Event","lepflav","ptlep0","ptjet0","ptjet1","mtlep0","mtjet0","mtjet1","dijetmass",
           "drjet01","MET","HT","dphimetjet0","dphimetjet1","dphimetlep0","njet","nbjet","dijetPT",
           "dijetMT","dphijet0lep0","dphijet1lep0","dphidijetlep0","dphimetdijet","ST"]

LabelName=["Lepton PT","Leading jet Pt","SubLeading jet pt","Lepton MT","Leading Jet MT",
           "Subleading Jet MT","Dijet Invariant Mass","deltaR(leading jet,subleading jet)","MET","HT",
           "dphi(met,leading jet)","dphi(met,subleading jet)","dphi(met,lepton)",
           "No of jets","No of b-jets","Dijet System PT","Dijet System MT","dphi(leading jet,lepton)",
           "dphi(subleading jet,lepton)","dphi(dijet system,lepton)","dphi(dijet system,met)","ST"]


cols = np.arange(0,len(col_names),1)

#dataFile
file_in = './data/dataSample.txt'

##Signal
df=ReadFile(file_in,5000,50000)
df['label']=1
df['sample']=0


##############################################
####            DASH APP                   ###
##############################################

external_stylesheets = ['https://www.w3schools.com/w3css/4/w3.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(children=[
    html.H1(className="w3-panel w3-pale-green w3-center",children="EHEP Study"),
    html.H2(className="w3-center",children="Input Variable Distributions"),

    html.Div([
        html.Div(className="box1",
                 style={
                    'float':'left',
                    'background-color':'white',
                    'color':'red',
                    'height':'100px',
                    'margin-left':'100px',
                    'width':'30%',
                    'display':'inline-block'
                    },children=[
                 html.H2(className="w3-center w3-text-gray w3-border w3-border-gray",children="Tune Your Plots"),
                 html.P('Variable Name',style={'text-align':'left','font-size':'20px'}),
                  dcc.Dropdown(
                        id="var-dropdown",
                        options=[
                            {'label':LabelName[index],'value':var}for index,var in enumerate(df.columns[2:-2])
                        ],
                        value='ptlep0'
                    ),
                #html.P('Process',style={'text-align':'left','font-size':'20px'}),

                #dcc.Checklist(id='process',labelStyle={'fontsize':'20px','color':'black'},options=[
                #        {'label':'Signal   ','value':'vllm100'},
                #        {'label':' Background','value':'wjets'},
                #  ], 
                #    value =['vllm100']
                #                
                #  ),
                     
                  html.P('Number of Bins',style={'text-align':'left','font-size':'20px'}),
                  dcc.Slider(id='binslider',min=25,max=100,step=25,value=25)

                 ]),
        html.Div(className="box2",
                 style={
                    'float':'right',
                    'background-color':'white',
                    'color':'red',
                    'height':'500px',
                    'margin-left':'10%',
                    'width':'50%',
                    'display':'inline-block'
                    },children=[
                 html.H2(className="w3-center w3-text-gray",children="Plots"),
                 dcc.Graph(id='graph'),
        ]),
    ]),
]) 

@app.callback(
    Output("graph", "figure"), 
    Input('binslider', 'value'),
    Input('var-dropdown','value'),
#    Input('process','value'),
)
def update_figure(Nbins,varname):
    fig = px.histogram(df, x=varname,nbins=Nbins,opacity=0.8,width=800,height=600,log_y=True)
    fig.update_layout(paper_bgcolor="LightGray",
                     font=dict(
                         family="monospace",
                         size=18
                     ))    

    return fig

if __name__== '__main__':
    app.run_server(debug=False)
