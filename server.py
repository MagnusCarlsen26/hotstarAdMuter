import os
import uuid
import logging
import traceback

from flask import Flask, request
from werkzeug.utils import secure_filename

from utils.LLM_PROCESS import process_image_classification
from utils.constants import UPLOAD_FOLDER
from utils.saveToDB import saveToDB

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=f"/logs/logs.txt",
    format="%(asctime)s - %(levelname)s - %(funcName)s  - %(message)s - %(filename)s - %(lineno)d",
    datefmt="%H:%M:%S",
    level=logging.INFO,
    filemode="w"
)

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_image():

    try :
        print("IH")
        if 'image' not in request.files:
            return {'error': 'No image part in the request'}, 400
        
        file = request.files['image']
        
        if file.filename == '':
            return {'error': 'No image selected for uploading'}, 400


        requestId = str(uuid.uuid4())
        imageId = str(uuid.uuid4()) + ".png"

        logging.info(f"File received: requestId: {requestId} imageId: {imageId}")

        imagePath = os.path.join(UPLOAD_FOLDER, imageId)

        file.save(imagePath)

        llm_resposne = process_image_classification( imagePath )

        saveToDB( requestId, "local_user", imageId, llm_resposne)

        logging.info(f"File processed: requestId: {requestId} imageId: {imageId} result: {llm_resposne}")

        return {'result': llm_resposne}, 200

    except Exception as e:

        logging.error(f"Error: {traceback.format_exc()}")
        return {'error': str(e)}, 500

if __name__ == '__main__':

    app.run(debug=True)