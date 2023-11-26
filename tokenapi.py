# tokenapi.py
import time
import requests
import json
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama
init()

# Constants for file paths of saved responses
LOGOUT_HEADERS_FILE_PATH = "logout_headers.json"
LOGOUT_PATH = "logout.txt"
LOGIN_HEADERS_FILE_PATH = "login_headers.json"
LOGIN_PATH = "login.txt"
TOKEN_HEADERS_FILE_PATH = "token_headers.json"
TOKEN_FILE_PATH = "token.txt"
ROOM_HEADERS_FILE_PATH = "room_response.json"
ROOM_FILE_PATH = "room.txt"

# Function to get headers from a file
def get_headers_from_file(file_path):
    with open(file_path, "r") as file:
        headers_data = json.load(file)
        return headers_data.get("headers", {})

time.sleep(5)

# Read the room name from the file
with open(ROOM_NAME_FILE_PATH, "r") as room_file:
    room_name = room_file.read().strip()

# Construct the URL for the Tinychat room
room_url = "https://tinychat.com/" + room_name

def get_token():
    # Logic to obtain the token
    # For the purpose of this example, let's assume the token is obtained as follows:
    token = "b3ae169001fb5ee487ec3a361f7977647d8e3db1"
    return token

# Get the headers from the login session
login_headers = get_headers_from_file(LOGIN_HEADERS_FILE_PATH)

# Get the current datestamp
current_datestamp = datetime.now().strftime("%a+%b+%d+%Y+%H%%3A%M%%3A%S+GMT%z")

# Set the headers for the new request
website_headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Cookie": login_headers.get("Set-Cookie", ""),
    "DNT": "1",
    "Host": "tinychat.com",
    "Referer": room_url,
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "TE": "trailers",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
}

# Print the request details in colorama lime
print(Fore.LIGHTGREEN_EX + "Sending request to Tinychat room:", room_url)
print("Headers:", website_headers)
print(Style.RESET_ALL)  # Reset color after printing

# Make the website request
try:
    website_response = requests.get(room_url, headers=room_headers)
except Exception as e:
    print(Fore.RED + "Error making website request:", e)
    print(Style.RESET_ALL)
    raise  # Re-raise the exception after printing the error

# Print the website response headers and content regardless of the status code
print(Fore.CYAN + "Website Response Headers:", dict(website_response.headers))
print("Website Response Content:", website_response.text)


# Save website response headers and cookies to a file
if website_response.status_code == 200:
    try:
        website_data = {
            "headers": dict(website_response.headers),
            "cookies": website_response.cookies.get_dict(),
            "content": website_response.text
        }
        with open(WEBSITE_RESPONSE_FILE_PATH, "w") as file:
            json.dump(website_data, file)
        print(Fore.LIGHTGREEN_EX + "Website Response Headers saved to '{}'".format(WEBSITE_RESPONSE_FILE_PATH))
    except ValueError as ve:
        # Print the error message if JSON decoding fails
        print(Fore.RED + "Error parsing JSON:", ve)
        print(Style.RESET_ALL)
    except Exception as e:
        # Print any other exceptions that may occur
        print(Fore.RED + "Error:", e)
        print(Style.RESET_ALL)
else:
    print(Fore.RED + "Website request failed. Status code:", website_response.status_code)
    print(Style.RESET_ALL)

# Set the URL for the API request
api_url = "https://tinychat.com/api/v1.0/room/token/cancers"

# Set the headers for the API request
api_headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Cookie": login_headers.get("Set-Cookie", ""),  # Corrected line
    "DNT": "1",
    "Host": "tinychat.com",
    "Referer": room_url,
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "TE": "trailers",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
}

# Print the request details in colorama lime
print(Fore.GREEN + "Sending API request to:", api_url)
print("Headers:", api_headers)
print(Style.RESET_ALL)  # Reset color after printing

# Make the API request
try:
    api_response = requests.get(api_url, headers=room_headers)
except Exception as e:
    print(Fore.RED + "Error making API request:", e)
    print(Style.RESET_ALL)
    raise  # Re-raise the exception after printing the error

# Print the API response headers and content regardless of the status code
print(Fore.CYAN + "API Response Headers:", dict(api_response.headers))
print("API Response Content:", api_response.text)

# Save API response headers and cookies to a file
if api_response.status_code == 200:
    try:
        api_data = {
            "headers": dict(api_response.headers),
            "cookies": api_response.cookies.get_dict(),
            "content": api_response.text
        }
        with open(TOKEN_HEADERS_FILE_PATH, "w") as file:
            json.dump(api_data, file)

        # Attempt to decode the content as JSON
        api_json_data = api_response.json()
        print(Fore.GREEN + "API Token:", api_json_data.get("result"))
        print("API Endpoint:", api_json_data.get("endpoint"))
        print("API Token and Headers saved to '{}'".format(TOKEN_HEADERS_FILE_PATH))
    except ValueError as ve:
        # Print the error message if JSON decoding fails
        print("Error parsing JSON:", ve)
    except Exception as e:
        # Print any other exceptions that may occur
        print("Error:", e)
else:
    print(Fore.RED + "API request failed. Status code:", api_response.status_code)



# Check if the API request was successful (status code 200)
if api_response.status_code == 200:
    try:
        # Attempt to decode the content as JSON
        api_data = api_response.json()
        print("API Token:", api_data.get("result"))
        print("API Endpoint:", api_data.get("endpoint"))

        # Save WebSocket details to a file
        wss_details = {
            "token": api_data.get("result"),
            "endpoint": api_data.get("endpoint")
        }
        with open("wss_details.json", "w") as file:
            json.dump(wss_details, file)

    except ValueError as ve:
        # Print the error message if JSON decoding fails
        print(Fore.RED + "Error parsing JSON:", ve)
        print(Style.RESET_ALL)
    except Exception as e:
        # Print any other exceptions that may occur
        print(Fore.RED + "Error:", e)
        print(Style.RESET_ALL)
else:
    print(Fore.RED + "API request failed. Status code:", api_response.status_code)
    print(Style.RESET_ALL)

