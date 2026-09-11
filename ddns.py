import boto3
import requests
import os
import time
import socket
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Credenciales y configuración con prefijo DYNR53_
aws_access_key_id = os.environ.get("DYNR53_AWS_ACCESS_KEY_ID") or os.environ.get("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.environ.get("DYNR53_AWS_SECRET_ACCESS_KEY") or os.environ.get("AWS_SECRET_ACCESS_KEY")
hosted_zone = os.environ.get("DYNR53_HOSTED_ZONE") or os.environ.get("HOSTED_ZONE")

# Variables de configuración personalizables mediante entorno con valores por defecto seguros
INTERVAL_SECONDS = int(os.environ.get("DYNR53_INTERVAL_SECONDS", "300"))
MAX_RETRY_DELAY = int(os.environ.get("DYNR53_MAX_RETRY_DELAY", "300"))
INITIAL_RETRY_DELAY = float(os.environ.get("DYNR53_INITIAL_RETRY_DELAY", "5.0"))

def get_current_ip():
    """Obtiene la IP pública actual utilizando múltiples servicios de respaldo y reintentos con backoff exponencial."""
    ip_services = [
        "https://api.ipify.org?format=json",
        "https://ifconfig.me/ip.json",
        "https://ipinfo.io/json"
    ]
    
    delay = INITIAL_RETRY_DELAY
    while True:
        for service in ip_services:
            try:
                response = requests.get(service, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    ip = data.get("ip") or data.get("query")
                    if ip:
                        return ip.strip()
            except Exception as e:
                print(f"[Advertencia] Fallo al consultar {service}: {e}")
                
        print(f"[Conectividad] No se pudo obtener la IP pública. Reintentando en {delay:.1f} segundos...")
        time.sleep(delay)
        delay = min(delay * 2, MAX_RETRY_DELAY)

def get_hosted_zone_id(route53, domain_name):
    response = route53.list_hosted_zones()
    hosted_zone_id = None
    for zone in response["HostedZones"]:
        if zone["Name"] == domain_name + ".":
            hosted_zone_id = zone["Id"]
            break
    return hosted_zone_id

def load_domains(filename):
    domain_names = []
    if not os.path.exists(filename):
        return domain_names
    with open(filename, "r") as file:
        for line in file:
            domain_name = line.strip()
            if domain_name and not domain_name.startswith("#"):
                domain_names.append(domain_name)
    return domain_names

def main():
    print(f"Iniciando servicio DDNS para Route53. Intervalo: {INTERVAL_SECONDS}s")
    
    route53 = boto3.client(
        "route53",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    
    last_ip = None

    while True:
        try:
            current_ip = get_current_ip()
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] IP pública actual detectada: {current_ip}")
            
            if current_ip != last_ip:
                domain_names = load_domains("domains.list")
                if not domain_names:
                    print("[Advertencia] No se encontraron dominios en domains.list")
                else:
                    hosted_zone_id = get_hosted_zone_id(route53, hosted_zone)
                    if not hosted_zone_id:
                        print(f"[Error] No se encontró la Hosted Zone ID para '{hosted_zone}'")
                    else:
                        for domain_name in domain_names:
                            try:
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
                                print(f"[Route53] Actualizado exitosamente {domain_name} -> {current_ip}")
                            except Exception as e:
                                print(f"[Error] Al actualizar el registro para {domain_name}: {e}")
                
                last_ip = current_ip
            else:
                print("[Route53] La IP no ha cambiado. No se requiere actualización.")
                
        except Exception as e:
            print(f"[Error general en el ciclo de ejecución] {e}")
            
        print(f"Esperando {INTERVAL_SECONDS} segundos para la siguiente verificación...")
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
