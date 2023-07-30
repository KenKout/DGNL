import time
import threading
import requests
from requests.structures import CaseInsensitiveDict
import queue
current = 100000
request_count = 0
start_time = time.time()
def abc(abc):
    global current

    url = "https://thinangluc.vnuhcm.edu.vn/dgnl/api-dgnl/app/tra-cuu-thong-tin-ho-so/v1?tuychon=KETQUATHI"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Accept"] = "application/json"
    headers["Accept-Encoding"] = "gzip, deflate, br"
    headers["Accept-Language"] = "vi"
    headers["Host"] = "thinangluc.vnuhcm.edu.vn"
    headers["Origin"] = "https://thinangluc.vnuhcm.edu.vn"
    headers["Connection"] = "keep-alive"
    headers[
        "User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15"
    headers["Referer"] = "https://thinangluc.vnuhcm.edu.vn/dgnl/app/home"
    headers[
        "Cookie"] = "JSESSIONID=D63E56FC08BE10C995DF7C3B95F3C63F; _ga_S1PMX4L6E6=GS1.1.1686425220.1.1.1686425355.0.0.0; _ga=GA1.3.1528417990.1686425221; _gid=GA1.3.519138198.1686425221"

    lock = threading.Lock()
    max_retries = 3
    output_lines = []

    def send_request(queue):
        global request_count
        global current
        while not queue.empty():
            data = queue.get()
            retries = 0
            while retries < max_retries:
                try:
                    response = requests.post(url,
                                             headers=headers,
                                             data=data,
                                             timeout=10)
                    request_count += 1  # Increase the request count
                    current += 1
                    cpm = calculate_cpm()
                    if 'maHoSoXetTuyen' in response.text:
                        with lock:
                            with open("/www/wwwroot/dgnl_fetch_api/test.txt", "a") as myfile:
                                myfile.write(response.text + "\n")
                        print(f"CPM: {cpm}" + response.text)
                    else:
                        print(f"CPM: {cpm}" + data + ": Not Available - " +
                              response.text)
                    break  # Successful request, exit the loop
                except Exception as e:
                    print(f"Error occurred for {data}: {str(e)}")
                    retries += 1
                    print(
                        f"Retrying request for {data} (Attempt {retries}/{max_retries})"
                    )

    def execute_requests(data_payloads):
        q = queue.Queue()
        for data in data_payloads:
            q.put(data)

        # Create and start a thread for each chunk of data payloads
        threads = []
        num_threads = min(max_threads, q.qsize())
        for _ in range(num_threads):
            t = threading.Thread(target=send_request, args=(q, ))
            t.start()
            threads.append(t)

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

    def calculate_cpm():
        global start_time
        global request_count
        elapsed_time = time.time() - start_time
        cpm = int(request_count / elapsed_time * 60)
        return cpm

    # Create a list of data payloads
    data_payloads = []
    i = current
    while i <= 999999:
        data_payloads.append(f'"D23{str(i).zfill(6)}"')
        i += 1
    ''' 
    data_payloads = []
    i = current
    while i < 999999:
        data_payloads.append(f'"D23{i}"')
        i += 1
    '''
    # Split the data payloads into chunks
    chunk_size = 100
    chunks = []
    i = 0
    while i < len(data_payloads):
        chunk = data_payloads[i:i + chunk_size]
        chunks.append(chunk)
        i += chunk_size

    # Limit the number of threads to 50
    max_threads = 50
    chunks = chunks[:max_threads]

    # Start time for CPM calculation
    #start_time = time.time()

    # Execute requests in sequential order
    for chunk in chunks:
        execute_requests(chunk)

    # Print the output lines
    print("\nOutput:")
    for line in output_lines:
        print(line)

    # Calculate and display the final CPM
    cpm = calculate_cpm()
    print(f"CPM: {cpm}")


while True:
    abc(current) #Some unknown error make python stops after 32k requests(seems because of integer limits), this makes sure it keeps running after 32k ones
