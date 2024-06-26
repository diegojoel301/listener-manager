import requests
import urllib3
import json
import paramiko
from pwn import *
from tabulate import tabulate
import getpass
import os
import time
from scp import SCPClient

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

api_key = os.getenv('LINODE_KEY')

linode_server_api = "https://api.linode.com"

context.log_level = 'error'

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Para listar imagenes

#r = requests.get(linode_server_api + "/v4/images/", headers=headers)

# Linode Types

#r = requests.get(linode_server_api + "/v4/linode/types", headers=headers)

# Regiones

#r = requests.get(linode_server_api + "/v4/regions", headers=headers)

def create_nanode(label, root_pass):

    data = {
        "type": "g6-nanode-1",
        "region": "us-east",
        "image": "linode/debian9",
        "root_pass": root_pass,# "My_s3cur3_P@$$w0rd_xd",
        "label": label
    }

    r = requests.post(linode_server_api + "/v4/linode/instances", headers=headers,json=data)

    return json.loads(r.text)

def crear_nanode():
    label = input("[?] Ingresa un label: ")
    root_pass = getpass.getpass("[?] Ingresa password: ")
 
    res = create_nanode(label, root_pass)
    
    if "errors" in res.keys():
        for error in res["errors"]:
            print(error["reason"])
    else:
        print("[!] Exito al crear el nanode")

def ssh_session(host, user, password, port=22):
    # Intentar establecer una conexión SSH
    try:
        ssh_connection = ssh(user=user, host=host, password=password, port=port)
        print("Conexión SSH establecida exitosamente.")
        
        # Abrir un shell interactivo
        ssh_connection.interactive()
        
    except Exception as e:
        print(f"Error al conectar: {e}")

    finally:
        # Asegurarse de cerrar la conexión al final
        if 'ssh_connection' in locals() and ssh_connection.connected():
            ssh_connection.close()
            print("Conexión SSH cerrada.")

def mostrar_linodes():
    data_a_mostrar = list()

    r = requests.get(linode_server_api + "/v4/linode/instances", headers=headers)
    datos_json_dict = json.loads(r.text)

    headers_table = ["id", "label", "status", "ipv4", "ipv6"]

    for linode in datos_json_dict["data"]:
        data_a_mostrar.append([linode["id"], linode["label"], linode["status"], linode["ipv4"], linode["ipv6"]])

    print(tabulate(data_a_mostrar, headers=headers_table, tablefmt="grid"))

def borrar_linode(id):
    r = requests.delete(linode_server_api + f"/v4/linode/instances/{id}", headers=headers)
    print(r.text)

def borrado_nanode():
    mostrar_linodes()
    id = input("[?] Introduce id: ")
    borrar_linode(id)

def conectar_linode():
    mostrar_linodes()
    ip_linode = input("[?] Ingresa la IP de tu linode: ")
    username = input("[?] Ingresa user: ")
    password = getpass.getpass("[?] Ingresa password: ")

    ssh_session(ip_linode, username, password)

def create_ssh_client(server, port, user, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

def scp_transfer_files(ssh_client, local_path, remote_path):
    scp = SCPClient(ssh_client.get_transport())
    scp.put(local_path, remote_path)
    scp.close()

def execute_command(ssh_client, command):
    stdin, stdout, stderr = ssh_client.exec_command(command)


def cargado_listener():
    mostrar_linodes()

    ip_linode = input("[?] Ingresa la IP de tu linode: ")
    username = input("[?] Ingresa user: ")
    password = getpass.getpass("[?] Ingresa password: ")

    # Rutas del archivo local y remoto

    local_file_path = "./listener-python.tar.gz"

    remote_file_path = "/root/listener-python.tar.gz"

    # Crear una conexión SSH
    ssh_s = create_ssh_client(ip_linode, 22, username, password)
    # Transferir archivos
    scp_transfer_files(ssh_s, local_file_path, remote_file_path)

    execute_command(ssh_s, "tar -xvf /root/listener-python.tar.gz")
    execute_command(ssh_s, "chmod +x /root/listener-python/deploy.sh")
    execute_command(ssh_s, "/root/listener-python/deploy.sh")

    # Cerrar la conexión SSH
    ssh_s.close()

def visualizado_de_logs():
    mostrar_linodes()

    ip_linode = input("[?] Ingresa la IP de tu linode: ")

    r = requests.get(f"http://{ip_linode}:5000/logs")

    print(r.text)
#create_nanode("prod-2", "My_s3cur3_P@$$w0rd_xd")
#mostrar_linodes()
#borrar_linode("60643869")
#conectar_linode()
#os.system("clear")

while True:
    print("\n--- Menú Principal ---")
    print("1. Ver nanodes")
    print("2. Crear un nanode")
    print("3. Shell en nanode")
    print("4. Borrar nanode")
    print("5. Cargar Listener en nanode")
    print("6. Visualizar logs en nanode")
    print("7. Salir")

    try:
        choice = int(input("Seleccione una opción: "))
        
        if choice == 1:
            mostrar_linodes()
        elif choice == 2:
            crear_nanode()
        elif choice == 3:
            conectar_linode()
        elif choice == 4:
            borrado_nanode()
        elif choice == 5:
            cargado_listener()
        elif choice == 6:
            visualizado_de_logs()
        elif choice == 7:
            break
        else:
            print("Opción no válida, por favor intente de nuevo.")
        
    except ValueError:
        print("Por favor, ingrese un número válido.")
