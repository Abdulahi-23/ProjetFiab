from django.shortcuts import render
from django.http import HttpResponse
from .forms import ExportForm
import pandas as pd
import datetime
import logging
import os
import unicodedata
from django.conf import settings

logger = logging.getLogger(__name__)



fichier_totalite = os.path.join(settings.BASE_DIR, "static", "Totalité_fibres.xlsx")



# --- EXCEPTIONS ---
exceptions_numero_serie = [
    "NA","na","Na","N/A","N/a","N\\A","N_A","Res","ReS","N.A","N.a","nan","NaN","Nan",
    "RES","R E S","RÉS","R.E.S","Récap","Recap","RÉCAP","RECAP",
    "Récapitulation","RECAPITULATION","RÉCAPITULATION",
    "RECAP INTÉRIEUR", "RECAP EXTÉRIEUR","RÉCAP EXTÉRIEUR","RECAP+INT PBO","RÉCAPITULATIF",
    "RECAP+INT","RECAP+EXT PBO","RECAP+INTERIEUR PBO","RECAP+ COUVERCLE PBO",
    "RECAP+COUVERCLE PBO","Récap- Ext","RECAP+ INT","RECAP + INT PBO",
    "Récap int","Récap intérieur", "Récap Extérieur","RÉCAP INTÉRIEUR","Récap Extérieur PBO","RECAP+ EXT PBO ",
    "RECAP+ INT PBO","RECAP+ EXT PBO","Récap PBO","Recap PBO"
]
complexe = "ALCLF"


# --- FONCTIONS (copiées de ton script) ---
def verifier_conformite(row):
    numero_serie = str(row.get('numero_serie') or "").upper().strip()
    nd = str(row.get('nd') or "").upper().strip()
    exceptions_upper = [str(x).strip().upper() for x in exceptions_numero_serie]
    is_nd_nan = pd.isna(nd) or nd == "" or nd.lower() in ["nan", "na", "n/a"]
    
    
    if len(numero_serie) == 12 and nd == "WILDCARD":
        return "Conforme"
    elif complexe in numero_serie and (("NT" in nd) or ("IP" in nd) or ("LL" in nd)):
        return "Conforme"
    elif complexe in numero_serie and len(nd) >= 6:
        return "Conforme"
    elif len(numero_serie) == 12 and len(nd) == 9:
        return "Conforme"
    elif numero_serie in exceptions_upper and len(nd) == 9:
        return "Conforme"
    elif numero_serie not in exceptions_upper and len(nd) != 9:
        return "Non conformeNAKAMOU"
    elif numero_serie in exceptions_upper and is_nd_nan:
        return "Conforme"
    elif numero_serie == nd:
        return "Non Conforme"
    
    else:
        return "Non conforme"
    


def motif(row):
    numero_serie = str(row.get('numero_serie') or "").upper().strip()
    nd = str(row.get('nd') or "").upper().strip()

    if numero_serie == nd:
        return "Répétition du ZTE ou ND"
    elif numero_serie in exceptions_numero_serie and nd == "NAN":
        return None
    elif complexe in numero_serie and (("NT" in nd) or ("IP" in nd) or ("LL" in nd)):
        return None
    elif complexe in numero_serie and len(nd) != 0:
        return None
    elif len(numero_serie) == 12 and nd == "NAN":
        return "ND non renseigné"
    elif nd == "VOIP":
        return "ND non conforme"
    elif len(numero_serie) == 0 and nd == "NAN":
        return "ZTE et Nd non renseignés"
    elif len(numero_serie) == 0 and nd != "NAN":
        return "ZTE non renseigné"
    elif 4 < len(numero_serie) < 12 and numero_serie not in exceptions_numero_serie:
        return "ZTE non conforme (trop court)"
    elif nd == "nan" and numero_serie not in exceptions_numero_serie:
        return "ND non renseigné"
    elif len(numero_serie) >= 13 and numero_serie not in exceptions_numero_serie:
        return "ZTE non conforme (trop long)"
    elif len(numero_serie) < 12 and nd == "NAN":
        return "ZTE trop court & ND non renseigné"
    elif len(numero_serie) > 12 and nd == "NAN":
        return "ZTE trop long & ND non renseigné"
    elif numero_serie not in exceptions_numero_serie and len(nd) != 9:
        return "ND non conforme"
    


def analyser_fibres(df_totalite, df_export):
    df_totalite = df_totalite.copy().reset_index(drop=True)
    df_export = df_export.copy().reset_index(drop=True)

    # Nettoyage
    df_totalite['nom_eqpt'] = df_totalite['nom_eqpt'].astype(str).str.strip().str.upper()
    df_totalite['plaque'] = df_totalite['plaque'].astype(str).str.strip().str.upper()
    df_export['pbo'] = df_export['pbo'].astype(str).str.strip().str.upper()
    df_export['plaque'] = df_export['plaque'].astype(str).str.strip().str.upper()

    df_export['fibre'] = pd.to_numeric(df_export['fibre'], errors='coerce')
    df_export = df_export.dropna(subset=['fibre'])
    df_export['fibre'] = df_export['fibre'].astype(int)

    # Jointure entre la totalité et l'export
    merged = df_totalite.merge(
        df_export,
        how="left",
        left_on=["nom_eqpt", "plaque"],
        right_on=["pbo", "plaque"]
    )

    # Calcul des fibres présentes
    fibres_par_pbo = (
        merged.groupby(["nom_eqpt", "plaque"])["fibre"]
        .apply(lambda x: sorted(x.dropna().unique().tolist()))
        .reset_index()
    )

    df_totalite = df_totalite.merge(fibres_par_pbo, on=["nom_eqpt", "plaque"], how="left")

    # Calcul des fibres attendues et manquantes
    df_totalite["fibres_attendues"] = df_totalite["total_brin"].apply(
        lambda x: list(range(1, int(x) + 1)) if pd.notna(x) else []
    )
    df_totalite["fibres_manquantes"] = df_totalite.apply(
        lambda r: sorted(set(r["fibres_attendues"]) - set(r["fibre"] or []))
        if isinstance(r["fibres_attendues"], list)
        else [],
        axis=1
    )

    # Completude
    df_totalite["Completude"] = df_totalite.apply(
        lambda r: "COMPLET"
        if isinstance(r["fibres_attendues"], list)
        and len(r["fibres_attendues"]) == len(r["fibre"] or [])
        else "INCOMPLET",
        axis=1,
    )

    results = {
        (r["nom_eqpt"], r["plaque"]): {
            "Completude": r["Completude"],
            "Fibres_manquantes": ", ".join(map(str, r["fibres_manquantes"])) or "Aucune",
            "total_brin": r["total_brin"],
        }
        for _, r in df_totalite.iterrows()
    }

    return results


def concat_motifs(motifs):
    motifs_filtrés = list(filter(None, motifs))
    if not motifs_filtrés:
        return None
    vus = set()
    motifs_uniques = [m for m in motifs_filtrés if not (m in vus or vus.add(m))]
    return " & ".join(motifs_uniques)


def evaluer_conformite_fibres(conformites):
    return "Conforme" if all(c == "Conforme" for c in conformites) else "Non conforme"


# --- VIEW PRINCIPALE ---
def traiter_export(request):
    if request.method == "POST":
        form = ExportForm(request.POST, request.FILES)
        if form.is_valid():
            fichier_export = form.cleaned_data["fichier_export"]
            

            try:
                df_totalite = pd.read_excel(fichier_totalite, usecols=["nom_eqpt","plaque","total_brin"])
                df_export = pd.read_excel(fichier_export)

                completude_map = analyser_fibres(df_totalite, df_export)
                df_export['Résultat Conformité'] = df_export.apply(verifier_conformite, axis=1)
                df_export['Motif Invalidation'] = df_export.apply(motif, axis=1)

                conformite_pbo = df_export.groupby(['plaque','pbo'])['Résultat Conformité'].apply(evaluer_conformite_fibres).reset_index()
                conformite_pbo.rename(columns={'Résultat Conformité': 'Résultat Conformité PBO'}, inplace=True)

                motifs_pbo = df_export.groupby(['plaque','pbo'])['Motif Invalidation'].apply(concat_motifs).reset_index()

                cols_utiles = ['plaque','pbo','prestataire','subcontract_team_name']
                df_group = df_export[cols_utiles].drop_duplicates(subset=['plaque','pbo'])
                df_group = df_group.merge(conformite_pbo, on=['plaque','pbo'], how='left')
                df_group = df_group.merge(motifs_pbo, on=['plaque','pbo'], how='left')

                df_group['Completude PBO'] = df_group.apply(
                    lambda r: completude_map.get((r['pbo'], r['plaque']), {}).get("Completude", "INCONNU"),
                    axis=1
                )
                df_group['Fibres_manquantes'] = df_group.apply(
                    lambda r: completude_map.get((r['pbo'], r['plaque']), {}).get("Fibres_manquantes", "INCONNU"),
                    axis=1
                )
                df_group['total_brin'] = df_group.apply(
                    lambda r: completude_map.get((r['pbo'], r['plaque']), {}).get("total_brin", "INCONNU"),
                    axis=1
                )

                df_group.loc[df_group['Completude PBO'] == "INCOMPLET", 'Résultat Conformité PBO'] = "Non conforme"
                df_group.loc[df_group['Completude PBO'] == "INCOMPLET", 'Motif Invalidation'] = "PBO incomplet"
                df_group.loc[df_group['Completude PBO'] == "INCONNU", 'Résultat Conformité PBO'] = "Non Conforme"
                df_group.loc[df_group['Completude PBO'] == "INCONNU", 'Motif Invalidation'] = "Nomenclature PBO non correspondante à celle de la base"

                df_final = df_group[['plaque','pbo','prestataire','subcontract_team_name',
                                     'Résultat Conformité PBO','Motif Invalidation',
                                     'Completude PBO','Fibres_manquantes','total_brin']]

                date_str = datetime.datetime.now().strftime("%d%m%Y-%H%M")
                fichier_sortie = f"Controle_Fusion_{date_str}.xlsx"

                response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                response["Content-Disposition"] = f'attachment; filename="{fichier_sortie}"'
                df_final.to_excel(response, index=False)
                return response

            except Exception as e:
                logger.error(f"Erreur: {e}")
                return HttpResponse(f"Erreur: {e}", status=500)
    else:
        form = ExportForm()

    return render(request, "index.html", {"form": form})
