import streamlit as st
from utils import Db
import plotly.graph_objects as go
import plotly.express as px
# creating a Db object
db = Db()

def main():
    st.sidebar.title("Flight Analytics")
    sidebar_menu = st.sidebar.selectbox("Menu:",['Home','Srach_Flights','Analytics'])
    
    if sidebar_menu == "Analytics":
        st.write("This is analytics page..")
        airline, num_of_flights = db.fetch_airline_frequency()

        fig = px.pie( values=num_of_flights, 
                      names=airline,
                        title='No. of flights belong to airline companies')
        st.plotly_chart(fig)



        airport, num_flights =  db.num_flights_airport()

        fig = px.bar(x=airport,
                     y=num_flights,
                     title="No. of flights from different airports")
        st.plotly_chart(fig)

        date, number_flights = db.daily_flight_frequency()

        fig = px.line(x=date,
                      y=number_flights,
                      title="Number of flights each day")
        st.plotly_chart(fig)

        city_sets , number_of_flights = db.flight_between_cities()

        fig = px.bar(y=city_sets,
                      x=number_of_flights,
                      title= "Number of flights between cities",
                      orientation="h")
        st.plotly_chart(fig)

        city_sets, avg_fare_of_flights = db.flight_fare_between_cities()

        fig = px.bar(x=city_sets,
                     y=avg_fare_of_flights,
                     title="Average fare of flights between two cities")
        st.plotly_chart(fig)

        city_set,avg_duration_of_flights = db.avg_duration_between_cities()

        fig = px.bar(y=city_set,
                     x=avg_duration_of_flights,
                     title="Average duration of flights between two cities",
                     orientation="h")
        
        st.plotly_chart(fig)

    elif sidebar_menu == "Srach_Flights":
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
        st.write("about")

if __name__ == "__main__":
    main()