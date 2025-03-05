import pandas as pd
from datetime import datetime

def saveToDB( requestId, user_id, imageId, llm_resposne):

    df = pd.read_csv('requestDb/DB.csv')
    new_row = pd.DataFrame({'requestId': [requestId], 'user_id': [user_id], 'imageId': [imageId], 'timestamp': [datetime.now()], 'llm_response': [llm_resposne]})
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv('requestDb/DB.csv', index=False)