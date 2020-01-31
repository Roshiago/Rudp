from client.client import Client
import time


if __name__ == "__main__":
    client = Client(('', 25566))

    client.connect(('localhost', 25565))

    client.close()


