import requests
import time
import os

# REPLACE THESE WITH THE DESIRED STOP NUMBERS 
northbound_stop = 0000
southbound_stop = 0000

# Queries the MetroTransit API to get the display info for the given stop number
# It grabs the name of the route and its departure time from the API

def get_stop_info(stop_num: int) -> list:
    r = requests.get(f'https://svc.metrotransit.org/nextrip/{stop_num}')
    if not 'departures' in r.json():
        print(f'Stop {stop_num} does not exist')
        exit()
    next_buses = r.json()['departures']
    display_info = []
    for next_bus in next_buses:
        depart_time= next_bus['departure_text']
        route_name = next_bus['route_id'] if 'terminal' not in next_bus else next_bus['route_id'] + next_bus['terminal']
        display_info.append((route_name, depart_time))
    
    return display_info

# Given the display Information from both stops, it prints the info to the terminal,
# stopping after 6 routes are displayed
def print_display(north_info: list, south_info: list, north_num: int, south_num: int) -> None:
    header1 = f'Departure Information for Northbound Stop {north_num}'
    print(header1, end='')
    space = ' ' * 20
    print(space, end=' ')
    print(f'Departure Information for Southbound Stop {south_num}')

    count = 0
    for depart in range(len(min(north_info, south_info))):
        if count == 6:
            break
        route_name = north_info[depart][0] 
        #used to space out the information so it lines up
        space = ' ' * (15 - len(route_name))
        row1 = f'Route: {route_name}{space}Arrival Time: {north_info[depart][1]}'
        print(row1, end='')

        space = ' ' * (len(header1) + 20 - len(row1))
        print(space, end=' ')
        route_name = south_info[depart][0] 
        space = ' ' * (15 - len(route_name))
        print(f'Route: {route_name}{space}Arrival Time: {south_info[depart][1]}')
        count+=1
    
# runs the loop to display the bus schedule for the 2 stops. 
def grab_display() -> None:
    while(True):
        north_info = get_stop_info(northbound_stop)
        south_info= get_stop_info(southbound_stop)
        # TODO: change this to whatever command your terminal uses to clear itself.
        # commmandprompt in Windows uses cls but others might use clear or something else.
        os.system('cls')
        print_display(north_info, south_info, northbound_stop, southbound_stop)
        time.sleep(20)
        

if __name__=="__main__":
    grab_display()

