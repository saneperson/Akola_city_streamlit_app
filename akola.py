import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import datetime

DATA_URL=("Corona Akola Location.csv")


st.title("🦠 Covid-19 🦠 Dashboard: Akola City")
st.markdown("This is a Streamlit-powered dashboard, can be used to study the spread of Corona Virus in the city of Akola. The dashboard is still under research and development. Advancements will be upgraded in the earliest time possible.")
st.markdown("*Disclaimer: The presented data does not give accurate location of infected people, but rather gives precise areas around which infected people were detected. Currently, we have the data from 16th of May. We are striving to get all the data of the city, as soon as possible. Current data is extracted from local media reports from **Yash News Network**.*")
@st.cache(persist=True)
def load_data(nrows):
    mydateparser = lambda x: pd.datetime.strptime(x, "%d-%m-%Y")
    data = pd.read_csv(DATA_URL, nrows=nrows, parse_dates=['Date'], date_parser=mydateparser)
    data=data.loc[data['Status']=='Infected']
    data.dropna(subset=['Latitude', 'Longitude'], inplace=True)
    lowercase = lambda x: str(x).lower() 
    data.rename(lowercase, axis="columns", inplace=True)
    data.reset_index(drop=True, inplace=True)
    #data = data[['date/time', 'latitude', 'longitude']]
    return data


data=load_data(835)
data[['latitude','longitude']].to_csv('lat_long.csv', index=False)

st.header("Where have been Covid-19 patients detected in Akola city?")
st.markdown("The following map shows probable locations of Infected People. If you have trouble finding your area in the map, check 'Point my area', and select your area from the dropdown menu appeared.")
choose1=  st.checkbox("Point my area")
if choose1:
    area = st.selectbox("Select Area", data["location"].unique())
    data1 = data.loc[data.location==area]
    data1.reset_index(drop=True, inplace=True)
else:
    st.markdown("Use the slider to see the spread Covid-19 in the past.")
    time=st.slider("Travel back in time =))", 0, 32)
    date1 = data.date[0]
    date2= date1 + datetime.timedelta(days=time)
    date_disp = date1 + datetime.timedelta(days=(32-time))
    st.write(date_disp)
    data1= data.loc[data['date']>=date2]
    data1.reset_index(drop=True, inplace=True)

midpoint = (np.average(data["latitude"]), np.average(data["longitude"]))
st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/dark-v9",
    initial_view_state={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch":40.5,
    },
    layers=[
        pdk.Layer(
        'HexagonLayer',
        data=data1[['location','latitude', 'longitude']],
        get_position=["longitude", "latitude"],
        auto_highlight=True,
        elevation_scale=5,
        pickable=True,
        radius=100,
        elevation_range=[0, 1000],
        extruded=True,
        coverage=1
        )
    ],
    tooltip={
        'text': 'Infection: {elevationValue}',
        'style': {
            'color': 'white'
        }
    }
))

st.markdown("### Cluster Map")
st.map(data[["latitude", "longitude"]].dropna(how="any"))
choose2=  st.checkbox("Show Raw Data")
if choose2:
    st.write(data)

st.header("Cumulative Infected/Recovered/Dead/Active Plot")
data_case = pd.read_csv('Corona Akola-cases.csv')
data_case.dropna(how='all', inplace=True)
data_case.dropna(axis=1, inplace=True)
data_case['Date'] = data_case['Date'].apply(pd.to_datetime, format = "%d-%m-%Y")
data_case.set_index('Date', drop=True, inplace=True)

st.line_chart(data_case)

st.header("Infections Detected per Day ")
infected=data_case.Infected-data_case.Infected.shift()
st.line_chart(infected)

st.markdown("#### Stay safe, stay home 🧴🤲😷")
st.markdown("Suggestions are always welcome. Mail me here : [:email:](sawadekarkamlesh@gmail.com)")
st.markdown("You can find me here: [LinkedIn](https://www.linkedin.com/in/kamlesh-sawadekar-298140171/)[ Facebook](https://www.facebook.com/kamlesh.sawadekar.5)")