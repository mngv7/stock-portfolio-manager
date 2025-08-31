import requests
import time

url = "http://ec2-3-25-228-25.ap-southeast-2.compute.amazonaws.com:5000/api/v1/portfolio/forecast"
numberOfRequests = 500
jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IlphY2siLCJleHAiOjE3NTY2MDczMzZ9.SGfYUuenqeQgSEez9jV63gHg4gLjWMIZHPavmGzadGI"

totalTime = 0

def time_ms():
    return round(time.time() * 1000)

headers = {
    "Authorization": f"Bearer {jwt}"
}

for i in range(numberOfRequests):
    startTime = time_ms()
    response = requests.get(url, headers=headers)
    request_time = time_ms() - startTime
    totalTime += request_time

    print(f'Request {i + 1} returned with status: {response.status_code} in {request_time}ms')

print(f'Average time {totalTime / numberOfRequests} ms')
