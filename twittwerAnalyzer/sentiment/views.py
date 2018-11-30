from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404

from .models import Tweet

def index(request):
    tweets = None
    if request.GET.get('search'):
        search = request.GET.get('search')
        # Search for hashtag like search term
        tweets = Tweet.objects.filter(hashtag__icontains=search)\
                              .values('hashtag', 'mention', 'tweetkey', 
                                      'tweet', 'sentiment', 'time_stamp')
        # Render the results in the same page    
    return render(request, 'sentiment/index.html', {'tweets': tweets,})
