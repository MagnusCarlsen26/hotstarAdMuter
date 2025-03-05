UPLOAD_FOLDER = 'imageDb'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

USER_ID = "Local User"

SYSTEM_PROMPT = """
You are a cricket expert. You are given a image and you need to tell if the image is part of a LIVE cricket match or is it an add shown during LIVE match.
Your task is to tell me if the image provided is an advertisement or not. Your response shoud have only one of the following words.
1. "YES" if the image has only advertisement and no LIVE cricket
2. "NO" if the image doesn't have advertisement.
3. "AMBIGUOUS" if you aren't sure
"""