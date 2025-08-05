
import pandas as pd
from django.shortcuts import render, redirect
from .forms import ExcelUploadForm
from .models import Derangement
from django.core.files.storage import default_storage
from django.conf import settings
import os
from django.utils.timezone import make_aware, get_default_timezone
from django.http import HttpResponse
from django.db.models import Count

tz = get_default_timezone()
# Create your views here.

def safe_parse_datetime(val):
    if pd.isna(val):
        return None
    if isinstance(val, str):
        try:
            val = pd.to_datetime(val)
        except Exception:
            return None
    if val.tzinfo is None:
        # Rendre le datetime timezone-aware en supposant le timezone par défaut
        val = make_aware(val, timezone=tz)
    return val

def importer_excels(request):
    if request.method == 'POST':
        fichiers = request.FILES.getlist('fichiers')

        for fichier in fichiers:
            # Chemin d'enregistrement temporaire
            path = default_storage.save(f'excels/{fichier.name}', fichier)
            file_path = os.path.join(settings.MEDIA_ROOT, path)

            try:
                df = pd.read_excel(file_path, sheet_name='Feuil1')
                for _, row in df.iterrows():
                    Derangement.objects.create(
                        id_drgt=row.get('ID_DRGT'),
                        service_technique=row.get('SERVICE_TECHNIQUE'),
                        ncli=row.get('NCLI'),
                        nd=row.get('ND'),
                        etat_dossier=row.get('ETAT_DOSSIER'),
                        produit=row.get('PRODUIT'),

                        nom_du_client=row.get('NOM_DU_CLIENT'),
                        prenom_du_client=row.get('PRENOM_DU_CLIENT'),
                        contact_client=row.get('CONTACT_CLIENT'),
                        commentaire_contact=row.get('COMMENTAIRE_CONTACT'),

                        c_gest=row.get('C_GEST'),
                        segment=row.get('SEGMENT'),
                        categorie=row.get('CATEGORIE'),
                        date_msv_acces_reseau=safe_parse_datetime(row.get('DATE_MSV_ACCES_RESEAU')),
                        acces_rx=row.get('ACCES_RX'),
                        date_resil_acces_rx=safe_parse_datetime(row.get('DATE_RESIL_ACCES_RX')),
                        etat_drgt=row.get('ETAT_DRGT'),
                        date_si=safe_parse_datetime(row.get('DATE_SI')),
                        agent_sig=row.get('AGENT_SIG'),

                        libel_orig=row.get('LIBEL_ORIG'),
                        libel_sig=row.get('LIBEL_SIG'),
                        commentaire_sig=row.get('COMMENTAIRE_SIG'),

                        ss_reseau=row.get('SS_RESEAU'),
                        secteur_geo=row.get('SECTEUR_GEO'),
                        zone_rs=row.get('ZONE_RS'),
                        libelle_commune=row.get('LIBELLE_COMMUNE'),
                        libelle_quartier=row.get('LIBELLE_QUARTIER'),
                        libelle_voie=row.get('LIBELLE_VOIE'),
                        nvoie=row.get('NVOIE'),

                        id_drgt_collectif=row.get('ID_DRGT_COLLECTIF'),
                        date_ess=safe_parse_datetime(row.get('DATE_ESS')),
                        priorite_drgt=row.get('PRIORITE_DRGT'),
                        option_atr_h=row.get('OPTION_ATR_H'),
                        priorite_serv=row.get('PRIORITE_SERV'),
                        specialite=row.get('SPECIALITE'),
                        result_ess=row.get('RESULT_ESS'),
                        commentaire_essai=row.get('COMMENTAIRE_ESSAI'),
                        agent_ess=row.get('AGENT_ESS'),

                        date_demande_int= safe_parse_datetime(row.get('DATE_DEMANDE_INT')),
                        commentaire_interv=row.get('COMMENTAIRE_INTERV'),
                        agent_dem_int=row.get('AGENT_DEM_INT'),

                        id_ot=row.get('ID_OT'),
                        type_ot=row.get('TYPE_OT'),
                        date_etat_ot=safe_parse_datetime(row.get('DATE_ETAT_OT')),
                        etat_ot=row.get('ETAT_OT'),

                        date_rv=safe_parse_datetime(row.get('DATE_RV')),
                        rdv=row.get('RDV'),

                        code_ui=row.get('CODE_UI'),
                        libelle_ui=row.get('LIBELLE_UI'),
                        equipe=row.get('EQUIPE'),

                        date_releve_prevision=safe_parse_datetime(row.get('DATE_RELEVE_PREVISION')),
                        date_releve=safe_parse_datetime(row.get('DATE_RELEVE')),
                        respect_delai=row.get('RESPECT_DELAI'),

                        libelle_releve=row.get('LIBELLE_RELEVE'),
                        libelle_cause=row.get('LIBELLE_CAUSE'),
                        libelle_localis=row.get('LIBELLE_LOCALIS'),
                        commentaire_releve=row.get('COMMENTAIRE_RELEVE'),
                        agent_releve=row.get('AGENT_RELEVE'),

                        techno=row.get('Techno'),
                        type=row.get('Type'),
                        cause=row.get('CAUSE'),
                        client=row.get('CLIENT'),
                        
                            )
                    

            except Exception as e:
                print(f"Erreur avec {fichier.name} : {e}")

        return HttpResponse('Les fichiers ont été uploadés dans la base avec succès!!')
    
    form = ExcelUploadForm()
    return render(request, 'importer.html', {'form': form})


def upload_et_recherche(request):
    message = ''
    result = None
    query = request.GET.get('q')

    # Traitement de l'import Excel
    if request.method == 'POST' and request.FILES.getlist('fichiers'):
        fichiers = request.FILES.getlist('fichiers')
        all_data = pd.DataFrame()

        for fichier in fichiers:
            df = pd.read_excel(fichier,sheet_name="Feuil1")
            all_data = pd.concat([all_data, df], ignore_index=True)

        # Insertion dans la base de données (évite les doublons si besoin)
        for _, row in all_data.iterrows():
            Derangement.objects.create(
                id_drgt=row.get('ID_DRGT'),
                        service_technique=row.get('SERVICE_TECHNIQUE'),
                        ncli=row.get('NCLI'),
                        nd=row.get('ND'),
                        etat_dossier=row.get('ETAT_DOSSIER'),
                        produit=row.get('PRODUIT'),

                        nom_du_client=row.get('NOM_DU_CLIENT'),
                        prenom_du_client=row.get('PRENOM_DU_CLIENT'),
                        contact_client=row.get('CONTACT_CLIENT'),
                        commentaire_contact=row.get('COMMENTAIRE_CONTACT'),

                        c_gest=row.get('C_GEST'),
                        segment=row.get('SEGMENT'),
                        categorie=row.get('CATEGORIE'),
                        date_msv_acces_reseau=safe_parse_datetime(row.get('DATE_MSV_ACCES_RESEAU')),
                        acces_rx=row.get('ACCES_RX'),
                        date_resil_acces_rx=safe_parse_datetime(row.get('DATE_RESIL_ACCES_RX')),
                        etat_drgt=row.get('ETAT_DRGT'),
                        date_si=safe_parse_datetime(row.get('DATE_SI')),
                        agent_sig=row.get('AGENT_SIG'),

                        libel_orig=row.get('LIBEL_ORIG'),
                        libel_sig=row.get('LIBEL_SIG'),
                        commentaire_sig=row.get('COMMENTAIRE_SIG'),

                        ss_reseau=row.get('SS_RESEAU'),
                        secteur_geo=row.get('SECTEUR_GEO'),
                        zone_rs=row.get('ZONE_RS'),
                        libelle_commune=row.get('LIBELLE_COMMUNE'),
                        libelle_quartier=row.get('LIBELLE_QUARTIER'),
                        libelle_voie=row.get('LIBELLE_VOIE'),
                        nvoie=row.get('NVOIE'),

                        id_drgt_collectif=row.get('ID_DRGT_COLLECTIF'),
                        date_ess=safe_parse_datetime(row.get('DATE_ESS')),
                        priorite_drgt=row.get('PRIORITE_DRGT'),
                        option_atr_h=row.get('OPTION_ATR_H'),
                        priorite_serv=row.get('PRIORITE_SERV'),
                        specialite=row.get('SPECIALITE'),
                        result_ess=row.get('RESULT_ESS'),
                        commentaire_essai=row.get('COMMENTAIRE_ESSAI'),
                        agent_ess=row.get('AGENT_ESS'),

                        date_demande_int= safe_parse_datetime(row.get('DATE_DEMANDE_INT')),
                        commentaire_interv=row.get('COMMENTAIRE_INTERV'),
                        agent_dem_int=row.get('AGENT_DEM_INT'),

                        id_ot=row.get('ID_OT'),
                        type_ot=row.get('TYPE_OT'),
                        date_etat_ot=safe_parse_datetime(row.get('DATE_ETAT_OT')),
                        etat_ot=row.get('ETAT_OT'),

                        date_rv=safe_parse_datetime(row.get('DATE_RV')),
                        rdv=row.get('RDV'),

                        code_ui=row.get('CODE_UI'),
                        libelle_ui=row.get('LIBELLE_UI'),
                        equipe=row.get('EQUIPE'),

                        date_releve_prevision=safe_parse_datetime(row.get('DATE_RELEVE_PREVISION')),
                        date_releve=safe_parse_datetime(row.get('DATE_RELEVE')),
                        respect_delai=row.get('RESPECT_DELAI'),

                        libelle_releve=row.get('LIBELLE_RELEVE'),
                        libelle_cause=row.get('LIBELLE_CAUSE'),
                        libelle_localis=row.get('LIBELLE_LOCALIS'),
                        commentaire_releve=row.get('COMMENTAIRE_RELEVE'),
                        agent_releve=row.get('AGENT_RELEVE'),

                        techno=row.get('Techno'),
                        type=row.get('Type'),
                        cause=row.get('CAUSE'),
                        client=row.get('CLIENT'),
                        
            )

        message = f"{len(all_data)} lignes importées avec succès."

    # Traitement de la recherche
    if query:
        result = (
            Derangement.objects
            .filter(commentaire_releve__icontains=query)
            .values('commentaire_releve')
            .annotate(freq=Count('commentaire_releve'))
            .order_by('-freq')
            .first()
        )

    return render(request, 'upload_recherche.html', {
        'result': result,
        'query': query,
        'message': message
    })

