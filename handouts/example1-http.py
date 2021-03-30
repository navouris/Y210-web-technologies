# πρόγραμμα που ζητάει ένα url και επιστρέφει την κεφαλίδα της απόκρισης HTTPimport requests
while True:
    url = input('url:')
    if url == '': break
    if not url.startswith('http'):
        url = 'http://'+ url
    try:
        with requests.get(url) as response:
            print("\nRESPONSE STATUS: ", response.status_code)
            print("RESPONSE HEADER")
            for key, value in response.headers.items():
                print("{:30s} {}".format(key, value))
    except:
        print('error opening', url)