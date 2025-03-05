import os
import google.generativeai as genai
from dotenv import load_dotenv
import logging
from utils.constants import SYSTEM_PROMPT

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
        system_instruction=SYSTEM_PROMPT,
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

    response = chat_session.send_message("Give your opinion")

    if "YES" in response.text:
        return "YES"
    elif "NO" in response.text:
        return "NO"
    else:
        logging.error(f"LLM returned unexpected response: {response.text}, imagePath: {imagePath}")
        return "AMBIGUOUS"