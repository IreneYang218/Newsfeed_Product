-- View: api.articles

-- DROP VIEW api.articles;

CREATE OR REPLACE VIEW api.articles AS
    SELECT *
    FROM news.articles;

grant select on api.articles to web_anon;