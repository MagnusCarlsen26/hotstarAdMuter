import os
import google.generativeai as genai
from dotenv import load_dotenv
import logging
from utils.constants import SYSTEM_PROMPT
from PIL import Image  # Add Pillow for image processing

load_dotenv()

def resize_image(image_path, max_size=(400, 400), quality=85):
    """
    Resize an image to reduce its file size before sending to API
    
    Args:
        image_path: Path to the image file
        max_size: Maximum dimensions (width, height) for the resized image
        quality: JPEG quality (1-100)
        
    Returns:
        Tuple of (path_to_resized_image, mime_type)
    """
    try:
        img = Image.open(image_path)
        
        # Preserve aspect ratio while resizing
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Create a temporary file path for the resized image
        filename, ext = os.path.splitext(image_path)
        resized_path = f"{filename}_resized{ext}"
        
        # Save with reduced quality
        img.save(resized_path, quality=quality, optimize=True)
        
        # Determine mime type based on extension
        if ext.lower() in ['.jpg', '.jpeg']:
            mime_type = "image/jpeg"
        elif ext.lower() == '.png':
            mime_type = "image/png"
        else:
            mime_type = "image/jpeg"  # Default
            
        logging.info(f"Resized image from {image_path} to {resized_path}")
        return resized_path, mime_type
    except Exception as e:
        logging.error(f"Error resizing image {image_path}: {e}")
        return image_path, "image/png"  # Return original if resize fails

def process_image_classification( imagePath, mime_type="image/png"):

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    def upload_to_gemini(path, mime_type=None):
        logging.info(f"Uploading image to Gemini")
        file = genai.upload_file(path, mime_type=mime_type)
        logging.info(f"Uploaded image to Gemini")
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

    # Resize the image before uploading to reduce network delay
    resized_path, resized_mime_type = resize_image(imagePath)
    
    files = [
        upload_to_gemini(resized_path, mime_type=resized_mime_type),
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