import requests
from utils.my_request import MyRequest, TestRequest


request = TestRequest()
# print(request.get_token())

TOKEN = 'XURl7dVqMo04FozQ0itQ4NGmoczv3uvWOGG1QLznzTsBeU3pKJX6ukFoZxdAVKZuAXNwl42CK1IlN0hf8gWIoAA3FGawEUZRe23wfmcY4QgR1CcajJ2MTp68hLUDjSQQ9soCsuTSCOF7NuBlL413Ng4u5ZrLxKtugaPY9y1dQmH6NjTju25ZB0SPgN8apbvhbgNW_nGS6JNTqwCb75Zyhg'

print(request.get_department(TOKEN))

