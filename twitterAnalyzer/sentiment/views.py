from django.shortcuts import render # For rendering HTTP requests
from django.http import HttpResponse
from django.http import Http404 # For not found
from django.db.models import Q, Subquery, Count, DecimalField # For running complex queries
from django.db.models.functions import ExtractHour
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import numpy as np
import matplotlib
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import itertools
import array as arr
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

    tweets = Tweet.objects.filter(Q(hashtag=tag) | Q(mention=tag))\
              .values(hour=ExtractHour('time_stamp'))\
              .annotate(negative=Count('sentiment',
                        output_field=DecimalField(max_digits=1, decimal_places=0),
                        filter=Q(sentiment='1',)), 
                        positive=Count('sentiment',
                        output_field=DecimalField(max_digits=1, decimal_places=0),
                        filter=Q(sentiment='0',)),
                        count=Count('sentiment',
                        output_field=DecimalField(max_digits=1, decimal_places=0))).order_by('hour')
    
    # Get statistics
    hours = list(range(0,24)) # Get a list of the hours in a day
    pos_hours = {hour: 0 for hour in hours} # Dictionary to store results
    neg_hours = {hour: 0 for hour in hours} # Dictionary to store results
    positive_count = 0
    negative_count = 0
    #count_tweets = {hour: 0 for hour in hours};
    #avg_positive = 0
    #avg_negative = 0
    counts = 0
    pos_cumulative = arr.array('f', [])
    neg_cumulative = arr.array('f', [])
    #tweets_cumulative = arr.array('i', [])
    for record in tweets.iterator():
        positive_count = positive_count + record["positive"]
        pos_hours[record["hour"]] = record["positive"]
        negative_count = negative_count + record["negative"]
        neg_hours[record["hour"]] = record["negative"]
        counts = counts + positive_count + negative_count
        #count_tweets[record["hour"]] = record["count"] 
        pos_cumulative.append(positive_count)
        neg_cumulative.append(negative_count)
        #tweets_cumulative.append(counts)
        #avg_positive[record["hour"]] = (positive_count // counts)
        #avg_negative[record["hour"]] = (negative_count // counts)
    
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
    plt.savefig(r'C:\twitterAnalyzer\Scripts\twitterAnalyzer\sentiment\static\sentiment\sentiment_piechart.png')
    plt.gcf().clear()
    
    # Get the histogram
    plt.bar(x_axis, y_axis, align='center')
    plt.xlabel('Sentiment')
    plt.ylabel('Frequency')
    plt.title('Sentiment Distribution')
    plt.legend('positive','negative')
    plt.savefig(r'C:\twitterAnalyzer\Scripts\twitterAnalyzer\sentiment\static\sentiment\sentiment_hist.png')
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
    plt.savefig(r'C:\twitterAnalyzer\Scripts\twitterAnalyzer\sentiment\static\sentiment\sentiment_hour.png')
    plt.gcf().clear()

    # Get the double line graph
    x = np.arange(len(hours))

    #plt.gca().set_color_cycle(['blue', 'red'])
    plt.xlabel('Hour');
    plt.ylabel('Tweet Frequency');
    plt.title('Positive vs Negative Sentiment Frequency Over Time (Hours)');

    plt.plot(x, pos_cumulative[:])
    plt.plot(x, neg_cumulative[:])
    #plt.plot(x, tweets_cumulative[:])
    

    plt.legend(['Positive sentiment', 'Negative sentiment'], loc='upper left')

    plt.savefig(r'C:\twitterAnalyzer\Scripts\twitterAnalyzer\sentiment\static\sentiment\double_line_sentiment_hour.png')
    plt.gcf().clear()
    #plt.show()
        
    header = tag
    
    return render(request, 'sentiment/detail.html', {'tweets': tweets,
                                                     'counts': counts,
                                                     'header': header,})
#def results(request, search):
#    return render(request, 'sentiment/results.html', {'search':search})
