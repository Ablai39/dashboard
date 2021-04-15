import requests
import traceback
from dashboard.data.variables import successful

url = 'https://ailabs.halykbank.kz:3001/monitorfunc?action=getCurrentStats&lastSeconds=3600'

def getData():

    try:
        responseString = requests.get(url=url, timeout=3)
        responseJson = responseString.json()
        return {
            'data': responseJson,
            'status': successful
        }

    except Exception:
        return {'status': traceback.format_exc()}
