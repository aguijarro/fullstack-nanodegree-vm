#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    sql = "DELETE FROM match;"
    c.execute(sql)
    DB.commit()
    DB.close()

def deleteScoreboard():
    """Remove all the scoreboard records from the database."""
    DB = connect()
    c = DB.cursor()
    sql = "DELETE FROM scoreboard;"
    c.execute(sql)
    DB.commit()
    DB.close()

def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    sql = "DELETE FROM player;"
    c.execute(sql)
    DB.commit()
    DB.close()

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    sql = '''SELECT count(*) as tot
                FROM player;
          '''
    c.execute(sql)
    count = c.fetchone()[0]
    DB.close()
    return count

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    sql_player = '''INSERT INTO player(id_tournament,name)
                VALUES (1,%s) RETURNING id_player;'''
    c.execute(sql_player,(name,))
    DB.commit()
    id_player = c.fetchone()[0]
    sql_scoreboard = '''INSERT INTO scoreboard(id_tournament,id_player, matches, win, lost)
                VALUES (1,%s,0,0,0);'''
    c.execute(sql_scoreboard,(id_player,))
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    c = DB.cursor()
    sql = '''SELECT  s.id_player, p.name, s.win, s.matches
                FROM scoreboard s, player p
                WHERE s.id_player = p.id_player
                ORDER BY 3 DESC;
          '''
    c.execute(sql)

    standings = []

    for row in c.fetchall():
        standings.append(row)
    DB.close()
    return standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()

    #get number of match for winners
    sql_win_num_match = '''SELECT  get_num_match(%s,%s);'''
    c.execute(sql_win_num_match,(1,winner))
    winner_num_match = c.fetchone()[0]

    #get number of match for loser
    sql_lost_num_match = '''SELECT  get_num_match(%s,%s);'''
    c.execute(sql_lost_num_match,(1,loser))
    loser_num_match = c.fetchone()[0]

    #get number of wins
    sql_winner_num_win = '''SELECT  get_num_win(%s,%s);'''
    c.execute(sql_winner_num_win,(1,winner))
    winner_num_win = c.fetchone()[0]

    #get number of lost
    sql_loser_num_lost = '''SELECT  get_num_lost(%s,%s);'''
    c.execute(sql_loser_num_lost,(1,loser))
    loser_num_lost = c.fetchone()[0]

    sql_match = '''INSERT INTO match(id_tournament,id_winner,id_loser)
                VALUES (1,%s,%s);'''
    c.execute(sql_match,(winner,loser,))

    sql_update_winner = '''UPDATE scoreboard set matches = %s , win = %s
                WHERE id_tournament = %s and id_player = %s;'''
    c.execute(sql_update_winner,(winner_num_match + 1, winner_num_win + 1, 1, winner,))

    sql_update_loser = '''UPDATE scoreboard set matches = %s , lost = %s
                WHERE id_tournament = %s and id_player = %s;'''
    c.execute(sql_update_loser,(loser_num_match + 1, loser_num_lost + 1, 1, loser,))

    DB.commit()
    DB.close()

def validPairs(first_player, second_player):
    """Return True if the pair for the match is valid. That means that the players never play before

    Args:
        first_player: the player's 1 id (as registered)
        second_player: the player's 2 id (as registered)
    """    
    DB = connect()
    c = DB.cursor()
    sql = '''SELECT  count(*) as num_match
                FROM match m
                WHERE (m.id_winner = %s and m.id_loser = %s)
                OR (m.id_winner = %s and m.id_loser = %s);
          '''
    c.execute(sql,(first_player,second_player,second_player,first_player))
    count = c.fetchone()[0]
    DB.close()

    if count == 0:
        return True
    else:
        return False

def makePairs(index_first_player, first_player, possiblePairs):
    """Return a player selected from the different alternatives

    Args:
        index_first_player: array position for a player_1
        first_player: the player's 1 id (as registered)
        possiblePairs: array of possible pairs for player 1
    """
    for index_second_player, second_player in enumerate(possiblePairs):
        #validar que los indices no produzcan error cuando son mas grandes que el tamanio del arreglo
        if validPairs(first_player[0],second_player[0]):
            return index_second_player + (index_first_player + 1), second_player

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    pairs = []
    standings = playerStandings()

    while len(standings) > 1:

        index_first_player = 0
        first_player = standings[0]

        index_second_player, second_player = makePairs(index_first_player, first_player, standings[1:])

        standings.pop(index_second_player)
        standings.pop(index_first_player)

        pairs.append((first_player[0],first_player[1],second_player[0],second_player[1]))

    return pairs
