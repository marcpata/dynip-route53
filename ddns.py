import boto3
import requests
import os
from dotenv import load_dotenv

# Cargue las variables de entorno desde el archivo .env
load_dotenv()

# Obtenga las credenciales de acceso a AWS
aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
hosted_zone = os.environ.get("HOSTED_ZONE")

# Cree un cliente de Route 53 utilizando las credenciales de acceso

def get_current_ip():
    response = requests.get("https://api.ipify.org?format=json")
    data = response.json()
    return data["ip"]
    
def get_hosted_zone_id(route53, domain_name):
    # Obtenga el ID de la zona de hospedaje del dominio principal
    response = route53.list_hosted_zones()
    hosted_zone_id = None
    for hosted_zone in response["HostedZones"]:
        if hosted_zone["Name"] == domain_name + ".":
            hosted_zone_id = hosted_zone["Id"]
            break
    return hosted_zone_id

def load_domains(filename):
    # Crear una lista de nombres de dominio
    domain_names = []

    # Abrir el archivo en modo lectura
    with open(filename, "r") as file:
        # Leer el archivo línea por línea
        for line in file:
            # Eliminar cualquier espacio en blanco al principio o al final de la línea
            domain_name = line.strip()
            # Añadir el nombre de dominio a la lista
            domain_names.append(domain_name)

    # Devolver la lista de nombres de dominio
    return domain_names

route53 = boto3.client("route53", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# Obtenga la dirección IP actual del host
current_ip = get_current_ip()

# Cargar la lista de nombres de dominio desde el archivo "domains.list"
domain_names = load_domains("domains.list")

# Recorra la lista de nombres de dominio y actualice cada dominio con la misma dirección IP
for domain_name in domain_names:
    # Obtenga el ID del registro A o AAAA que desea actualizar
    # record_id = get_record_id(route53, domain_name)
    # if record_id is None:
    #     continue

    # Actualice el registro con la nueva dirección IP
    hosted_zone_id = get_hosted_zone_id(route53, hosted_zone)
    response = route53.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch={
            "Changes": [
                {
                    "Action": "UPSERT",
                    "ResourceRecordSet": {
                        "Name": domain_name + ".",
                        "Type": "A",
                        "TTL": 60,
                        "ResourceRecords": [{"Value": current_ip}],
                    },
                }
            ]
        },
    )
    print(response)