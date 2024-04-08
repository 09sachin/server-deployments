import socket
import os
import subprocess

def execute_bash_script(script_path):
    try:
        subprocess.run(['bash', script_path], check=True)
        print("Bash script executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing bash script: {e}")


def read_env_file(filename):
    env_vars = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    return env_vars 

def create_response(script):
    execute_bash_script(script)
    response = """HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<h1>Deployment done!</h1>"""
    return response.encode('utf-8')

def parse_headers(request):
    headers = {}
    lines = request.split('\r\n')
    for line in lines[1:]:
        if line.strip():  # Ignore empty lines
            key, value = line.split(': ', 1)
            headers[key] = value
    return headers

def run_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    env = read_env_file('.env')

    print(f"Server listening on {host}:{port}")

    while True:
        client_conn, client_addr = server_socket.accept()
        print(f"Connection from {client_addr}")

        request = client_conn.recv(1024).decode('utf-8')
        print("Received:", request)

        headers = parse_headers(request)
        url = request.split()[1]
        client_id = headers.get('Client-ID')
        client_secret = headers.get('Client-Secret')
        id = env.get('ClientId')
        secret = env.get('ClientSecret')
        script_path = env.get('ScriptPath')

        if client_id!=id  or client_secret!=secret:
            response = """HTTP/1.1 400 Bad Request\r\nContent-Type: text/html\r\n\r\n<h1>Client ID or Client Secret missing</h1>"""
            response = response.encode('utf-8')
        elif  url == env['SecretUrl']:
            response = create_response(script_path)
        else:
            response = """HTTP/1.1 400 Bad Request\r\nContent-Type: text/html\r\n\r\n<h1>Page missing</h1>"""
            response = response.encode('utf-8')
        print(response)
        client_conn.sendall(response)
        client_conn.close()

if __name__ == "__main__":
    HOST = '127.0.0.1'  # Localhost
    PORT = 8080
    run_server(HOST, PORT)
