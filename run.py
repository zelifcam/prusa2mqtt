#!/usr/bin/env python3
import json
import os
import sys
import random
import time
import paho.mqtt.client as mqtt_client
import requests
from requests.auth import HTTPDigestAuth
from dotenv import load_dotenv
from datetime import datetime

# Uncomment for local development
#load_dotenv()

# Generate Random MQTT Client ID
MQTT_CLIENT_ID = f'curl2mqtt-{random.randint(0, 1000)}'

# Get environment variables
APP_VERSION = os.getenv('APP_VERSION')

MQTT_HOST = os.getenv('MQTT_HOST')
MQTT_PORT = int(os.getenv('MQTT_PORT'))
MQTT_USER = os.getenv('MQTT_USER')
MQTT_PASS = os.getenv('MQTT_PASS')

PRUSALINK_HOST = os.getenv('PRUSALINK_HOST')
PRUSALINK_USER = os.getenv('PRUSALINK_USER')
PRUSALINK_PASS = os.getenv('PRUSALINK_PASS')
PRUSALINK_CALLS = os.getenv('PRUSALINK_CALLS')
PRUSALINK_UPDATE = int(os.getenv('PRUSALINK_UPDATE'))

def print_to_stdout(*a):
    print(*a, file=sys.stderr)

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print_to_stdout("Connected to MQTT Broker!")
        else:
            print_to_stdout("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(f'pi-sensor-{random.randint(0, 1000)}')
    client.username_pw_set(username=MQTT_USER,password=MQTT_PASS)
    client.on_connect = on_connect
    client.connect(MQTT_HOST,MQTT_PORT)
    return client


def get_request(call):
    # Create a session
    s = requests.Session()

    # Make a request to the endpoint with digest authentication
    if call == "version":
        call_path = call
    else:
        call_path = "v1/"+call

    response = requests.get(PRUSALINK_HOST+"/api/"+call_path, verify=False, auth=HTTPDigestAuth(PRUSALINK_USER, PRUSALINK_PASS))

    return response

def iterate_json(obj,serial,client):
    stack = [(obj, '')]  # Stack to keep track of objects and their paths

    while stack:
        current_obj, path = stack.pop()
        if isinstance(current_obj, dict):  # If object is a dictionary
            for key, value in current_obj.items():
                new_path = f'{path}/{key}' if path else key
                stack.append((value, new_path))
        elif isinstance(current_obj, list):  # If object is a list
            for index, value in enumerate(current_obj):
                new_path = f'{path}[{index}]'
                stack.append((value, new_path))
        else:  # If object is a leaf node
            # debug
            #print(f'{path}: {current_obj}')
            client.publish("prusa2mqtt/"+serial+"/"+path, current_obj)

def publish(client,count):

    # Timestamp
    TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # forced delay
    time.sleep(PRUSALINK_UPDATE)

    # get serial
    printer = json.loads(get_request("info").text)
    serial = printer['serial']
    print(PRUSALINK_CALLS)

    for call in PRUSALINK_CALLS.split(","):
        data = json.loads(get_request(call).text)
        # LOG
        print_to_stdout(TIMESTAMP,data)
        # Publish
        print(data,serial,client)
        print(iterate_json(data,serial,client))
        client.publish("prusa2mqtt/"+serial+"/json/"+call,str(data))

def run():
    # Start LOG Header
    print_to_stdout("-=-=-=-")
    print_to_stdout("|",APP_VERSION,"|")
    print_to_stdout("-=-=-=-")

    # Uncomment to DEBUG
    # print_to_stdout(os.environ)

    # connect to MQTT server
    client = connect_mqtt()
    client.loop_start()

    # MQTT Publish
    while True:
        try:
            publish(client,count=0)
        except Exception as e:
            print_to_stdout("An error occurred:", str(e))
            continue
 
if __name__ == '__main__':
    run()
