# Configuración de Dynamic DNS Route53

Este script actualiza automáticamente registros tipo A en Amazon Route53 con la IP pública actual de tu host.

## Variables de Entorno

El script utiliza variables de entorno con el prefijo `DYNR53_` para evitar colisiones. (También admite retrocompatibilidad con las variables estándar sin prefijo).

| Variable | Descripción | Valor por defecto / Ejemplo |
|---|---|---|
| `DYNR53_AWS_ACCESS_KEY_ID` | Access Key ID de AWS | `AKIAIOSFODNN7EXAMPLE` |
| `DYNR53_AWS_SECRET_ACCESS_KEY` | Secret Access Key de AWS | `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` |
| `DYNR53_HOSTED_ZONE` | Nombre de la zona alojada en Route53 | `example.com` |
| `DYNR53_INTERVAL_SECONDS` | Intervalo de tiempo entre verificaciones | `300` |
| `DYNR53_INITIAL_RETRY_DELAY` | Retardo inicial ante pérdida de conectividad | `5.0` |
| `DYNR53_MAX_RETRY_DELAY` | Retardo máximo en reintentos con backoff | `300` |

## Uso

1. Configura tus credenciales y dominios en `domains.list`.
2. Define las variables de entorno o crea un archivo `.env`.
3. Ejecuta el script:
   ```bash
   python ddns.py
   ```
