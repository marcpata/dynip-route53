FROM python:3.8-slim

# Instale las dependencias necesarias a partir del archivo requirements.txt
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

# Copie la aplicación ddns.py, el archivo domains.list y el script run-ddns.sh al contenedor
COPY ddns.py /app/
COPY domains.list /app/
COPY run-ddns.sh /app/

# Establezca el permiso de ejecución en el script run-ddns.sh
RUN chmod +x /app/run-ddns.sh
WORKDIR /app/
# Ejecute el script run-ddns.sh para que se ejecute la aplicación
CMD ["/app/run-ddns.sh"]
~~