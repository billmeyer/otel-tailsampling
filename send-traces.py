from opentelemetry import baggage, trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    BatchSpanProcessor
)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.trace import Status, StatusCode
import datetime, random, socket, time, uuid

otlp_endpoint = "localhost:4317"

def get_tracer(service_name, env):
    provider = TracerProvider(resource=Resource.create({
        "service.name": service_name,
        "service.instance.id": str(uuid.uuid4()),
        "env": env,
        "deployment.environment.name": env,
        "host.name": socket.gethostname(),
    }))
    provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)))
    print(provider._resource.__dict__)
    return trace.get_tracer("python", tracer_provider=provider)

def checkout(env):
    tracer = get_tracer("checkout-worker", env)
    with tracer.start_as_current_span("checkout-worker") as span:
        # time.sleep(random.random())
        span.set_status(Status(StatusCode.OK))
        trace_id = trace.format_trace_id(span.context.trace_id)
        # print(f"Trace ID: {trace_id}")
        return trace_id

def frontend(env):
    tracer = get_tracer("frontend-worker", env)
    with tracer.start_as_current_span("frontend-worker") as frontend_span:
        frontend_span.set_status(Status(StatusCode.OK))
        trace_id = trace.format_trace_id(frontend_span.context.trace_id)
        # print(f"Trace ID: {trace_id}")
        return trace_id

def main():
    # for count in range(100):
        # Should be sampled
        env = "qa01-eus2"
        # trace_id = checkout(env)
        # print(f"View checkout trace in Datadog: https://app.datadoghq.com/apm/traces?query=%40otel.trace_id%3A{trace_id}")
        # trace_id = frontend(env)
        # print(f"View frontend trace in Datadog: https://app.datadoghq.com/apm/traces?query=%40otel.trace_id%3A{trace_id}")

        # Should be dropped
        env = "prod-eus2"
        trace_id = checkout(env)
        # print(f"View checkout in Datadog: https://app.datadoghq.com/apm/traces?query=%40otel.trace_id%3A{trace_id}")
        # trace_id = frontend(env)
        # print(f"View frontend trace in Datadog: https://app.datadoghq.com/apm/traces?query=%40otel.trace_id%3A{trace_id}")

if __name__ == "__main__":
    main()

