import socket
import ssl

# Server IP address and port
HOST = "127.0.0.1"
PORT = 4433


def create_tls_context():
    # Create TLS context for the server
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

    # Load server certificate and private key
    context.load_cert_chain(
        certfile="server.crt",
        keyfile="server.key"
    )

    return context


def handle_client(tls_socket, address):
    try:
        # Receive message from the client
        data = tls_socket.recv(1024)

        if data:
            # Convert bytes to text
            message = data.decode()

            print(f"Message received from {address}: {message}")

            # Create a reply
            reply = "Your secure message was received by the TLS server: " + message

            # Send reply to the client
            tls_socket.sendall(reply.encode())

    except Exception as error:
        # Display communication errors
        print("Communication error:", error)


def main():
    # Create the TLS configuration
    context = create_tls_context()

    try:
        # Create a normal TCP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

            # Allow the port to be reused
            server_socket.setsockopt(
                socket.SOL_SOCKET,
                socket.SO_REUSEADDR,
                1
            )

            # Attach the socket to the IP address and port
            server_socket.bind((HOST, PORT))

            # Wait for client connections
            server_socket.listen(5)

            print(f"TLS server is listening on {HOST}:{PORT}")

            # Accept a TCP client
            client_socket, address = server_socket.accept()

            print(f"TCP connection received from {address}")

            # Add TLS security to the TCP connection
            with context.wrap_socket(
                client_socket,
                server_side=True
            ) as tls_socket:

                print("Secure TLS connection established.")
                print("TLS version:", tls_socket.version())

                # Communicate with the client
                handle_client(tls_socket, address)

    except ssl.SSLError as error:
        # TLS-specific error
        print("TLS server error:", error)

    except OSError as error:
        # Network/socket error
        print("Network error:", error)


# Start the server
if __name__ == "__main__":
    main()
