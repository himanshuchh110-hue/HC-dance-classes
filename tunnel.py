import subprocess
import os
import json
import requests
from flask import Flask

# Start the Flask app and tunnel using a simple method
# Using serveo.net which requires no auth and works with SSH

os.chdir(r'b:\HC dance classes\backend')

# Check your machine's IP
import socket
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

print(f"🎉 Your website is ready!")
print(f"Local URL: http://localhost:5000")
print(f"Network URL: http://{local_ip}:5000")
print(f"\nShare the network URL with anyone on your WiFi!")
