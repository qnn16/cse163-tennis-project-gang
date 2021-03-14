"""
Name: Quang and Steven Nguyen
CSE 163 Project: Analysis on Men’s Tennis Match Outcomes

In this file,
"""


import pandas as pd
import glob
import plotly.express as px
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import os


def combine_file(directory):
    """
    In this function, it takes a directory and returns a new dataframe
    combining all the csv files into one.
    """
    all_files = glob.glob(directory + "/*.csv")
    li = []
    for filename in all_files:
        if os.stat(filename).st_size != 0:
            df = pd.read_csv(filename, index_col=None, header=0)
            li.append(df)
    if li == []:
        return None
    frame = pd.concat(li, axis=0, ignore_index=True)
    return frame


def court_surface(df):
    """
    In this function, it takes a dataframe and will create four bar graphs
    presenting the top 10 players that won the most games within that
    type of court. With plotly, the bar graph displays the name, games won
    on that court, number of times that player played on that court, and
    their winning percentage on that court.

    Special cases:
    """
    winner = df.groupby(['winner_name', 'surface', 'winner_id'], as_index=False).size()
    loser = df.groupby(['loser_name', 'surface', 'loser_id'], as_index=False).size()
    winner_loser = winner.merge(loser, left_on=['winner_name', 'surface'],
                                right_on=['loser_name', 'surface'],
                                how='inner')
    winner_loser['surface_total'] = (winner_loser['size_x'] +
                                     winner_loser['size_y'])
    winner_loser['total_matches'] = (winner_loser['surface_total']
                                     .groupby(winner_loser['winner_name'])
                                     .transform('sum'))
    winner_loser = winner_loser.rename(columns={'winner_name': 'name',
                                       'size_x': 'won', 'size_y': 'lost'})
    winner_loser = winner_loser.drop(['loser_name'], axis=1)
    winner_loser['win_rate'] = round((winner_loser['won'] /
                                      winner_loser['surface_total']) * 100, 2)
    # winner_loser.to_csv('winner_loser.csv')
    # print(winner_loser)

    grass_court = winner_loser[winner_loser['surface'] == 'Grass']
    grass_court_top10 = grass_court.nlargest(10, 'won')
    fig1 = px.bar(grass_court_top10, x='name', y='won',
                  color_discrete_sequence=['green'],
                  hover_data=['surface_total', 'win_rate'],
                  labels={
                     'name': 'Player Name',
                     'won': 'Games Won',
                     'surface_total': 'Total Matches on Grass',
                     'win_rate': 'Winning Percentage on Grass'
                  })
    fig1.update_layout(title_text='Players With the Most Wins on Grass Court',
                       title_x=0.5)
    fig1.show()

    hard_court = winner_loser[winner_loser['surface'] == 'Hard']
    hard_court_top10 = hard_court.nlargest(10, 'won')
    fig2 = px.bar(hard_court_top10, x='name', y='won',
                  color_discrete_sequence=['blue'],
                  hover_data=['surface_total', 'win_rate'],
                  labels={
                     'name': 'Player Name',
                     'won': 'Games Won',
                     'surface_total': 'Total Matches on Hard',
                     'win_rate': 'Winning Percentage on Hard'
                  })
    fig2.update_layout(title='Players With the Most Wins on Hard Court',
                       title_x=0.5)
    fig2.show()

    clay_court = winner_loser[winner_loser['surface'] == 'Clay']
    clay_court_top10 = clay_court.nlargest(10, 'won')
    fig3 = px.bar(clay_court_top10, x='name', y='won',
                  color_discrete_sequence=['red'],
                  hover_data=['surface_total', 'win_rate'],
                  labels={
                     'name': 'Player Name',
                     'won': 'Games Won',
                     'surface_total': 'Total Matches on Clay',
                     'win_rate': 'Winning Percentage on Clay'
                  })
    fig3.update_layout(title_text='Players With the Most Wins on Clay Court',
                       title_x=0.5)
    fig3.show()

    carpet_court = winner_loser[winner_loser['surface'] == 'Carpet']
    carpet_court_top10 = carpet_court.nlargest(10, 'won')
    fig4 = px.bar(carpet_court_top10, x='name', y='won',
                  color_discrete_sequence=['orange'],
                  hover_data=['surface_total', 'win_rate'],
                  labels={
                     'name': 'Player Name',
                     'won': 'Games Won',
                     'surface_total': 'Total Matches on Carpet',
                     'win_rate': 'Winning Percentage on Carpet'
                  })
    fig4.update_layout(title='Players With the Most Wins on Carpet Court',
                       title_x=0.5)
    fig4.show()

    # top 10 players overall with the most wins
    top_10 = winner_loser
    top_10['total_won'] = (top_10['won']
                           .groupby(top_10['name'])
                           .transform('sum'))
    top_10_player_names = top_10.groupby('name')['total_matches'].mean().nlargest(10).to_frame().reset_index()
    merged = top_10.merge(top_10_player_names, left_on=['name', 'total_matches'], right_on=['name', 'total_matches'], how='inner')
    merged = merged.sort_values(by=['total_won'], ascending=False)
    fig5 = px.bar(merged, x='name', y='won', color='surface',
                  color_discrete_map={
                      'Carpet': 'orange',
                      'Clay': '#EF553B',
                      'Grass': '#00CC96',
                      'Hard': '#636EFA'},
                  hover_data=['surface_total', 'win_rate'],
                  labels={
                     'name': 'Player Name',
                     'won': 'Matches Won',
                     'surface_total': 'Total Matches on Surface',
                     'win_rate': 'Winning Percentage on Surface'
                  })
    fig5.update_layout(title='Top 10 Players with the Most Wins Overall',
                       title_x=0.5)
    fig5.show()


def first_set_win(df):
    """
    In this function, it takes in a dataframe and returns a value that
    represents the percentage of players that won the first set and led
    them to winning the whole match overall.

    Special cases: If the the dataframe is empty, it will return None.
    """
    # changes the scores from a string to a list of scores
    # remove unknown and walkover scores and injuries

    # first set score of match winner
    if len(df) == 0:
        return None
    scores = df.loc[:, ['winner_name', 'loser_name', 'score']]
    scores['first_score_mw'] = scores.score.astype(str).str.split('[-|(|)| ]').str[0]
    scores = scores[scores['first_score_mw'].apply(lambda x: x.isnumeric())]
    scores['first_score_mw'] = scores['first_score_mw'].astype(int)

    # first set score of match loser
    scores['first_score_ml'] = scores.score.astype(str).str.split('[-|(|)| ]').str[1]
    scores = scores[scores['first_score_ml'].apply(lambda x: x.isnumeric())]
    scores['first_score_ml'] = scores['first_score_ml'].astype(int)

    won_set_won_game = scores[scores['first_score_mw'] >
                              scores['first_score_ml']]

    return round(len(won_set_won_game) / len(scores) * 100, 2)


def hand_dominance(df):
    """
    """
    hand = df.loc[:, ['winner_hand', 'loser_hand', 'surface']]
    right = (hand['winner_hand'] == 'R') | (hand['loser_hand'] == 'R')
    left = (hand['winner_hand'] == 'L') | (hand['loser_hand'] == 'L')
    hand = hand[right & left]
    hand = hand.value_counts().to_frame().reset_index()
    hand.columns = ['winner_hand', 'loser_hand', 'surface', 'counts']
    hand.to_csv('test.csv')

    # overall matchup statistics no matter the court
    fig1 = px.pie(hand, values='counts', names='winner_hand')
    fig1.update_layout(title='Win Percentage of Tennis Matches based on Hand Dominance', title_x=0.5)
    fig1.update_traces(textposition='inside', textinfo='percent+label')
    fig1.show()

    # hard court matchup stats
    hard = hand[hand['surface'] == 'Hard']
    fig2 = px.pie(hard, values='counts', names='winner_hand', color_discrete_sequence=['blue'])
    fig2.update_layout(title='Hard Court Win Percentage based on Hand Dominance', title_x=0.5)
    fig2.update_traces(textposition='inside', textinfo='percent+label')
    fig2.show()

    # grass court matchup stats
    grass = hand[hand['surface'] == 'Grass']
    fig3 = px.pie(grass, values='counts', names='winner_hand', color_discrete_sequence=['green'])
    fig3.update_layout(title='Grass Court Win Percentage based on Hand Dominance', title_x=0.5)
    fig3.update_traces(textposition='inside', textinfo='percent+label')
    fig3.show()

    # clay court matchup stats
    clay = hand[hand['surface'] == 'Clay']
    fig4 = px.pie(clay, values='counts', names='winner_hand', color_discrete_sequence=['red'])
    fig4.update_layout(title='Clay Court Win Percentage based on Hand Dominance', title_x=0.5)
    fig4.update_traces(textposition='inside', textinfo='percent+label')
    fig4.show()

    # carpet court matchup stats
    carpet = hand[hand['surface'] == 'Carpet']
    fig5 = px.pie(carpet, values='counts', names='winner_hand', color_discrete_sequence=['orange'])
    fig5.update_layout(title='Carpet Court Win Percentage based on Hand Dominance', title_x=0.5)
    fig5.update_traces(textposition='inside', textinfo='percent+label')
    fig5.show()


def predict_match_outcome(df):
    """
    number of ace diff = abs(w_ace - 1_ace)
    """
    winner = df.loc[:, ['winner_name', 'score', 'w_ace', 'w_df', 'w_svpt', 'w_1stIn', 'w_1stWon', 'w_2ndWon', 'w_SvGms', 'w_bpSaved', 'w_bpFaced']]

    winner = winner.dropna()
    winner['winner_name'] = 'W'
    winner = winner.rename(columns={'winner_name': 'Won/Lost',
        'w_ace': 'ace', 'w_df': 'df', 'w_svpt': 'svpt', 'w_1stIn': '1stIn', 'w_1stWon': '1stWon', 'w_2ndWon': '2ndWon', 'w_SvGms': 'SvGms', 'w_bpSaved': 'bpSaved', 'w_bpFaced': 'bpFaced'})
    # print(winner.head())

    loser = df.loc[:, ['loser_name', 'score', 'l_ace', 'l_df', 'l_svpt', 'l_1stIn', 'l_1stWon', 'l_2ndWon', 'l_SvGms', 'l_bpSaved', 'l_bpFaced']]

    loser = loser.dropna()
    loser['loser_name'] = 'L'
    loser = loser.rename(columns={'loser_name': 'Won/Lost',
        'l_ace': 'ace', 'l_df': 'df', 'l_svpt': 'svpt', 'l_1stIn': '1stIn', 'l_1stWon': '1stWon', 'l_2ndWon': '2ndWon', 'l_SvGms': 'SvGms', 'l_bpSaved': 'bpSaved', 'l_bpFaced': 'bpFaced'})
    # print(loser.head())

    test = pd.concat([winner, loser], ignore_index=True)
    test.to_csv('test2.csv')
    # print(len(test))

    features = test.loc[:, test.columns != 'Won/Lost']
    features = pd.get_dummies(features)
    labels = test['Won/Lost']
    features_train, features_test, labels_train, labels_test \
        = train_test_split(features, labels, test_size=0.2)
    model = DecisionTreeClassifier()
    model.fit(features_train, labels_train)
    train_pred = model.predict(features_train)
    train_acc = accuracy_score(labels_train, train_pred)
    test_pred = model.predict(features_test)
    test_acc = accuracy_score(labels_test, test_pred)
    print(train_acc)
    print(test_acc)


def main():
    directory = 'data/'
    data = combine_file(directory)
    print(first_set_win(data))
    court_surface(data)
    hand_dominance(data)
    
    empty = 'testdata/'
    empty_set = combine_file(empty)
    assert first_set_win(empty_set) is None
    
    test_directory = 'testdata2/'
    data_test = combine_file(test_directory)
    assert first_set_win(data_test) == 100.0
    
    test2_directory = 'testdata3/'
    data2_test = combine_file(test2_directory)
    assert first_set_win(data2_test) == 85.71
    
    
    # predict_match_outcome(data)


if __name__ == '__main__':
    main()
