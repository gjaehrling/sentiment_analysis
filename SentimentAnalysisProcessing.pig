-- load data
raw = LOAD 'SentimentAnalysis/output/temp_results_reducer_final' AS (
key:chararray,
sentiment:int
);

-- split input datat
splitted_raw = FOREACH raw GENERATE FLATTEN(STRSPLIT(key,'-')) as (productId:chararray, Aspect:chararray),sentiment;
ProductAspectSentiment = foreach splitted_raw generate productId,Aspect,sentiment;

-- group by artist and track
grouped_sentiment = GROUP ProductAspectSentiment BY (productId);

-- count tracks
counted_sentiment = FOREACH grouped_sentiment GENERATE FLATTEN(group), COUNT(ProductAspectSentiment) AS count;
total_sentiment = FOREACH grouped_sentiment GENERATE FLATTEN(group), SUM(ProductAspectSentiment.sentiment)

-- total sentiment by product
total_sentiment = FOREACH grouped_sentiment GENERATE FLATTEN(group), SUM(ProductAspectSentiment.sentiment);

-- order by counters
ordered_sentiment = ORDER counted_sentiment BY count DESC;

-- limit top 100 and dump
top_100_products = LIMIT ordered_sentiment 100;
STORE top_100_products INTO 'top_100_products.tsv';