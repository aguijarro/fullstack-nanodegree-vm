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

CREATE TABLE scoreboard(
  id_scoreboard serial primary key,
  id_tournament integer references tournament,
  id_player integer references player,
  matches integer,
  win integer,
  lost integer
);

CREATE OR REPLACE FUNCTION get_num_match(p_id_tournament integer, p_id_player integer)
RETURNS integer AS $num_match$
declare
  num_match integer;
BEGIN
    SELECT matches into num_match
    FROM scoreboard
    WHERE id_tournament = $1
    AND id_player = $2;
    RETURN num_match;
END;
$num_match$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_num_win(p_id_tournament integer, p_id_player integer)
RETURNS integer AS $num_win$
DECLARE
  num_win integer;
BEGIN
    SELECT win into num_win
    FROM scoreboard
    WHERE id_tournament = p_id_tournament
    AND id_player = p_id_player;
    RETURN num_win;
END;
$num_win$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_num_lost(p_id_tournament integer, p_id_player integer)
RETURNS integer AS $num_lost$
declare
  num_lost integer;
BEGIN
    SELECT lost into num_lost
    FROM scoreboard
    WHERE id_tournament = p_id_tournament
    AND id_player = p_id_player;
    RETURN num_lost;
END;
$num_lost$ LANGUAGE plpgsql;




-- Insert data to support a single tournament at a time
-- \d name_table
insert into tournament(name,description,init_date,end_date) values ('World Tournament','The biggest tournament ever','2015-12-24','2015-12-31');
