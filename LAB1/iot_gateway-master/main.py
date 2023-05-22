print("IOT gateway")
print("Xin chào ThingsBoard")
import paho.mqtt.client as mqttclient
import time
import json
import geocoder
import random

BROKER_ADDRESS = "demo.thingsboard.io"
PORT = 1883
THINGS_BOARD_ACCESS_TOKEN = "5ROY8XpEiwZCHRpLeVmg"
# 5ROY8XpEiwZCHRpLeVmg
# 7b2juGR8vWVGb5iKWLP7
def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")


def recv_message(client, userdata, message):
    print("Received: ", message.payload.decode("utf-8"))
    temp_data = {'value': True}
    try:
        jsonobj = json.loads(message.payload)
        if jsonobj['method'] == "setValue":
            temp_data['value'] = jsonobj['params']
            client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
    except:
        pass


def connected(client, usedata, flags, rc):
    if rc == 0:
        print("Thingsboard connected successfully!!")
        client.subscribe("v1/devices/me/rpc/request/+")
    else:
        print("Connection is failed")


client = mqttclient.Client("Gateway_Thingsboard")
client.username_pw_set(THINGS_BOARD_ACCESS_TOKEN)

client.on_connect = connected
client.connect(BROKER_ADDRESS, 1883)
client.loop_start()

client.on_subscribe = subscribed
client.on_message = recv_message

temp = 30
humi = 50
light_intesity = 100
longitude = 106.6297
latitude = 10.8231
counter = 0


g = geocoder.ip('me')

print(g.latlng)
# g.latlng[1] long
# g.latlng[0] lat
while True:
    temp = random.randint(-31,30)
    humi = random.randint(-1,100)
    collect_data = {'temperature': temp, 'humidity': humi, 'light':light_intesity,
                    'longitude':g.latlng[1], 'latitude':g.latlng[0]}
    # temp += 1
    # humi += 1
    light_intesity += 1
    client.publish('v1/devices/me/telemetry', json.dumps(collect_data), 1)
    time.sleep(10)

## Retrieve address from geography coordinates
# import reverse_geocoder as rg
# def reverseGeocode(coordinates):
#     result = rg.search(coordinates)
#     print(result)
#
# coordinates = (16.8163, 107.1003)
#
# reverseGeocode(coordinates)
