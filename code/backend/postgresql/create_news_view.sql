-- View: api.articles

-- DROP VIEW api.articles;

CREATE OR REPLACE VIEW api.articles AS
    WITH topic_std as (
    SELECT news_topic, STDDEV(sentiment_score) as std_sentiment
    FROM news_articles
    GROUP BY 1)
	SELECT *
	FROM news_articles
	LEFT JOIN
	    (
	    SELECT *, (std_sentiment - (SELECT MIN(std_sentiment) FROM topic_std))*100/
	        ((SELECT MAX(std_sentiment) FROM topic_std) - 
	            (SELECT MIN(std_sentiment) FROM topic_std)) as controversy_score_new
	    FROM topic_std) as f
	USING (news_topic);

ALTER TABLE api.articles OWNER TO newsphi;
grant ALL on TABLE api.articles to newsphi;
grant select on TABLE api.articles to web_anon;