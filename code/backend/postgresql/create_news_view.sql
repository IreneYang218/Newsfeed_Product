-- View: api.articles

-- DROP VIEW api.articles;

CREATE OR REPLACE VIEW api.articles AS
    SELECT *
    FROM newsphi.news_articles;

ALTER TABLE api.articles OWNER TO newsphi;
grant ALL on TABLE api.articles to newsphi;
grant select on TABLE api.articles to web_anon;