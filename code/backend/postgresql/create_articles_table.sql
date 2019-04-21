-- Table: newsphi.news_articles

-- DROP TABLE newsphi.news_articles;

CREATE TABLE newsphi.news_articles
(
    article_id SERIAL PRIMARY KEY,
    author_id integer REFERENCES newsphi.authors (author_id),
    title varchar(256) NOT NULL,
    author varchar(256),
    published_time TIMESTAMP NOT NULL,
    site_full varchar(256) NOT NULL,
    main_image varchar(256),
    post_link varchar(256) NOT NULL,
    news_topic varchar(256),
    controversy_score double precision
);

ALTER TABLE newsphi.news_articles OWNER to newsphi;