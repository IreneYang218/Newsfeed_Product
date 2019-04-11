-- Table: api.user

-- DROP TABLE api.user;

CREATE TABLE api.user
(
    user_name text NOT NULL,
    user_email text NOT NULL,
    user_pwd text NOT NULL,
    favorite text NOT NULL
);