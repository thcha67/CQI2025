import requests

url = "http://192.168.4.1"

def send_request(path, send=True, print_code=False, print_request=False):
    if print_request:
        print(path)
    if not send:
        return "Requesting disabled"
    path = url + path
    try:
        code = requests.get(path, timeout=0.5)
        if print_code:
            print(code)
        message = "Request Success"
    except requests.exceptions.ConnectTimeout:
        message = "Request Timeout"
    except requests.exceptions.ReadTimeout:
        message = "Read Timeout"
    except requests.exceptions.ConnectionError:
        message = "Connection Error"
    except Exception as e:
        print(e)
        message = "Error cause: " + str(e.__cause__)
    return message
