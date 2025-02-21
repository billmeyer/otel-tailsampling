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