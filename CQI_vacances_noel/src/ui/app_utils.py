import requests
from concurrent.futures import ThreadPoolExecutor

url = "http://192.168.4.1"

def send_request_threaded(path, *params):
    # Function to send request in a separate thread
    #threading.Thread(target=send_request, args=(path, *params)).start()
    print(path)
    requests.get(url + path)
    return
    with ThreadPoolExecutor() as executor:
        value = executor.submit(send_request, path, *params)
        return value.result()
    #send_request(path, *params)

def send_request(path, send=True, print_code=True, print_request=True):
    if not send: # Disable request for debug
        return "Requesting disabled"
    if print_request: # Print path to debug
        print(path)
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
    return message
