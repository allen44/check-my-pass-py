# """Uses the haveibeenpwned.com api while maintaining k-anonimity"""
# (optional) argv[1] is a SHA1 hashed password that you want to check 


from sys import argv
import requests

# (optional) argv[1] is a SHA1 hashed password that you want to check 
try:
    hashed_pw = argv[1]
except:
    hashed_pw = input('Hashed PW (SHA1):   ')

# Only send the prefix of the hased password to the server, to maintain anonimity
hashed_prefix, hashed_suffix = hashed_pw[:5], hashed_pw[5:]
print(f'printing hashed_prefix: {hashed_prefix}')
print(f"Printing hashed_suffix: {hashed_suffix}")

url = 'https://api.pwnedpasswords.com/range/' + hashed_prefix
res = requests.get(url)

if res.status_code == 200:
    print('Got a response from haveibeenpwned.com')
    for line in res.text.splitlines():
        if line.startswith(hashed_suffix):
            print(line)
            start_index = line.index(':') + 1
            count = line[start_index:]
            if count == 0:
                print('Congrats. This password hash has never been found in a data breach.')
            else:
                print(f'Your password has been pwned {count} times. It would be a good idea to not use this password anymore.')
elif res.status_code == 404:
    print('Not Found.')

