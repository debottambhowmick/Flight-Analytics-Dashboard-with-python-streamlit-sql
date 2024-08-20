import streamlit as st
from utils import Db
import plotly.graph_objects as go
import plotly.express as px

# Creating a Db object
db = Db()

def main():
    # Set page configuration for wider layout
    st.set_page_config(layout="wide")

    st.sidebar.title("Flight Analytics")
    sidebar_menu = st.sidebar.selectbox("Menu:", ['Home', 'Search_Flights', 'Analytics'])
    
    if sidebar_menu == "Analytics":
        # Title
        st.markdown("<h2 style='text-align: center; color: grey;'>Flight Analytics Dashboard</h2>", unsafe_allow_html=True)
        st.text("")  # Adds vertical space
        st.text("")  # Adds vertical space
        
        col1, col2 = st.columns(2, gap="medium", vertical_alignment="center")
        
        with col1:
            # Flights by airline
            st.markdown("<h6 style='text-align: center; color: grey;'>No. of Flights by Airline</h6>", unsafe_allow_html=True)
            airline, num_of_flights = db.fetch_airline_frequency()
            fig = px.pie(values=num_of_flights, names=airline)
            st.plotly_chart(fig, use_container_width=True)

            # Flights by airport
            st.markdown("<h6 style='text-align: center; color: grey;'>No. of Flights by Airport</h6>", unsafe_allow_html=True)
            airport, num_flights = db.num_flights_airport()
            fig = px.bar(x=airport, y=num_flights)
            fig.update_layout(xaxis_title='Airport', yaxis_title='Number of Flights')
            st.plotly_chart(fig, use_container_width=True)

            # Daily flights
            st.markdown("<h6 style='text-align: center; color: grey;'>Daily Flight Frequency</h6>", unsafe_allow_html=True)
            date, number_flights = db.daily_flight_frequency()
            fig = px.line(x=date, y=number_flights)
            fig.update_layout(xaxis_title='Date', yaxis_title='Number of Flights')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Flights between cities
            st.markdown("<h6 style='text-align: center; color: grey;'>No. of Flights Between Cities</h6>", unsafe_allow_html=True)
            city_sets, number_of_flights = db.flight_between_cities()
            fig = px.bar(y=city_sets, x=number_of_flights, orientation="h")
            fig.update_layout(xaxis_title='Number of Flights', yaxis_title='City Pairs')
            st.plotly_chart(fig, use_container_width=True)

            # Average fare between cities
            st.markdown("<h6 style='text-align: center; color: grey;'>Average Fare Between Cities</h6>", unsafe_allow_html=True)
            city_sets, avg_fare_of_flights = db.flight_fare_between_cities()
            fig = px.bar(x=city_sets, y=avg_fare_of_flights)
            fig.update_layout(xaxis_title='City Pairs', yaxis_title='Average Fare')
            st.plotly_chart(fig, use_container_width=True)

            # Average duration between cities
            st.markdown("<h6 style='text-align: center; color: grey;'>Average Duration Between Cities</h6>", unsafe_allow_html=True)
            city_set, avg_duration_of_flights = db.avg_duration_between_cities()
            fig = px.bar(y=city_set, x=avg_duration_of_flights, orientation="h")
            fig.update_layout(xaxis_title='Average Duration (hours)', yaxis_title='City Pairs')
            st.plotly_chart(fig, use_container_width=True)
    
    elif sidebar_menu == "Search_Flights":
        st.write("Searching flights")
        col1, col2 = st.columns(2)
        cities = db.fetch_all_cities()
        with col1:
            source = st.selectbox("Source", sorted(cities), placeholder="Choose a city",index=None)
        with col2:
            destination = st.selectbox("Destination", sorted(cities), placeholder="Choose a city",index=None)

        # Date Input
        journey_date = st.date_input("Select Date", format="YYYY-MM-DD",value=None)

        # Search Button
        if st.button("Search Flights"):
            result = db.search_flights(source, destination, journey_date)
            st.write(result)

    else:
        st.markdown("<h2 style='text-align: center; color: grey;'>Welcome</h2>", unsafe_allow_html=True)
        st.image("assets/flight.jpg", use_column_width=True)
        st.markdown(
            """
            <style>
            .stImage {
                display: flex;
                justify-content: center;
                align-items: center;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()
