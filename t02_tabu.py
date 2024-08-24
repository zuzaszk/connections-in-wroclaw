import argparse
import random
import sys
from classes import Graph
from functions import parse_time, print_path


def objective_function(graph, path, start_time, criterion):
    if criterion == 't':
        total_time = start_time - start_time
        for i in range(len(path) - 1):
            connections = graph.get_connections(path[i])
            for connection in connections:
                if connection.end_stop == path[i + 1]:
                    waiting_time = connection.departure_time - start_time
                    tarnsfer_time = connection.arrival_time - connection.departure_time
                    total_time += waiting_time + tarnsfer_time
                    break
        return total_time.total_seconds()
    elif criterion == 'p':  
        transfers = 0
        # TODO: Number of transfers
        return transfers


def tabu_search(graph, start_stop, stops_to_visit, criterion, start_time, max_iterations=1000):
    
    initial_connection = None
    connections_from_start = graph.get_connections(start_stop)
    for connection in connections_from_start:
        if connection.end_stop in stops_to_visit:
            initial_connection = connection
            break

    if initial_connection is None:
        print("Error: No valid initial connection found.")
        return []
    
    current_solution = [(start_stop, initial_connection)]
    tabu_list = []  # tabu list to store visited solutions
        
    for _ in range(max_iterations):
        neighbors = generate_neighbors(graph, current_solution, stops_to_visit)
        
        if not neighbors:
            continue
        
        best_neighbor = None
        best_score = float('inf')

        for neighbor in neighbors:
            print(f"{neighbor[0]}, {neighbor[1]}")
            if neighbor not in tabu_list:
                score = objective_function(graph, neighbor, start_time, criterion)
                current_conn = neighbor[1]
                start_time = current_conn.arrival_time
                if score < float(best_score):
                    best_neighbor = neighbor
                    best_score = score

        if best_neighbor is None:
            best_neighbor = random.choice(neighbors)

        current_solution = best_neighbor
        tabu_list.append(best_neighbor[0])
        
        # remove old moves from the tabu list if they exceed a certain tenure
        if len(tabu_list) > len(stops_to_visit):
            tabu_list.pop(0)

    return current_solution


def generate_neighbors(graph, current_solution, stops_to_visit):
    neighbors = []
    current_stop, prev_connection = current_solution[-1]
    connections = graph.get_connections(current_stop)
    
    for connection in connections:
        next_stop = connection.end_stop
        if next_stop in stops_to_visit and next_stop not in current_solution:
            neighbors.append(current_solution + [(next_stop, connection)])
            
    return neighbors

def main():
    parser = argparse.ArgumentParser(description="Find the shortest path between two stops.")
    parser.add_argument("start_stop", help="Starting stop")
    parser.add_argument("stops_to_visit", help="List of stops to visit separated by a semicolon")
    parser.add_argument("criterion", choices=["t", "p"], help="Optimization criterion: t (travel time) or p (number of transfers)")
    parser.add_argument("start_time", type=parse_time, help="Start time in form HH:MM or HH:MM:SS")

    args = parser.parse_args()
    minimized_criterion_value = "Travel Time" if args.criterion == 't' else "Number of Transfers"

    try:
        stops_to_visit = args.stops_to_visit.split(';')
    except AttributeError:
        print("Error: Stops to visit must be provided as a semicolon-separated list.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}", file=sys.stderr)
        sys.exit(1)
        
    # Loading connections from CSV file
    graph = Graph()
    graph.load_connections('connection_graph.csv')
    
    print(f"Starting time: {args.start_time}")

    # Run Tabu Search algorithm
    best_solution = tabu_search(graph, args.start_stop, stops_to_visit, args.criterion, args.start_time)
    connections = []
    for stop, connection in best_solution:
        connections.append(connection)
        
    print_path(connections)
    # Printing results
    #print("Best solution found:", best_solution)
    print(f"Minimized Criterion: {minimized_criterion_value}", file=sys.stderr)

if __name__ == "__main__":
    main()
