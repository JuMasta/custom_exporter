from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from prometheus_client.core import CounterMetricFamily, HistogramMetricFamily, REGISTRY



class CustomServiceExporter(object):
    """docstring forCustomServiceExporter."""

    stored_errors_count = {}

    def collect(self):
        errors_total = CounterMetricFamily(
         "elasticsearch_logs_errors_total",
         "Service HTTP elasticsearch_logs_errors_total",
         labels=["pod_name","namespace_name","level"]
        )

        # for pod, error_obj in self.stored_errors_count.items():
        #     for level, data in error_obj:
        #         print(pod)
        #         # errors_total.add_metric([pod, data['namespace_name'],level ],data['count'])
        #     yield errors_total
        for pod in self.stored_errors_count:
            for level in self.stored_errors_count[pod]:
                namespace_name = self.stored_errors_count[pod][level]['namespace_name']
                count = self.stored_errors_count[pod][level]['count']
                errors_total.add_metric([pod, namespace_name ,level ],count)
                yield errors_total
