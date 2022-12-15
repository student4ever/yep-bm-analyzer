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

# Load the data
sheet_id = "1ZRFcyil83dX7jwTFI37AS8zjvrwBinAMwQ8ZMkQnu8s"

sheet_name = "app_text"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
total_text = pd.read_csv(url, index_col=[0], header=[0])

sheet_name = "app_data"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
total_data = pd.read_csv(url, index_col=[0], decimal=",")

st.write("{}".format(total_text.loc["Introtext"].iloc[0]))

name_use_case1 = total_data.index.name
table_use_case1 = total_data.iloc[0:7]
name_use_case2 = total_data.index[7]
table_use_case2 = total_data.iloc[8:8 + 7]
name_use_case3 = total_data.index[15]
table_use_case3 = total_data.iloc[16:16 + 7]

columns_with_text = total_data.columns.str.contains('Text_')
number_columns = total_data.columns[~columns_with_text]
text_columns = total_data.columns[columns_with_text]

st.header("Evaluierung der Geschäftsmodelle")

tab1_1, tab1_2 = st.tabs(['Use Cases', 'Beschreibung'])

use_cases = [name_use_case1, name_use_case2, name_use_case3]
with tab1_1:
    uc = st.radio(label="Auswahl des Use-Cases", options=use_cases)

with tab1_2:
    # with st.expander("Annahmen zum Use Case {}".format(uc)):

    for u in use_cases:
        txt_idx = pd.Index(
            ["Case", "Beispielunternehmen", "Gründung", "Mitarbeiteranzahl", "Markt", "Shareholder Struktur",
             "Wertschöpfungskette", "Umsatz", "Bestehende GM", "Umsatz Kundensegment",
             "Know-how / Interne Expertise", "Bestehendes Kraftwerksportfolio", "Strategie des Unternehmens"])
        uc_description = total_text.loc[txt_idx]
        uc_description.columns = uc_description.loc["Case"]
        uc_description = uc_description.iloc[1:].loc[:, u]
        uc_description.name = "Annahmen"
        st.subheader("{}".format(u))
        st.table(uc_description)

if uc == name_use_case1:
    table_use_case = table_use_case1
elif uc == name_use_case2:
    table_use_case = table_use_case2
elif uc == name_use_case3:
    table_use_case = table_use_case3
else:
    raise ValueError("Use case not defined.")
data = table_use_case.loc[:, number_columns]
text = table_use_case.loc[:, text_columns]

tab2_1, tab2_2 = st.tabs(['Neue Geschäftsmodelle', 'Beschreibung'])

with tab2_1:
    new_bm = [st.radio(label="Auswahl der neuen Geschäftsmodelle", options=number_columns[1:])]
    bm_to_plot = [number_columns[0]] + new_bm
    entries = data.index

with tab2_2:
    bm_description = total_text.loc[["New BM", "Beschreibung neue BM", "Bsp1", "Bsp2", "Bsp3"]]

    for b in total_text.loc["New BM"]:
        st.subheader("{}".format(b))
        bm_column = bm_description.loc[:, bm_description.loc["New BM"] == b]
        st.write(bm_column.loc["Beschreibung neue BM"].iloc[0])

        st.markdown("**Beispiele:**")
        for bsp in [1, 2, 3]:
            bsp_text = bm_column.loc["Bsp" + str(bsp)].iloc[0]
            if bsp_text != "0":
                st.write(bsp_text)

# Plotting the stuff

layout = go.Layout(
    font=dict(
        family="Arial",  # Arial, Helvetica, Roboto, IBM Plex Sans
        size=12,
    ),
    paper_bgcolor='white',
    plot_bgcolor='#e5ecf6',
    # yaxis={'side': 'right'},
    autosize=True,
)

fig = go.Figure(layout=layout)

for b in bm_to_plot:
    s = data[b]

    # rename the reference case
    if b == number_columns[0]:
        s.name = uc[9:]

    numbers = list(s.values)
    idx = s.index.tolist()
    numbers.append(numbers[0])
    idx.append(idx[0])

    fig.add_trace(go.Scatterpolar(
        name=s.name,
        r=numbers,
        theta=idx,
        opacity=0.75,
    ))

# if st.checkbox("Plot befüllen", True):
fig.update_traces(fill='toself')

fig.update_layout(
    title="Evaluierungsmatrix",
    font_size=12,
    # showlegend = True,
    legend=dict(
        orientation="h",
        yanchor="top", y=-0.2,
        xanchor="left", x=0.02),
    polar=dict(
        # bgcolor = "rgb(223, 223, 223)",
        angularaxis=dict(
            linewidth=1,
            showline=True,
            linecolor='darkgrey'
        ),
        radialaxis=dict(
            side="clockwise",
            showline=True,
            linewidth=1,
            gridcolor="white",
            gridwidth=1,
            dtick=1,
            range=[0, 5.5],
        ),
    ),
    paper_bgcolor="white"
)

tab3_1, tab3_2, tab3_3 = st.tabs(['Evaluierungsmatrix', 'Beschreibung', 'Annahmen'])

with tab3_1:
    st.plotly_chart(fig, use_container_width=True)
    st.subheader("Interpretation der Evaluierungsmatrix")

    legend = pd.Series(
        index=[
            "{} hat einen höheren Wert als {} 🔼".format(bm_to_plot[1], uc[9:]),
            "{} hat einen niedrigern Wert als {} 🔽".format(bm_to_plot[1], uc[9:])
        ],
        dtype=str,
        name="Interpretation"
    )
    legend.iloc[
        0] = "Der Nutzen bei {} überwiegt den Aufwand. Somit stellt die Einführung des neuen Geschäftsmodells eine Verbesserung dar.".format(
        bm_to_plot[1])
    legend.iloc[
        1] = "Der Aufwand bei {} überwiegt den Nutzen. Somit stellt die Einführung des neuen Geschäftsmodells eine Verschlechterung dar.".format(
        bm_to_plot[1])

    st.table(legend)

    # col1, col2 = st.columns(2)
    #
    # with col1:
    #     st.markdown("{} hat einen **höheren Wert** als {} 🔼".format(bm_to_plot[1], uc[9:]))
    #     st.markdown("")
    #     st.markdown("")
    #     st.markdown("{} hat einen **niedrigern Wert** als {} 🔽".format(bm_to_plot[1], uc[9:]))
    #
    # with col2:
    #     st.markdown("Der Nutzen bei {} überwiegt den Aufwand. Somit stellt die Einführung des neuen Geschäftsmodells eine Verbesserung dar.".format(bm_to_plot[1]))
    #     st.markdown("Der Aufwand bei {} überwiegt den Nutzen. Somit stellt die Einführung des neuen Geschäftsmodells eine Verschlechterung dar.".format(bm_to_plot[1]))

with tab3_2:
    bm_elements_description = total_text.loc[
        ["Wirtschaftlichkeit", "Organisation", "Regulatorik", "Technik", "Strategie",
         "Umwelt", "Gesellschaft"], "Text1"]
    for ele in bm_elements_description.index:
        bsp_text = bm_elements_description.loc[ele]
        st.write("**" + ele + "**")
        st.write(bsp_text)
with tab3_3:
    st.write("{}".format(total_text.loc["Assumptions"].iloc[0]))

st.header("Änderungen durch die Implementierung der neuen Geschäftsmodelle")

for b in new_bm:
    st.subheader("Geschäftsmodell {}".format(b))
    text_table = text.loc[:, "Text_" + b]
    text_table.name = "Änderung gegenüber " + uc[9:]
    st.table(text_table)

st.header("Daten")
st.write(
    "[Datenquelle](https://docs.google.com/spreadsheets/d/1ZRFcyil83dX7jwTFI37AS8zjvrwBinAMwQ8ZMkQnu8s/edit?usp=sharing)")
if st.checkbox("Ergebnisse der quantitative Bewertung der Geschäftsmodelle anzeigen", False):
    st.table(data)

st.header("Autoren")
from PIL import Image

# decide if
# if st.checkbox(label="Zoom in", value=True):
if st.button(label="🔍 Zoom in"):
    image1 = Image.open('authors1.PNG')
    image2 = Image.open('authors2.PNG')
    st.image(image1, caption=None)
    st.image(image2, caption='Arbeitsgruppe 9 - YEP 3. Zyklus')
else:
    image = Image.open('authors.PNG')
    st.image(image, caption='Arbeitsgruppe 9 - YEP 3. Zyklus')
