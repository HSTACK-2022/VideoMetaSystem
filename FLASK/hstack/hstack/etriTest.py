
#-*- coding:utf-8 -*-
import urllib3
import json
 
openApiURL = "http://aiopen.etri.re.kr:8000/WiseQAnal"
accessKey = "YOUR_ACCESS_KEY"
text = "운영체제의 개념"
 
requestJson = {
    "access_key": "40c498a8-7d33-4909-9b60-427b3d0ccf8b",
    "argument": {
        "text": text
    }
}
 
http = urllib3.PoolManager()
response = http.request(
    "POST",
    openApiURL,
    headers={"Content-Type": "application/json; charset=UTF-8"},
    body=json.dumps(requestJson)
)
 
print("[responseCode] " + str(response.status))
print("[responBody]")
print(str(response.data,"utf-8"))