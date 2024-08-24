from classes import PriorityQueue
from functions import time_diff_seconds


def dijkstra(graph, start, goal, start_time):
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
                    priority = new_cost
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