import streamlit as st
from utils import Db
import plotly.graph_objects as go
import plotly.express as px
# creating a Db object
db = Db()

def main():
    # Set page configuration for wider layout
    st.set_page_config(layout="wide")

    st.sidebar.title("Flight Analytics")
    sidebar_menu = st.sidebar.selectbox("Menu:",['Home','Search_Flights','Analytics'])
    
    if sidebar_menu == "Analytics":
        
        # title
        st.markdown("<h2 style='text-align: center; color: grey;'>Flight Analytics Dashboard</h2>", unsafe_allow_html=True)
        st.text("")  # Adds vertical space
        st.text("")  # Adds vertical space
        col1, col2 = st.columns(2,gap="medium",vertical_alignment="center")
        
        with col1:
            # How many flights belong to each airline company?
            st.markdown("<h6 style='text-align: center; color: grey;'>No. of flights belong to airline companies</h6>", unsafe_allow_html=True)
            airline, num_of_flights = db.fetch_airline_frequency()
            fig = px.pie( values=num_of_flights, 
                        names=airline
                            )
            st.plotly_chart(fig)

            # Number of flights from each airport
            st.markdown("<h6 style='text-align: center; color: grey;'>No. of flights from different airports</h6>", unsafe_allow_html=True)
            airport, num_flights =  db.num_flights_airport()

            fig = px.bar(x=airport,
                        y=num_flights)
            st.plotly_chart(fig)

            # Number of flights each day
            st.markdown("<h6 style='text-align: center; color: grey;'>Number of flights each day</h6>", unsafe_allow_html=True)
            date, number_flights = db.daily_flight_frequency()

            fig = px.line(x=date,
                        y=number_flights)
            st.plotly_chart(fig)
        
        with col2:

            # How many flights run between two cities?
            st.markdown("<h6 style='text-align: center; color: grey;'>Number of flights between cities</h6>", unsafe_allow_html=True)
            city_sets , number_of_flights = db.flight_between_cities()

            fig = px.bar(y=city_sets,
                        x=number_of_flights,
                        orientation="h")
            st.plotly_chart(fig)

            # Average fare of flights between two cities
            st.markdown("<h6 style='text-align: center; color: grey;'>Average fare of flights between two cities</h6>", unsafe_allow_html=True)
            city_sets, avg_fare_of_flights = db.flight_fare_between_cities()

            fig = px.bar(x=city_sets,
                        y=avg_fare_of_flights)
            st.plotly_chart(fig)

            # Average time duration between two cities
            st.markdown("<h6 style='text-align: center; color: grey;'>Average duration of flights between two cities</h6>", unsafe_allow_html=True)
            city_set,avg_duration_of_flights = db.avg_duration_between_cities()

            fig = px.bar(y=city_set,
                        x=avg_duration_of_flights,
                        orientation="h")
            
            st.plotly_chart(fig)

    elif sidebar_menu == "Search_Flights":
        st.write("Searching flights")
        col1, col2 = st.columns(2)
        cities = db.fetch_all_cities()
        with col1:
            source = st.selectbox("Source",sorted(cities), placeholder="choose a city",index=None)
        with col2:
            destination = st.selectbox("Destination",sorted(cities), placeholder="choose a city",index=None)
        if st.button("search flights"):
            result = db.search_flights(source,destination)
            st.write(result)

    else:
        st.markdown("<h2 style='text-align: center; color: grey;'>Welcome</h2>", unsafe_allow_html=True)
        # Load and display the image with st.image
        st.image("assets/flight.jpg", use_column_width=True)

        # Custom CSS to center the image
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