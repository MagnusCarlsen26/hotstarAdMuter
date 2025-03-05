import pandas as pd

def saveToDB( requestId, user_id, imageId, llm_resposne):

    df = pd.read_csv('requestDb/DB.csv')
    new_row = pd.DataFrame({'requestId': [requestId], 'imageId': [imageId], 'llm_response': [llm_resposne]})
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv('requestDb/DB.csv', index=False)

    print("Saved to DB")