# dynip-route53

Script de Python para actualizar dinámicamente registros DNS A en AWS Route 53 utilizando la IP pública actual, empaquetado con Docker.

## Características

- Obtiene la IP pública actual a través de `api.ipify.org`.
- Lee una lista de dominios y subdominios desde el archivo `domains.list`.
- Actualiza automáticamente los registros en Route 53 mediante la API de AWS (`boto3`).
- Se ejecuta continuamente cada 30 minutos o mediante Docker/Docker Compose.

## Requisitos

- Python 3.8+
- Credenciales de AWS con permisos para Route 53 (`AmazonRoute53FullAccess` o similar).

## Configuración

1. Crear un archivo `.env` o configurar las siguientes variables de entorno:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `HOSTED_ZONE` (ej. `example.com`)

2. Editar el archivo `domains.list` con los subdominios que desea actualizar (uno por línea).

## Uso

### Local
```bash
pip install -r requirements.txt
python ddns.py
```

### Con Docker Compose
```bash
docker-compose up --build
```

