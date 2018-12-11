--- Marlo Zeroth
--- 861309346
--- Indeces to optimize most made queries.

CREATE INDEX IF NOT EXISTS hashtag_fts_index
ON sentiment_tweet
USING GIN
(to_tsvector('english', hashtag));

CREATE INDEX IF NOT EXISTS mention_fts_index
ON sentiment_tweet
USING GIN
(to_tsvector('english', mention));

CREATE INDEX IF NOT EXISTS hashtag_mention_fts_index
ON sentiment_tweet
USING GIN
((to_tsvector('english', mention)), (to_tsvector('english', hashtag)));



CREATE INDEX IF NOT EXISTS hastag_mention_index
ON sentiment_tweet
USING BTREE
(hashtag, mention);

CREATE INDEX IF NOT EXISTS hashtag_lower_index
ON sentiment_tweet
USING BTREE
(lower(hashtag));

CREATE INDEX IF NOT EXISTS metion_lower_index
ON sentiment_tweet
USING BTREE
(lower(mention));

CREATE INDEX  IF NOT EXISTS hashtag_index
ON sentiment_tweet
USING BTREE
(hashtag);

CREATE INDEX  IF NOT EXISTS mention_index
ON sentiment_tweet
USING BTREE
(mention);

CREATE INDEX  IF NOT EXISTS user_index
ON sentiment_tweet
USING BTREE
(user_name);

CREATE INDEX  IF NOT EXISTS time_index
ON sentiment_tweet
USING BTREE
(time_stamp);

CREATE INDEX  IF NOT EXISTS geo_index
ON sentiment_tweet
USING BTREE
(geo);
