import argparse
from datetime import datetime, timedelta
import math


def print_path(path):
    for connection in path:
        print(f"{connection.start_stop} -> {connection.end_stop}, Line: {connection.line}, Departure: {connection.departure_time.time()}, Arrival: {connection.arrival_time.time()}")

def time_diff_seconds(time1, time2):
    return (time1 - time2).total_seconds()

def calculate_distance(lat1, lon1, lat2, lon2):
    return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)

def calculate_distance_stops(stop1, stop2, graph):
    lat1, lon1 = graph.get_connections(stop1)[0].start_stop_lat, graph.get_connections(stop1)[0].start_stop_lon
    lat2, lon2 = graph.get_connections(stop2)[0].start_stop_lat, graph.get_connections(stop2)[0].start_stop_lon
    return calculate_distance(lat1, lon1, lat2, lon2)

def choose_common_line(graph, current, goal):
    current_lines = {connection.line for connection in graph.get_connections(current)}
    end_lines = {connection.line for connection in graph.get_connections(goal)}
    common_lines = current_lines.intersection(end_lines)
    if common_lines:
        return list(common_lines)[0]
    else:
        return None
    
def parse_time(time_str):
    try:
        hours, minutes, seconds = map(int, time_str.split(':'))
    except ValueError:
        try:
            hours, minutes = map(int, time_str.split(':'))
            seconds = 0
        except ValueError:
            raise argparse.ArgumentTypeError("Invalid time format. Please use HH:MM or HH:MM:SS.")
    base_date = datetime(2023, 3, 2)
    if hours >= 24:
        hours -= 24
        return base_date.replace(hour=hours, minute=minutes, second=seconds) + timedelta(days=1)
    elif hours < 0:
        hours += 24
        return base_date.replace(hour=hours, minute=minutes, second=seconds) - timedelta(days=1)
    else:
        return base_date.replace(hour=hours, minute=minutes, second=seconds)