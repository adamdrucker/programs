import socket

HOST = "127.0.0.1"
PORT = 47343

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    '''
    * these are constants that are passed into the socket object
    * INET specifies IPv4
    * stream is the socket type for TCP, which is how messages will be sent
    '''
    s.bind((HOST, PORT))    # bind method associates the socket with an IP and a port
    s.listen()              # listen method allows the socket to listen for incoming connections
    conn, addr = s.accept() # the accept method creates the socket used to communicate with the client

    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)

