from django.shortcuts import render
from search.models import Derangement
from django.db.models import Count

def index(request):
    return render(request,'accueil.html')

from django.db.models import Count

def searchdb(request):
    query = request.GET.get('q')  # nom du paramètre dans le formulaire : q ou autre
    cause = None
    commentaire = None
    total = 0
    
    if query:
        # Filtrer les dérangements avec commentaire_releve qui contient la query
        filtered = Derangement.objects.filter(commentaire_releve__icontains=query)
        
        # Grouper par cause, compter occurrences et prendre la cause la plus fréquente
        cause_agg = filtered.values('cause').annotate(total=Count('cause')).order_by('-total').first()
        
        if cause_agg:
            cause = cause_agg['cause']
            total = cause_agg['total']
            
            # Récupérer un commentaire_releve associé à cette cause (par exemple le premier)
            commentaire_obj = filtered.filter(cause=cause).first()
            if commentaire_obj:
                commentaire = commentaire_obj.commentaire_releve

    return render(request, 'searchdb.html', {
        'cause': cause,
        'commentaire': commentaire,
        'total': total,
        'query': query
    })
def login(request):
    return render(request,'login.html')
    
def signup(request):
    return render(request,'inscription.html')
