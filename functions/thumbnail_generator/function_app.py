import azure.functions as func
import logging
from io import BytesIO
from PIL import Image
from azure.storage.blob import BlobServiceClient
import os

app = func.FunctionApp()

@app.blob_trigger(arg_name="myblob",
                  path="originals/{name}",
                  connection="BUSINESS_STORAGE_CONNECTION_STRING")
def thumbnail_generator(myblob: func.InputStream):
    logging.info(f"Processing blob: {myblob.name}, Size: {myblob.length} bytes")

    try:
        # read image from blob
        img_data = myblob.read()
        img = Image.open(BytesIO(img_data))

        # generate thumbnail (150x150)
        img.thumbnail((150, 150), Image.Resampling.LANCZOS)

        # save to bytes
        output = BytesIO()
        img_format = img.format if img.format else 'JPEG'
        img.save(output, format=img_format)
        output.seek(0)

        # upload to thumbnails container
        connection_string = os.environ["BUSINESS_STORAGE_CONNECTION_STRING"]
        blob_service = BlobServiceClient.from_connection_string(connection_string)

        # extract filename from path
        filename = myblob.name.split('/')[-1]

        # upload to thumbnails container
        blob_client = blob_service.get_blob_client(
            container="thumbnails",
            blob=filename
        )

        blob_client.upload_blob(output.getvalue(), overwrite=True)

        logging.info(f"Thumbnail created successfully: {filename}")

    except Exception as e:
        logging.error(f"Error processing blob: {str(e)}")
        raise
