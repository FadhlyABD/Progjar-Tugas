from socket import *
import threading
import logging
import datetime


class ClientHandler(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        while True:
            data = self.connection.recv(1024)
            if data:
                request = data.decode("utf-8").strip()
                if request == "TIME":
                    current_time = datetime.datetime.now().strftime("%H:%M:%S")
                    response = f"JAM {current_time}\r\n"
                    self.connection.sendall(response.encode("utf-8"))
                elif request == "QUIT":
                    response = "Server terminating connection\r\n"
                    self.connection.sendall(response.encode("utf-8"))
                    break
            else:
                break
        self.connection.close()


class Server(threading.Thread):
    def __init__(self):
        self.client_threads = []
        self.socket = socket(AF_INET, SOCK_STREAM)
        threading.Thread.__init__(self)

    def run(self):
        self.socket.bind(("0.0.0.0", 45000))
        self.socket.listen(1)
        logging.warning("Server listening on port 45000")
        while True:
            connection, client_address = self.socket.accept()
            logging.warning(f"Connection from {client_address}")

            client_thread = ClientHandler(connection, client_address)
            client_thread.start()
            self.client_threads.append(client_thread)


def main():
    server = Server()
    server.start()


if __name__ == "__main__":
    main()
