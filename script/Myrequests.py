import requests
from utils.my_request import MyRequest


request = MyRequest()
if not request.Token:
    request.get_token()
    print(request.Token.json())
else:
    print(request.Token.json())