FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends tesseract-ocr tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

COPY requirements-tools.txt /tmp/requirements-tools.txt
RUN pip install --no-cache-dir -r /tmp/requirements-tools.txt

COPY src/tools /workspace/src/tools

ENV PYTHONPATH=/workspace/src

ENTRYPOINT ["python", "-m", "tools"]
