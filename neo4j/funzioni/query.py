import time
import pandas as pd
from statistics import stdev
from neo4j import GraphDatabase

URI      = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "12345678"

QUERIES = {
    "Q1": """
    MATCH (p:Persona)-[:HA_FONTE]->(f:Fonte),
      (p)-[:HA_DOCUMENTO]->(d:Documento)
WHERE p.NomeProfessione = "Medical sales representative"
  AND toFloat(f.Affidabilita) > 0.5
  AND date(d.Scadenza) > date("2028-01-01")
RETURN 
  p.Nome AS Nome,
  p.Cognome AS Cognome,
  f.NomeFonte AS NomeFonte,
  f.Nazione AS NazioneFonte,
  d.Scadenza AS ScadenzaDocumento,
  d.Citta AS CittaDocumento





    """,
    "Q2": """
   MATCH (p:Persona)-[:HA_FONTE]->(f:Fonte),
      (p)-[:HA_DOCUMENTO]->(d:Documento)
WHERE p.NomeProfessione = "Medical sales representative"
  AND toFloat(f.Affidabilita) > 0.5
  AND date(d.Scadenza) > date("2028-01-01")
RETURN 
  p.Nome AS Nome,
  p.Cognome AS Cognome,
  f.NomeFonte AS NomeFonte,
  f.Nazione AS NazioneFonte,
  d.Scadenza AS ScadenzaDocumento,
  d.Citta AS CittaDocumento



    """,
    "Q3": """
   MATCH (p:Persona)
WHERE p.ID_Locale = p.ID_Documento OR p.ID_Locale = p.ID_Fonte
RETURN p.ID_Locale AS idPersona, 
       p.Nome AS nome,  // Modificato da 'name' a 'Nome'
       p.Cognome AS cognome,  // Modificato da 'surname' a 'Cognome'
       p.ID_Documento AS idDocumento, 
       p.ID_Fonte AS idFonte
    """,
    "Q4": """
    MATCH (p:Persona), (f:Fonte), (d:Documento)
WHERE p.ID_Fonte = f.ID_Fonte
  AND p.ID_Documento = d.ID_Documento
  AND p.NomeProfessione STARTS WITH "A"
  AND f.Affidabilita > 0.5
  AND date(d.Scadenza) > date("2028-01-01")
RETURN
  p.Nome AS Nome,
  p.Cognome AS Cognome,
  p.NomeProfessione AS NomeProfessione,
  p.Settore AS Settore,
  f.NomeFonte AS NomeFonte,
  f.Nazione AS NazioneFonte,
  f.Affidabilita AS AffidabilitaFonte,
  d.Scadenza AS ScadenzaDocumento,
  d.Citta AS CittaDocumento,
  d.Nazione AS NazioneDocumento,
  d.CAP AS CAP






    """
}

def run_query_single(query):
    with GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD)) as driver:
        with driver.session() as session:
            start = time.perf_counter()
            session.run(query).consume()
            end = time.perf_counter()
            return (end - start) * 1000  # ms

def run_query_repeated(query, repetitions=30):
    times = []
    with GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD)) as driver:
        with driver.session() as session:
            for i in range(repetitions):
                start = time.perf_counter()
                session.run(query).consume()
                end = time.perf_counter()
                ms = (end - start) * 1000
                times.append(ms)
                print(f"    Esecuzione {i+1:02}: {ms:.2f} ms")
    return times

def benchmark_query(name, query):
    print(f"\nBenchmark per {name}:")

    t_freddo = run_query_single(query)
    print(f"  Tempo freddo: {t_freddo:.2f} ms")

    times = run_query_repeated(query)
    media = sum(times) / len(times)
    sigma = stdev(times)

    print(f"  Tempo medio (30): {media:.2f} ms")
    print(f"  Deviazione standard: {sigma:.2f} ms")

    return {
        "Query": name,
        "Tempo a freddo (ms)": round(t_freddo, 2),
        "Tempo medio (ms)": round(media, 2),
        "Deviazione std (ms)": round(sigma, 2)
    }

def main():
    results = []
    for name, query in QUERIES.items():
        results.append(benchmark_query(name, query))

    df = pd.DataFrame(results)
    output_path = r"C:\Users\fabyp\OneDrive\Documents\Progetto DB2\neo4j\risultati\benchmark_queries.xlsx"
    df.to_excel(output_path, index=False)
    print(f"\n✅ Risultati salvati in: {output_path}")

if __name__ == "__main__":
    main()
