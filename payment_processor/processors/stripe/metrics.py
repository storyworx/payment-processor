from prometheus_client import CollectorRegistry, Summary, push_to_gateway

registry = CollectorRegistry()
stripe_initialized_status_timer = Summary(
    "stripe_initialized_status_timer",
    "How long it takes to progress Transaction from INITIALIZED status",
    registry=registry,
)


def send_stripe_elapsed_time(elapsed: int):
    stripe_initialized_status_timer.observe(elapsed)
    push_to_gateway(
        "pushgateway-service:9091", job="stripe-complete-payment", registry=registry
    )
