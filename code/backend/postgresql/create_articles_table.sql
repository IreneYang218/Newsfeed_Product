-- Table: news.articles

-- DROP TABLE news.articles;

CREATE TABLE news.articles
(
    title text NOT NULL,
    author text,
    published TIMESTAMP NOT NULL,
    site_full text NOT NULL,
    main_image text NOT NULL,
    post_link text NOT NULL,
    dominat_topic NUMERIC,
    keywords text,
    controversy_score NUMERIC
);