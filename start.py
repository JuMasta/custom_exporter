from flask import Flask, request, Response
from prometheus_exporter import CustomServiceExporter
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from prometheus_client.core import CounterMetricFamily, HistogramMetricFamily, REGISTRY


app = Flask(__name__)

REGISTRY.register(CustomServiceExporter())

@app.route("/metric-reciever",methods=["POST"])
def track_metric():
    data_json = request.json
    namespaces_obj = data_json['namespace_names']


    for namespace in namespaces_obj:
        for pod in namespaces_obj[namespace]:
            for level in namespaces_obj[namespace][pod]:
                pod_obj = CustomServiceExporter.stored_errors_count.get(pod, {})
                level_obj = pod_obj.get(level , {})
                level_obj['namespace_name'] = namespace
                level_obj['count'] = level_obj.get('count',0) + namespaces_obj[namespace][pod][level]
                pod_obj[level] = level_obj
                CustomServiceExporter.stored_errors_count[pod] = pod_obj

    return Response(status=200)


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.route("/clean-metrics", methods=["POST"])
def clean_metrics():
    CustomServiceExporter.stored_errors_count = {}
    return Response(status=200)

app.run(host='0.0.0.0', port=80)
