-- View: api.authors

-- DROP VIEW api.authors;

CREATE OR REPLACE VIEW api.authors AS
    SELECT *
    FROM newsphi.news_authors;

ALTER TABLE api.authors OWNER TO newsphi;
grant ALL on TABLE api.authors to newsphi;
grant select on TABLE api.authors to web_anon;