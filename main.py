import uuid
import random
import json
from datetime import datetime, timedelta
import os
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import time

incidents = []

# função de gerar uuid
def random_uuid():
    return str(uuid.uuid4())

# função de gerar uma data aleatória
def random_date():
    now = datetime.utcnow()
    random_past_time = now - timedelta(days=random.randint(1, 30), hours=random.randint(0, 23), minutes=random.randint(0, 59))
    return random_past_time



# função de gerar um incidente aleatório
def generate_random_incident(incident_number):
    data_criacao = random_date()    
    data_modificacao = (data_criacao + timedelta(days=random.randint(1, 30), hours=random.randint(0, 23), minutes=random.randint(0, 59)))
    incident = {
        "eventUniqueId": random_uuid(),
        "objectSchemaType": "Incident",
        "objectEventType": "Create",
        "workspaceInfo": {
            "SubscriptionId": "556ac391-e8b4-4a9e-8f05-024974300f27",
            "ResourceGroupName": "rg-siem",
            "WorkspaceName": "sentinelhml"
        },
        "workspaceId": "8d300aff-d535-4430-9eef-3046965c48cf",
        "object": {
            "id": f"/subscriptions/556ac391-e8b4-4a9e-8f05-024974300f27/resourceGroups/rg-siem/providers/Microsoft.OperationalInsights/workspaces/sentinelhml/providers/Microsoft.SecurityInsights/Incidents/{random_uuid()}",
            "name": random_uuid(),
            "etag": f"\"{random_uuid()}\"",
            "type": "Microsoft.SecurityInsights/Incidents",
            "properties": {
                "title": f"Incidente Teste - {random.choice(["Porto Digital", "BBTS", "Banco do Brasil"])}",
                "description": f"{random.choice(["Sistema caiu", "Erro de conexão", "Falha no login"])}",
                "severity": f"{random.choice(["High", "Medium", "Low"])}",
                "status": f"{random.choice(["New", "In Progress", "Resolved"])}",
                "owner": {
                    "objectId": random_uuid(),
                    "email": f"{random.choice(["lohhanguilherme@bbts.com.br", "arthurcoelho@bbts.com.br", "lucaskaua@bbts.com.br"])}",
                    "assignedTo": f"{random.choice(["Lohhan Guilherme", "Arthur Coelho", "Lucas Kauã"])}",
                    "userPrincipalName": "ext-teste@bbts.com.br",
                },
                "labels": [],
                "firstActivityTimeUtc": data_criacao.isoformat() + "Z",
                "lastActivityTimeUtc": data_modificacao.isoformat() + "Z",
                "lastModifiedTimeUtc": data_modificacao.isoformat() + "Z",
                "createdTimeUtc": data_criacao.isoformat() + "Z",
                "incidentNumber": str(incident_number),
                "additionalData": {
                    "alertsCount": 0,
                    "bookmarksCount": 0,
                    "commentsCount": 0,
                    "alertProductNames": [],
                    "tactics": [],
                    "techniques": []
                },
                "relatedAnalyticRuleIds": [],
                "incidentUrl": "https://portal.azure.com/#asset/Microsoft_Azure_Security_Insights/Incident/subscriptions/556ac391-e8b4-4a9e-8f05-024974300f27/resourceGroups/rg-siem/providers/Microsoft.OperationalInsights/workspaces/sentinelhml/providers/Microsoft.SecurityInsights/Incidents/22d80f17-3e6d-49a7-8cc4-ad88fc708c95",
                "providerName": "Azure Sentinel",
                "providerIncidentId": str(incident_number),
                "alerts": [],
                "bookmarks": [],
                "relatedEntities": [],
                "comments": []
            }
        }
    }
    return incident

# função de adicionar os incidentes aleatórios à uma lista
def generate_incidents(n):
    for i in range(1,n+1):
        incidents.append(generate_random_incident(i))
    return incidents

# função de salvar os incidentes em um file incidents.json
def save(incidents):
    filename = "incidents.json"
    with open (filename, "w") as file:
        json.dump(incidents, file)

def add_incidents():
    incidents.append(generate_random_incident(random.randint(1, 9999)))
    save(incidents)
    print("novo")

def post_incidents():
   try:
      with open("incidents.json", "r") as file:
         dados = json.load(file)
        
      url = "http://127.0.0.1:8000/api/tickets/new_incidents"
      response = requests.post(url, json=dados)
      if response.status_code == 200:
         print(f"[{datetime.now()}] Dados enviados com sucesso:", response.json())
      else:
         print(f"[{datetime.now()}] Erro ao enviar dados:", response.status_code, response.text)
   except Exception as e:
      print(f"[{datetime.now()}] Ocorreu um erro ao enviar dados: {e}")

if __name__ == "__main__":
   scheduler = BackgroundScheduler()
   scheduler.add_job(add_incidents, 'interval', seconds=60)
   scheduler.add_job(post_incidents, 'interval', seconds=60)
   scheduler.start()

   try:
      while True:
         time.sleep(1)
   except (KeyboardInterrupt, SystemExit):
      scheduler.shutdown()