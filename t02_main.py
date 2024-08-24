import argparse
import sys
from classes import Graph
from functions import parse_time


def main():
    parser = argparse.ArgumentParser(description="Find the shortest path between two stops.")
    parser.add_argument("start_stop", help="Starting stop")
    parser.add_argument("stops_to_visit", help="List of stops to visit separated by a semicolon")
    parser.add_argument("criterion", choices=["t", "p"], help="Optimization criterion: t (travel time) or p (number of transfers)")
    parser.add_argument("start_time", type=parse_time, help="Start time in form HH:MM or HH:MM:SS")

    args = parser.parse_args()
    minimized_criterion_value = "Travel Time" if args.criterion == 't' else "Number of Transfers"
    
    req_time = 0
    
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

    # Printing minimized criterion and time required for calculation
    #print(f"Total journey time: {journey_time}")
    print(f"Minimized Criterion: {minimized_criterion_value}", file=sys.stderr)
    print(f"Time Required: {req_time}", file=sys.stderr)

if __name__ == "__main__":
    main()

