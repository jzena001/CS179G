------------------
---Marlo Zeroth---
----11/26/2018----
------------------

--------------
---Clean up---
--------------

DROP TABLE IF EXISTS sentiment_tweet CASCADE;--OK
DROP TABLE IF EXISTS tweets CASCADE;--OK
------------
---TABLES---
------------

CREATE TABLE sentiment_tweet (   
    id SERIAL NOT NULL,
    geo CHAR (6) NOT NULL,
    hashtag VARCHAR(280),
    tweetkey NUMERIC(19,0) NOT NULL,
    latitude NUMERIC(9,6),
    longitude NUMERIC(9,6),
    mention VARCHAR(280),
    tweet VARCHAR(1024) NOT NULL,
    time_stamp TIMESTAMPTZ NOT NULL,
    user_name VARCHAR(280) NOT NULL,
    sentiment NUMERIC(1,0) NOT NULL,
    PRIMARY KEY(id)
);

----------------
--Import Data---
----------------

COPY sentiment_tweet (
    geo,
    hashtag,
    tweetkey,
    latitude,
    longitude,
    mention,
    tweet,
    time_stamp,
    user_name,
    sentiment)
FROM 'c:/postgresql/scripts/sentimentTweets20181104.csv'
WITH DELIMITER ',';

COPY sentiment_tweet (
    geo,
    hashtag,
    tweetkey,
    latitude,
    longitude,
    mention,
    tweet,
    time_stamp,
    user_name,
    sentiment)
FROM 'c:/postgresql/scripts/sentimentTweets20181105.csv'
WITH DELIMITER ',';

COPY sentiment_tweet (
    geo,
    hashtag,
    tweetkey,
    latitude,
    longitude,
    mention,
    tweet,
    time_stamp,
    user_name,
    sentiment)
FROM 'c:/postgresql/scripts/sentimentTweets20181106.csv'
WITH DELIMITER ',';

        
COPY sentiment_tweet (
    geo,
    hashtag,
    tweetkey,
    latitude,
    longitude,
    mention,
    tweet,
    time_stamp,
    user_name,
    sentiment)
FROM 'c:/postgresql/scripts/sentimentTweets20181107.csv'
WITH DELIMITER ',';

COPY sentiment_tweet (
    geo,
    hashtag,
    tweetkey,
    latitude,
    longitude,
    mention,
    tweet,
    time_stamp,
    user_name,
    sentiment)
FROM 'c:/postgresql/scripts/sentimentTweets20181122.csv'
WITH DELIMITER ',';
--- Error
COPY sentiment_tweet (
    geo,
    hashtag,
    tweetkey,
    latitude,
    longitude,
    mention,
    tweet,
    time_stamp,
    user_name,
    sentiment)
FROM 'c:/postgresql/scripts/sentimentTweets20181123.csv'
WITH DELIMITER ',';

COPY sentiment_tweet (
    geo,
    hashtag,
    tweetkey,
    latitude,
    longitude,
    mention,
    tweet,
    time_stamp,
    user_name,
    sentiment)
FROM 'c:/postgresql/scripts/sentimentTweets20181124.csv'
WITH DELIMITER ',';
                