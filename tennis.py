"""
Name: Quang and Steven Nguyen
CSE 163 Project: Analysis on Men’s Tennis Match Outcomes
This file contains functions that are used to perform
data analysis on our tennis dataset.
"""

import pandas as pd
import plotly.express as px
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def court_surface(df):
    """
    In this function, it takes a dataframe and will create four bar graphs
    presenting the top 10 players that won the most games within that
    type of court. With plotly, the bar graph displays the name, games won
    on that court, number of times that player played on that court, and
    their winning percentage on that court.
    Special cases: If the dataframe does not contain all 4 surfaces,
    only the surfaces that are included will be graphed.
    """
    winner = df.groupby(['winner_name', 'surface'], as_index=False).size()
    loser = df.groupby(['loser_name', 'surface'], as_index=False).size()
    winner_loser = pd.merge(winner.reset_index(), loser.reset_index(),
                            left_on=['winner_name', 'surface'],
                            right_on=['loser_name', 'surface'],
                            how='inner')
    winner_loser['surface_total'] = (winner_loser['0_x'] +
                                     winner_loser['0_y'])
    winner_loser['total_matches'] = (winner_loser['surface_total']
                                     .groupby(winner_loser['winner_name'])
                                     .transform('sum'))
    winner_loser = winner_loser.rename(columns={'winner_name': 'name',
                                       '0_x': 'won', '0_y': 'lost'})
    winner_loser = winner_loser.drop(['loser_name'], axis=1)
    winner_loser['win_rate'] = round((winner_loser['won'] /
                                      winner_loser['surface_total']) * 100, 2)

    # top 10 grass court players
    grass_court = winner_loser[winner_loser['surface'] == 'Grass']
    if grass_court.empty is not True:
        grass_court_top10 = grass_court.nlargest(10, 'won')
        fig1 = px.bar(grass_court_top10, x='name', y='won',
                      hover_data=['surface_total', 'win_rate'],
                      labels={
                        'name': 'Player Name',
                        'won': 'Matches Won',
                        'surface_total': 'Total Matches on Grass',
                        'win_rate': 'Winning Percentage on Grass'
                      })
        fig1.update_traces(marker_color='#00CC96')
        fig1.update_layout(
            title_text='Players With the Most Wins on Grass Court',
            title_x=0.5)
        fig1.show()

    # top 10 hard court players
    hard_court = winner_loser[winner_loser['surface'] == 'Hard']
    if hard_court.empty is not True:
        hard_court_top10 = hard_court.nlargest(10, 'won')
        fig2 = px.bar(hard_court_top10, x='name', y='won',
                      color_discrete_sequence=['blue'],
                      hover_data=['surface_total', 'win_rate'],
                      labels={
                        'name': 'Player Name',
                        'won': 'Matches Won',
                        'surface_total': 'Total Matches on Hard',
                        'win_rate': 'Winning Percentage on Hard'
                      })
        fig2.update_traces(marker_color='#636EFA')
        fig2.update_layout(
            title='Players With the Most Wins on Hard Court',
            title_x=0.5)
        fig2.show()

    # top 10 clay court players
    clay_court = winner_loser[winner_loser['surface'] == 'Clay']
    if clay_court.empty is not True:
        clay_court_top10 = clay_court.nlargest(10, 'won')
        fig3 = px.bar(clay_court_top10, x='name', y='won',
                      color_discrete_sequence=['red'],
                      hover_data=['surface_total', 'win_rate'],
                      labels={
                        'name': 'Player Name',
                        'won': 'Matches Won',
                        'surface_total': 'Total Matches on Clay',
                        'win_rate': 'Winning Percentage on Clay'
                      })
        fig3.update_traces(marker_color='#EF553B')
        fig3.update_layout(
            title_text='Players With the Most Wins on Clay Court',
            title_x=0.5)
        fig3.show()

    # top 10 carpet court players
    carpet_court = winner_loser[winner_loser['surface'] == 'Carpet']
    if carpet_court.empty is not True:
        carpet_court_top10 = carpet_court.nlargest(10, 'won')
        fig4 = px.bar(carpet_court_top10, x='name', y='won',
                      color_discrete_sequence=['orange'],
                      hover_data=['surface_total', 'win_rate'],
                      labels={
                        'name': 'Player Name',
                        'won': 'Matches Won',
                        'surface_total': 'Total Matches on Carpet',
                        'win_rate': 'Winning Percentage on Carpet'
                      })
        fig4.update_layout(
            title='Players With the Most Wins on Carpet Court',
            title_x=0.5)
        fig4.show()

    # top 10 players overall with the most wins
    top_10 = winner_loser
    top_10['total_won'] = (top_10['won']
                           .groupby(top_10['name'])
                           .transform('sum'))
    # we take the mean of the total_matches
    # since it will return the number as a singular
    top_10_player_names = (
        top_10.groupby('name')['total_matches'].mean()
                                               .nlargest(10)
                                               .to_frame()
                                               .reset_index())
    merged = top_10.merge(top_10_player_names,
                          left_on=['name', 'total_matches'],
                          right_on=['name', 'total_matches'], how='inner')
    merged = merged.sort_values(by=['total_won'], ascending=False)
    fig5 = px.bar(merged, x='name', y='won', color='surface',
                  color_discrete_map={
                      'Carpet': 'orange',
                      'Clay': '#EF553B',
                      'Grass': '#00CC96',
                      'Hard': '#636EFA'},
                  hover_data=['surface_total', 'win_rate'],
                  labels={
                     'surface': 'Surface',
                     'name': 'Player Name',
                     'won': 'Matches Won',
                     'surface_total': 'Total Matches on Surface',
                     'win_rate': 'Winning Percentage on Surface'
                  })
    fig5.update_layout(title='Top 10 Players with the Most Wins Overall',
                       title_x=0.5)
    fig5.show()

    # fig1.write_html('graphs/court_surface/grass.html')
    # fig2.write_html('graphs/court_surface/hard.html')
    # fig3.write_html('graphs/court_surface/clay.html')
    # fig4.write_html('graphs/court_surface/carpet.html')
    # fig5.write_html('graphs/court_surface/top10overall.html')


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
    scores['first_score_mw'] = (scores.score.astype(str).str.split('[-|(|)| ]')
                                .str[0])
    scores = scores[scores['first_score_mw'].apply(lambda x: x.isnumeric())]
    scores['first_score_mw'] = scores['first_score_mw'].astype(int)

    # first set score of match loser
    scores['first_score_ml'] = (scores.score.astype(str).str.split('[-|(|)| ]')
                                .str[1])
    scores = scores[scores['first_score_ml'].apply(lambda x: x.isnumeric())]
    scores['first_score_ml'] = scores['first_score_ml'].astype(int)

    won_set_won_game = (scores[scores['first_score_mw'] >
                               scores['first_score_ml']])

    return round(len(won_set_won_game) / len(scores) * 100, 2)


def hand_dominance(df):
    """
    In this function, we are returning a graph of the hand dominance match-ups
    between left and right handed players. Then also returning graphs of the
    match-ups based on the type of courts.
    Special cases: If the dataframe does not contain any players at a specific
    court, it will not return a graph.
    """
    hand = df.loc[:, ['winner_hand', 'loser_hand', 'surface']]
    right = (hand['winner_hand'] == 'R') | (hand['loser_hand'] == 'R')
    left = (hand['winner_hand'] == 'L') | (hand['loser_hand'] == 'L')
    hand = hand[right & left]
    hand = (hand.groupby(['surface', 'winner_hand', 'loser_hand'])
                .size().to_frame().reset_index())
    hand.columns = ['surface', 'winner_hand', 'loser_hand', 'counts']

    # overall matchup statistics no matter the court
    fig1 = px.pie(hand, values='counts', names='winner_hand')
    fig1.update_layout(
        title='Win Percentage of Tennis Matches based on Hand Dominance',
        title_x=0.5)
    fig1.update_traces(textposition='inside', textinfo='percent+label')
    fig1.show()

    # hard court matchup stats
    hard = hand[hand['surface'] == 'Hard']
    if hard.empty is not True:
        fig2 = px.pie(hard, values='counts', names='winner_hand',
                      color_discrete_sequence=['blue'])
        fig2.update_layout(
            title='Hard Court Win Percentage based on Hand Dominance',
            title_x=0.5)
        fig2.update_traces(textposition='inside', textinfo='percent+label')
        fig2.show()

    # grass court matchup stats
    grass = hand[hand['surface'] == 'Grass']
    if grass.empty is not True:
        fig3 = px.pie(grass, values='counts', names='winner_hand',
                      color_discrete_sequence=['green'])
        fig3.update_layout(
            title='Grass Court Win Percentage based on Hand Dominance',
            title_x=0.5)
        fig3.update_traces(textposition='inside', textinfo='percent+label')
        fig3.show()

    # clay court matchup stats
    clay = hand[hand['surface'] == 'Clay']
    if clay.empty is not True:
        fig4 = px.pie(clay, values='counts', names='winner_hand',
                      color_discrete_sequence=['red'])
        fig4.update_layout(
            title='Clay Court Win Percentage based on Hand Dominance',
            title_x=0.5)
        fig4.update_traces(textposition='inside', textinfo='percent+label')
        fig4.show()

    # carpet court matchup stats
    carpet = hand[hand['surface'] == 'Carpet']
    if carpet.empty is not True:
        fig5 = px.pie(carpet, values='counts', names='winner_hand',
                      color_discrete_sequence=['orange'])
        fig5.update_layout(
            title='Carpet Court Win Percentage based on Hand Dominance',
            title_x=0.5)
        fig5.update_traces(textposition='inside', textinfo='percent+label')
        fig5.show()

    # fig1.write_html('graphs/hand_dominance/all_surfaces.html')
    # fig2.write_html('graphs/hand_dominance/hard.html')
    # fig3.write_html('graphs/hand_dominance/grass.html')
    # fig4.write_html('graphs/hand_dominance/clay.html')
    # fig5.write_html('graphs/hand_dominance/carpet.html')


def predict_match_outcome(df):
    """
    In this function, we are taking a dataset and making a machine learning
    model. This will print the training and test accuracy scores.
    Note: Because the dataset is quite large, it will take a while
    (~3-5 minutes)
    """
    winner = df.loc[:, ['winner_name', 'w_ace', 'w_df', 'w_svpt',
                        'w_1stIn', 'w_1stWon', 'w_2ndWon', 'w_SvGms',
                        'w_bpSaved', 'w_bpFaced']]

    winner = winner.dropna()
    winner['winner_name'] = 'W'
    winner = winner.rename(
        columns={'winner_name': 'Won/Lost', 'w_ace': 'ace', 'w_df': 'df',
                 'w_svpt': 'svpt', 'w_1stIn': '1stIn', 'w_1stWon': '1stWon',
                 'w_2ndWon': '2ndWon', 'w_SvGms': 'SvGms',
                 'w_bpSaved': 'bpSaved', 'w_bpFaced': 'bpFaced'})

    loser = df.loc[:, ['loser_name', 'l_ace', 'l_df', 'l_svpt',
                       'l_1stIn', 'l_1stWon', 'l_2ndWon', 'l_SvGms',
                       'l_bpSaved', 'l_bpFaced']]

    loser = loser.dropna()
    loser['loser_name'] = 'L'
    loser = loser.rename(
        columns={'loser_name': 'Won/Lost', 'l_ace': 'ace', 'l_df': 'df',
                 'l_svpt': 'svpt', 'l_1stIn': '1stIn', 'l_1stWon': '1stWon',
                 'l_2ndWon': '2ndWon', 'l_SvGms': 'SvGms',
                 'l_bpSaved': 'bpSaved', 'l_bpFaced': 'bpFaced'})

    test = pd.concat([winner, loser], ignore_index=True)

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
