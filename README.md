# Testing Tail Sampling with OTel and Python

## One Time Setup

1. Create a Python virtualenv:

    ```bash
    python3 -m venv venv
    ```

2. Source the new env:

    ```bash
    source venv/bin/activate
    ```

3. Install dependencies:

    ```bash
    pip3 install -r requirements.txt
    ```
   
4. Download a OTel Collector

Download a [Contrib release](https://github.com/open-telemetry/opentelemetry-collector-releases/releases/tag/v0.120.0) of the OTel Collector and extract in the local directory.

## Execution

1. Start the Collector with the supplied config:

   ```bash
   ./otelcol-contrib --config config.yaml
   ```

2. In another terminal, run the python script to generate trace(s):

   ```bash
   source venv/bin/activate
   python3 send-traces.py
   ```
    
## Description

The python script send two traces-- one from a service named `checkout-worker` and the other named `frontend-worker`, both of which have an attribute named `env` with a value of `prod-eus2`.

The expectation is the following:

* the traces do not match Policy #1 (`env-based-sampling-policy`) because `env` does not match any of the listed values,
* the trace with `service.name` == `frontend-worker` **should** match Policy #2 and the trace should always be sampled resulting in it being sent to an exporter.
* the trace with `service.name` == `checkout-worker` **should** match Policy #3 and the trace should always be sampled resulting in it being sent to an exporter.

## Result

Only the trace for the `frontend-worker` (Policy #2) get sent to the exporter. 

## Test cases

Comment out Policy #2 in the collector config, restart and send the trace. The `checkout-worker` trace now gets sampled properly and sent to an exporter.

## Suspicion

It would seem as if a key/value check in *any* policy uses an `invert_match` condition, the key/value pair can't be used in other policies. Note: changing the policy order in the collector config make no difference.