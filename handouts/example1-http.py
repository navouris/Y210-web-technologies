# πρόγραμμα που ζητάει ένα url και επιστρέφει την κεφαλίδα της απόκρισης HTTP
import requests
import time

while True:
    url = input('url:')
    if url == '': break
    if not url.startswith('http'):
        url = 'http://'+ url
    try:
        t_start = time.process_time()
        with requests.get(url) as response:
            t_elapsed = time.process_time() - t_start
            print("\nRESPONSE STATUS: ", response.status_code)
            print("RESPONSE HEADER")
            for key, value in response.headers.items():
                print("{:30s} {}".format(key, value))
            print("\nαπάντηση σε {:.3f} ms".format(t_elapsed))
    except:
        print('error opening', url)