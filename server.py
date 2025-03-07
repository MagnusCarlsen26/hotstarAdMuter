import os
import uuid
import logging
import traceback
import base64

from flask import Flask, request, jsonify

from utils.LLM_PROCESS import process_image_classification
from utils.constants import UPLOAD_FOLDER
from utils.saveToDB import saveToDB

logging.basicConfig(
    filename=f"logs/logs.txt",
    format="%(asctime)s - %(levelname)s - %(funcName)s  - %(message)s - %(filename)s - %(lineno)d",
    datefmt="%H:%M:%S",
    level=logging.INFO,
    filemode="w"
)

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_image():

    logging.info(f"Upload image request received")

    try:

        if request.is_json:
            data = request.get_json()
            
            if 'imageData' not in data:
                return jsonify({'error': 'No image data in the request'}), 400
            
            requestId = str(uuid.uuid4())
            imageId = str(uuid.uuid4()) + ".png"
            
            logging.info(f"JSON request received: requestId: {requestId} imageId: {imageId}")
            
            try:
                image_data = data['imageData']

                if image_data.startswith('data:image'):
                    image_data = image_data.split(',')[1]
                
                image_bytes = base64.b64decode(image_data)
                imagePath = os.path.join(UPLOAD_FOLDER, imageId)
                
                with open(imagePath, 'wb') as f:
                    f.write(image_bytes)
                    
            except Exception as e:
                logging.error(f"Error decoding base64 image: {str(e)}")
                return jsonify({'error': 'Invalid image data'}), 400
        
        else:
            if 'image' not in request.files:
                return jsonify({'error': 'No image part in the request'}), 400
            
            file = request.files['image']
            
            if file.filename == '':
                return jsonify({'error': 'No image selected for uploading'}), 400

            requestId = str(uuid.uuid4())
            imageId = str(uuid.uuid4()) + ".png"

            logging.info(f"File received: requestId: {requestId} imageId: {imageId}")

            imagePath = os.path.join(UPLOAD_FOLDER, imageId)
            file.save(imagePath)
        
        llm_response = process_image_classification(imagePath)
        
        saveToDB(requestId, "local_user", imageId, llm_response)
        
        logging.info(f"File processed: requestId: {requestId} imageId: {imageId} result: {llm_response}")
        
        return jsonify({'result': llm_response}), 200

    except Exception as e:
        logging.error(f"Error: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)