import requests
import time

url = "http://ec2-3-27-35-211.ap-southeast-2.compute.amazonaws.com:8080/portfolio/assets"
numberOfRequests = 500
jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IlphY2siLCJleHAiOjE3NTYwMzc4MDl9.-zSYqnOIfTueRQ-CCzq28QnX6O5WgHPi5mlTRv-lvu8"

totalTime = 0

def time_ms():
    return round(time.time() * 1000)

headers = {
    "Authorization": f"Bearer {jwt_token}"
}

for i in range(numberOfRequests):
    startTime = time_ms()
    response = requests.get(url, headers=headers)
    request_time = time_ms() - startTime
    totalTime += request_time

    print(f'Request {i + 1} returned with status: {response.status_code} in {request_time}ms')

print(f'Average time {totalTime / numberOfRequests} ms')
