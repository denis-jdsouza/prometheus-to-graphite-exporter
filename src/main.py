#!/usr/bin/env python3.6
from datetime import datetime
from socket import socket
from prometheus_api_client import PrometheusConnect
from prometheus_api_client.utils import parse_datetime
import defs

# Time-range to query Prometheus metrics (change values as per requirements)
start_time = parse_datetime("1m")
end_time = parse_datetime("now")
step_size = 60  # seconds

# Graphite/Carbon Deatils
CARBON_SERVER = '127.0.0.1'
CARBON_PORT = 2003  # plaintext port

def get_metrics_prom(query_index):
    """ Function to Query Prometheus """
    prom = PrometheusConnect(url=defs.PROM_URL[loop_count], disable_ssl=True)
    query_results = prom.custom_query_range(
    query=defs.PROMQL[query_index],
    start_time=start_time,
    end_time=end_time,
    step=step_size)
    return query_results

def process_metrics(query_out,query_index):
    """ Function to process Prometheus metics into Graphite format """
    values_list = []
    for metric in query_out:
        lines_list = []
        for value in metric['values']:
            lines = defs.GRAPHITE_TAGS[query_index] % (metric['metric'][defs.PROM_LABELS[query_index]],value[1],value[0])
            lines_list.append(lines)
        values_list.extend(lines_list)
    return values_list

def send_metrics_graphite(message):
    """ Function to send metrics to Graphite/Carbon """
    sock = socket()
    sock.connect((CARBON_SERVER, CARBON_PORT))
    sock.sendall(message.encode())
    sock.close()

if __name__ == "__main__":
    metrics_count = 0
    loop_count = -1
    for query in defs.PROMQL:
        metrics_count += 1
        loop_count += 1
        query_index = loop_count
        query_out = get_metrics_prom(query_index)
        if query_out != []:
            message = process_metrics(query_out,query_index)
            message_formatted = '\n'.join(message) + '\n'
            print(message_formatted)
            send_metrics_graphite(message_formatted)
        else:
            print(f'No hits for query: {query}')
            metrics_count -=1
    print(f'Metrics sent for: {str(metrics_count)} queries')