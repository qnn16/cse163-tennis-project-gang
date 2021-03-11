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


def combine_file(directory):
    """
    In this function, it takes a directory and returns a new dataframe
    combining all the csv files into one.
    """
    all_files = glob.glob(directory + "/*.csv")
    li = []
    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)
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
    winner = df.groupby(['winner_name', 'surface'], as_index=False).size()
    loser = df.groupby(['loser_name', 'surface'], as_index=False).size()
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
    # fig1.show()

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
    # fig2.show()

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
    # fig3.show()

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
    # fig4.show()

# figure 5 is top 10 player overall


def first_set_win(df):
    """
    In this function, it takes in a dataframe and returns a value that
    represents the percentage of players that won the first set and led
    them to winning the whole match overall.

    Special cases: If the the dataframe is empty, it will return None.
    """
    scores = df.loc[:, ['winner_name', 'score']]
    # changes the scores from a string to a list of scores
    # remove unknown and walkover scores and injuries
    scores['first_score'] = scores.score.astype(str).str.split('-').str[0]
    # print(scores['first_score'].unique())
    scores = scores[scores['first_score'].apply(lambda x: x.isnumeric())]
    total = len(scores)
    scores['first_score'] = pd.to_numeric(scores['first_score'])
    won_first_set = scores[scores['first_score'] > 5]
    win = len(won_first_set)
    lost_first_set = scores[scores['first_score'] < 6]
    won_first_set.to_csv('won_first_set.csv')
    lost_first_set.to_csv('lost_first_set.csv')
    if total == 0:
        return None
    return win / total


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
    scores = df.loc[:, ['winner_name', 'score', 'surface', 'winner_hand',
                        'winner_ioc', 'winner_age', 'loser_hand',
                        'loser_ioc', 'loser_age', 'minutes', 'w_ace',
                        'l_ace']]
    scores = scores.dropna()
    features = scores.loc[:, scores.columns != 'winner_name']
    features = pd.get_dummies(features)
    labels = scores['winner_name']
    features_train, features_test, labels_train, labels_test \
        = train_test_split(features, labels, test_size=0.2)

    # model = DecisionTreeRegressor()
    # model.fit(features, labels)
    # predictions = model.predict(features)
    # error = mean_squared_error(labels, predictions)
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
    # court_surface(data)
    # first_set_win(data)
    # hand_dominance(data)
    predict_match_outcome(data)


if __name__ == '__main__':
    main()
