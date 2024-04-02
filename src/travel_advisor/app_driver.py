import streamlit as st
from app_backend import TravelMapperForUI
from constants import EXAMPLE_QUERY
from dotenv import load_dotenv
load_dotenv()

def main():
    st.title("🗺️ AI Trip Planner")
    col1, col2 = st.columns(2)

    # Add title with emojis
    # Add description below the title

    with col1:
        st.write("""
    Welcome to the AI Trip Planner! This application helps you plan your trips with ease.
    Here's what you can do:
    - Input your travel queries
    - Choose your preferred options
    - Let the AI assist you in planning your perfect trip
    """)
    with col2:
        # Add GIF below the description
        gif_url = "https://qph.cf2.quoracdn.net/main-qimg-b9f07949f54b06dc6d7944db12eece59"  # Replace with the URL of your GIF
        st.image(gif_url, caption='GIF: AI Trip Planner in action')

    st.sidebar.markdown("## Input")
    tab_selection = st.sidebar.radio("Choose a tab", ("Generate with map", "Generate without map"))

    
    travel_map = TravelMapperForUI()


    if tab_selection == "Generate with map":
        st.sidebar.markdown("### Generate with map")
        text_input_map = st.sidebar.text_area("Travel query", value=EXAMPLE_QUERY, height=150)
        model_choice_map = st.sidebar.radio("Model choices", ("gpt-3.5-turbo", "gpt-4", "models/text-bison-001"))

        if st.sidebar.button("Generate"):
            map, itinerary = travel_map.generate_with_leafmap(query=text_input_map)
            
            # Split the page into two columns
            # col1, col2 = st.columns(2)

            # Display the text output in the left column
            itinerary_output=travel_map.generate_without_leafmap(query=text_input_map)
            # with col1:
            # st.text_area("Itinerary suggestion", value=itinerary_output[0], height=700)

                            # Display the map output in the right column
            # with col2:
            st.success("Map generation in process")
                # st.markdown(map, unsafe_allow_html=True)
            st.markdown(map,unsafe_allow_html=True)
            st.markdown(itinerary_output[0],unsafe_allow_html=True)


    # if tab_selection == "Generate with map":
    #     st.sidebar.markdown("### Generate with map")
    #     text_input_map = st.sidebar.text_area("Travel query", value=EXAMPLE_QUERY, height=150)
    #     model_choice_map = st.sidebar.radio("Model choices", ("gpt-3.5-turbo", "gpt-4", "models/text-bison-001"))

    #     if st.sidebar.button("Generate"):
    #         map, itinerary_output = travel_map.generate_with_leafmap(query=text_input_map)
    #         map_output = st_folium(map,height=500,width=500)
    #         st.markdown(itinerary_output[0], unsafe_allow_html=True)

    #         st.success("Map generation in process")
    #         st.markdown(map_output, unsafe_allow_html=True)
    #         st.success("Map generated")




    elif tab_selection == "Generate without map":
        st.sidebar.markdown("### Generate without map")
        text_input_no_map = st.sidebar.text_area("Travel query", value=EXAMPLE_QUERY, height=100)
        model_choice_no_map = st.sidebar.radio("Model choices", ("gpt-3.5-turbo", "gpt-4", "models/text-bison-001"))

        if st.sidebar.button("Generate"):
            text_output_no_map = travel_map.generate_without_leafmap(query=text_input_no_map)
            st.markdown(text_output_no_map[0], unsafe_allow_html=True)

if __name__ == "__main__":
    main()







