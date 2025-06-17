import pandas as pd
import xml.etree.ElementTree as ET
import os
print("Sto cercando i file nella cartella:", os.getcwd())

# Caricamento CSV
df_persone = pd.read_csv("persone_25.csv")
df_documenti = pd.read_csv("documenti_25.csv")
df_fonti = pd.read_csv("fonti_25.csv")

# Radice XML
root = ET.Element("Dataset")

# Sezione FONTI
fonti_elem = ET.SubElement(root, "Fonti")
for _, row in df_fonti.iterrows():
    fonte = ET.SubElement(fonti_elem, "Fonte", attrib={"ID_Fonte": str(row["ID_Fonte"])})
    ET.SubElement(fonte, "Affidabilita").text = str(row["Affidabilita"])
    ET.SubElement(fonte, "Nazione").text = row["Nazione"]
    ET.SubElement(fonte, "NomeFonte").text = row["NomeFonte"]

# Sezione DOCUMENTI
documenti_elem = ET.SubElement(root, "Documenti")
for _, row in df_documenti.iterrows():
    doc = ET.SubElement(documenti_elem, "Documento", attrib={"ID_Documento": str(row["ID_Documento"]), "ID_Fonte": str(row["ID_Fonte"])})
    indirizzo = ET.SubElement(doc, "Indirizzo")
    ET.SubElement(indirizzo, "Via").text = row["Via"]
    ET.SubElement(indirizzo, "Citta").text = row["Citta"]
    ET.SubElement(indirizzo, "CAP").text = str(row["CAP"])
    ET.SubElement(indirizzo, "Nazione").text = row["Nazione"]
    ET.SubElement(doc, "Scadenza").text = str(row["Scadenza"])

# Sezione PERSONE
persone_elem = ET.SubElement(root, "Persone")
for _, row in df_persone.iterrows():
    persona = ET.SubElement(persone_elem, "Persona", attrib={"ID_Locale": str(row["ID_Locale"]), "ID_Documento": str(row["ID_Documento"]), "ID_Fonte": str(row["ID_Fonte"])})
    ET.SubElement(persona, "Nome").text = row["Nome"]
    ET.SubElement(persona, "Cognome").text = row["Cognome"]
    prof = ET.SubElement(persona, "Professione")
    ET.SubElement(prof, "NomeProfessione").text = row["NomeProfessione"]
    ET.SubElement(prof, "Settore").text = row["Settore"]

# Funzione per rientri (indentazione XML leggibile)
def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for child in elem:
            indent(child, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

# Salvataggio
indent(root)
tree = ET.ElementTree(root)
tree.write("dataset_25.xml", encoding="utf-8", xml_declaration=True)

print("✅ File XML generato correttamente: dataset_100.xml")
