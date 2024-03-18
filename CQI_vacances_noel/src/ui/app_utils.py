import requests
import threading

url = "http://192.168.4.1"

def send_request_threaded(path, **params):
    if not params["send"]: # Disable request for debug
        return "Requesting disabled"
    if params["print_request"]: # Print path to debug
        print(path)
    # Function to send request in a separate thread
    threading.Thread(target=send_request, args=(path, params["print_code"])).start()
    return "Request Success"

def send_request(path, print_code=False):
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
        message = "Error cause: " + str(e.__cause__)
    print(message)
    return message
