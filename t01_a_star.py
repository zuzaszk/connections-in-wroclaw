from classes import PriorityQueue
from functions import calculate_distance, time_diff_seconds, choose_common_line

"""A* by time optimization criteria"""
def heuristic_t(graph, current_connection, goal):
        current_lat = current_connection.start_stop_lat
        current_lon = current_connection.start_stop_lon
        next_lat = current_connection.end_stop_lat
        next_lon = current_connection.end_stop_lon
        
        last_distance = calculate_distance(current_lat, current_lon, next_lat, next_lon)
        
        arrival = current_connection.arrival_time
        departure = current_connection.departure_time
        
        last_time = time_diff_seconds(arrival, departure)
        last_velocity = last_distance / last_time if last_time > 0 else float('inf')
        
        goal_connection = graph.get_connections(goal)[0]
        goal_lat = goal_connection.start_stop_lat
        goal_lon = goal_connection.start_stop_lon
        
        to_goal_distance = calculate_distance(goal_lat, goal_lon, current_lat, current_lon)
        if last_velocity == 0:
            estimated_time = float('inf')
        elif last_velocity == float('inf'):
            estimated_time = 0 
        else:
            estimated_time = to_goal_distance / last_velocity
        return estimated_time
    
def a_star_time(graph, start, goal, start_time):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {start: 0}
    path = []

    journey_start_time = start_time
        
    while not frontier.empty():
        current = frontier.get()
        
        # modification: early exit
        if current == goal:
            break
        
        for connection in graph.get_connections(current):
            next_stop = connection.end_stop
            departure_time = connection.departure_time
            arrival_time = connection.arrival_time
            
            if departure_time >= start_time:
                waiting_time = time_diff_seconds(departure_time, start_time)
                travel_time = time_diff_seconds(arrival_time, departure_time)
                new_cost = cost_so_far[current] + travel_time + waiting_time
                if next_stop not in cost_so_far or new_cost < cost_so_far[next_stop]:
                    cost_so_far[next_stop] = new_cost
                    priority = new_cost + heuristic_t(graph, connection, goal)
                    frontier.put(next_stop, priority)
                    came_from[next_stop] = (current, connection)
            if current in came_from:
                start_time = (came_from[current][1]).arrival_time 
                            
    current = goal
    if current not in came_from:
        return []
    while current != start:
        path.append(came_from[current][1])
        current = came_from[current][0]
    
    path.reverse()
    
    journey_end_time = path[-1].arrival_time
    total_journey_time = journey_end_time - journey_start_time
    
    return path, total_journey_time  


"""A* by number of transfers optimization criteria"""
def heuristic_p(graph, current_connection, goal):
    current_lines = {connection.line for connection in graph.get_connections(current_connection.start_stop)}
    end_lines = {connection.line for connection in graph.get_connections(goal)}
        
    common_lines = current_lines.intersection(end_lines)
    if common_lines:
        # if there are common lines, return 0 transfers
        return 0
    else:
        # calculate the minimum number of transfers needed based on the number of lines at each stop
        return min(len(current_lines), len(end_lines))

def a_star_transfer(graph, start, goal, start_time):
    first_line = choose_common_line(graph, start, goal)
    frontier = PriorityQueue()
    frontier.put((start, first_line), 0)
    came_from = {}
    cost_so_far = {start: 0}
    path = []
    
    journey_start_time = start_time
    
    while not frontier.empty():
        current_stop, current_line = frontier.get()
        
        # modification: early exit
        if current_stop == goal:
            break
        
        for connection in graph.get_connections(current_stop):
            next_stop = connection.end_stop

            departure_time = connection.departure_time
            line = connection.line
            
            if departure_time >= start_time:
                transfer_count = 1 if (current_line != line) else 0
                new_cost = cost_so_far[current_stop] + transfer_count
                if next_stop not in cost_so_far or new_cost < cost_so_far[next_stop]:
                    cost_so_far[next_stop] = new_cost
                    priority = new_cost + heuristic_p(graph, connection, goal)
                    frontier.put((next_stop, line), priority)
                    came_from[next_stop] = (current_stop, connection)
            if current_stop in came_from:
                start_time = (came_from[current_stop][1]).arrival_time 
        
                    
    current_stop = goal
    if current_stop not in came_from:
        return []
    while current_stop != start:
        path.append(came_from[current_stop][1])
        current_stop = came_from[current_stop][0]
    
    path.reverse()
    
    journey_end_time = path[-1].arrival_time
    total_journey_time = journey_end_time - journey_start_time
    
    return path, total_journey_time