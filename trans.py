#!/usr/bin/env python
#-*- coding: utf-8 -*-
import requests
import json

url = 'https://api.cognitive.microsofttranslator.com//Detect?api-version=3.0'
body =[{"text": "你好"}]
headers = {'Content-Type': 'application/json',"Ocp-apim-subscription-key": "b12776c*****14f5","Ocp-apim-subscription-region": "koreacentral"}
r = requests.post(url, data=json.dumps(body), headers=headers)
result=json.loads(r.text)
a=result[0]["language"]
print(r.text)
print("Language = " + a)