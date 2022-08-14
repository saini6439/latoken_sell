from this import d
import requests
import hashlib
from datetime import datetime
import hmac
from config import settings
import time
from sell_new_order import sell_order

apiKey = settings.apiKey
apiSecret = str.encode(settings.apiSecret)
baseUrl = 'https://api.latoken.com'
endpoint = '/v2/auth/trade'


#https://api.latoken.com/v2/auth/stopOrder/place

def get_orders():      
    params = {
    'from': int(datetime.now().timestamp()*1000),
    'limit': '100'
    }
    serializeFunc = map(lambda it : it[0] + '=' + str(it[1]), params.items())
    queryParams = '&'.join(serializeFunc)
                    
    signature = hmac.new(
        apiSecret, 
        ('GET' + endpoint + queryParams).encode('ascii'), 
        hashlib.sha512
    )

    url = baseUrl + endpoint + '?' + queryParams

    response = requests.get(
        url,
        headers = {
            'X-LA-APIKEY': apiKey,
            'X-LA-SIGNATURE': signature.hexdigest(),
            'X-LA-DIGEST': 'HMAC-SHA512'
        }
    )
    # print(response.json())
    # send_sms(str(response.json()))
    return response.json()
        # print("10X",price_token_5,price_token_10,price_token_20,price_token_50,price_token_100,data.get("id"),data.get("filled"))

while True:
    print("while called")
    response_result = get_orders()
    for data in response_result:
        # print(data)
        dt_obj = datetime.fromtimestamp(data.get('timestamp')/1000)
        duration = datetime.now() - dt_obj
        duration_in_s = duration.total_seconds()
        if(data.get("direction")=="TRADE_DIRECTION_BUY") and int(duration_in_s)<10:
            print("date_time:",int(duration_in_s))
            print(float(data.get("quantity")),data.get("price"))
            quantity = round((float(data.get("quantity"))*20)/100,2)
            print(quantity)
            baseCurrency = data['baseCurrency']
            quoteCurrency = data['quoteCurrency']
            # print((int(datetime.datetime.now().timestamp())*1000)-)
            # print(data.get('timestamp'))
            price_token = float(data.get("price"))
            price_token_5 = round(price_token*5,9) # 20%
            price_token_10 = round(price_token*10,9) # 20%
            price_token_20 = round(price_token*20,9) # 20%
            price_token_50 = round(price_token*50,9) # 20%
            price_token_100 = round(price_token*100,9) # 20%
            sell_order(baseCurrency,quoteCurrency,price_token_5,quantity)
            sell_order(baseCurrency,quoteCurrency,price_token_10,quantity)
            sell_order(baseCurrency,quoteCurrency,price_token_20,quantity)
            sell_order(baseCurrency,quoteCurrency,price_token_50,quantity)
            sell_order(baseCurrency,quoteCurrency,price_token_100,quantity)


    time.sleep(10)
    