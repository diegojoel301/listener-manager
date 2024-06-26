apt update

apt-get install python3 -y

apt-get install python3-pip -y

python3 -m pip install Flask

chmod +x /root/listener-python/app.py

cp python_app.service /etc/systemd/system/python_app.service

# Recargar systemd para que lea las nuevas definiciones de los servicios
systemctl daemon-reload

# Habilitar el servicio para que se inicie en el arranque
systemctl enable python_app.service

# Iniciar el servicio
systemctl start python_app.service
