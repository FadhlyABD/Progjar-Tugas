import socket
import json
import base64
import logging

server_address = ('0.0.0.0', 7878)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"Connecting to {server_address}")
    try:
        logging.warning("Sending message")
        sock.sendall((command_str + "\r\n\r\n").encode())
        received_data = ""
        while True:
            data = sock.recv(1024)
            if data:
                received_data += data.decode()
                if "\r\n\r\n" in received_data:
                    break
            else:
                break
        result = json.loads(received_data.strip())
        logging.warning("Data received from server:")
        return result
    except Exception as e:
        logging.warning(f"Error during data receiving: {e}")
        return None
    finally:
        sock.close()

def list_files():
    command_str = "LIST"
    result = send_command(command_str)
    if result and result['status'] == 'OK':
        print("File list:")
        for filename in result['data']:
            print(f"- {filename}")
        return True
    else:
        print("Failed")
        return False

def get_file(filename=""):
    command_str = f"GET {filename}"
    result = send_command(command_str)
    if result and result['status'] == 'OK':
        file_name = result['filename']
        file_content = base64.b64decode(result['file_content'])
        with open(file_name, 'wb+') as file:
            file.write(file_content)
        return True
    else:
        print("Failed")
        return False

def upload_file(filepath=""):
    try:
        with open(filepath, 'rb') as file:
            file_data = base64.b64encode(file.read()).decode()
        filename = filepath.split('/')[-1]
        command_str = f"UPLOAD {filename} {file_data}"
        result = send_command(command_str)
        if result and result['status'] == 'OK':
            print(f"File {filename} uploaded successfully.")
            return True
        else:
            print("Failed")
            return False
    except FileNotFoundError:
        print("File not found")
        return False

def delete_file(filename=""):
    command_str = f"DELETE {filename}"
    result = send_command(command_str)
    if result and result['status'] == 'OK':
        print(f"File {filename} deleted successfully.")
        return True
    else:
        print("Failed")
        return False

if __name__ == '__main__':
    server_address = ('127.0.0.1', 7878)

    while True:
        print("\nOptions:")
        print("1. List files")
        print("2. Get file")
        print("3. Upload file")
        print("4. Delete file")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            list_files()
        elif choice == '2':
            filename = input("Enter the filename to get: ")
            get_file(filename)
        elif choice == '3':
            filepath = input("Enter the full path of the file to upload: ")
            upload_file(filepath)
        elif choice == '4':
            filename = input("Enter the filename to delete: ")
            delete_file(filename)
        elif choice == '5':
            break
        else:
            print("Invalid choice, please try again.")
