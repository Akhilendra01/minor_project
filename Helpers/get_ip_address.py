import socket

def get_ip_address():
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Connect to a remote server (doesn't actually connect)
        s.connect(("8.8.8.8", 80))
        # Get the local IP address associated with the socket
        ip_address = s.getsockname()[0]
    except Exception as e:
        print("Error occurred while getting IP address:", e)
        ip_address = None
    finally:
        # Close the socket
        s.close()
    return ip_address
