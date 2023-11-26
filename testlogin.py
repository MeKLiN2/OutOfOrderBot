# testlogin.py
import subprocess
import requests
import json
from bs4 import BeautifulSoup
import time
from tokenapi import get_token
from colorama import Fore, Style  # Import colorama for colored printing

# Constants for file paths of saved responses
LOGOUT_HEADERS_FILE_PATH = "logout_headers.json"
LOGOUT_PATH = "logout.txt"
LOGIN_HEADERS_FILE_PATH = "login_headers.json"
LOGIN_PATH = "login.txt"
TOKEN_FILE_PATH = "token.txt"
TOKEN_HEADERS_FILE_PATH = "token_headers.json"
ROOM_NAME_FILE_PATH = "roomname.txt"

def print_colored(message, color):
    print("{}{}{}".format(color, message, Style.RESET_ALL))


# Set the URL for logout
logout_url = "https://tinychat.com/logout"

# Set the headers for logout
logout_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Cookie": "XSRF-TOKEN=eyJpdiI6Im1wT2hGMXNvUktTaE1Ic0lZc3RsREE9PSIsInZhbHVlIjoieHUxTWVlZThMS1cxXC9DRGVpN284NGdQWFNpeU5uRkp2WGtsMFU3cDh2MU1mWFFVMkNCcldodHRvaERoeHJjTnhwTXRMaXZibXBVaWNnRE5Ha1hmTHVRPT0iLCJtYWMiOiJmYTE5NTI0YzQ0MjgyYWFkYzUzYTg2OTYzOWRiMDk4ZmZhY2M3NDRmMDBhYjlkNTljYmJhMjdhMTA0YjhiNmE4In0%3D; tcsession=392371fc18380c7440423a1418a7a9339f8f798b; sm_dapi_session=1; remember_82e5d2c56bdd0811318f0cf078b78bfc=eyJpdiI6Imp2VzJzeU1zMDVHNXN5N0l0TXR3VFE9PSIsInZhbHVlIjoia1M0bFBUbmFYR1dkeU8xWGRvS0xLNlp4b2JFY0R1dDRMS1wvXC9CWVVCTUtqRUhudnZTQmhVTWdtKzlXQm5uNGVYTzd5alJHNFN2RWRGQ25VbGlnVEdzRTlyTVAxTEJ6bVwvSWkrU0NsSFQzRnc9IiwibWFjIjoiNmYxZmJmODMwZmRhYzgwMDc2NDZkYWU2ODdiODNkMzEwZWU3MjVhMzg0YzI2YzQ2ZDk1ZTI4OTg3YjY1OGIxMiJ9; hash=2cb970db9a52c88454a79dfaec59a9dc; user=raise; pass=6e07933fcd8d45b0f3b985c2eb0f52fa",
    "DNT": "1",
    "Host": "tinychat.com",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "TE": "trailers",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0"
}

# Create a session to handle cookies
logout_session = requests.Session()

# Send a POST request to logout
logout_response = logout_session.post(logout_url, headers=logout_headers)

# Save the response headers to file
with open(LOGOUT_HEADERS_FILE_PATH, "w") as headers_file:
    json.dump(dict(logout_response.headers), headers_file)

# Save the response to logout.txt
with open(LOGOUT_PATH, "w") as logout_file:
    logout_file.write(logout_response.text)

# Print in yellow
print_colored("Logged out successfully!", Fore.YELLOW)

# Read username and password from logpass.txt
with open("logpass.txt", "r") as file:
    lines = file.readlines()
    login_username = lines[0].strip()
    login_password = lines[1].strip()

# Set the URL for login
login_url = "https://tinychat.com/login"

# Set the headers
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "DNT": "1",
    "Host": "tinychat.com",
    "Origin": "https://tinychat.com",
    "Referer": "https://tinychat.com/start?",
    "Upgrade-Insecure-Requests": "1",
}

# Create a session to handle cookies
session = requests.Session()

# Function to extract token from the login page
def extract_token(login_page_content):
    soup = BeautifulSoup(login_page_content, "html.parser")
    token_input = soup.find("input", {"name": "_token"})
    if token_input:
        return token_input["value"]
    return None

# Load the login page to extract the token
login_page_response = session.get(login_url)

# Print or save headers to a file
with open(LOGIN_HEADERS_FILE_PATH, "w") as header_file:
    header_file.write(str(login_page_response.headers))

# Extract the token
token = extract_token(login_page_response.content)

# Set the payload data for login
payload = {
    "login_username": login_username,
    "login_password": login_password,
    "remember": "1",
    "next": "",
    "_token": token,
}

# Perform the login
response = session.post(login_url, headers=headers, data=payload, allow_redirects=False)

# Save the response headers to login_headers.json
login_headers = {"Response Headers ({} kB)".format(len(response.headers) / 1024): {"headers": []}}
for header, value in response.headers.items():
    login_headers["Response Headers ({} kB)".format(len(response.headers) / 1024)]["headers"].append({"name": header, "value": value})

with open(LOGIN_HEADERS_FILE_PATH, "w") as headers_file:
    json.dump(login_headers, headers_file, indent=4)

# Save the response to login.txt
with open(LOGIN_PATH, "w") as login_file:
    login_file.write(response.text)


# Save the response to log.txt
with open(LOGIN_PATH, "w") as login_file:
    login_file.write(response.text)

# Check if the login was successful (status code 302 indicates redirection)
if response.status_code == 302:
    print("Login successful")
    
    # Wait for 5 seconds before requesting API token...
    print("Waiting for 5 seconds before requesting API token...")
    time.sleep(5)
    
    # Use subprocess.Popen to run wss.py in the background
    subprocess.Popen(["python", "wss.py"])

    # You can print or use the response.headers to get additional information
    print("Headers:", response.headers)

    # Save cookies and other information for future use in tokenapi.py
    with open(TOKEN_FILE_PATH, "w") as token_file:
        token_file.write(str(session.cookies.get_dict()))
        # Add other information you may need from the response.headers
else:
    print("Login failed. Status code:", response.status_code)
    print("Response content:", response.text)



# Run tokenapi.py to get the token
token = get_token()

# Save the token to a file (optional)
with open("token.txt", "w") as file:
    file.write(token)

