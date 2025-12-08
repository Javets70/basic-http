import socket


HOST = "127.0.0.1"
PORT = 5000


class MiniApp:
    def __init__(self):
        self.routes = {}

    def router(self, method, path):
        def decorator(handler):
            self.routes[(method, path)] = handler
            return handler

        return decorator

    def run(self, host, port):
        addr = (host, port)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(addr)
            server_socket.listen(1)
            print(f"Listening on address: {addr}")
            while True:
                conn, addr = server_socket.accept()
                with conn:
                    data = conn.recv(1024)
                    if not data:
                        return

                    request_text = data.decode("utf-8")
                    method, path, version, headers, body = self.parse_http_request(
                        request_text
                    )

                    handler = self.routes.get((method, path))
                    if handler is None:
                        status_line = "HTTP/1.1 404 Not Found"
                        body = "Not found"
                    else:
                        request = {
                            "method": method,
                            "path": path,
                            "headers": headers,
                            "body": body,
                        }
                        body = handler(request)
                        status_line = "HTTP/1.1 200 OK"

                    body_bytes = body.encode("utf-8")
                    response = (
                        f"{status_line}\r\n"
                        "Content-Type: text/plain\r\n"
                        f"Content-Length: {len(body_bytes)}\r\n"
                        "\r\n"
                    ).encode("utf-8") + body_bytes

                    conn.sendall(response)

    @staticmethod
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


app = MiniApp()


@app.router("GET", "/")
def home(request):
    print(request)
    return "Hello from /"


if __name__ == "__main__":
    app.run("127.0.0.1", 5000)
