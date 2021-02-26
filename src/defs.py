'''
The items in each of the tuples (PROM_URL, PROMQL, PROM_LABELS, GRAPHITE_TAGS) correspond to each other at a given index-number
Eg: item at PROM_URL[0] corresponds to the items at PROMQL[0], PROM_LABELS[0], GRAPHITE_TAGS[0]
'''

# Prometheus URL (different Prometheus endpoints are supported)
PROM_URL = (
    'http://prometheus.example.com/',
    'http://prometheus.example.com/'
)

# PromQL Queries
PROMQL = (
    'sum(kube_node_info{job="kube-state-metrics"}) by(job)',
    'kube_deployment_status_replicas{job="kube-state-metrics",namespace=~"demo",deployment=~"web-01|web-02"}'
)

# Metrics Labels used to extract values from Prometheus output, will be used as series-name/tags in Graphite format
PROM_LABELS = (
    'job',
    'deployment'
)

# Series-name/tags to be processes in Graphite format, corresponds to Prometheus Query defined in 'PROMQL'
GRAPHITE_TAGS = (
    'workernode.count;source=prometheus;kind=node;team=devops;job=%s %s %s',
    'replica.count;source=prometheus;kind=deployment;team=devops;app=%s %s %s'
)