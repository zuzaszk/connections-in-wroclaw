import argparse
from datetime import datetime
import sys
import time
from classes import Graph
from t01_dijkstra import dijkstra
from t01_a_star import a_star_time, a_star_transfer
from functions import parse_time, print_path


def main():
    parser = argparse.ArgumentParser(description="Find the shortest path between two stops.")
    parser.add_argument("start_stop", help="Starting stop")
    parser.add_argument("ending_stop", help="Ending stop")
    parser.add_argument("criterion", choices=["t", "p"], help="Optimization criterion: t (travel time) or p (number of transfers)")
    parser.add_argument("start_time", type=parse_time, help="Start time in form HH:MM or HH:MM:SS")

    args = parser.parse_args()
    minimized_criterion_value = "Travel Time" if args.criterion == 't' else "Number of Transfers"
 
    # Loading connections from CSV file
    graph = Graph()
    graph.load_connections('connection_graph.csv')
    
    print(f"Starting time: {args.start_time}")
    
    req_time = 0
    journey_time = 0
    if args.criterion == 't':
        start_d = time.time()
        dijkstra_path, dijkstra_journey = dijkstra(graph, args.start_stop, args.ending_stop, args.start_time)
        end_d = time.time()
        dijkstra_time = end_d - start_d
        
        start_a = time.time()
        a_star_time_path, a_star_time_journey = a_star_time(graph, args.start_stop, args.ending_stop, args.start_time)
        end_a = time.time()
        a_star_time_time = end_a - start_a
        
        if dijkstra_journey < a_star_time_journey:
            algorithm = "Dijkstra"
            req_time = dijkstra_time
            journey_time = dijkstra_journey
            print_path(dijkstra_path)
        elif dijkstra_journey == a_star_time_journey:
            if dijkstra_time < a_star_time_time:
                algorithm = "Dijkstra"
                req_time = dijkstra_time
                journey_time = dijkstra_journey
                print_path(dijkstra_path)
            else:
                algorithm = "A*"
                req_time = a_star_time_time
                journey_time = a_star_time_journey
                print_path(a_star_time_path)
        else:
            algorithm = "A*"
            req_time = a_star_time_time
            journey_time = a_star_time_journey
            print_path(a_star_time_path)
    else:
        algorithm = "A*"
        start = time.time()
        a_star_transfer_path, a_star_transfer_journey = a_star_transfer(graph, args.start_stop, args.ending_stop, args.start_time)
        end = time.time()
        req_time = end - start
        journey_time = a_star_transfer_journey
        print_path(a_star_transfer_path)

    # Printing minimized criterion and time required for calculation
    print(f"Total journey time: {journey_time}")
    print(f"Used algorithm: {algorithm}")
    print(f"Minimized Criterion: {minimized_criterion_value}", file=sys.stderr)
    print(f"Time Required: {req_time}", file=sys.stderr)

if __name__ == "__main__":
    main()

