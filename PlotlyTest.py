import pandas as pd
import numpy as np
import pickle
import _ModifyResult_
import plotly.io as pio
import plotly.graph_objects as go
import plotly.express as px

# pio.renderers.default = "browser"

tmppath = 'D:\\uno\\unoDB\\'
tmppath2 = 'D:\\uno\\unoDB\\ResultDB\\'
tmppath3 = 'D:\\uno\\unoDB\\FinalDB\\'


FT = pickle.load(open(tmppath3 + 'DBF_FT' + '.pkl', 'rb'))
# FT = _ModifyResult_.unoDB(DBFT, 'FT')

# fig = px.scatter(FT.DB, y='CA', x='JLC_TYPE', trendline='ols', template='plotly_white')
# fig.update_traces(marker_size=2)
# fig.show()

fig = px.scatter(FT.DB, y='CA', x='CTB_COMPOUND', marginal_y="histogram")
fig1 = px.scatter(FT.DB, y='CA_1', x='CTB_COMPOUND', marginal_y="histogram")
fig.add_traces(fig1.data)
# fig.add_trace(go.Scatter(y=FT.DB['CA_1'], x=FT.DB['CTB_COMPOUND'], mode='markers', name='data'))
fig.show()

# fig = px.scatter(FT.DB, y='CA', x='BT1_ANGLE')
# fig.update_traces(marker_size=2)
# fig.show()
#
# fig = px.scatter(FT.DB, y='CA', x='C01_MATERIAL')
# fig.update_traces(marker_size=2)
# fig.show()
