# """Uses the haveibeenpwned.com api while maintaining k-anonimity"""
# (optional) argv[1] is a SHA1 hashed password that you want to check 

import hashlib
def hash_pw(plaintext):
    hashed = (hashlib.sha1(plaintext_pw.encode('utf-8')))
    # print(f'printing hashed.digest: {hashed.hexdigest()}')
    return hashed.hexdigest().upper()


def split_hashed_pw(hash_str):
    # Only send the prefix of the hashed password to the server, to maintain anonimity
    prefix, suffix = hash_str[:5], hash_str[5:]
    # print(f'printing hashed_prefix: {prefix}')
    # print(f"Printing hashed_suffix: {suffix}")
    return prefix, suffix


import requests
def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RunTimeError(f'Error fetching: {res.status_code}')
    return res

def pwned_count(api_response, hashed_suffix):
    """Returns zero if pw is not ibn database."""
    for line in api_response.text.splitlines():
        if line.startswith(hashed_suffix):
            print(line)
            start_index = line.index(':') + 1
            count = line[start_index:]
            return count
    return 0
    

if __name__ == "__main__":
    from sys import argv
    # (optional) argv[1] is a plaintext password (UTF-8) that you want to check 
    try:
        plaintext_pw = argv[1]
    except:
        plaintext_pw = input('Plaintext PW:   ')
    hashed_pw = hash_pw(plaintext_pw)
    print(f'printing hashed_pw: {hashed_pw}')
    split_pw = split_hashed_pw(hashed_pw)
    print(f'printing split_pw: {split_pw}')
    server_response = request_api_data(split_pw[0])
    print(f'Printing server_response.text: {server_response.text}')
    count = pwned_count(server_response, split_pw[1])
    if count == 0:
        print('Congrats. This password has never been found in a public data breach.')
    else:
        print(f'Your password has been pwned {count} times. It would be a good idea to not use this password anymore.')