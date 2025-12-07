import socket

HOST = "127.0.0.1"
PORT = 5000
ADDR = (HOST, PORT)


def parse_http_request(raw_text: str):
    head, body = raw_text.split("\r\n\r\n", 1)

    # Process Request Line
    request_line, raw_headers = head.split("\r\n", 1)
    method, path, version = request_line.split(" ", 2)

    # Process Headers
    headers_dict = dict()
    for item in raw_headers.split("\r\n"):
        if not item:
            continue
        if ":" not in item:
            continue
        key, value = item.split(":", 1)
        key, value = key.strip(), value.strip()
        headers_dict[key] = value

    return method, path, version, headers_dict, body


def main():
    print("Hello from basic-http!")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(ADDR)
        server_socket.listen(1)
        print(f"Listening on address: {ADDR}")

        conn, addr = server_socket.accept()
        with conn:
            print("Connected to ", addr)
            data = conn.recv(1024)
            if not data:
                return

            request_text = data.decode("utf-8")
            method, path, version, headers, body = parse_http_request(request_text)
            print("Method:", method)
            print("Path:", path)
            print("Version:", version)
            print("Headers:", headers)
            print("Body:", body)

            body = "Hello, World!"
            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html\r\n"
                f"Content-Length: {len(body)}\r\n"
                "\r\n"
                f"{body}"
            )
            conn.sendall(response.encode("utf-8"))


if __name__ == "__main__":
    main()
