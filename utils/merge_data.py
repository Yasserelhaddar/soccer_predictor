
from api_utils import API_UTILS


def form_to_points(form):

    if form:
        form_in_points = [int(result) for result in list(form.replace('W', '3').replace('D', '1').replace('L', '0'))]
    else:
        form_in_points = [0]
    
    return sum(form_in_points)

def get_fixture_df(api_utils, league_id, season):
    fixtures_json = api_utils.get_fixtures_season(league_id, season)

    # List to store fixture dictionaries
    fixtures_list = []

    for fixture_data in fixtures_json['response']:
        fixtures_list.append({
            'fixture_id': fixture_data['fixture']['id'],
            'fixture_date': fixture_data['fixture']['date'],
            'venue_id': fixture_data['fixture']['venue']['id'],
            'home_team_id': fixture_data['teams']['home']['id'],
            'away_team_id': fixture_data['teams']['away']['id'],
            'home_team_goals': fixture_data['goals']['home'],
            'away_team_goals': fixture_data['goals']['away'],
            'home_team_result': fixture_data['goals']['home'] > fixture_data['goals']['away'],
            'away_team_result': fixture_data['goals']['home'] < fixture_data['goals']['away']
        })

    # Create DataFrame from list of dictionaries
    fixture_df = pd.DataFrame(fixtures_list)

    return fixture_df

def get_fixture_stats_df(api_utils, fixture_id):
    fixture_stats_json = api_utils.get_fixture_stats(fixture_id)

    # Initialize an empty list to store the stats for both teams
    fixture_stats_list = []

    # Initialize a dictionary to store the combined statistics
    stats_dict = {'fixture_id': fixture_id}

    # Collect home team statistics
    for stat in fixture_stats_json['response'][0]['statistics']:
        stat_type = stat['type'].replace(' ', '_').lower()
        stats_dict[f"home_{stat_type}"] = stat['value']

    # Collect away team statistics
    for stat in fixture_stats_json['response'][1]['statistics']:
        stat_type = stat['type'].replace(' ', '_').lower()
        stats_dict[f"away_{stat_type}"] = stat['value']

    # Append the dictionary to the list
    fixture_stats_list.append(stats_dict)

    # Create DataFrame from the list of dictionaries
    fixture_stats_df = pd.DataFrame(fixture_stats_list)

    return fixture_stats_df


def get_team_stats_df(api_utils, league_id, season, team_id, date, prefix):
    teams_stats_json = api_utils.get_team_stats(league_id, season, team_id, date)

    team_stats_dict = {
            f'{prefix}_team_id': team_id,
            'date': date,
            f'{prefix}_form': teams_stats_json['response']['form'], 
            f'{prefix}_played': teams_stats_json['response']['fixtures']['played']['total'], 
            f'{prefix}_played_as_home': teams_stats_json['response']['fixtures']['played']['home'],
            f'{prefix}_played_as_away': teams_stats_json['response']['fixtures']['played']['away'],
            f'{prefix}_won': teams_stats_json['response']['fixtures']['wins']['total'], 
            f'{prefix}_won_as_home': teams_stats_json['response']['fixtures']['wins']['home'],
            f'{prefix}_won_as_away': teams_stats_json['response']['fixtures']['wins']['away'],
            f'{prefix}_drawn': teams_stats_json['response']['fixtures']['draws']['total'], 
            f'{prefix}_drawn_as_home': teams_stats_json['response']['fixtures']['draws']['home'],
            f'{prefix}_drawn_as_away': teams_stats_json['response']['fixtures']['draws']['away'],
            f'{prefix}_lost': teams_stats_json['response']['fixtures']['loses']['total'],
            f'{prefix}_lost_as_home': teams_stats_json['response']['fixtures']['loses']['home'],
            f'{prefix}_lost_as_away': teams_stats_json['response']['fixtures']['loses']['away'],
            f'{prefix}_goals_for': teams_stats_json['response']['goals']['for']['total']['total'],
            f'{prefix}_goals_for_as_home': teams_stats_json['response']['goals']['for']['total']['home'],
            f'{prefix}_goals_for_as_away': teams_stats_json['response']['goals']['for']['total']['away'],
            f'{prefix}_goals_against': teams_stats_json['response']['goals']['against']['total']['total'],
            f'{prefix}_goals_against_as_home': teams_stats_json['response']['goals']['against']['total']['home'],
            f'{prefix}_goals_against_as_away': teams_stats_json['response']['goals']['against']['total']['away'],
            f'{prefix}_points': form_to_points(teams_stats_json['response']['form']),
            }

    team_stats_df = pd.DataFrame(team_stats_dict, index=[0])

    
    return team_stats_df

def get_lineup_df(api_utils, fixture_id, team_id, prefix):

    team_lineup_json = api_utils.get_lineup(fixture_id, team_id)

    if team_lineup_json['response']:

        team_lineup_dict = {
                'fixture_id': fixture_id,
                f'{prefix}_team_id': team_id,
                f'{prefix}_coach_id': team_lineup_json['response'][0]['coach']['id'],
                f'{prefix}_formation': team_lineup_json['response'][0]['formation'],
        }

        for index, player_info in enumerate(team_lineup_json['response'][0]['startXI']):
            team_lineup_dict[f'{prefix}_player_{index}_id'] = player_info['player']['id']
        
    else:

        team_lineup_dict = {
                'fixture_id': fixture_id,
                f'{prefix}_team_id': team_id,
                f'{prefix}_coach_id': None,
                f'{prefix}_formation': None,
        }

        for index in range(1,12):
            team_lineup_dict[f'{prefix}_player_{index}_id'] = None

        
    
    team_lineup_df = pd.DataFrame(team_lineup_dict, index=[0])
    

    return team_lineup_df
            
def get_player_stats_df(api_utils, season, player_id, prefix, index):

    player_stats_json = api_utils.get_player_stats(season, player_id)

    player_stats_dict = {
        f'{prefix}_player_{index}_id': player_id,
        f'{prefix}_player_{index}_overall_rating': statistics.mean([float(player_competition_stats['games']['rating']) for player_competition_stats in player_stats_json['response'][0]['statistics'] if player_competition_stats['games']['rating']])}

    player_stats_df = pd.DataFrame(player_stats_dict, index=[0])

    return player_stats_df


def get_merged_data(league_id, season):

    fixtures_df = get_fixture_df(api_utils, league_id=league_id, season=season)[100:101]
    
    # merge fixtures stats
    fixtures_id_list = list(fixtures_df['fixture_id'])

    merged_fixture_stats_df = pd.DataFrame()
    for fixture_id in fixtures_id_list:
        merged_fixture_stats_df = pd.concat([merged_fixture_stats_df, get_fixture_stats_df(api_utils, fixture_id=fixture_id)])


    merged_df = pd.merge(fixtures_df, merged_fixture_stats_df, on='fixture_id', how='inner')


    # merge teams stats
    fixture_date_list = list(merged_df['fixture_date'])
    home_team_id_list = list(merged_df['home_team_id'])
    away_team_id_list = list(merged_df['away_team_id'])


    merged_home_team_stats_df = pd.DataFrame()
    merged_away_team_stats_df = pd.DataFrame()

    for index, home_team_id in enumerate(home_team_id_list):
        merged_home_team_stats_df = pd.concat([merged_home_team_stats_df, get_team_stats_df(api_utils, league_id=league_id, season=season, team_id=home_team_id, date=(datetime.fromisoformat(fixture_date_list[index]) - timedelta(days=1)).strftime('%Y-%m-%d'), prefix='home')])


    for index, away_team_id in enumerate(away_team_id_list):
        merged_away_team_stats_df = pd.concat([merged_away_team_stats_df, get_team_stats_df(api_utils, league_id=league_id, season=season, team_id=away_team_id, date=(datetime.fromisoformat(fixture_date_list[index]) - timedelta(days=1)).strftime('%Y-%m-%d'), prefix='away')])


    merged_df = pd.merge(merged_df, merged_home_team_stats_df, on='home_team_id')
    merged_df = pd.merge(merged_df, merged_away_team_stats_df, on='away_team_id')

    # merge lineup

    merged_home_team_lineup_df = pd.DataFrame()
    merged_away_team_lineup_df = pd.DataFrame()

    for index, home_team_id in enumerate(home_team_id_list):
        merged_home_team_lineup_df = pd.concat([merged_home_team_lineup_df, get_lineup_df(api_utils, fixture_id=fixtures_id_list[index], team_id=home_team_id, prefix='home')])


    for index, away_team_id in enumerate(away_team_id_list):
        merged_away_team_lineup_df = pd.concat([merged_away_team_lineup_df, get_lineup_df(api_utils, fixture_id=fixtures_id_list[index], team_id=away_team_id, prefix='away')])


    merged_df = pd.merge(merged_df, merged_home_team_lineup_df, on=['fixture_id','home_team_id'])
    merged_df = pd.merge(merged_df, merged_away_team_lineup_df, on=['fixture_id','away_team_id'])

    # merge 11 players stats

    for index, fixture_id in enumerate(fixtures_id_list):

        merged_home_player_stats_df = pd.DataFrame()
        merged_away_player_stats_df = pd.DataFrame()

        for player_number in range(0,11):
            
            merged_home_player_stats_df = pd.concat([merged_home_player_stats_df, get_player_stats_df(api_utils, season=season-1, player_id=int(merged_df.loc[merged_df['fixture_id'] == fixture_id, f'home_player_{player_number}_id'].iloc[0]), prefix='home', index=player_number)], axis=1)
            merged_away_player_stats_df = pd.concat([merged_away_player_stats_df, get_player_stats_df(api_utils, season=season-1, player_id=int(merged_df.loc[merged_df['fixture_id'] == fixture_id, f'away_player_{player_number}_id'].iloc[0]), prefix='away', index=player_number)], axis=1)

            merged_df = pd.merge(merged_df, merged_home_player_stats_df, on=f'home_player_{player_number}_id')
            merged_df = pd.merge(merged_df, merged_away_player_stats_df, on=f'away_player_{player_number}_id')



    return merged_df


def main(host="api-football-v1.p.rapidapi.com", api_key="c0a22fc569mshcda17018d7f63cdp15f2cdjsnd99d626c6df3"):

    api_utils = API_UTILS(host, api_key)
    merged_df = get_merged_data(39, 2023)