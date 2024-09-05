import socket
import ssl
import uuid

def recv_ssl_data(ssl_conn, buffer_size=1024, timeout=5):
    """
    Receive data from an SSL connection.

    Args:
        ssl_conn (ssl.SSLSocket): SSL connection.
        buffer_size (int): Size of the buffer for receiving data.
        timeout (int): Timeout for the receive operation.

    Returns:
        bytes: Received data.
    """
    data = b''
    ssl_conn.settimeout(timeout)  # 设置超时时间
    try:
        while True:
            chunk = ssl_conn.recv(buffer_size)
            if not chunk:
                break
            data += chunk
    except ssl.SSLWantReadError:
        print("SSLWantReadError: Timeout while waiting for data")
    except Exception as e:
        print(f"Exception during data receive: {e}")
    finally:
        return data

def generate_http_request_header_00(host,uri=f'/'):
    bypass_cache = uuid.uuid4()
    parts = [
        f"GET {uri} HTTP/1.1\r\n",
        f"Host: {host}\r\n",
        f"User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36\r\n",
        f"Connection: close\r\n",
        "\r\n",
    ]
    return "".join(parts)

def resolve_sni_hostname(sni_hostname):
    try:
        addr_info = socket.getaddrinfo(sni_hostname, None)
        ip_address = addr_info[0][4][0]
        return ip_address
    except socket.gaierror as e:
        return None

def send_https_request(request, sni_hostname):
    port = 443
    try:
        ip = resolve_sni_hostname(sni_hostname)
        if not ip:
            return 0, {}, b''

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((ip, port))
            context = ssl.create_default_context()
            context.check_hostname = False 
            context.verify_mode = ssl.CERT_NONE  

            ssl_conn = context.wrap_socket(s, server_hostname=sni_hostname)

            ssl_conn.sendall(request.encode())
           
            response = recv_ssl_data(ssl_conn)

        if response != b'':
            header, body = response.split(b'\r\n\r\n', 1)

            header_lines = header.decode().split('\r\n')
            status_line = header_lines[0]
            status_code = int(status_line.split(' ')[1])

            headers = {}
            for line in header_lines[1:]:
                key, value = line.split(': ', 1)
                headers[key] = value
        else:
            status_code = 0
            headers = {}
            body = b''
        return status_code, headers, body.decode()
    except Exception as e:
        return 0, {}, b''

def test_step1(dt="tencent.lzytest.tech", uri= f'/'):
    """
    df means front domain
    dt means target domain
    """
    sni_hostname = dt

    target_request = generate_http_request_header_00(host=dt, uri=uri)

    status_code, headers, body = send_https_request(request=target_request, sni_hostname=sni_hostname)

    return body
def test_step2(df="tencentgz.lzytest.tech",dt="tencent.lzytest.tech", uri= f'/'):
    """
    df means front domain
    dt means target domain
    """
    sni_hostname = df

    target_request = generate_http_request_header_00(host=dt, uri=uri)

    status_code, headers, body = send_https_request(request=target_request, sni_hostname=sni_hostname)
    return body

def test_step3(df="tencentgz.lzytest.tech", uri= f'/'):
    """
    df means front domain
    dt means target domain
    """
    sni_hostname = df

    target_request = generate_http_request_header_00(host=df, uri=uri)

    status_code, headers, body = send_https_request(request=target_request, sni_hostname=sni_hostname)

    return body


# if __name__ == "__main__":
#     body1 = test_step1()
#     body2 = test_step2()
#     body3 = test_step3()
#     print(f"body1:{body1}")
#     print(f"body2:{body2}")
#     print(f"body3:{body3}")
#     if body1 == body2 and body2 != body3:
#         print("Domain Fronting")
    