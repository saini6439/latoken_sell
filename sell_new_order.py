import requests
import datetime
import hashlib
import hmac
from config import settings

apiKey = settings.apiKey
apiSecret = str.encode(settings.apiSecret)
baseUrl = 'https://api.latoken.com'
endpoint = '/v2/auth/order/place'

#https://api.latoken.com/v2/auth/stopOrder/place

def sell_order(baseCurrency,quoteCurrency,price,quantity):
    print(round(price,10))
    params = {
            'baseCurrency': baseCurrency,
            'quoteCurrency': quoteCurrency,
            'side': 'SELL',
            'condition': 'GOOD_TILL_CANCELLED',
            'type': 'LIMIT',
            'clientOrderId': 'mobile-Android_1.97.02',
            'price': price,
            'quantity': quantity,
            'timestamp': int(datetime.datetime.now().timestamp()*1000)
        }
    serializeFunc = map(lambda it : it[0] + '=' + str(it[1]), params.items())
    bodyParams = '&'.join(serializeFunc)
                    
    signature = hmac.new(
        apiSecret, 
        ('POST' + endpoint + bodyParams).encode('ascii'), 
        hashlib.sha512
    )

    url = baseUrl + endpoint

    response = requests.post(
        url,
        headers = {
            'Content-Type': 'application/json',
            'X-LA-APIKEY': apiKey,
            'X-LA-SIGNATURE': signature.hexdigest(),
            'X-LA-DIGEST': 'HMAC-SHA512'
        },
        json = params
    )
    print(response.json())
    # send_sms(str(response.json()))
    return response.json()
