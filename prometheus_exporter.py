from flask import Flask, request, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from prometheus_client.core import CounterMetricFamily, HistogramMetricFamily, REGISTRY


app = Flask(__name__)

class CustomServiceExporter(object):
    """docstring forCustomServiceExporter."""

    stored_errors_count = {}

    def collect(self):
        errors_total = CounterMetricFamily(
         "elasticsearch_logs_errors_total",
         "Service HTTP elasticsearch_logs_errors_total",
         labels=["pod_name","namespace_name"]
        )

        for pods, obj in self.stored_errors_count.items():
            errors_total.add_metric([pods, obj['namespace_name'] ],obj['count'])
        yield errors_total



REGISTRY.register(CustomServiceExporter())


@app.route("/metric-reciever",methods=["POST"])
def track_metric():
    data_json = request.json
    namespaces_obj = data_json['namespace_names']

    for namespace in namespaces_obj:
        for pod in namespaces_obj[namespace]:
            pod_obj = CustomServiceExporter.stored_errors_count.get(pod, {})
            pod_obj['pod_name'] = pod
            pod_obj['namespace_name'] = namespace
            pod_obj['count'] = pod_obj.get('count',0) + namespaces_obj[namespace][pod]
            CustomServiceExporter.stored_errors_count[pod] = pod_obj
            print(CustomServiceExporter.stored_errors_count)


    return Response(status=200)


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


app.run(host='0.0.0.0', port=80)
