import streamlit as st
import pickle as pkl
import pandas as pd

model          = pkl.load(open('model.pkl',       'rb'))
encoder        = pkl.load(open('encoder.pkl',     'rb'))
featureEncoder = pkl.load(open('feature11.pkl',   'rb'))
numCols        = pkl.load(open('numCols.pkl',     'rb'))
bounds         = pkl.load(open('bounds.pkl',      'rb'))

st.set_page_config(page_title="Weather Prediction", layout="wide")

st.markdown("""
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }

header[data-testid="stHeader"]      { display: none !important; }
footer                               { display: none !important; }
[data-testid="stToolbar"]           { display: none !important; }
[data-testid="stDecoration"]        { display: none !important; }
[data-testid="stStatusWidget"]      { display: none !important; }

.block-container {
    padding: 2rem 4rem !important;
    margin: 0 auto !important;
    max-width: 900px !important;
    width: 100% !important;
}

div.stButton > button {
    background-color: #e5322d !important;
    color: white !important;
    border-radius: 8px !important;
}

div.stButton > button:hover {
    background-color: #CC4422 !important;
}

/* Tab text */
button[data-baseweb="tab"] {
    font-size: 20px !important;
    font-weight: 600 !important;
    color: #888888 !important;
    width: 150px !important;
    # margin:30px !important;

}

/* Active tab text */
button[data-baseweb="tab"][aria-selected="true"] {
    color: #FF5733 !important;
    font-family:poppins !important;
    font-size: 15px !important;
}
button[data-testid="stTab"] p {
    font-size: 20px !important;
    font-family: 'Poppins', sans-serif !important;
    color: #888888 !important;
}

button[data-testid="stTab"][aria-selected="true"] p {
    color: #FF5733 !important;
}
/* Tab hover */
button[data-baseweb="tab"]:hover {
    color: #FF5733 !important;
}
</style>
""", unsafe_allow_html=True)

# Month label → int mapping (string shown to user, int sent to model)
MONTH_MAP = {
    "Jan":1,"Feb":2,"Mar":3,"Apr":4, "May":5, "Jun":6,
    "Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12
}

st.markdown("<h1 style='text-align:center; margin-bottom:1.5rem;'>Weather Prediction Model</h1>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Manual Input", "Batch Prediction", "Dashboard"])


with tab1:
    st.subheader("Manual Input")

    precipitation = st.slider("Precipitation",  min_value=0.0,  max_value=50.0, step=0.1)
    tempMax       = st.slider("Temp Max (°C)",  min_value=0.0,  max_value=50.0, step=0.1)
    tempMin       = st.slider("Temp Min (°C)",  min_value=-0.5, max_value=30.0, step=0.1)
    windSpeed     = st.slider("Wind Speed",     min_value=0.0,  max_value=9.9,  step=0.1)

    year  = st.select_slider("Year",  options=list(range(2012, 2017)))
    month = st.select_slider("Month", options=list(MONTH_MAP.keys()))
    day   = st.select_slider("Day",   options=list(range(1, 32)))

    if st.button("Predict", use_container_width=True):
        dataWeather = pd.DataFrame({
            "precipitation": [precipitation],
            "temp_max":      [tempMax],
            "temp_min":      [tempMin],
            "wind":          [windSpeed],
            "Year":          [year],
            "Month":         [MONTH_MAP[month]],
            "Day":           [day],
        })
        for col in numCols:
            dataWeather[col] = dataWeather[col].clip(lower=bounds[col]['lower'], upper=bounds[col]['upper'])
        predict     = model.predict(dataWeather)
        target      = encoder.inverse_transform(predict)
        dataWeather["Predicted Weather"] = target
        dataWeather["Month"] = month
        st.success("Prediction complete!")
        st.dataframe(dataWeather, use_container_width=True)

with tab2:
    st.subheader("Batch Prediction via CSV Upload")

    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if st.button("Predict from File", use_container_width=True):
        if uploaded_file is not None:
            dataWeather = pd.read_csv(uploaded_file)
            if dataWeather["Month"].dtype == object:
                dataWeather["Month"] = dataWeather["Month"].map(MONTH_MAP)
            for col in numCols:
                dataWeather[col] = dataWeather[col].clip(lower=bounds[col]['lower'], upper=bounds[col]['upper'])
            predict     = model.predict(dataWeather)
            target      = encoder.inverse_transform(predict)
            dataWeather["Predicted Weather"] = target
            st.dataframe(dataWeather, use_container_width=True)
        else:
            st.warning("Please upload a CSV file before predicting.")

with tab3:
    st.subheader("Dashboard")
    st.markdown("""
    COMING SOON
    """)