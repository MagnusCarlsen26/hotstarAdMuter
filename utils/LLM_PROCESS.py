import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def process_image_classification( imagePath, mime_type="image/png"):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    def upload_to_gemini(path, mime_type=None):
        file = genai.upload_file(path, mime_type=mime_type)
        print(f"Uploaded file '{file.display_name}' as: {file.uri}")
        return file

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction="I am making a program that will classify if a given image is part of a LIVE cricket match or is it an add shown during LIVE match. Your task is to tell me if the image provided is an advertisement or not. Your response shoud have only one of the following words .\n\n1. \"YES\" if the image has only advertisement and no LIVE cricket\n2. \"NO\" if the image doesn't have advertisement.\n3. \"AMBIGUOUS\" if you aren;t sure",
    )

    files = [
        upload_to_gemini( imagePath, mime_type=mime_type),
    ]

    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    files[0],
                ],
            },
        ]
    )

    response = chat_session.send_message("INSERT_INPUT_HERE")

    return response.text