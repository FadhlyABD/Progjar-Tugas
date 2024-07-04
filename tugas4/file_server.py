from socket import *
import socket
import threading
import logging
import json

from file_protocol import FileProtocol
file_protocol = FileProtocol()

class ClientHandler(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        received_data = ""
        try:
            while True:
                data = self.connection.recv(1024)
                if data:
                    received_data += data.decode()
                    if "\r\n\r\n" in received_data:
                        break
                else:
                    break
            logging.warning(f"Full data received: {received_data}")
            result = file_protocol.process_string(received_data.strip())
            result += "\r\n\r\n"
            self.connection.sendall(result.encode())
        except Exception as e:
            logging.warning(f"Error: {e}")
        finally:
            self.connection.close()


class Server(threading.Thread):
    def __init__(self, ipaddress='0.0.0.0', port=8989):
        self.ip_info = (ipaddress, port)
        self.client_handlers = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        threading.Thread.__init__(self)

    def run(self):
        logging.warning(f"Server running on IP address {self.ip_info}")
        self.socket.bind(self.ip_info)
        self.socket.listen(1)
        while True:
            connection, client_address = self.socket.accept()
            logging.warning(f"Connection from {client_address}")

            client_handler = ClientHandler(connection, client_address)
            client_handler.start()
            self.client_handlers.append(client_handler)


def main():
    server = Server(ipaddress='0.0.0.0', port=7878)
    server.start()


if __name__ == "__main__":
    main()
