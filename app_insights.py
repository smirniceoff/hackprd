import json
import uuid
import requests
from datetime import datetime, timezone

# Instrumentation Key extraída da Connection String
instrumentation_key = "24d4b622-db85-4c0e-a731-0676dc9078a6"

# Endpoint fixo da API REST do App Insights
endpoint = "https://dc.services.visualstudio.com/v2/track"

def send_log(message, severity="Information"):
    data = {
        "name": "Microsoft.ApplicationInsights.Event",
        "time": datetime.now(timezone.utc).isoformat(),
        "iKey": instrumentation_key,
        "tags": {
            "ai.device.id": "python-script",
            "ai.cloud.role": "PowerAutomateScript",
            "ai.operation.id": str(uuid.uuid4())
        },
        "data": {
            "baseType": "EventData",
            "baseData": {
                "ver": 2,
                "name": "HachathonLog",
                "properties": {
                    "message": message,
                    "severity": severity
                }
            }
        }
    }

    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(endpoint, data=json.dumps(data), headers=headers)
        response.raise_for_status()
        print(f"Log enviado com sucesso: {message}")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar log: {e}")

def gerar_trafego_http():
    
    #200 OK	
    url = "https://httpstat.us/200"  # URL pública para testes
    try:
        response = requests.get(url)
        send_log(f"Requisição GET para {url} retornou status {response.status_code}", "Information")
    except requests.exceptions.RequestException as e:
        send_log(f"Erro na requisição GET para {url}: {str(e)}", "Error")

    #404 Not Found
    url = "https://httpstat.us/404"  # URL pública para testes
    try:
        response = requests.get(url)
        send_log(f"Requisição GET para {url} retornou status {response.status_code}", "Information")
    except requests.exceptions.RequestException as e:
        send_log(f"Erro na requisição GET para {url}: {str(e)}", "Error")

    #500 Internal Server Error
    url = "https://httpstat.us/500"  # URL pública para testes
    try:
        response = requests.get(url)
        send_log(f"Requisição GET para {url} retornou status {response.status_code}", "Information")
    except requests.exceptions.RequestException as e:
        send_log(f"Erro na requisição GET para {url}: {str(e)}", "Error")
    
    #502 Bad Gateway
    url = "https://httpstat.us/502"  # URL pública para testes
    try:
        response = requests.get(url)
        send_log(f"Requisição GET para {url} retornou status {response.status_code}", "Information")
    except requests.exceptions.RequestException as e:
        send_log(f"Erro na requisição GET para {url}: {str(e)}", "Error")

# Testes
send_log("Script Python iniciado via Power Automate", "Information")
send_log("Este é um aviso de teste para o App Insights", "Warning")
send_log("Erro simulado para rastreamento", "Error")

try:
    1 / 0
except ZeroDivisionError as e:
    send_log(f"Divisão por zero capturada: {str(e)}", "Critical")

# Gera tráfego HTTP e registra no App Insights
gerar_trafego_http()
