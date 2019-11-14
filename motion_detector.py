from gpiozero import MotionSensor
from time import sleep
import requests
import json

#OUT pin on the PIR Sensor is configured to be connected to the 4th numbered GPIO pin on the Pi
pir = MotionSensor(4)

'''
    All the data required by the back end to make get and put requests to the endpoint
'''
API_ENDPOINT = "http://169.254.140.236:8000/counters"
COUNTER_NAME = "Dog Park"
PUT_REQUEST_PAYLOAD = {"name": "Dog Park"}
PUT_REQUEST_HEADERS = {"Content-Type": "application/json"}

# Grabbing the relevant counter and its most recent count to start the recursive function from
response = requests.get(API_ENDPOINT)
counters = json.loads(response.text)
counter_dict = [obj for obj in counters if obj['name'] == COUNTER_NAME][0]
count = counter_dict['count']

'''
    This recursive function simply waits for motion to be detected, then motion to cease, and sends a put request
    to the server holding the counter data.  The initial count is grabbed from the server.
'''
def increment_counter_recursive(count = count):
    pir.wait_for_motion()
    sleep(1)
    pir.wait_for_no_motion()
    response = requests.put(API_ENDPOINT, data=json.dumps(PUT_REQUEST_PAYLOAD), headers=PUT_REQUEST_HEADERS)
    response_dict = json.loads(response.text)
    print(response_dict)
    count += 1
    print(count)
    increment_counter_recursive(count)
increment_counter_recursive()