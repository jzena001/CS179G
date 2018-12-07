from django.shortcuts import render # For rendering HTTP requests
from django.http import HttpResponse
from django.http import Http404 # For not found
from django.db.models import Q, Subquery # For running complex queries
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

from .models import Tweet

def index(request):
    tweets = None
    counts = 0
    search = ''

    if request.GET.get('search'):
        search = request.GET.get('search')
        # Search for hashtag or mention like search term
        #tweets_with_hashtags = Tweet.objects.filter(~Q(hashtag='') | ~Q(mention=''))
        tweets = Tweet.objects.filter(Q(hashtag__search=search) | Q(mention__search=search))\
                              .values('hashtag', 'mention', 'tweeturl', 
                                      'tweet', 'sentiment', 'user_name', 'time_stamp')
                                      
        counts = tweets.count()
        # Render the results in the same page    
    return render(request, 'sentiment/index.html', {'tweets': tweets, 
                                                    'counts':counts, 'search': search})
        


def detail(request, tag):
    tweets = None
    counts = 0
    # Search for that specific hashtag
    #tweets = Tweet.object.filter(~Q(hashtag='') | ~Q(mention=''))\
    #                     .filter(Q(hashtag=tag) | Q(mention=tag))\
    #                     .values('hashtag', 'mention', 'tweetkey', 
    #                             'tweet', 'sentiment', 'user_name', 
    #                             'time_stamp')
                                                                             
    tweets = Tweet.objects.filter(Q(hashtag=tag) | Q(mention=tag))\
                          .values('hashtag', 'mention', 'tweetkey', 
                                  'tweet', 'sentiment', 'user_name', 'time_stamp')
    
    positive_count = tweets.filter(sentiment='0').count()
    negative_count = tweets.filter(sentiment='1').count()
    
    y_axis = [positive_count, negative_count]
    x_axis = ['positive', 'negative']

    plt.bar(x_axis, y_axis, align='center')
    plt.xlabel('Sentiment')
    plt.ylabel('Frequency')
    path = 'C:\twitter_analyzer\Scripts\twitterAnalyzer\sentiment_hist.png'
    plt.savefig(r'C:\twitter_analyzer\Scripts\twitterAnalyzer\sentiment\static\sentiment\sentiment_hist.png')
    plt.gcf().clear()
    counts = tweets.count()
    header = tag
    return render(request, 'sentiment/detail.html', {'tweets': tweets, 
                                                     'counts': counts, 
                                                     'header': header,})

#def results(request, search):
#    return render(request, 'sentiment/results.html', {'search':search})
