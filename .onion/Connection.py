##connection to tor network 
import time
import requests
from fake_useragent import UserAgent
from stem import Signal
from stem.control import Controller

# Define the proxy settings to route through Tor 
proxies = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}

#test print 
#print("Changing IP Address every 10 seconds....\n\n")

# Infinite loop to keep changing the IP Address change every 10 seconds
while True:
    #generate random user agent
    headers = { 'User-Agent': UserAgent().random }
    #10 second delay 
    time.sleep(10)
    #connect to tor control port 
    with Controller.from_port(port = 9051) as c:
        #authenticate the connection
        c.authenticate(password='cRilXm5Mc6kFyUT7AASDbH9qEsGiPdO1DXGOcLK4') 
        #send signal to change ip address
        c.signal(Signal.NEWNYM)
    #print the new ip address and user agent
       ## print(f"Your IP is : {requests.get('https://ident.me', proxies=proxies, headers=headers).text}  ||  User Agent is : {headers['User-Agent']}")