import weaviate
import os
import cv2
import uuid
import base64


TEST_DATA_DIR = "/images/"
DATA_DIR = "/images/"

def _prepare_image(file_path):
    img = cv2.imread(file_path)
    return img

def insert_data(client):
    for file_name in os.listdir(DATA_DIR):
        file_path = os.path.join(DATA_DIR, file_name)
        print(file_path)
        img = _prepare_image(file_path)        
        jpg_img = cv2.imencode('.jpg', img)
        b64_string = base64.b64encode(jpg_img[1]).decode('utf-8')
        # define properties as expected by the class definition
        data_properties = {
            "path": file_name,
            "image": b64_string,
        }
    # create data of type "ProductItem" with a random UUID
    r = client.data_object.create(data_properties, "ProductItem", str(uuid.uuid4()))
    print(file_path, r)

def define_schema(client):
    class_obj = {
       "class": "ProductItem",
       "description": "ProductItem with an image blob and a path to the image file",  
       "properties": [
            {
                "dataType": [
                    "blob"
                ],
                "description": "Image",
                "name": "image"
            },
            {
                "dataType": [
                    "string"
                ],
                "description": "",
                "name": "path"
            }
            
        ],
        "vectorIndexType": "hnsw",
        "moduleConfig": {
            "img2vec-neural": {
                "imageFields": [
                    "image"
                ]
            }
        },
        "vectorizer": "img2vec-neural"
    }
    return class_obj


def search(client, image_path):

    nearImage = {"image": image_path}
    res = (
     client.query
      .get("ProductItem", "path")
      .with_near_image(nearImage)
      .with_limit(3) # Top 5 best matches
      .do()
    )

    # return res["data"]["Get"]["ProductItem"]
    return res


client = weaviate.Client("http://localhost:8080")

init_database = os.getenv("INIT_DATABASE")
if init_database == "1":
  print ("Adding default database vector info and schema/etc...")
  class_obj = define_schema(client)
  client.schema.create_class(class_obj)
  insert_data(client)
  quit()

test_image = os.path.join(TEST_DATA_DIR, "item.jpg")

res = search(client, test_image)
print(res)


