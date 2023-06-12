import requests

headers={"X-OTX-API-KEY":"56d28c0e6e2ac43bd75cd33620fb699b99d38156543ca201d4ca2bf095faf699"}
url="https://otx.alienvault.com/api/v1/pulses/subscribed"
re=requests.get(url,headers=headers)
print(re.text)

a=open("file1.json","w")
a.write(re.text)