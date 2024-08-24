import csv
from functions import parse_time
import heapq


class Connection:
    def __init__(self, company, line, departure_time, arrival_time, start_stop, end_stop, start_stop_lat, start_stop_lon, end_stop_lat, end_stop_lon):
        self.company = company
        self.line = line
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.start_stop = start_stop
        self.end_stop = end_stop
        self.start_stop_lat = start_stop_lat
        self.start_stop_lon = start_stop_lon
        self.end_stop_lat = end_stop_lat
        self.end_stop_lon = end_stop_lon
    
    def __str__(self) -> str:
        return f"Company: {self.company}, Line: {self.line}, Departure: {self.departure_time}, Arrival: {self.arrival_time}, Start Stop: {self.start_stop}, End Stop: {self.end_stop}, Start Stop Lat: {self.start_stop_lat}, Start Stop Lon: {self.start_stop_lon}, End Stop Lat: {self.end_stop_lat}, End Stop Lon: {self.end_stop_lon}"

class Graph:
    def __init__(self):
        self.graph = {}

    def load_connections(self, file_path):
        # Loading connections from CSV into self.connections
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                departure_time = parse_time(row['departure_time'])
                arrival_time = parse_time(row['arrival_time'])
                connection = Connection(
                    row['company'],
                    row['line'],
                    departure_time,
                    arrival_time,
                    row['start_stop'],
                    row['end_stop'],
                    float(row['start_stop_lat']),
                    float(row['start_stop_lon']),
                    float(row['end_stop_lat']),
                    float(row['end_stop_lon'])
                )
                if connection.start_stop not in self.graph:
                    self.graph[connection.start_stop] = []
                self.graph[connection.start_stop].append(connection)

    def get_connections(self, stop):
        return self.graph.get(stop, [])
    
class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return not self.elements

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]
