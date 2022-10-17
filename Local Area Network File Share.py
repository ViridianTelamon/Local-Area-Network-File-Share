import socket
import time
import os

print("Local Area Network File Share")

print("\nBy:  ViridianTelamon.")

time.sleep(0.2)

host = socket.gethostbyname(socket.gethostname())

option = input("\nEnter In Send To Start Sending Files Or Enter In Receive To Start Receiving Files:  ")

option = option.lower()

def file_sender():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, 9999))

    file_input = input("\nEnter The File Name That You Want To Share, Make Sure That The File Is In The Same Directory As This Script:  ")

    file = open(file_input, "rb")

    file_size = os.path.getsize(file_input)

    client.send(file_input.encode())
    client.send(str(file_size).encode())

    data = file.read()
    client.sendall(data)
    client.send(b"<12121212121212END12121212121212>")

    file.close()

    client.close()

def file_receiver():
    a_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    a_server.bind((host, 9999))

    print("\nAttempting To Receive A Connection.")

    a_server.listen()

    a_client, a_address = a_server.accept()

    a_file_name = a_client.recv(1024).decode()

    print(f"\nReceiving File Name:  {a_file_name}")

    a_file_size = a_client.recv(1024).decode()

    print(f"Receiving File Size:  {a_file_size}")

    a_file = open(a_file_name, "wb")

    a_file_part = b""

    print("\nThe File Has Been Shared.")

    done = False

    while not done:
        a_data = a_client.recv(1024)

        if a_file_part[-33:] == b"<12121212121212END12121212121212>":
            done = True
        else:
            a_file_part += a_data

    a_file.write(a_file_part)

    a_client.close()

    a_server.close()

if option == "send":
    try:
        file_sender()
    except Exception:
        print("\nThere Is No Receiver Currently Available.")
elif option == "receive":
    file_receiver()
else:
    time.sleep(0.2)

    exit()