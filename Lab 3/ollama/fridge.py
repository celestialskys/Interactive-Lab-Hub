import requests
import json

response = requests.post('http://localhost:11434/api/generate',
    json={
        "model": "qwen2.5:0.5b-instruct",
        "prompt": "Why is the sky blue?",
        "stream": False
    })

print(response.json()['response'])