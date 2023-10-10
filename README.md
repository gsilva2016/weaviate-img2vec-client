# Weaviate img2vec client in a Docker Container


## Prerequisites

* Weaviate Resnet-50 Model Container with Intel GPU Support

  Follow the instructions to build and run the Weaviate Resnet-50 img2vec model container provided in
  ```
  https://github.com/gsilva2016/i2v-pytorch-models
  ```
  
* Weaviate FastAPI/Uvicorn Web Server Container

  Execute the below to start the Weaviate web service to listen for future weaviate client requests.

  ```
  docker run -it --net host -v `pwd`/data:/data -e QUERY_DEFAULTS_LIMIT=20 -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED="true" -e PERSISTENCE_DATA_PATH="/data" -e ENABLE_MODULES="img2vec-neural" -e DEFAULT_VECTORIZER_MODULE="img2vec-neural" -e IMAGE_INFERENCE_API="http://127.0.0.1:8000" semitechnologies/weaviate:1.21.5
  ```

* Optional Step - Monitor Intel GPU Usage for Intel Flex, Intel Arc, Intel integrated GPU (iGPU)
  * Refer to https://github.com/gsilva2016/docker-intel-gpu-telegraf and load the dashboard for the GPU to monitor such as Arc, Flex, or integrated gpu (iGPU)

## Weaviate Client via Docker Container

Please perform the above steps before proceeding.

### Build Docker Image
*  Open the Dockerfile and replace "REPLACE_WITH_MY_IMAGE_URL" with a URL to your test image. The image will be downloaded and used for the feature vector extraction.
*  ```
   ./build.sh
   ```

### Add database information for the feature search when comparing results against upcoming requests.  Only perform this step once.
```
INIT_DATABASE=1 ./run-client.sh
```

### Perform vector feature extraction inference and perform feature search
```
./run-client.sh
```

or repeat 10 times

```
./run-client.sh 10
```
