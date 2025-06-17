    MATCH (p1:Persona)-[:HA_DOCUMENTO]->(d:Documento)<-[:HA_DOCUMENTO]-(p2:Persona)
WHERE p1 <> p2
  AND p1.Nome = p2.Nome
  AND p1.Cognome = p2.Cognome
  AND p1.ID_Documento = p2.ID_Documento
  AND (p1.Settore <> p2.Settore OR p1.ID_Fonte <> p2.ID_Fonte)
RETURN p1.ID_Locale AS ID1, p2.ID_Locale AS ID2,
       p1.Settore AS Settore1, p2.Settore AS Settore2,
       p1.ID_Fonte AS Fonte1, p2.ID_Fonte AS Fonte2,
       d.ID_Documento AS Documento;