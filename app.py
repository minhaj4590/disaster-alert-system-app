import streamlit as st
import time
import google.generativeai as genai
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
import json

# sending alerts to subscribers

from datetime import datetime
from streamlit_autorefresh import st_autorefresh

import smtplib
from email.message import EmailMessage

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
# Auto-refresh every hour (3600 * 1000 ms)
st_autorefresh(interval=3600 * 1000, key="alert_refresh")

def send_email(to_email, subject, body):
    print(f"Trying to send email to {to_email} with subject: {subject}")
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = "disaster.alerts.app@gmail.com"
    msg['To'] = to_email
    msg.set_content(body)
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("fahadgillani08@gmail.com", "nqgz nnii bpwr qavf")
            smtp.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def send_alert_to_subscriber(subscriber, todays_disasters, today):
    # Normalize subscriber data
    subscriber_country = str(subscriber['country']).strip().lower()
    preferred_list = [a.strip().upper() for a in subscriber['preferred_alerts'].split(',')]

    st.write(f"✅ Normalized Subscriber Country: {subscriber_country}")
    st.write(f"✅ Normalized Subscriber Preferred Alerts: {preferred_list}")
    st.write(f"📊 Number of disasters today: {len(todays_disasters)}")

    for _, dis in todays_disasters.iterrows():
        # Normalize disaster data
        disaster_country = str(dis['country']).strip().lower()
        disaster_type = str(dis['event_type']).strip().upper()

        # Debug print for each comparison
        st.write(f"🔍 Comparing: subscriber_country={subscriber_country} == disaster_country={disaster_country}, "
                 f"disaster_type={disaster_type} in preferred_list={preferred_list}")

        if subscriber_country == disaster_country and disaster_type in preferred_list:
            st.write("✅ Match found, sending email to", subscriber['email'])
            email = subscriber['email']

            # Unique key to avoid duplicate emails per day
            key = f"{email}_{today}"

            if key in st.session_state.get("alerts_sent", {}):
                st.write("⚠️ Alert already sent today to", email)
                return False  # Already sent today

            # Compose message
            message = f"""
            Hello {subscriber['name']},
            ⚠️ Alert: {dis['event_type']} reported in {dis.get('city', 'your area')} on {pd.to_datetime(dis['from_date']).date()}.
            Population exposed: {dis.get('population_exposed', 'Unknown')}

            Stay safe.
            - Disaster Alert System
            """

            send_email(email, "🌍 Disaster Alert Notification", message)

            # Mark as sent
            if "alerts_sent" not in st.session_state:
                st.session_state.alerts_sent = {}
            st.session_state.alerts_sent[key] = True
            return True  # Sent now

    st.write("❌ No matching disasters for this subscriber.")
    return False  # No match found







# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "disaster-alert-system-2b695",
  "private_key_id": "59cebebf8787043a9752f03d90253b61291f614a",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDYMglT66o53I/j\n430mSDU4nYwnbY3zWNAHxRtxUAmN5hOoF5AsAYQHIu5irhgGqCGBzvjg2PI6x+NH\n6pIcSdxjEPCvu2GD2dTOP/1M0B+ZYwHGsKXb8tdiCKsxsgS1USk/c0BVqx+hBANX\nny8rNEpuyqU2oi1norVqYU3FwwULn91Q5MA0/pn8mwt7lgtDUGS0gqgFQdCEcn4f\nLPw6BgffBxWjbzJKobeGVYv4ugRyv3ZfBuGS/B7e4dqUgvyKAzt2gOTR4Z+IzIdM\ni7XqaNvmlDHFWzpWcwKauJJUBNJFRrpBqShGNtbAmLRqpGAwREwsAZDyerg6B9vc\nY6WOyl3HAgMBAAECggEAEU8YPhbNHyrQfl9VQr5fPHQop3N2/PesWCLoyo6s5SZ5\nhmi0i0Fnz6Z1TYNAuy+01w66EE5uPlSIltZp8kfblDbj/j3TVdoX1pd68S5siTxL\nBRxZex2bLucgxa7J/7ZKxiC1EubLdnm6xsYg4aWjG/GvfotHdVeqjKTTtDSj78Us\nD8YCWYVaDs0LH6DW5aI5Yw2wm9q+JG5NvnaKkG5HEuNHqxEnhI0SFN6Zbl47vdNB\nwGmgx5XLKlGarQh9aDEQ63/uG0JI3l6XM5yxNnJY5np4Lp8GiqqYei0HI1ZldLVk\nc4c+ea1jmjczPsT1Hd+DjMqovYoPe4ooL77u0FKmoQKBgQD8nizUcKaEl8QDiAdd\nC+WtfWdctFTnb8ceQXeJJCxkYTezaBT4vFbC16fVmp/lbmH7jUkTpEiE43mBhxRm\nQTXPiP2Ppypi2HrLSLFBkntTyjxPxO9Fh01XpjCRNf1/W6nkL1IuKKnHxTd8IQ34\ncwSWlaVS3Mcj9fj/kxFUTUT2EQKBgQDbFwbbWQVnytq+JgH+c9yKjx6g3eknYHeN\nGwYMh9Svrko1kn/pKiW/Qqxt3hgRD3DFuk3GER6DGBt0lmz0nE61hiKBEYVqnecy\nzuvuBLbFyh1Nh6gnqcR4tn6rkivHqVCq5YRNc8TowAMhdI+6AdEIkFlWhM43ojDt\n2wCEt3jeVwKBgBL45jEGTNtEcqo5OyRX0mYXNv4VZRMEqBWzoQChwNvBGWfV900/\nB90WSTqXpE6c3asAz240NmYUl3mM5ZFQcHQnu7NgQKSv0XkW+okMMUr3s1PiXH4C\nTWK5zof5YBKCld3XV/qzfxzLyQD/kocITF3q20G/5wziWlMHfpOwQe+hAoGAF3RX\nn5PgKERnNoQLIpp0ucConsAi/bwuEEUcWKsR8dzOxP1yBBwm/lq86uYj3W+xuvk+\n6j1a7t3d0pVoBKfXJUe+2eJuTgOphJ7yUwDeMD569JnZPqXGCsY+uU9ksHNH14PK\nrh/+rIwhyasY1+jp3+jUJ5cAHKSYaF5Rp+OcZPECgYAKOCjOpavG8qLhb3o9JjvZ\nJWWUu7ekp2u6dp+WHXUE1CvzoCxf63xcm44Wd7QgTBwW4fVIzAqTVJoitf7zRQyv\nMhErPCKvuifZN26aMLJuU0rwtLnAID73lv0icm8MwOJ1n1Nj29VSv5T9M7MR6Ept\n2316eVoEFVPF9aDvbkZ4aw==\n-----END PRIVATE KEY-----\n",
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

# db = firestore.client()

# # Fetch and prepare data
# disasters_ref = db.collection('disasters')
# data = [doc.to_dict() for doc in disasters_ref.stream()]
# df = pd.DataFrame(data)






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
            'from_date': '2025-06-03 14:00:00',
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
        # Initialize Firebase only if it hasn't been initialized yet
        if not firebase_admin._apps:
            cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "disaster-alert-system-2b695",
  "private_key_id": "59cebebf8787043a9752f03d90253b61291f614a",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDYMglT66o53I/j\n430mSDU4nYwnbY3zWNAHxRtxUAmN5hOoF5AsAYQHIu5irhgGqCGBzvjg2PI6x+NH\n6pIcSdxjEPCvu2GD2dTOP/1M0B+ZYwHGsKXb8tdiCKsxsgS1USk/c0BVqx+hBANX\nny8rNEpuyqU2oi1norVqYU3FwwULn91Q5MA0/pn8mwt7lgtDUGS0gqgFQdCEcn4f\nLPw6BgffBxWjbzJKobeGVYv4ugRyv3ZfBuGS/B7e4dqUgvyKAzt2gOTR4Z+IzIdM\ni7XqaNvmlDHFWzpWcwKauJJUBNJFRrpBqShGNtbAmLRqpGAwREwsAZDyerg6B9vc\nY6WOyl3HAgMBAAECggEAEU8YPhbNHyrQfl9VQr5fPHQop3N2/PesWCLoyo6s5SZ5\nhmi0i0Fnz6Z1TYNAuy+01w66EE5uPlSIltZp8kfblDbj/j3TVdoX1pd68S5siTxL\nBRxZex2bLucgxa7J/7ZKxiC1EubLdnm6xsYg4aWjG/GvfotHdVeqjKTTtDSj78Us\nD8YCWYVaDs0LH6DW5aI5Yw2wm9q+JG5NvnaKkG5HEuNHqxEnhI0SFN6Zbl47vdNB\nwGmgx5XLKlGarQh9aDEQ63/uG0JI3l6XM5yxNnJY5np4Lp8GiqqYei0HI1ZldLVk\nc4c+ea1jmjczPsT1Hd+DjMqovYoPe4ooL77u0FKmoQKBgQD8nizUcKaEl8QDiAdd\nC+WtfWdctFTnb8ceQXeJJCxkYTezaBT4vFbC16fVmp/lbmH7jUkTpEiE43mBhxRm\nQTXPiP2Ppypi2HrLSLFBkntTyjxPxO9Fh01XpjCRNf1/W6nkL1IuKKnHxTd8IQ34\ncwSWlaVS3Mcj9fj/kxFUTUT2EQKBgQDbFwbbWQVnytq+JgH+c9yKjx6g3eknYHeN\nGwYMh9Svrko1kn/pKiW/Qqxt3hgRD3DFuk3GER6DGBt0lmz0nE61hiKBEYVqnecy\nzuvuBLbFyh1Nh6gnqcR4tn6rkivHqVCq5YRNc8TowAMhdI+6AdEIkFlWhM43ojDt\n2wCEt3jeVwKBgBL45jEGTNtEcqo5OyRX0mYXNv4VZRMEqBWzoQChwNvBGWfV900/\nB90WSTqXpE6c3asAz240NmYUl3mM5ZFQcHQnu7NgQKSv0XkW+okMMUr3s1PiXH4C\nTWK5zof5YBKCld3XV/qzfxzLyQD/kocITF3q20G/5wziWlMHfpOwQe+hAoGAF3RX\nn5PgKERnNoQLIpp0ucConsAi/bwuEEUcWKsR8dzOxP1yBBwm/lq86uYj3W+xuvk+\n6j1a7t3d0pVoBKfXJUe+2eJuTgOphJ7yUwDeMD569JnZPqXGCsY+uU9ksHNH14PK\nrh/+rIwhyasY1+jp3+jUJ5cAHKSYaF5Rp+OcZPECgYAKOCjOpavG8qLhb3o9JjvZ\nJWWUu7ekp2u6dp+WHXUE1CvzoCxf63xcm44Wd7QgTBwW4fVIzAqTVJoitf7zRQyv\nMhErPCKvuifZN26aMLJuU0rwtLnAID73lv0icm8MwOJ1n1Nj29VSv5T9M7MR6Ept\n2316eVoEFVPF9aDvbkZ4aw==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@disaster-alert-system-2b695.iam.gserviceaccount.com",
  "client_id": "100804845813075149982",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40disaster-alert-system-2b695.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
)

        # After initialization (or if already initialized), get the Firestore client
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
        print("Firebase error:", e) # Good for debugging
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
    options=["Dashboard", "Forecast Report", "Map View","AlertBot", "Subscribe"],
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


# sending data to Github
from github import Github
import pandas as pd
from io import StringIO

from github import Github
import pandas as pd
from io import StringIO
import re
import streamlit as st

TOKEN = st.secrets["GITHUB_TOKEN"]
REPO = "minhaj4590/disaster-forecasting"
FILE_PATH = "subscribers.csv"

def append_to_github_csv(new_data: dict):
    g = Github(TOKEN)
    repo = g.get_repo(REPO)  # Define repo here
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

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_phone(phone):
    return re.match(r"^\+?\d{10,15}$", phone)  # Adjust regex as needed

# ---- Inside your Subscribe tab form ----
if tabs == "Subscribe":
    st.title("📬 Subscribe or Unsubscribe to Alerts")

    # --- Subscribe Form ---
    st.subheader("Subscribe to Alerts")
    with st.form("subscribe_form"):
        name = st.text_input("Name")
        phone = st.text_input("Phone Number")
        email = st.text_input("Email")
        country = st.text_input("Country")
        preferred_alerts = st.multiselect("Preferred Alerts", df["event_type"].unique())
        submitted_sub = st.form_submit_button("Subscribe")

    if submitted_sub:
        if not name or not phone or not email or not country or not preferred_alerts:
            st.error("All fields must be filled!")
        elif not is_valid_email(email):
            st.error("Please enter a valid email address.")
        elif not is_valid_phone(phone):
            st.error("Please enter a valid phone number.")
        else:
            try:
                g = Github(TOKEN)
                repo = g.get_repo(REPO)
                contents = repo.get_contents(FILE_PATH)
                csv_str = contents.decoded_content.decode()
                subscribers_df = pd.read_csv(StringIO(csv_str))
            except Exception:
                subscribers_df = pd.DataFrame(columns=["name", "phone", "email", "country", "preferred_alerts"])

            # Check for duplicates
            duplicate_email = not subscribers_df[ subscribers_df['email'] == email ].empty
            duplicate_phone = not subscribers_df[ subscribers_df['phone'] == phone ].empty

            if duplicate_email:
                st.error("A user is already subscribed with this email address.")
            elif duplicate_phone:
                st.error("This phone number is already registered for alerts.")
            else:
                new_data = {
                    "name": name,
                    "phone": phone,
                    "email": email,
                    "country": country,
                    "preferred_alerts": ",".join(preferred_alerts)
                }
                append_to_github_csv(new_data)
                st.success("Subscription data saved to GitHub successfully!")

                # --- Send alert if today's disaster matches
                if 'from_date' in df.columns:
                    today = pd.to_datetime("2025-06-01")
                    df['from_date'] = pd.to_datetime(df['from_date'], errors='coerce')
                    todays_disasters = df[df['from_date'].dt.normalize() == today]
                    st.write(todays_disasters)
                else:
                    todays_disasters = pd.DataFrame()
                    st.write("⚠️ No 'from_date' column in the dataframe.")

                # Alert tracking
                if "alerts_sent" not in st.session_state:
                    st.session_state.alerts_sent = {}

                if send_alert_to_subscriber(new_data, todays_disasters, today):
                    st.info("⚠️ Alert email sent to you for today's disaster event(s).")
                else:
                    st.info("You are subscribed successfully, no new alerts to send at this moment.")


    st.markdown("---")  # Divider line


    # --- Unsubscribe Form ---
    st.subheader("Unsubscribe from Alerts")
    with st.form("unsubscribe_form"):
        email_or_phone = st.text_input("Enter your Email or Phone Number to unsubscribe")
        submitted_unsub = st.form_submit_button("Unsubscribe")
    
        if submitted_unsub:
            if not email_or_phone:
                st.error("Please enter an email or phone number.")
            else:
                g = Github(TOKEN)
                repo = g.get_repo(REPO)
                try:
                    contents = repo.get_contents(FILE_PATH)
                    csv_str = contents.decoded_content.decode()
                    df = pd.read_csv(StringIO(csv_str))
    
                    query = email_or_phone.strip().lower()
                    is_email = is_valid_email(query)
                    is_phone = is_valid_phone(query)
    
                    if not is_email and not is_phone:
                        st.error("Please enter a valid email or phone number.")
                    else:
                        if is_email:
                            filtered_df = df[df['email'].str.lower() != query]
                        else:
                            filtered_df = df[df['phone'].str.lower() != query]
    
                        if len(filtered_df) == len(df):
                            st.info("No subscription found with this email or phone number.")
                        else:
                            updated_csv = filtered_df.to_csv(index=False)
                            repo.update_file(contents.path, "Unsubscribe user", updated_csv, contents.sha)
                            st.success("You have been unsubscribed successfully!")
                except Exception as e:
                    st.error("Error accessing subscriber data or updating file.")



# -------------- Footer --------------
st.markdown("---")
st.write("© 2023 Disaster Alert System ®. All rights reserved.")


# -------------- AlertBot Tab --------------
import time
import google.generativeai as genai

if tabs == "AlertBot":

    st.title("AlertBot - Disaster Assistant")
    
    gemini_key = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=gemini_key)

    generation_config = {
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 40,
        "max_output_tokens": 2048,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    def generate_response(user_input):
        prompt = [
            "You are a Disaster Alert Assistant named *AlertBot*.",
            "Your sole responsibility is to provide information and guidance about ongoing or possible natural disasters such as earthquakes, floods, heatwaves, wildfires, and related safety instructions.",
            "You should refuse to answer any unrelated questions politely and stay on topic.",
            "Examples:",
            "User: What is the capital of France?",
            "Bot: I'm here to help with disaster alerts only. Please ask a disaster-related question.",
            "User: How can I prepare for an earthquake?",
            "Bot: To prepare for an earthquake, secure heavy furniture, make an emergency kit, and identify safe spots like under sturdy tables.",
            f"User: {user_input}",
            "Bot:"
        ]
        response = model.generate_content(prompt)
        return response.text.strip()

    # --- Streamlit UI Setup ---

    st.markdown(
        """
        <style>
        .centered-container {
            max-width: 700px;
            margin: auto;
        }
        .stChatInputContainer {
            position: fixed;
            bottom: 0;
            width: 100%;
            background-color: white;
            z-index: 999;
            padding: 10px 0;
            border-top: 1px solid #ccc;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # --- AlertBot ---

    
    st.markdown("<div class='centered-container'>", unsafe_allow_html=True)
    st.markdown(
        """
        <h1 style='text-align:center; color:#00bcd4;'>🌐 AlertBot - Disaster Assistant</h1>
        <p style='text-align:center; color:#ccc; font-size:18px;'>
            Ask about natural disasters and get instant guidance. Stay safe. Stay alert.
        </p>
        <hr style='border: 1px solid #333;'/>
        """,
        unsafe_allow_html=True)

    # --- Chat History ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # --- Typing simulation ---
    def stream_response(user_input):
        try:
            full_text = generate_response(user_input)
        except Exception as e:
            full_text = f"⚠️ Error: {e}"

        for word in full_text.split():
            yield word + " "
            time.sleep(0.03)

    # --- Chat input ---
    prompt = st.chat_input("Type your disaster-related question:")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response_words = []
            for word in stream_response(prompt):
                full_response_words.append(word)
                placeholder.markdown("".join(full_response_words))
            full_response = "".join(full_response_words)

        st.session_state.messages.append({"role": "assistant", "content": full_response})

    st.markdown("</div>", unsafe_allow_html=True)


