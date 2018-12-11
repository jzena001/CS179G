import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

class Tweet(models.Model):
    geo = models.CharField(max_length=6)
    
    hashtag = models.CharField(max_length=280, 
                               null = True)
                               
    tweetkey = models.DecimalField(max_digits = 19, 
                                   decimal_places=0)
                                   
    latitude = models.DecimalField(max_digits = 9, 
                                   decimal_places = 6, 
                                   null = True)
                                   
    longitude = models.DecimalField(max_digits = 9, 
                                    decimal_places = 6, 
                                    null = True)
                                    
    mention = models.CharField(max_length=280, 
                               null = True)
                               
    tweet = models.CharField(max_length=1024)
    
    time_stamp = models.DateTimeField('date posted')
    
    tweeturl = models.CharField(max_length=128)
    
    user_name = models.CharField(max_length = 280)
    
    sentiment = models.DecimalField(max_digits = 1, 
                                    decimal_places = 0)
    
    def __str__(self):
        output = self.geo + "\t" + self.hashtag + "\t" + self.tweet_id\
                          + "\t" + latitude + "\t" + self.longitude\
                          + "\t" + self.mention + "\t" + self.tweet + "\t"\
                          + self.time_stamp + "\t" + self.user_name + "\t"\
                          + self.sentiment
        return output
    
