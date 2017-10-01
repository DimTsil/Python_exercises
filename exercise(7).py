import requests  # https://github.com/requests/requests('pip install requests' in terminal)
import time     # Used for setting the intervals(3 seconds)
import hashlib  # Used for converting the file in checksum MD5
import os       # Used for clearing the terminal


def check_file(file_name): # Simultaneously, checking if the file exists and hashing it with MD5
    md5 = hashlib.md5()
    while True:
        try:
            f = open(file_name, 'rb')
            for chunk in f:
                md5.update(chunk)
            break
        except IOError:
            print("The file {} couldn' t be found".format(file_name))
            file_name = input('Please, give the correct file name again or press 0 to exit: ')
            if file_name == '0':
                exit(0)
    return md5.hexdigest(), file_name


def json_file(file_name):   # Opening the user's file input in reading-binary mode and saving it in a json file
    files = {'file': (file_name, open(file_name, 'rb'))}
    return files


def print_sortedList(sorted_jsonList, json_response):
    '''
        Checking if any antivirus detected that the file is infected
        and printing a sorted list based on the name of the antivirus.
        (Only the antiviruses who has found this file infected will be printed) !!!
    '''
    if json_response['positives'] == 0:
        print("No antiviruses found your file infected")
    else:
        for i in range(0, json_response['total']):
            if sorted_jsonList[i][1]['detected']:
                print(sorted_jsonList[i][0])


def waiting(par, head): # Waiting for 3 seconds and sending a request with the method POST
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Waiting for the results.")
    time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Waiting for the results..")
    time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Waiting for the results...")
    time.sleep(1)
    final_response = requests.post('https://www.virustotal.com/vtapi/v2/file/report', params=par, headers=head)
    return final_response


if __name__ == '__main__':
    key = input('Please, give your personal api key or press 0 to exit: ') # Giving the personal user's API-KEY or 0(zero) to exit
    if key == '0':
        exit(0)
    api_key2send = {'apikey': key}
    file_name = input('Please, give the name of your file to upload: ')

    hashed_file, file_name = check_file(file_name)  # Checking if the file exists and hashing it
    params = {'apikey': key, 'resource': hashed_file}

    ''' 
        First, sending a method POST request the user's file to check if already is in the database of the api,
        in order to reduce the bandwidth(not sending the whole file, just the checksum MD5 of the file)
    '''

    response = requests.post('https://www.virustotal.com/vtapi/v2/file/rescan', params=params)
    json_response = response.json()

    if json_response['response_code'] == 0:  # Case that the file isn 't in the database of the api
        file2send = json_file(file_name)

        # Sending the whole user's file with a method POST request
        response = requests.post('https://www.virustotal.com/vtapi/v2/file/scan', files=file2send, params=api_key2send)
        json_response = response.json()

        if json_response['response_code'] == 1:  # Taking the response that the file queued for scanning
            headers = {
                "Accept-Encoding": "gzip, deflate",
                "User-Agent": "gzip"
            }

            # Sending a method POST request in order to take the results
            response = requests.post('https://www.virustotal.com/vtapi/v2/file/report', params=params, headers=headers)
            json_response2 = response.json()
            while json_response2['response_code'] != 1: # Case that the scanning hasn't finished yet
                response = waiting(params, headers)
                while response.status_code == 204: # There is a case that the response is empty(error code 204) and retrying by sending a method POST request again
                    response = waiting(params, headers)
                json_response2 = response.json()

            '''
                When the scanning has finished it will take the results, convert the results in a list
                and sort this list based on the name of the antivirus(anonymous lambda function)
            '''
            sorted_jsonList = sorted(json_response2['scans'].items(), key=lambda antivirus: antivirus[0])
            print_sortedList(sorted_jsonList, json_response2)

    elif json_response['response_code'] == 1: # Case that the file is in the database of the api
        headers = {
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "gzip"
        }

        '''
            Simply, just sending a method POST request to the api with the checksum MD5 of the file as a 
            parameter, because the user's file is already in the database and printing a sorted list with the results
            
        '''

        response = requests.post('https://www.virustotal.com/vtapi/v2/file/report', params=params, headers=headers)
        json_response = response.json()
        sorted_jsonList = sorted(json_response['scans'].items(), key=lambda antivirus: antivirus[0])
        print_sortedList(sorted_jsonList, json_response)

    else:  # Case that something else happen
        print("An unexpected error occurred!!! Try again...")






