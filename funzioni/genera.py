from faker import Faker
import pandas as pd
import random

fake = Faker()
random.seed(42)

N = 500000  #numero totale di record

#Genera FONTI
fonti = []
for i in range(1, N + 1):
    fonti.append({
        "ID_Fonte": i,
        "Affidabilita": round(random.uniform(0.0, 1.0), 2),
        "Nazione": fake.country(),
        "NomeFonte": fake.company()
    })

df_fonti = pd.DataFrame(fonti)
df_fonti.to_csv("fonti.csv", index=False)

#DOCUMENTI
documenti = []
for i in range(1, N + 1):
    documenti.append({
        "ID_Documento": i,
        "ID_Fonte": i,  # 1:1 con fonte
        "Via": fake.street_address(),
        "Citta": fake.city(),
        "CAP": fake.postcode(),
        "Nazione": fake.country(),
        "Scadenza": fake.date_between(start_date="+30d", end_date="+5y")
    })

df_documenti = pd.DataFrame(documenti)
df_documenti.to_csv("documenti.csv", index=False)

#PERSONE
persone = []
for i in range(1, N + 1):
    persone.append({
        "ID_Locale": i,
        "Nome": fake.first_name(),
        "Cognome": fake.last_name(),
        "NomeProfessione": fake.job(),
        "Settore": fake.bs(),
        "ID_Documento": i,  # 1:1
        "ID_Fonte": i       # 1:1
    })

#duplica 100 persone
duplicati = random.sample(persone, 100)
for i, p in enumerate(duplicati, start=N+1):
    persone.append({
        "ID_Locale": i,
        "Nome": p["Nome"],
        "Cognome": p["Cognome"],
        "NomeProfessione": p["NomeProfessione"],
        "Settore": fake.bs(),              #cambia solo il settore
        "ID_Documento": p["ID_Documento"], #usa lo stesso documento dell'originale
        "ID_Fonte": i                      #nuova fonte
    })
    #aggiunge solo nuova fonte
    fonti.append({
        "ID_Fonte": i,
        "Affidabilita": round(random.uniform(0.0, 1.0), 2),
        "Nazione": fake.country(),
        "NomeFonte": fake.company()
    })

df_persone = pd.DataFrame(persone)
df_documenti = pd.DataFrame(documenti)
df_fonti = pd.DataFrame(fonti)

df_persone.to_csv("persone_100.csv", index=False)
df_documenti.to_csv("documenti.csv", index=False)
df_fonti.to_csv("fonti.csv", index=False)

#sottoinsieme al 25%
df_persone[:125000].to_csv("persone_25.csv", index=False)
df_documenti[:125000].to_csv("documenti_25.csv", index=False)
df_fonti[:125000].to_csv("fonti_25.csv", index=False)
