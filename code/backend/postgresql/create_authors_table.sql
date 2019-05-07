-- Table: newsphi.news_authors

-- DROP TABLE newsphi.news_authors cascade;

CREATE TABLE newsphi.news_authors
(
    author_name varchar(256) PRIMARY KEY,
    reputation_score double precision,
    tweet_site varchar(256),
    rank numeric
);

ALTER TABLE newsphi.news_authors OWNER to newsphi;