import pandas as pd

#caricamento file completi
df_persone = pd.read_csv("persone.csv")
df_documenti = pd.read_csv("documenti.csv")
df_fonti = pd.read_csv("fonti.csv")

#funzione per creare subset
def crea_subset(percentuale):
    taglio = int(len(df_persone) * percentuale)
    subset_persone = df_persone.iloc[:taglio]
    
    #documenti usati da queste persone
    id_documenti_usati = subset_persone["ID_Documento"].unique()
    subset_documenti = df_documenti[df_documenti["ID_Documento"].isin(id_documenti_usati)]
    
    #fonti usate da queste persone
    id_fonti_usate = subset_persone["ID_Fonte"].unique()
    subset_fonti = df_fonti[df_fonti["ID_Fonte"].isin(id_fonti_usate)]

    #salvataggio
    nome = str(int(percentuale * 100))
    subset_persone.to_csv(f"persone_{nome}.csv", index=False)
    subset_documenti.to_csv(f"documenti_{nome}.csv", index=False)
    subset_fonti.to_csv(f"fonti_{nome}.csv", index=False)
    print(f"✔️ Generato subset {nome}%: {len(subset_persone)} persone, {len(subset_documenti)} documenti, {len(subset_fonti)} fonti")

#genera i tre subset
crea_subset(0.25)
crea_subset(0.50)
crea_subset(0.75)
