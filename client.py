import argparse
import ipaddress
import requests
import getpass
import json
import time


parser = argparse.ArgumentParser()
parser.add_argument("-H", "--host",
                    help="IP address of the Tweetcool server",
                    default='127.0.0.1')  # Equals 'localhost'
parser.add_argument("-P", "--port",
                    help="Post used by the Tweetcool server",
                    type=int,
                    default=9876)
args = parser.parse_args()

try:
    server = {
        'host': ipaddress.ip_address(args.host),
        'port': args.port
    }
except ValueError as e:
    print('The given host is not a valid IP address')
    exit(0)

if not(1024 < server["port"] < 65535):
    print('The given port number is not in the range between 1024 and 65535!')
    exit(0)

server["address"] = 'http://' + server["host"].compressed + ':' + str(server["port"])

# Logic starts here... somewhere..


message = None
while message != 'q':
    r = requests.get(server['address'] + '/tweet')
    for tweet in r.json():
        print('''%s: %s''' % (tweet['poster'], tweet['content']))
        print('At:', time.strftime("%D %H:%M", time.localtime(int(tweet['timestamp']))) + '\n')
    try:
        message = input('Enter a cool message to post:("!refresh" or "exit"):')
    except EOFError:
        print('/n')
        raise SystemExit

    if message == '!refresh':
        continue
    r = requests.post(server['address'] + '/tweet', data=json.dumps({
        "content": message,
        "poster": getpass.getuser()
    }))
