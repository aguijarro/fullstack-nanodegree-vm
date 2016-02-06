-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Create database

--psql
--vagrant=> \i tournament.sql

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;


CREATE TABLE tournament(
  id_tournament serial primary key,
  name text,
  description text,
  init_date date,
  end_date date
);

CREATE TABLE player(
  id_player serial primary key,
  id_tournament integer references tournament,
  name text
);

CREATE TABLE match(
  id_match serial primary key,
  id_tournament integer references tournament,
  id_winner integer references player,
  id_loser integer references player
);

CREATE or REPLACE VIEW scoreboard AS
SELECT  p.id_player,
        p.name,
         coalesce (played.matches, 0) matches,
         coalesce (win.win, 0) win,
         coalesce (lost.lost, 0) lost
    FROM (  SELECT un.PLAYER, SUM (un.MATCHES) matches
              FROM (  SELECT id_winner player, COUNT (*) AS matches
                        FROM match
                    GROUP BY id_winner
                    UNION ALL
                      SELECT id_loser player, COUNT (*) AS matches
                        FROM match
                    GROUP BY id_loser) un
          GROUP BY PLAYER) played
         LEFT JOIN (  SELECT id_winner player, COUNT (*) AS win
                        FROM match
                    GROUP BY id_winner) win
            ON played.PLAYER = win.PLAYER
         LEFT JOIN (  SELECT id_loser player, COUNT (*) AS lost
                        FROM match
                    GROUP BY id_loser) lost
            ON played.PLAYER = lost.PLAYER
          RIGHT JOIN player p
           ON played.PLAYER = p.id_player
ORDER BY coalesce (win.win, 0) DESC;

-- Insert data to support a single tournament at a time
-- \d name_table
insert into tournament(name,description,init_date,end_date) values ('World Tournament','The biggest tournament ever','2015-12-24','2015-12-31');
