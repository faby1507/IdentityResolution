//nodi
CREATE CONSTRAINT IF NOT EXISTS FOR (p:Persona) REQUIRE p.ID_Locale IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (d:Documento) REQUIRE d.ID_Documento IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (f:Fonte) REQUIRE f.ID_Fonte IS UNIQUE;

//caricamento nodi da CSV
LOAD CSV WITH HEADERS FROM 'file:///persone_25.csv' AS row
CREATE (:Persona {
  ID_Locale: toInteger(row.ID_Locale),
  Nome: row.Nome,
  Cognome: row.Cognome,
  NomeProfessione: row.NomeProfessione,
  Settore: row.Settore
});

LOAD CSV WITH HEADERS FROM 'file:///documenti_25.csv' AS row
CREATE (:Documento {
  ID_Documento: toInteger(row.ID_Documento),
  Via: row.Via,
  Citta: row.Citta,
  CAP: row.CAP,
  Nazione: row.Nazione,
  Scadenza: row.Scadenza
});

LOAD CSV WITH HEADERS FROM 'file:///fonti_25.csv' AS row
CREATE (:Fonte {
  ID_Fonte: toInteger(row.ID_Fonte),
  Affidabilita: toFloat(row.Affidabilita),
  Nazione: row.Nazione,
  NomeFonte: row.NomeFonte
});

//relazioni

//persona->documento (1:1)
LOAD CSV WITH HEADERS FROM 'file:///persone_25.csv' AS row
MATCH (p:Persona {ID_Locale: toInteger(row.ID_Locale)})
MATCH (d:Documento {ID_Documento: toInteger(row.ID_Documento)})
MERGE (p)-[:HA_DOCUMENTO]->(d);


//persona-> fonte (1:N_1:1)
LOAD CSV WITH HEADERS FROM 'file:///persone_25.csv' AS row
MATCH (p:Persona {ID_Locale: toInteger(row.ID_Locale)})
MATCH (f:Fonte {ID_Fonte: toInteger(row.ID_Fonte)})
WHERE NOT (f)<-[:HA_FONTE]-(:Persona)  //impedisce doppio legame
MERGE (p)-[:HA_FONTE]->(f);



//documento -> fonte (1:1)
LOAD CSV WITH HEADERS FROM 'file:///documenti_25.csv' AS row
MATCH (d:Documento {ID_Documento: toInteger(row.ID_Documento)})
MATCH (f:Fonte {ID_Fonte: toInteger(row.ID_Fonte)})
MERGE (d)-[:DERIVA_DA]->(f);

