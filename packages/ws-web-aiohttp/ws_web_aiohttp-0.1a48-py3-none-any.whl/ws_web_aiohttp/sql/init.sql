CREATE TABLE IF NOT EXISTS users
(
  id BIGSERIAL PRIMARY KEY,
  userid character varying(256) NOT NULL,
  disabled boolean NOT NULL DEFAULT false,
  CONSTRAINT user_userid_key UNIQUE (userid)
);

CREATE TABLE IF NOT EXISTS books
(
  id BIGSERIAL PRIMARY KEY,
  user_id integer NOT NULL,
  bookid character varying(256) NOT NULL,
  CONSTRAINT user_book_fkey FOREIGN KEY (user_id)
      REFERENCES users (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE
);


