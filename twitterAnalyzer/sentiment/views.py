from django.shortcuts import render # For rendering HTTP requests
from django.http import HttpResponse
from django.http import Http404 # For not found
from django.db.models import Q, Subquery, Count, DecimalField # For running complex queries
from django.db.models.functions import ExtractHour
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import itertools
from .models import Tweet

def index(request):
    tweets = None
    counts = 0
    search = ''
    if request.GET.get('search'):
        search = request.GET.get('search')
        # Search for hashtag or mention like search term
        #tweets_with_hashtags = Tweet.objects.filter(~Q(hashtag='') | ~Q(mention=''))
        tweets = Tweet.objects.filter(Q(hashtag=search) | Q(mention=search))\
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
    #tweets = Tweet.objects.filter(Q(hashtag=tag) | Q(mention=tag))\
    #                      .values('hashtag', 'mention', 'tweeturl', 
    #                              'tweet', 'sentiment', 'user_name', 'time_stamp')

    tweets = Tweet.objects.filter(Q(hashtag='vote') | Q(mention='vote'))\
              .values(hour=ExtractHour('time_stamp'))\
              .annotate(negative=Count('sentiment',
                        output_field=DecimalField(max_digits=1, decimal_places=0),
                        filter=Q(sentiment='1',)), 
                        positive=Count('sentiment',
                        output_field=DecimalField(max_digits=1, decimal_places=0),
                        filter=Q(sentiment='0',))).order_by('hour')
    
    # Get statistics
    hours = list(range(0,24)) # Get a list of the hours in a day
    pos_hours = {hour: 0 for hour in hours} # Dictionary to store results
    neg_hours = {hour: 0 for hour in hours} # Dictionary to store results
    positive_count = 0
    negative_count = 0
    counts = 0
    for record in tweets.iterator():
        positive_count = positive_count + record["positive"]
        pos_hours[record["hour"]] = record["positive"]
        negative_count = negative_count + record["negative"]
        neg_hours[record["hour"]] = record["negative"]
        counts = counts + positive_count + negative_count
    
    #positive_count = tweets.filter(sentiment='0').count()
    #negative_count = tweets.filter(sentiment='1').count()
    positive_percent = positive_count/counts
    negative_percent = negative_count/counts
    
    # Values for y_axis bar graph and pie chart
    y_axis = [positive_count, negative_count]
    
    
    # For use as labels
    x_axis = ['positive', 'negative']
    
    # Get the pie chart
    colors = ['lightskyblue','gold']
    explode= (0.1,0)
    plt.pie(y_axis, explode=explode, labels=x_axis, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)
    plt.title('Positive vs Negative Sentiment Percentage')
    plt.legend('positive','negative')
    plt.axis('equal')
    plt.savefig(r'C:\twitter_analyzer\Scripts\twitterAnalyzer\sentiment\static\sentiment\sentiment_piechart.png')
    plt.gcf().clear()
    
    # Get the histogram
    plt.bar(x_axis, y_axis, align='center')
    plt.xlabel('Sentiment')
    plt.ylabel('Frequency')
    plt.title('Sentiment Distribution')
    plt.legend('positive','negative')
    plt.savefig(r'C:\twitter_analyzer\Scripts\twitterAnalyzer\sentiment\static\sentiment\sentiment_hist.png')
    plt.gcf().clear()
    
    number_bins = np.arange(len(hours))
    width = 0.35
    
    fig, ax = plt.subplots()
    
    pos_rect = ax.bar(number_bins, pos_hours.values(), width, color = 'lightskyblue')
    neg_rect = ax.bar(number_bins + width, neg_hours.values(), width, color = 'gold')
    ax.set_xlabel('Hour')
    ax.set_ylabel('Tweet Frequency')
    ax.set_title('Positive vs Negative Sentiment by Hour')
    ax.legend('positive','negative')
    ax.set_xticks(number_bins + width/2)
    ax.set_xticklabels(hours)
    plt.savefig(r'C:\twitter_analyzer\Scripts\twitterAnalyzer\sentiment\static\sentiment\sentiment_hour.png')
    plt.gcf().clear()
    
    header = tag
    
    return render(request, 'sentiment/detail.html', {'tweets': tweets,
                                                     'counts': counts,
                                                     'header': header,})
#def results(request, search):
#    return render(request, 'sentiment/results.html', {'search':search})
