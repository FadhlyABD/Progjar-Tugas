import socket


def run_client():
    # Membuat soket client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 45000))

    while True:
        # Meminta input dari pengguna
        user_input = input("Enter your request (TIME or QUIT): ").strip()

        if user_input == "TIME":
            request = "TIME\r\n"
        elif user_input == "QUIT":
            request = "QUIT\r\n"
        else:
            print("Invalid input. Please enter 'TIME' or 'QUIT'.")
            continue

        # Mengirim permintaan ke server
        client.sendall(request.encode("utf-8"))

        # Menerima respons dari server
        response = client.recv(1024).decode("utf-8")
        print("Response from server:", response)

        if "Server terminating connection" in response:
            break

    # Menutup koneksi
    client.close()


if __name__ == "__main__":
    run_client()
