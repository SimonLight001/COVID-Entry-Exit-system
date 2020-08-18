import jwt
import requests
import json
import socket
import time
import os


def get_API_Key_and_auth():
    # Gets public key from spaces and places in correct format
    print("-- No API Key Found --")
    pubKey = requests.get(
        'https://partners.dnaspaces.io/client/v1/partner/partnerPublicKey/')
    pubKey = json.loads(pubKey.text)
    pubKey = pubKey['data'][0]['publicKey']
    pubKey = '-----BEGIN PUBLIC KEY-----\n' + pubKey + '\n-----END PUBLIC KEY-----'

    # Gets user to paste in generated token from app
    token = input('Enter token here: ')

    # Decodes JSON Web Token to get JSON out
    decodedJWT = jwt.decode(token, pubKey)
    decodedJWT = json.dumps(decodedJWT, indent=2)
    # print(decodedJWT)

    # picks up required values out of JWT
    decodedJWTJSON = json.loads(decodedJWT)
    appId = decodedJWTJSON['appId']
    activationRefId = decodedJWTJSON['activationRefId']

    # creates payloads and headers ready to activate app
    authKey = 'Bearer ' + token
    payload = {'appId': appId, 'activationRefId': activationRefId}
    header = {'Content-Type': 'application/json', 'Authorization': authKey}

    # Sends request to spaces with all info about JWT to confirm its correct, if it is, the app will show as activated
    activation = requests.post(
        'https://partners.dnaspaces.io/client/v1/partner/activateOnPremiseApp/', headers=header, json=payload)

    print(activation.text)
    activation = json.loads(activation.text)
    print(activation['message'])

    apiKey = activation['data']['apiKey']
    f = open("API_KEY.txt", "a")
    f.write(apiKey)
    f.close()
    return apiKey


# work around to get IP address on hosts with non resolvable hostnames
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IP_ADRRESS = s.getsockname()[0]
s.close()
url = 'http://' + str(IP_ADRRESS) + '/'

try:
    if os.stat("API_KEY.txt").st_size > 0:
        f = open("API_KEY.txt")
        apiKey = f.read()
        f.close()
        print("-- API Key Found -- ")
        print("-- If you wanted to renew your API key, just delete the file API_KEY.txt --")
    else:
        apiKey = get_API_Key_and_auth()
except:
    apiKey = get_API_Key_and_auth()

s = requests.Session()
s.headers = {'X-API-Key': apiKey}
r = s.get(
    'https://partners.dnaspaces.io/api/partners/v1/firehose/events', stream=True)

for line in r.iter_lines():
    if line:
        decoded_line = line.decode('utf-8')
        event = json.loads(decoded_line)
        # print(str(event))
        eventType = event['eventType']
        if eventType == "USER_PRESENCE":
            location = event['userPresence']['location']['name']
            activeUsers = event['userPresence']['activeUsersCount']['totalUsers']
            if location == "Location - 6861a1f0":
                payload = {'location': location, 'users': str(activeUsers)}
                r = requests.post(url, json=payload)
                print(r.text)
                # would love to run time.sleep here to slow things down, but this kills the stream
