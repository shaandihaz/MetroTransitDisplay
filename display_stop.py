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
def print_display(north_info: list, south_info: list, north_num: int, south_num: int, line_width: int) -> None:
    header1 = f'Northbound Stop {north_num}'
    print(header1, end='')
    space = ' ' * ((line_width // 2) - len(header1))
    print(space, end=' ')
    header2 = f'Southbound Stop {south_num}'
    print(header2)
    dash = '-' * (len(header1) + len(space) + len(header2))
    print(dash)

    count = 0
    for depart in range(min(len(north_info), len(south_info))):
        if count == 6:
            break
        if north_info:
            route_name = north_info[depart][0] 
            #used to space out the information so it lines up
            space = ' ' * (5 - len(route_name))
            row1 = f'Route: {route_name}{space}|{north_info[depart][1]}'
            
        else:
            row1 = '----------'
        
        print(row1, end='')
        space = ' ' * ((line_width // 2) - len(row1))
        print(space, end=' ')
        if south_info:
            route_name = south_info[depart][0] 
            space = ' ' * (5 - len(route_name))
            print(f'Route: {route_name}{space}|{south_info[depart][1]}')
        else:
            print('----------')
        count+=1
    
# runs the loop to display the bus schedule for the 2 stops. 
def grab_display() -> None:
    while(True):
        north_info = get_stop_info(northbound_stop)
        south_info= get_stop_info(southbound_stop)
        # TODO: change this to whatever command your terminal uses to clear itself.
        # commmandprompt in Windows uses cls but others might use clear or something else.
        os.system('clear')
        line_width = line_width = os.get_terminal_size()[0]
        print_display(north_info, south_info, northbound_stop, southbound_stop, line_width)
        time.sleep(20)
        

if __name__=="__main__":
    grab_display()

