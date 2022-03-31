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
         labels=["errors"]
        )

        for errors, count in self.stored_errors_count.items():
            errors_total.add_metric([errors],count)
        yield errors_total



REGISTRY.register(CustomServiceExporter())


@app.route("/metric-reciever",methods=["POST"])
def track_metric():
    data = request.json
    # new_errors = data['errors']
    for key in data:
        CustomServiceExporter.stored_errors_count[key] = CustomServiceExporter \
                .stored_errors_count.get(key, 0) + data[key]


    return Response(status=200)


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


app.run(host='0.0.0.0', port=80)
