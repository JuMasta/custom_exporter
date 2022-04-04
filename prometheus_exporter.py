from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from prometheus_client.core import CounterMetricFamily, HistogramMetricFamily, REGISTRY



class CustomServiceExporter(object):
    """docstring forCustomServiceExporter."""

    stored_errors_count = {}

    def collect(self):
        errors_total = CounterMetricFamily(
         "elasticsearch_logs_errors_total",
         "Service HTTP elasticsearch_logs_errors_total",
         labels=["pod_name","namespace_name"]
        )

        for pod, obj in self.stored_errors_count.items():
            errors_total.add_metric([pod, obj['namespace_name'] ],obj['count'])
        yield errors_total
