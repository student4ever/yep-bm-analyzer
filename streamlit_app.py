import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
import plotly.graph_objects as go
import plotly.io as pio

st.set_page_config(
    layout="centered", page_icon="⚡", page_title="Interactive YEP app"
)
st.title("⚡ YEP | Geschäftsmodelle jenseits der reinen Energieversorgung")
st.write(
    """
    Diese App stellt die aus Sicht der YEP Arbeitsgruppe interessantesten Geschäftsmodelle interaktiv dar. 
    """
)

# Load the data
# https://docs.google.com/spreadsheets/d/1ZRFcyil83dX7jwTFI37AS8zjvrwBinAMwQ8ZMkQnu8s/edit?usp=sharing
sheet_id = "1ZRFcyil83dX7jwTFI37AS8zjvrwBinAMwQ8ZMkQnu8s"
sheet_name = "app_data"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

data = pd.read_csv(url, index_col=[0])
bm_to_plot = st.multiselect(label="Auswahl der Dazustellende Business Models", options=data.columns,
                            default=data.columns[0])
entries = data.index

# Plotting the stuff

layout=go.Layout(
    font=dict(
        family="Arial",  # Arial, Helvetica, Roboto, IBM Plex Sans
        size=12,
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    yaxis={'side': 'right'},
    autosize=True,
    # width=800,
    # height=800,
    # margin=go.layout.Margin(
    #     l=50,
    #     r=50,
    #     b=50,
    #     t=50,
    #     pad=4
    # )

)

fig = go.Figure(layout=layout)

for b in bm_to_plot:
    df = data[b]
    numbers = list(df.values)
    idx = df.index.tolist()
    numbers.append(numbers[0])
    idx.append(idx[0])

    fig.add_trace(go.Scatterpolar(
          name=b,
          r=numbers,
          theta=idx,
          opacity=0.75,
        ))

if st.checkbox("Plot befüllen", True):
    fig.update_traces(fill='toself')

fig.update_layout(
    title = "Evaluierungsmatrix",
    font_size = 15,
    # showlegend = True,
    legend=dict(
        orientation="h",
        yanchor="top", y=-0.2,
        xanchor="left", x=0.02),
    polar = dict(
      # bgcolor = "rgb(223, 223, 223)",
      angularaxis = dict(
        linewidth = 1,
        showline=True,
        linecolor='black'
      ),
      radialaxis = dict(
        side = "clockwise",
        showline = False,
        linewidth = 2,
        gridcolor = "white",
        gridwidth = 2,
        dtick=1,
        range=[0, 5.5],
      ),
    ),
    paper_bgcolor = "white"
)


st.plotly_chart(fig, use_container_width=True)

st.header("Daten")
st.write("[Datenquelle](https://docs.google.com/spreadsheets/d/1ZRFcyil83dX7jwTFI37AS8zjvrwBinAMwQ8ZMkQnu8s/edit?usp=sharing)")
if st.checkbox("Ergebnisse der quantitative Bewertung der Geschäftsmodelle anzeigen", False):
    st.write(data)

st.header("Autoren")
from PIL import Image
image = Image.open('authors.PNG')

st.image(image, caption='Arbeitsgruppe 9 - YEP 3. Zyklus')
