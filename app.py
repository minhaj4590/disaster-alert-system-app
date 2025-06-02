import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import pydeck as pdk
from datetime import datetime
from streamlit_option_menu import option_menu
import folium
from streamlit_folium import st_folium


# innit firebase
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "disaster-alert-system-2b695",
  "private_key_id": "cfd31ff32e91bc2395b61f17f910394dbd716935",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCtXZyBLkPpIKoI\n0ffqgyHAckstuufQsqDjxUPFuMPP0oM9kfxJQ4yu476hHdcojts8vmPAqV7QXzM7\nRV8C9Nm4OUx1Ubm03AboF5Y2jCvq0HWwUkO4K8AZ8C+6syfK6MiOiz6IH/+r+u4E\n4hZoP9PWleMtw1AP0j58B/al07ul6n5XkKWMH5GQx399ch++6MyYePopInmjsGNU\ntwA3NhR0FQ/5hyyL/u8/WwxfNBuLZs3OzGJ2amovYQnkPKfdJvVKLkzz8VXeE/hl\nC6ohR8Iha2AGzI98iOA5lhlwh80vh3xeJ3emVBh4GoV0557mjjrmjr/WzxBXbCmj\nWSwjlgINAgMBAAECggEAIMTOdb5seK7DZPpnHW0e3pTb7+9hrNluvs7FEiTr4ibc\nxrEG2kRJ3a7Pk/2jcxeZigBEs6Bv+vvbn6rrnA/y7TbrZEuHyg9CwPDgZDwXewFf\nFW5fPXsLivuS0fvWHCzm58abEbjWp0e9YK/pY1gZLvjS4Y4G3o6zX9dTgCGm2OPL\nJzhS0ASsAZOsBaYklJmYTsohO89PxlFt4umGBJLGC0OhNU/gvgaMbBOSHnGuMWWP\nvy2h8qBxR9JCeMTQv8y7JBr71zRzy3LAQ/1ae3enKo9+1/D/hjqnGAfrF3xe5Xwy\nOz4blS0kcQ9EHy2zw7cNqWoqhk8Ja5M6+P1MGhuiAQKBgQDvRm46hP6Ovkd9y5Pi\nKygoHsKH5OX5YB2Lh7BE905fVEok0cAgNJGUusG14+s2d4FS8YWuov3UHW8DqZqf\nNutn3XF1334JRpdvkSfwbU/1jYFiPpR8/l/6E6hyqa27ksz8ekyB9T6+jf3b8Rdt\neL50XT6nRwJoG7zqIydrL3sZDQKBgQC5e81tsnClnQ3YeuyWnJAcPL0sMyJgockg\n2R4lv/S23qO3O7fraYju9Y83wD2w56KKMY36ExaI8RXs6aBr5TkVhid89kBWPAc1\njzbIWTsq4fSwHt/0AXpoy3ZyjkeJ+/nl+zi28aOqR8a6rdyim6RpFd2oxQC1xwL3\nCo7U21pNAQKBgQCOoiJ1WfBQ8Ra241MtgGJ4wBVgYs/Af049bc5i3jVm2F02Y56u\n1AdwbH+qyMne9xAtfHIfL2Q2PLF/smvMuzVK/hNzm52LM/xz8kinptICY68b/IgR\nlqVp8qv4ZjN9XD47xz+yPJqBhy0sHiTECjUmMqt1lfvWSaqsu/X0jCJKRQKBgC+Z\nN6R48DNv1EfDc8dKsiis5ZbcIGxP2D9XuEbTtcbf5390EcSVtpAr7+7MpIgrSSjR\ngq+0CkpmI8xCP+qwTi/Z13RX9Tar/OWftN1BGM/uYE55/dquLm2KGQFYxb8BLKX6\nDBnWdLuT48mwKDiKXGyjMdjHhWEgiwA+c1zoVYoBAoGBANd78WMtGG9p+l9hdpVi\nnxY67Lw8dOYvnO4BDdcejD4UliV83uDeauTjXeUqsII8SlTG1hIBEeFFLflB8XUa\n0rydMdnNcuVVe92YeKEwQerohVznyGMz/962cmI/fnzcya8OlBomumDUcedBNAeW\nV+xiQHTvbYhCKkphEquy7vXo\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@disaster-alert-system-2b695.iam.gserviceaccount.com",
  "client_id": "100804845813075149982",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40disaster-alert-system-2b695.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
)
#     firebase_admin.initialize_app(cred)

# db = firestore.client()

# # Fetch and prepare data
# disasters_ref = db.collection('disasters')
# data = [doc.to_dict() for doc in disasters_ref.stream()]
# df = pd.DataFrame(data)




# -------------- Page Config & Logo --------------
st.set_page_config(page_title="🌍 Disaster Alert System", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
body {
    background: linear-gradient(-45deg, #1e3c72, #2a5298, #0f2027, #2c5364);
    background-size: 600% 600%;
    animation: gradientBG 15s ease infinite;
    color: white;
}
@keyframes gradientBG {
    0% { background-position: 0% 50% }
    50% { background-position: 100% 50% }
    100% { background-position: 0% 50% }
}
.css-1d391kg {background: rgba(255,255,255,0.05) !important; border-radius: 15px;}
[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(15px);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
}
[data-testid="collapsedControl"] {
    visibility: visible;
}
h1, h2, h3, h4 {
    color: #ffffff;
}
.logo {
    font-size: 36px;
    font-weight: 700;
    text-align: center;
    margin-top: -40px;
    margin-bottom: 20px;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="logo">🌍 Disaster Alert System ®</div>', unsafe_allow_html=True)

# -------------- Dummy Data --------------
# np.random.seed(42)
# dates = pd.date_range("2023-01-01", "2023-12-31")
# locations = ['California', 'Tokyo', 'Jakarta', 'Istanbul', 'Mexico City']
# disaster_types = ['Earthquake', 'Flood', 'Hurricane', 'Wildfire', 'Tornado']
# data = {
#     "Date": np.random.choice(dates, 300),
#     "Location": np.random.choice(locations, 300),
#     "Disaster Type": np.random.choice(disaster_types, 300),
#     "Magnitude": np.random.uniform(3, 9, 300).round(2),
#     "Latitude": np.random.uniform(-90, 90, 300),
#     "Longitude": np.random.uniform(-180, 180, 300)
# }
# df = pd.DataFrame(data)

# -------------- Real Firestore Data --------------
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import streamlit as st

@st.cache_data
def get_dummy_data():
    return pd.DataFrame([
        {
            'alert_level': 'Green',
            'country': 'Mexico',
            'description': 'From 28/05/2025 to 31/05/2025, a Tropical Depression (max wind 93 km/h) ALVIN-25 was active in EastPacific.',
            'event_id': '1001163',
            'event_name': 'ALVIN-25',
            'event_type': 'TC',
            'from_date': '2025-05-28 21:00:00',
            'iso3': 'MEX',
            'latitude': 23.6585116,
            'link': 'https://www.gdacs.org/report.aspx?eventtype=TC&eventid=1001163',
            'longitude': -102.0077097,
            'population_exposed': 'Unknown',
            'pub_date': '2025-05-28 20:50:38',
            'severity': 92.592,
            'title': 'Green alert for tropical cyclone ALVIN-25',
            'to_date': '2025-05-31 15:00:00'
        },
        # Add 3–4 more records here as needed...
        {
            'alert_level': 'Orange',
            'country': 'India',
            'description': 'Severe flood in Bihar region. Thousands affected.',
            'event_id': '2002456',
            'event_name': 'Bihar Floods',
            'event_type': 'FL',
            'from_date': '2025-06-01 10:00:00',
            'iso3': 'IND',
            'latitude': 25.0961,
            'longitude': 85.3131,
            'link': 'https://www.gdacs.org/report.aspx?eventtype=FL&eventid=2002456',
            'population_exposed': '50000',
            'pub_date': '2025-06-01 09:50:00',
            'severity': 75.0,
            'title': 'Orange alert for floods in Bihar, India.',
            'to_date': '2025-06-05 18:00:00'
        },
        {
            'alert_level': 'Red',
            'country': 'Japan',
            'description': 'Strong earthquake recorded near Tokyo.',
            'event_id': '3003749',
            'event_name': 'Tokyo Quake',
            'event_type': 'EQ',
            'from_date': '2025-05-30 03:00:00',
            'iso3': 'JPN',
            'latitude': 35.6762,
            'longitude': 139.6503,
            'link': 'https://www.gdacs.org/report.aspx?eventtype=EQ&eventid=3003749',
            'population_exposed': '120000',
            'pub_date': '2025-05-30 02:45:00',
            'severity': 95.3,
            'title': 'Red alert: Tokyo hit by earthquake.',
            'to_date': '2025-05-30 03:30:00'
        },
        {
            'alert_level': 'Yellow',
            'country': 'USA',
            'description': 'Wildfire spreads in California forests.',
            'event_id': '4004890',
            'event_name': 'CA Wildfire',
            'event_type': 'WF',
            'from_date': '2025-06-02 14:00:00',
            'iso3': 'USA',
            'latitude': 36.7783,
            'longitude': -119.4179,
            'link': 'https://www.gdacs.org/report.aspx?eventtype=WF&eventid=4004890',
            'population_exposed': 'Unknown',
            'pub_date': '2025-06-02 13:50:00',
            'severity': 88.4,
            'title': 'Wildfire alert in California.',
            'to_date': '2025-06-10 20:00:00'
        },
        {
            'alert_level': 'Purple',
            'country': 'USA',
            'description': 'Tornado warning issued for Oklahoma.',
            'event_id': '5005922',
            'event_name': 'OK Tornado',
            'event_type': 'TR',
            'from_date': '2025-06-01 17:00:00',
            'iso3': 'USA',
            'latitude': 35.4676,
            'longitude': -97.5164,
            'link': 'https://www.gdacs.org/report.aspx?eventtype=TR&eventid=5005922',
            'population_exposed': '15000',
            'pub_date': '2025-06-01 16:55:00',
            'severity': 70.2,
            'title': 'Tornado alert for Oklahoma.',
            'to_date': '2025-06-02 00:00:00'
        }
    ])

@st.cache_data
def fetch_data_safely():
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "disaster-alert-system-2b695",
  "private_key_id": "cfd31ff32e91bc2395b61f17f910394dbd716935",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCtXZyBLkPpIKoI\n0ffqgyHAckstuufQsqDjxUPFuMPP0oM9kfxJQ4yu476hHdcojts8vmPAqV7QXzM7\nRV8C9Nm4OUx1Ubm03AboF5Y2jCvq0HWwUkO4K8AZ8C+6syfK6MiOiz6IH/+r+u4E\n4hZoP9PWleMtw1AP0j58B/al07ul6n5XkKWMH5GQx399ch++6MyYePopInmjsGNU\ntwA3NhR0FQ/5hyyL/u8/WwxfNBuLZs3OzGJ2amovYQnkPKfdJvVKLkzz8VXeE/hl\nC6ohR8Iha2AGzI98iOA5lhlwh80vh3xeJ3emVBh4GoV0557mjjrmjr/WzxBXbCmj\nWSwjlgINAgMBAAECggEAIMTOdb5seK7DZPpnHW0e3pTb7+9hrNluvs7FEiTr4ibc\nxrEG2kRJ3a7Pk/2jcxeZigBEs6Bv+vvbn6rrnA/y7TbrZEuHyg9CwPDgZDwXewFf\nFW5fPXsLivuS0fvWHCzm58abEbjWp0e9YK/pY1gZLvjS4Y4G3o6zX9dTgCGm2OPL\nJzhS0ASsAZOsBaYklJmYTsohO89PxlFt4umGBJLGC0OhNU/gvgaMbBOSHnGuMWWP\nvy2h8qBxR9JCeMTQv8y7JBr71zRzy3LAQ/1ae3enKo9+1/D/hjqnGAfrF3xe5Xwy\nOz4blS0kcQ9EHy2zw7cNqWoqhk8Ja5M6+P1MGhuiAQKBgQDvRm46hP6Ovkd9y5Pi\nKygoHsKH5OX5YB2Lh7BE905fVEok0cAgNJGUusG14+s2d4FS8YWuov3UHW8DqZqf\nNutn3XF1334JRpdvkSfwbU/1jYFiPpR8/l/6E6hyqa27ksz8ekyB9T6+jf3b8Rdt\neL50XT6nRwJoG7zqIydrL3sZDQKBgQC5e81tsnClnQ3YeuyWnJAcPL0sMyJgockg\n2R4lv/S23qO3O7fraYju9Y83wD2w56KKMY36ExaI8RXs6aBr5TkVhid89kBWPAc1\njzbIWTsq4fSwHt/0AXpoy3ZyjkeJ+/nl+zi28aOqR8a6rdyim6RpFd2oxQC1xwL3\nCo7U21pNAQKBgQCOoiJ1WfBQ8Ra241MtgGJ4wBVgYs/Af049bc5i3jVm2F02Y56u\n1AdwbH+qyMne9xAtfHIfL2Q2PLF/smvMuzVK/hNzm52LM/xz8kinptICY68b/IgR\nlqVp8qv4ZjN9XD47xz+yPJqBhy0sHiTECjUmMqt1lfvWSaqsu/X0jCJKRQKBgC+Z\nN6R48DNv1EfDc8dKsiis5ZbcIGxP2D9XuEbTtcbf5390EcSVtpAr7+7MpIgrSSjR\ngq+0CkpmI8xCP+qwTi/Z13RX9Tar/OWftN1BGM/uYE55/dquLm2KGQFYxb8BLKX6\nDBnWdLuT48mwKDiKXGyjMdjHhWEgiwA+c1zoVYoBAoGBANd78WMtGG9p+l9hdpVi\nnxY67Lw8dOYvnO4BDdcejD4UliV83uDeauTjXeUqsII8SlTG1hIBEeFFLflB8XUa\n0rydMdnNcuVVe92YeKEwQerohVznyGMz/962cmI/fnzcya8OlBomumDUcedBNAeW\nV+xiQHTvbYhCKkphEquy7vXo\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@disaster-alert-system-2b695.iam.gserviceaccount.com",
  "client_id": "100804845813075149982",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40disaster-alert-system-2b695.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
)
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        docs = db.collection('disasters').stream()
        records = []
        for doc in docs:
            data = doc.to_dict()
            if 'Date' in data and hasattr(data['Date'], 'to_pydatetime'):
                data['Date'] = data['Date'].to_pydatetime()
            records.append(data)

        df = pd.DataFrame(records)
        if df.empty:
            st.warning("✅ Connected to Firebase, but no data found.")
            return get_dummy_data()
        return df

    except Exception as e:
        st.warning("⚠️ Firebase unavailable or quota exceeded. Showing dummy data.")
        print("Firebase error:", e)
        return get_dummy_data()

# Fetch data
df = fetch_data_safely()

# Ensure proper datetime conversion
df['to_date'] = pd.to_datetime(df['to_date'], errors='coerce')
df['from_date'] = pd.to_datetime(df['from_date'], errors='coerce')
df['pub_date'] = pd.to_datetime(df['pub_date'], errors='coerce')


# Data Cleaning
df['from_date'] = pd.to_datetime(df['from_date'], errors='coerce')
df['to_date'] = pd.to_datetime(df['to_date'], errors='coerce')
df['pub_date'] = pd.to_datetime(df['pub_date'], errors='coerce')
df['population_exposed'] = pd.to_numeric(df['population_exposed'], errors='coerce')
df['month'] = df['from_date'].dt.to_period('M').astype(str)

# -------------- Sidebar --------------
with st.sidebar:
    st.header("⚙️ Settings")

    # Disaster Type filter
    disaster_types = df['event_type'].dropna().unique()
    selected_disaster = st.multiselect("Disaster Type", disaster_types, default=disaster_types)

    # Country filter
    countries = df['country'].dropna().unique()
    selected_countries = st.multiselect("Country", countries, default=countries)

    # Date range slider (only valid dates selectable)
    min_date = df['from_date'].min().date()
    max_date = df['to_date'].max().date()
    selected_date_range = st.slider(
        "Date Range",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="YYYY-MM-DD"
    )

    # st.radio("🌓 Theme Mode", ["Dark Glass", "Light"], index=0)
    st.markdown("---")
    st.caption("Made with ❤️ in Streamlit")

# -------------- Filtering --------------
filtered_df = df[
    (df['event_type'].isin(selected_disaster)) &
    (df['country'].isin(selected_countries)) &
    (df['from_date'].dt.date >= selected_date_range[0]) &
    (df['to_date'].dt.date <= selected_date_range[1])
]



# -------------- Navigation Tabs --------------
tabs = option_menu(
    menu_title=None,
    options=["Dashboard", "Forecast Report", "Map View", "Subscribe"],
    icons=["bar-chart", "graph-up", "map", "envelope-open"],
    orientation="horizontal"
)

# -------------- Dashboard --------------
if tabs == "Dashboard":
    st.title("📊 Real-time Disaster Dashboard")
    kpi1, kpi2, kpi3 = st.columns(3)

    kpi1.metric("Total Alerts", len(filtered_df))
    kpi2.metric("Avg. Severity", f"{filtered_df['severity'].mean():.2f}")
    total_population = pd.to_numeric(filtered_df['population_exposed'], errors='coerce').sum()
    kpi3.metric("Total Population Exposed", f"{total_population:.2f}")


    st.subheader("📍 Disaster Counts by Country")
    loc_counts = filtered_df["country"].value_counts().reset_index()
    loc_counts.columns = ["country", "count"]
    loc_chart = px.bar(
        loc_counts,
        x="country", y="count", color="country", title="Alerts by Country"
    )
    st.plotly_chart(loc_chart, use_container_width=True)

    col4, col5 = st.columns(2)
    with col4:
        st.subheader("Disaster Distribution by Event Type")
        pie = px.pie(filtered_df, names="event_type", title="Disasters by Type")
        st.plotly_chart(pie, use_container_width=True)

    with col5:
        st.subheader("Disaster Severity Over Time")
        # Convert from_date to datetime for sorting & plotting
        filtered_df['from_date_dt'] = pd.to_datetime(filtered_df['from_date'])
        line = px.line(
            filtered_df.sort_values("from_date_dt"),
            x="from_date_dt",
            y="severity",
            color="event_type",
            markers=True,
            title="Severity Over Time by Disaster Type"
        )
        st.plotly_chart(line, use_container_width=True)

elif tabs == "Forecast Report":
    st.title("📊 Forecast Report")
    st.markdown("This report provides a 12-month forecast for various disaster types using SARIMA modeling.")

    # Load forecast data
    url = "https://raw.githubusercontent.com/minhaj4590/disaster-forecasting/main/forecast_sarima.csv"
    forecast_df = pd.read_csv(url, index_col=0, parse_dates=True)

    st.subheader("📈 Forecasted Trends by Disaster Type")

    # Multi-line plot using Plotly
    fig = px.line(
        forecast_df,
        x=forecast_df.index,
        y=forecast_df.columns,
        labels={"value": "Forecasted Count", "index": "Date", "variable": "Disaster Type"},
        title="Disaster Type Forecasts (Next 12 Months)"
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Forecasted Count",
        legend_title="Disaster Type",
        height=500,
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📋 Forecast Summary Table")
    st.dataframe(forecast_df.round(2))

    st.markdown("---")
    st.markdown("**Note:** Forecasts are generated using SARIMA models trained on monthly disaster counts per type.")

elif tabs == "Map View":
    st.title("🗺️ Global Disaster Events Map")

    st.markdown("""
    <style>
        .stApp {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
        }

        .block-container {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            height: auto !important;
            margin-top: 0 !important;
        }

        .element-container, iframe, .st_folium {
            height: 100% !important;
            max-height: 650px !important;
            width: 100% !important;
            margin-top: 0 !important;
            padding-top: 0 !important;
        }

        h1 {
            margin-top: 0 !important;
            padding-top: 0 !important;
        }

        /* Positioning for the legend */
        .folium-legend {
            position: absolute !important;
            top: 10px !important;
            right: 10px !important;
            z-index: 9999 !important;
            background-color: rgba(0, 0, 0, 0.7) !important;
            color: white !important;
            padding: 10px !important;
            font-size: 13px !important;
            border-radius: 8px !important;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.3) !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- Reload Functionality ---
    # if st.button("Reload Map"):
    #     st.experimental_rerun()

    # --- Map setup ---
    icon_urls = {
        "TC": "https://cdn-icons-png.flaticon.com/128/594/594869.png",
        "FL": "https://cdn-icons-png.flaticon.com/128/17990/17990803.png",
        "EQ": "https://cdn-icons-png.flaticon.com/128/18153/18153578.png",
        "WF": "https://cdn-icons-png.flaticon.com/128/1453/1453025.png",
        "TR": "https://cdn-icons-png.flaticon.com/128/6631/6631648.png",
    }
    default_icon_url = "https://cdn-icons-png.flaticon.com/512/252/252000.png"

    filtered_df_clean = filtered_df.dropna(subset=["latitude", "longitude"])
    max_rows = 300
    filtered_df_sample = filtered_df_clean.head(max_rows)

    if not filtered_df_sample.empty:
        avg_lat = filtered_df_sample["latitude"].mean()
        avg_lon = filtered_df_sample["longitude"].mean()
        m = folium.Map(location=[avg_lat, avg_lon], zoom_start=2, tiles="CartoDB Dark_Matter")
    else:
        m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB Dark_Matter")

    bounds = []
    for _, row in filtered_df_sample.iterrows():
        icon_url = icon_urls.get(row["event_type"], default_icon_url)
        popup_html = (
            f"<b>Event:</b> {row['event_type']}<br>"
            f"<b>Country:</b> {row['country']}<br>"
            f"<b>Severity:</b> {row['severity']}<br>"
            f"<b>Population:</b> {row.get('population_exposed', 'N/A')}"
        )
        location = [row["latitude"], row["longitude"]]
        folium.Marker(
            location=location,
            popup=popup_html,
            icon=folium.CustomIcon(icon_url, icon_size=(28, 28))
        ).add_to(m)
        bounds.append(location)

    if bounds:
        m.fit_bounds(bounds, padding=(30, 30))

    # --- Legend HTML added to map ---
    legend_html = """
    <div class="folium-legend">
        <b>🌍 Disaster Legend</b><br>
        <img src="https://cdn-icons-png.flaticon.com/128/594/594869.png" width="18"> Tropical Cyclone<br>
        <img src="https://cdn-icons-png.flaticon.com/128/17990/17990803.png" width="18"> Flood<br>
        <img src="https://cdn-icons-png.flaticon.com/128/18153/18153578.png" width="18"> Earthquake<br>
        <img src="https://cdn-icons-png.flaticon.com/128/1453/1453025.png" width="18"> Wildfire<br>
        <img src="https://cdn-icons-png.flaticon.com/128/6631/6631648.png" width="18"> Tornado<br>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    # --- Display the map ---
    st_folium(m, width=None, height=650)

    # --- Summary Section ---
    st.subheader("Summary of Displayed Disasters")
    total_events = len(filtered_df_sample)
    events_by_type = filtered_df_sample['event_type'].value_counts()

    summary_text = f"🌍 *Total events displayed: {total_events}*\n\n"

    for event_type, count in events_by_type.items():
        top_countries = (
            filtered_df_sample[filtered_df_sample["event_type"] == event_type]["country"]
            .value_counts()
            .head(5)
            .index.tolist()
        )
        country_str = ", ".join(top_countries)
        event_name = {
            "EQ": "Earthquake",
            "FL": "Flood",
            "TC": "Tropical Cyclone",
            "WF": "Wildfire",
            "TR": "Tornado"
        }.get(event_type, event_type)
        summary_text += f"- *{event_name}* — {count} events in {country_str}\n"

    st.markdown(summary_text)
    st.caption("Zoom or hover over markers to view event details.")



    #st.markdown("---")



# -------------- Subscribe Tab --------------
# GitHub token & repo info
TOKEN = st.secrets["GITHUB_TOKEN"]
REPO = "minhaj4590/disaster-forecasting"
FILE_PATH = "subscribers.csv"

# sending data to Github
from github import Github
import pandas as pd
from io import StringIO

def append_to_github_csv(new_data: dict):
    g = Github(TOKEN)
    repo = g.get_repo(REPO)
    try:
        contents = repo.get_contents(FILE_PATH)
        csv_str = contents.decoded_content.decode()
        df = pd.read_csv(StringIO(csv_str))
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        updated_csv = df.to_csv(index=False)
        repo.update_file(contents.path, "Update subscriber list", updated_csv, contents.sha)
    except Exception as e:
        # File doesn't exist or any other error: create new file
        df = pd.DataFrame([new_data])
        updated_csv = df.to_csv(index=False)
        repo.create_file(FILE_PATH, "Create subscriber list", updated_csv)

# ---- Inside your Subscribe tab form ----
if tabs == "Subscribe":
    st.title("📬 Subscribe to Alerts")
    with st.form("subscribe_form"):
        name = st.text_input("Name")
        phone = st.text_input("Phone Number")
        email = st.text_input("Email")
        country = st.text_input("Country")  # Changed from city to country
        preferred_alerts = st.multiselect("Preferred Alerts", df["event_type"].unique())
        submitted = st.form_submit_button("Subscribe")
        
        if submitted:
            new_data = {
                "name": name,
                "phone": phone,
                "email": email,
                "country": country,  # changed here too
                "preferred_alerts": ",".join(preferred_alerts)
            }
            append_to_github_csv(new_data)
            st.success("Subscription data saved to GitHub successfully!")





# sending alerts to subscribers

from datetime import datetime

# Filter disasters for today
today = pd.to_datetime(datetime.now().date())
todays_disasters = df[
    (df['from_date'].dt.date == today.date()) &
    (df['event_type'].notna()) &
    (df['country'].notna())
]


# load subscribers from GitHub

# GitHub setup
g = Github(TOKEN)
repo = g.get_repo("minhaj4590/disaster-forecasting")
contents = repo.get_contents("subscribers.csv")
csv_data = contents.decoded_content.decode()
subs_df = pd.read_csv(StringIO(csv_data))


# Matching subscribers with today's disasters
matches = []

for _, sub in subs_df.iterrows():
    for _, dis in todays_disasters.iterrows():
        if sub['country'].strip().lower() == dis['country'].strip().lower() and \
           sub['preferred_alerts'].strip().lower() in dis['event_type'].strip().lower():
            message = f"""
Hello {sub['name']},
⚠️ Alert: {dis['event_type']} reported in {dis['city']} on {dis['from_date'].date()}.
Population exposed: {dis.get('population_exposed', 'Unknown')}

Stay safe.
- Disaster Alert System
"""
            matches.append({
                'phone': sub['phone'],
                'email': sub['email'],
                'message': message
            })


# Sending alerts via email
import smtplib
from email.message import EmailMessage

def send_email(to_email, subject, body):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = "disaster.alerts.app@gmail.com"
    msg['To'] = to_email
    msg.set_content(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login("disaster.alerts.app@gmail.com", "asvvaaujerqsbvoi")  # Use App Password
        smtp.send_message(msg)


from twilio.rest import Client

def send_whatsapp(to_number, body):
    account_sid = "AC6d28d5c70483dc090932c503950ce03f"
    auth_token = "c029840eabab6bf83f6eee23924d9669"
    client = Client(account_sid, auth_token)

    client.messages.create(
        body=body,
        from_='whatsapp:+14155238886',  # Twilio Sandbox WhatsApp number
        to=f'whatsapp:{to_number}'
    )


# Send alerts to matched subscribers
for match in matches:
    send_email(match['email'], "Disaster Alert", match['message'])
    send_whatsapp(match['phone'], match['message'])


# -------------- Footer --------------
st.markdown("---")
st.write("© 2023 Disaster Alert System ®. All rights reserved.")


