FROM ubuntu:22.04

RUN apt-get update -y || true; DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    curl \
    libgl1-mesa-glx \
    libglib2.0-0 \
    python3  \
    python3-pip  && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install weaviate-client opencv-python

WORKDIR /images

# Replace REPLACE_WITH_MY_IMAGE_URL with your image URL
RUN curl "REPLACE_WITH_MY_IMAGE_URL" --output item.jpg

WORKDIR /app
COPY img2vec_client.py .

ENTRYPOINT ["/bin/sh", "-c"]
CMD ["python3 /app/img2vec_client.py"]
