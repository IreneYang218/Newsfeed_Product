-- View: api.news

-- DROP VIEW api.news;

CREATE OR REPLACE VIEW api.news AS
    SELECT *
    FROM news.sample;

create role web_anon nologin;

grant select on api.news to web_anon;