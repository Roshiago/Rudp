from server.server import Server
import time


if __name__ == "__main__":
    server = Server()

    server.listen()

    server.close()


