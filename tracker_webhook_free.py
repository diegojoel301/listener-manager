import requests
import json
import urllib3
import time
import os
from tabulate import tabulate

# Desactivar advertencias de seguridad HTTPS no verificadas
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Realizar una solicitud GET

web_hook_site = "https://webhook.site"

s = requests.Session()

s.get(web_hook_site)

s.get(web_hook_site + "/user").text

datos_web_hook_free = json.loads(s.post(web_hook_site + "/token").text)

while True:

    print("[+] Url a enviar: https://webhook.site/" + datos_web_hook_free["uuid"])
    data_tracked = json.loads(s.get(web_hook_site + "/token/" + datos_web_hook_free["uuid"] + "/requests?page=1&password=&query=&sorting=newest").text)["data"]

    head = ["ip", "url", "user-agent"]
    
    data = list()

    for elem in data_tracked:        
        data.append([elem['ip'], elem['url'], elem['user_agent']])

    print(tabulate(data, headers=head, tablefmt="grid"))

    time.sleep(3)
    os.system("clear")



