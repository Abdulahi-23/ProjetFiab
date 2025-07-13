from django.db import models

class Derangement(models.Model):
    # Ce champ 'id' est automatiquement ajouté par Django, mais on peut le rendre explicite :
    id_db = models.AutoField(primary_key=True)

    id_drgt = models.BigIntegerField()  # plus clé primaire, mais doit rester unique
    service_technique = models.CharField(max_length=50)
    ncli = models.CharField(max_length=50, null=True, blank=True)
    nd = models.CharField(max_length=50, null=True, blank=True)
    etat_dossier = models.CharField(max_length=50)
    produit = models.CharField(max_length=50)

    nom_du_client = models.CharField(max_length=100, null=True, blank=True)
    prenom_du_client = models.CharField(max_length=100, null=True, blank=True)
    contact_client = models.CharField(max_length=30, null=True, blank=True)
    commentaire_contact = models.TextField(null=True, blank=True)

    c_gest = models.CharField(max_length=50, null=True, blank=True)
    segment = models.CharField(max_length=50, null=True, blank=True)
    categorie = models.CharField(max_length=50, null=True, blank=True)
    date_msv_acces_reseau = models.DateTimeField(null=True, blank=True)
    acces_rx = models.CharField(max_length=100, null=True, blank=True)
    date_resil_acces_rx = models.DateTimeField(null=True, blank=True)
    etat_drgt = models.CharField(max_length=50, null=True, blank=True)
    date_si = models.DateTimeField(null=True, blank=True)
    agent_sig = models.CharField(max_length=100, null=True, blank=True)

    libel_orig = models.TextField(null=True, blank=True)
    libel_sig = models.TextField(null=True, blank=True)
    commentaire_sig = models.TextField(null=True, blank=True)

    ss_reseau = models.CharField(max_length=50, null=True, blank=True)
    secteur_geo = models.CharField(max_length=50, null=True, blank=True)
    zone_rs = models.CharField(max_length=50, null=True, blank=True)
    libelle_commune = models.CharField(max_length=100, null=True, blank=True)
    libelle_quartier = models.CharField(max_length=100, null=True, blank=True)
    libelle_voie = models.CharField(max_length=100, null=True, blank=True)
    nvoie = models.CharField(max_length=100, null=True, blank=True)

    id_drgt_collectif = models.CharField(max_length=50, null=True, blank=True)
    date_ess = models.DateTimeField(null=True, blank=True)
    priorite_drgt = models.CharField(max_length=50, null=True, blank=True)
    option_atr_h = models.CharField(max_length=20, null=True, blank=True)
    priorite_serv = models.CharField(max_length=50, null=True, blank=True)
    specialite = models.CharField(max_length=50, null=True, blank=True)
    result_ess = models.CharField(max_length=100, null=True, blank=True)
    commentaire_essai = models.TextField(null=True, blank=True)
    agent_ess = models.CharField(max_length=100, null=True, blank=True)

    date_demande_int = models.DateTimeField(null=True, blank=True)
    commentaire_interv = models.TextField(null=True, blank=True)
    agent_dem_int = models.CharField(max_length=100, null=True, blank=True)

    id_ot = models.CharField(max_length=50, null=True, blank=True)
    type_ot = models.CharField(max_length=50, null=True, blank=True)
    date_etat_ot = models.DateTimeField(null=True, blank=True)
    etat_ot = models.CharField(max_length=50, null=True, blank=True)

    date_rv = models.DateTimeField(null=True, blank=True)
    rdv = models.CharField(max_length=50, null=True, blank=True)

    code_ui = models.CharField(max_length=50, null=True, blank=True)
    libelle_ui = models.CharField(max_length=100, null=True, blank=True)
    equipe = models.CharField(max_length=50, null=True, blank=True)

    date_releve_prevision = models.DateTimeField(null=True, blank=True)
    date_releve = models.DateTimeField(null=True, blank=True)
    respect_delai = models.CharField(max_length=20, null=True, blank=True)

    libelle_releve = models.TextField(null=True, blank=True)
    libelle_cause = models.TextField(null=True, blank=True)
    libelle_localis = models.TextField(null=True, blank=True)
    commentaire_releve = models.TextField(null=True, blank=True)
    agent_releve = models.CharField(max_length=100, null=True, blank=True)

    techno = models.CharField(max_length=50, null=True, blank=True)
    type = models.CharField(max_length=50, null=True, blank=True)
    cause = models.CharField(max_length=100, null=True, blank=True)
    client = models.CharField(max_length=255, null=True, blank=True)
    semaine = models.CharField(max_length=15)

    class Meta:
        verbose_name = "Relevé"
        verbose_name_plural = "Relevés"

    def __str__(self):
        return f"{self.id_drgt} - {self.nom_du_client or ''}"
