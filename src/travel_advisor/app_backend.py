from initialize_models import Agent
from mapper import RouteFinder
from dotenv import load_dotenv
from pathlib import Path
import os
from dotenv import load_dotenv
import folium
import leafmap
load_dotenv()
from streamlit_folium import st_folium, folium_static


class TravelMapperBase:
    def __init__(
        self, verbose=False):


        self.travel_agent = Agent(
            llm_api_key=os.environ['GOOGLE_PALM_API_KEY'],
            debug=verbose,
        )
        self.route_finder = RouteFinder(google_maps_api_key=os.environ['GOOGLE_MAPS_API_KEY'])

    def parse(self, query, make_map=True):
        """
        For running when we don't want to call streamlit
        """
        itinerary, list_of_places = self.travel_agent.plan(query)

        directions, sampled_route, mapping_dict = self.route_finder.generate_route(
            list_of_places=list_of_places, itinerary=itinerary, include_map=make_map
        )



class TravelMapperForUI(TravelMapperBase):


    def generate_generic_leafmap():
        map = leafmap.Map(location=[0, 0], tiles="OpenStreetMap", zoom_start=3)
        return map.to_streamlit()

            
    def generate_leafmap(self,directions_list, sampled_route):

        map_start_loc_lat = directions_list[0]["legs"][0]["start_location"]["lat"]
        map_start_loc_lon = directions_list[0]["legs"][0]["start_location"]["lng"]
        map_start_loc = [map_start_loc_lat, map_start_loc_lon]

        marker_points = []

        # extract the location points from the previous directions function
        for segment in directions_list:
            for leg in segment["legs"]:
                leg_start_loc = leg["start_location"]
                marker_points.append(
                    ([leg_start_loc["lat"], leg_start_loc["lng"]], leg["start_address"])
                )

        last_stop = directions_list[-1]["legs"][-1]
        last_stop_coords = last_stop["end_location"]
        marker_points.append(
            (
                [last_stop_coords["lat"], last_stop_coords["lng"]],
                last_stop["end_address"],
            )
        )

        map = folium.Map(location=map_start_loc, tiles="OpenStreetMap", zoom_start=8)

        # Add waypoint markers to the map
        for location, address in marker_points:
            folium.Marker(
                location=location,
                popup=address,
                tooltip="<strong>Click for address</strong>",
                icon=folium.Icon(color="red", icon="info-sign"),
            ).add_to(map)

        for leg_id, route_points in sampled_route.items():
            leg_distance = route_points["distance"]
            leg_duration = route_points["duration"]

            f_group = folium.FeatureGroup("Leg {}".format(leg_id))
            folium.PolyLine(
                route_points["route"],
                popup="<b>Route segment {}</b>".format(leg_id),
                tooltip="Distance: {}, Duration: {}".format(leg_distance, leg_duration),
                color="blue",
                weight=2,
            ).add_to(f_group)
            f_group.add_to(map)

        map = folium_static(map, height=700, width=700)
        return map


    def generate_without_leafmap(self, query):
        itinerary = self.travel_agent.plan(query)
        return itinerary

    def generate_with_leafmap(self, query):

        itinerary, list_of_places= self.travel_agent.plan(query)

        directions_list,sampled_route,mapping_dict = self.route_finder.generate_route(
                list_of_places=list_of_places, itinerary=itinerary, include_map=False
            )

        map_html = self.generate_leafmap(directions_list=directions_list,sampled_route=sampled_route)
        return map_html, itinerary
    
