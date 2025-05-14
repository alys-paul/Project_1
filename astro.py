import streamlit as st
import mysql.connector
import pandas as pd
from datetime import date
# Streamlit app
st.set_page_config(page_title="NASA NEO -:comet: Asteroid Analytics", layout="wide")
st.title("NASA NEO -:comet: Asteroid Analytics")
st.markdown('<h3 style="color: #e65c00;">Track near-Earth objects, analyze asteroid encounters with Earth, identify potential threats, and explore patterns across time.</h3>', unsafe_allow_html=True)

from streamlit_option_menu import option_menu

# Sidebar for choosing between queries and filters
with st.sidebar:
    selected = option_menu(
        "Asteroid Tracker",  # Title
        ["Queries", "Filters"],  # Menu options
        icons=["search", "sliders"],  # Icons (FontAwesome)
        menu_icon="cast",  # Sidebar Icon
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#f0f2f6"},
            "icon": {"color": "white", "font-size": "18px"},
            "nav-link": {
                "font-size": "18px",
                "text-align": "left",
                "margin": "5px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "#ff6600", "color": "white"},
        }
    )

st.markdown("""
    <style>
    /* PAGE BACKGROUND - Dark Orange to Golden Yellow Gradient */
    body {
        background: linear-gradient(135deg, #ff7e5f, #feb47b);
        background-attachment: fixed;
        background-size: cover;
    }

    /* MAIN APP BOX - Pure White */
    .stApp {
        background: white;
        border-radius: 20px;
        padding: 3rem;
        margin: 2% auto;
        width: 95%;
        box-shadow: 0 8px 30px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

 # Function to connect and fetch based on a query
def run_query(query):
    connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "paul",
    database = "asteroid"
    )
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [i[0] for i in cursor.description]
    df = pd.DataFrame(rows, columns=columns)
    cursor.close()
    connection.close()
    return df

# Dropdown menu for selecting a query
if selected == "Queries":
    option = st.selectbox(
        'Select a query to display:', ["Count how many times each asteroid has approached Earth",
                                    "Average velocity of each asteroid over multiple approaches",
                                    "List top 10 fastest asteroids",
                                    "Find potentially hazardous asteroids that have approached Earth more than 3 times",
                                    "Find the month with the most asteroid approaches",
                                    "Get the asteroid with the fastest ever approach speed",
                                    "Sort asteroids by maximum estimated diameter (descending)",
                                    "Asteroids whose closest approach is getting nearer over time",
                                    "Display the name of each asteroid along with the date and miss distance of its closest approach to Earth",
                                    "List names of asteroids that approached Earth with velocity > 50,000 km/h",
                                    "Count how many approaches happened per month",
                                    "Find asteroid with the highest brightness (lowest magnitude value)",
                                    "Get number of hazardous vs non-hazardous asteroids",
                                    "Find asteroids that passed closer than the Moon (lesser than 1 LD), along with their close approach date and distance",
                                    "Find asteroids that came within 0.05 AU(astronomical distance)",
                                    "List 10 slowest asteroids",
                                    "Find asteroid with the lowest brightness (highest magnitude value)",
                                    "List asteroids with an estimated diameter larger than 1 km",
                                    "List asteroids that made multiple close approaches on the same day",
                                    "Asteroids with the highest relative velocity ever recorded in any approach",
                                    "Find the smallest asteroid (by minimum estimated diameter) marked as hazardous",
                                    "Find the total number of unique asteroids observed",
                                    "Find which dates had the most asteroid approaches",
                                    "Top 5 Largest Hazardous Asteroids",
                                    "Most Recent Close Approach"])

   
    # Run queries based on selection
    # Submit button
    if st.button('Submit'):
        if option == 'Count how many times each asteroid has approached Earth':
            query = """
            SELECT neo_reference_id, COUNT(*) as approach_count
            FROM close_approach
            GROUP BY neo_reference_id
            ORDER BY approach_count DESC;
            """
            df = run_query(query)
            st.dataframe(df)

        elif option == 'Average velocity of each asteroid over multiple approaches':
            query = """
            SELECT neo_reference_id, AVG(relative_velocity_kmph) as avg_velocity
            FROM close_approach
            GROUP BY neo_reference_id
            ORDER BY avg_velocity DESC;
            """
            df = run_query(query)
            st.dataframe(df)

        elif option == 'List top 10 fastest asteroids':
            query = """
            SELECT neo_reference_id, MAX(relative_velocity_kmph) as max_velocity
            FROM close_approach
            GROUP BY neo_reference_id
            ORDER BY max_velocity DESC
            LIMIT 10;
            """
            df = run_query(query)
            st.dataframe(df)

        elif option == 'Find potentially hazardous asteroids that have approached Earth more than 3 times':
            query = """
            SELECT ca.neo_reference_id, COUNT(*) as approach_count
            FROM close_approach ca
            JOIN asteroids a ON ca.neo_reference_id = a.id
            WHERE a.is_potentially_hazardous_asteroid = True
            GROUP BY ca.neo_reference_id
            HAVING COUNT(*) > 3;
            """
            df = run_query(query)
            st.dataframe(df)

        elif option == 'Find the month with the most asteroid approaches':
            query = """
            SELECT MONTH(close_approach_date) as approach_month, COUNT(*) as num_approaches
            FROM close_approach
            GROUP BY approach_month
            ORDER BY num_approaches DESC
            LIMIT 1;
            """
            df = run_query(query)
            st.metric(label="Month with Most Approaches (Month Number)", value=int(df['approach_month'].iloc[0]))
            st.metric(label="Number of Approaches", value=int(df['num_approaches'].iloc[0]))

        elif option == 'Get the asteroid with the fastest ever approach speed':
            query = """
            SELECT neo_reference_id, relative_velocity_kmph
            FROM close_approach
            ORDER BY relative_velocity_kmph DESC
            LIMIT 1;
            """
            df = run_query(query)
            st.dataframe(df)

        elif option == 'Sort asteroids by maximum estimated diameter (descending)':
            query = """
            SELECT id, name, estimated_diameter_max_km
            FROM asteroids
            ORDER BY estimated_diameter_max_km DESC;
            """
            df = run_query(query)
            st.dataframe(df)

        elif option == 'Asteroids whose closest approach is getting nearer over time':
            query = """
            SELECT neo_reference_id, close_approach_date, miss_distance_km
            FROM close_approach
            ORDER BY close_approach_date ASC, miss_distance_km ASC;
            """
            df = run_query(query)
            st.dataframe(df)

        elif option == 'Display the name of each asteroid along with the date and miss distance of its closest approach to Earth':
            query = """
            SELECT a.name, ca.close_approach_date, ca.miss_distance_km
            FROM close_approach ca
            JOIN asteroids a ON ca.neo_reference_id = a.id
            ORDER BY ca.miss_distance_km ASC;
            """
            df = run_query(query)
            st.dataframe(df)

        elif option == 'List names of asteroids that approached Earth with velocity > 50,000 km/h':
            query = """
            SELECT neo_reference_id, relative_velocity_kmph
            FROM close_approach
            WHERE relative_velocity_kmph > 50000;
            """
            df = run_query(query)
            st.dataframe(df)

        elif option == 'Count how many approaches happened per month':
            query = """
            SELECT MONTH(close_approach_date) as approach_month, COUNT(*) as num_approaches
            FROM close_approach
            GROUP BY approach_month
            ORDER BY approach_month ASC;
            """
            df = run_query(query)
            st.dataframe(df)

        elif option == 'Find asteroid with the highest brightness (lowest magnitude value)':
            query = """
            SELECT id, name, absolute_magnitude_h
            FROM asteroids
            ORDER BY absolute_magnitude_h ASC
            LIMIT 1;
            """
            df = run_query(query)
            st.dataframe(df)

        elif option == 'Get number of hazardous vs non-hazardous asteroids':
            query = """
            SELECT is_potentially_hazardous_asteroid, COUNT(*) as count
            FROM asteroids
            GROUP BY is_potentially_hazardous_asteroid;
            """
            df = run_query(query)
            st.dataframe(df)

        elif option == 'Find asteroids that passed closer than the Moon (lesser than 1 LD), along with their close approach date and distance':
            query = """
            SELECT neo_reference_id, close_approach_date, miss_distance_lunar
            FROM close_approach
            WHERE miss_distance_lunar < 1
            ORDER BY miss_distance_lunar ASC;
            """
            df = run_query(query)
            st.dataframe(df)

        elif option == 'Find asteroids that came within 0.05 AU(astronomical distance)':
            query = """
            SELECT neo_reference_id, close_approach_date, astronomical
            FROM close_approach
            WHERE astronomical < 0.05
            ORDER BY astronomical ASC;
            """
            df = run_query(query)
            st.dataframe(df)

        elif option == 'List 10 slowest asteroids':
            query = """
            SELECT neo_reference_id, MIN(relative_velocity_kmph) as min_velocity
            FROM close_approach
            GROUP BY neo_reference_id
            ORDER BY min_velocity ASC
            LIMIT 10;
            """
            df = run_query(query)
            st.dataframe(df)

        elif option == 'Find asteroid with the lowest brightness (highest magnitude value)':
            query = """
            SELECT id, name, absolute_magnitude_h
            FROM asteroids
            ORDER BY absolute_magnitude_h DESC
            LIMIT 1;
            """
            df = run_query(query)
            st.dataframe(df)

        elif option == 'List asteroids with an estimated diameter larger than 1 km':
            query = """
            SELECT id, name, estimated_diameter_max_km
            FROM asteroids
            WHERE estimated_diameter_max_km > 1
            ORDER BY estimated_diameter_max_km DESC;
            """
            df = run_query(query)
            st.dataframe(df)

        elif option == 'List asteroids that made multiple close approaches on the same day':
            query = """
            SELECT close_approach_date, COUNT(*) as num_approaches
            FROM close_approach
            GROUP BY close_approach_date
            HAVING COUNT(*) > 1
            ORDER BY num_approaches DESC;
            """
            df = run_query(query)
            st.dataframe(df)

        elif option == 'Asteroids with the highest relative velocity ever recorded in any approach':
            query = """
            SELECT neo_reference_id, relative_velocity_kmph
            FROM close_approach
            ORDER BY relative_velocity_kmph DESC
            LIMIT 5;
            """
            df = run_query(query)
            st.dataframe(df)

        elif option == 'Find the smallest asteroid (by minimum estimated diameter) marked as hazardous':
            query = """
            SELECT id, name, estimated_diameter_min_km
            FROM asteroids
            WHERE is_potentially_hazardous_asteroid = 1
            ORDER BY estimated_diameter_min_km ASC
            LIMIT 1;
            """
            df = run_query(query)
            st.dataframe(df)

        elif option == 'Find the total number of unique asteroids observed':
            query = """
            SELECT COUNT(DISTINCT id) as unique_asteroid_count
            FROM asteroids;
            """
            df = run_query(query)
            st.dataframe(df)

        elif option == 'Find which dates had the most asteroid approaches':
            query = """
            SELECT DATE(close_approach_date) as approach_date, COUNT(*) as num_approaches
            FROM close_approach
            GROUP BY approach_date
            ORDER BY num_approaches DESC;
            """
            df = run_query(query)
            st.dataframe(df)

        elif option == 'Top 5 Largest Hazardous Asteroids':
            query = """
            SELECT id, name, estimated_diameter_max_km
            FROM asteroids
            WHERE is_potentially_hazardous_asteroid = TRUE
            ORDER BY estimated_diameter_max_km DESC
            LIMIT 5;
            """
            df = run_query(query)
            st.dataframe(df)

        elif option == 'Most Recent Close Approach':
            query = """
            SELECT neo_reference_id, close_approach_date
            FROM close_approach
            ORDER BY close_approach_date DESC
            LIMIT 1;
            """
            df = run_query(query)
            st.dataframe(df)
    
#Filters section 
if selected == "Filters":
     # Date Range
    start_date = st.date_input("Start Date", date(2000, 1, 1))
    end_date = st.date_input("End Date", date(2025, 12, 31))

    # Astronomical Unit Range
    au_range = st.slider("Astronomical Units (AU)", min_value=0.0, max_value=1.0, value=(0.0, 0.05))

    # Lunar Distance Range
    lunar_range = st.slider("Lunar Distance (LD)", min_value=0.0, max_value=200.0, value=(0.0, 200.0))

    # Relative Velocity Range
    velocity_range = st.slider("Relative Velocity (km/h)", min_value=0.0, max_value=150000.0, value=(0.0, 50000.0))

    # Estimated Diameter Range
    diameter_range = st.slider("Estimated Diameter (km)", min_value=0.0, max_value=10.0, value=(0.0, 1.0))

    # Hazardous Filter
    hazardous_option = st.selectbox("Hazardous Asteroids Only?", ["Both", "Yes", "No"])

    if st.button("Apply Filters"):
        # Build query dynamically
        filter_query = f"""
        SELECT ca.neo_reference_id, ca.close_approach_date, ca.astronomical, ca.miss_distance_lunar,
               ca.relative_velocity_kmph, a.estimated_diameter_min_km, a.estimated_diameter_max_km,
               a.is_potentially_hazardous_asteroid
        FROM close_approach ca
        JOIN asteroids a ON ca.neo_reference_id = a.id
        WHERE close_approach_date BETWEEN '{start_date}' AND '{end_date}'
          AND astronomical BETWEEN {au_range[0]} AND {au_range[1]}
          AND miss_distance_lunar BETWEEN {lunar_range[0]} AND {lunar_range[1]}
          AND relative_velocity_kmph BETWEEN {velocity_range[0]} AND {velocity_range[1]}
          AND estimated_diameter_min_km >= {diameter_range[0]}
          AND estimated_diameter_max_km <= {diameter_range[1]}
        """

        if hazardous_option == "Yes":
            filter_query += " AND is_potentially_hazardous_asteroid = 1"
        elif hazardous_option == "No":
            filter_query += " AND is_potentially_hazardous_asteroid = 0"

        df = run_query(filter_query)
        st.dataframe(df)
