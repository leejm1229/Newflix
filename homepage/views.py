from django.shortcuts import render, redirect
from .models import Youtube, YoutubeReal
def home(request):
    
    MBCNEWS = YoutubeReal.objects.order_by('-id')
    SBSNEWS = Youtube.objects.filter(channel = 'SBS 뉴스')[:40]
    KBSNEWS = Youtube.objects.filter(channel = 'KBS News')

    return render(request, 'homepage/homepage.html', {'MBCNEWS':MBCNEWS, 'SBSNEWS':SBSNEWS, 'KBSNEWS':KBSNEWS})

