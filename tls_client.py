import socket
import ssl

# Server IP address and port
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 4433


def create_tls_context():
    # Create TLS context for the client
    context = ssl.create_default_context(
        ssl.Purpose.SERVER_AUTH,
        cafile="ca.crt"
    )

    return context


def main():
    # Create TLS configuration
    context = create_tls_context()

    try:
        # Create TCP connection to the server
        with socket.create_connection(
            (SERVER_HOST, SERVER_PORT)
        ) as tcp_socket:

            print("TCP connection established.")

            # Add TLS security to the TCP socket
            with context.wrap_socket(
                tcp_socket,
                server_hostname="localhost"
            ) as tls_socket:

                print("Secure TLS connection established.")
                print("TLS version:", tls_socket.version())

                # Ask the user to enter a message
                message = input("Enter a message to send securely: ")

                # Send the message
                tls_socket.sendall(message.encode())

                # Receive the server reply
                response = tls_socket.recv(1024)

                # Convert bytes to text
                response_text = response.decode()

                print("Server response:", response_text)

    except ssl.SSLError as error:
        # TLS or certificate error
        print("TLS error:", error)

    except OSError as error:
        # Network/socket error
        print("Network error:", error)


# Start the client
if __name__ == "__main__":
    main()
