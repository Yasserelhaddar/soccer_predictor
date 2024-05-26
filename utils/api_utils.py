import http.client
import pandas as pd
import json
import statistics
from datetime import datetime, timedelta


class API_UTILS():

    def __init__(self, host, api_key):

        self.host = host
        self.api_key = api_key
    
        self.conn = http.client.HTTPSConnection(self.host)
        self.headers = {
            'X-RapidAPI-Key': self.api_key,
            'X-RapidAPI-Host': self.host,
        }
    
    def get_league(self, league_id, season):

        """ Get league statistics for a given league and season. 

            Arguments:
            league_id: type: int, example: 39 - Premier League
            season: type: int, example: 2021

        """

        self.conn.request("GET", f"/v3/leagues?id={league_id}&season={season}", headers=self.headers)
        res = self.conn.getresponse()
        data = res.read()

        json_data = json.loads(data.decode("utf-8"))

        return json_data

    def get_fixtures_season(self, league_id, season):

        """ Get fixture statistics for a given fixture, based on league id and season. 

            Arguments:
            league_id: type: int, example: 39 - Premier League
            season: type: int, example: 2021
            
        
        """

        self.conn.request("GET", f"/v3/fixtures?league={league_id}&season={season}", headers=self.headers)
        res = self.conn.getresponse()
        data = res.read()

        json_data = json.loads(data.decode("utf-8"))

        return json_data

    

    def get_fixture_stats(self, fixture_id):

        """ Get fixture statistics for a given fixture. 

            Arguments:
            fixture_id: type: int, example: 56622
        
        """

        self.conn.request("GET", f"/v3/fixtures/statistics?fixture={fixture_id}", headers=self.headers)
        res = self.conn.getresponse()
        data = res.read()

        json_data = json.loads(data.decode("utf-8"))

        return json_data
    
    def get_team_stats(self, league_id, season, team_id, date):

        """ Get team statistics for a given team, league, season and date. 
        
            Arguments: 
            league_id: type: int, example: 39 - Premier League
            season: type: int, example: 2021
            team_id: type: int, example: 45 - Everton
            date: type: str, example: 2021-01-01

        """

        self.conn.request("GET", f"/v3/teams/statistics?league={league_id}&season={season}&team={team_id}&date={date}", headers=self.headers)
        res = self.conn.getresponse()
        data = res.read()

        json_data = json.loads(data.decode("utf-8"))

        return json_data

    
    def get_lineup(self, fixture_id, team_id):

        """ Get lineup statistics for a given fixture. 

            Arguments:
            fixture_id: type: int, example: 56622

        """

        self.conn.request("GET", f"/v3/fixtures/lineups?fixture={fixture_id}&team={team_id}", headers=self.headers)
        res = self.conn.getresponse()
        data = res.read()

        json_data = json.loads(data.decode("utf-8"))

        return json_data

    def get_player_stats(self, season, player_id):

        """ Get player statistics for a given fixture. 

            Arguments:
            season: type: int, example: 2021
            fixture_id: type: int, example: 29371

        """

        self.conn.request("GET", f"/v3/players?id={player_id}&season={season}", headers=self.headers)
        res = self.conn.getresponse()
        data = res.read()

        json_data = json.loads(data.decode("utf-8"))

        return json_data


    
    def get_player_trophies(self, player_id):

        """ Get player trophies for a given player. 

            Arguments:
            player_id: type: int, example: 29371

        """

        self.conn.request("GET", f"/v3/trophies/player/{player_id}", headers=self.headers)
        res = self.conn.getresponse()
        data = res.read()

        json_data = json.loads(data.decode("utf-8"))

        return json_data


    

    def get_coach_trophies(self, coach_id):

        """ Get player trophies for a given coach. 

            Arguments:
            coach_id: type: int, example: 29371

        """

        self.conn.request("GET", f"/v3/trophies/coach/{coach_id}", headers=self.headers)
        res = self.conn.getresponse()
        data = res.read()

        json_data = json.loads(data.decode("utf-8"))

        return json_data


    def get_injuries(self, fixture_id, team_id):

        """ Get injuries for a given fixture. 

            Arguments:
            fixture_id: type: int, example: 56622
            team_id: type: int, example: 45 - Everton

        """
        
        self.conn.request("GET", f"/v3/injuries?fixture={fixture_id}&team{team_id}", headers=self.headers)
        res = self.conn.getresponse()
        data = res.read()

        json_data = json.loads(data.decode("utf-8"))

        return json_data


    def get_head_to_head(self, league_id, season, first_team_id, second_team_id, from_date, to_date):


        self.conn.request("GET", f"/v3/fixtures/headtohead?h2h={first_team_id}-{second_team_id}&league={league_id}&season={season}&from={from_date}&to={to_date}", headers=self.headers)

        res = self.conn.getresponse()
        data = res.read()

        json_data = json.loads(data.decode("utf-8"))

        return json_data


