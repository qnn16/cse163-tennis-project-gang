import pandas as pd
import plotly.express as px
import glob


def combine_file(directory):
    all_files = glob.glob(directory + "/*.csv")
    li = []
    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)
    frame = pd.concat(li, axis=0, ignore_index=True)
    return frame


def main():
    directory = 'data/'
    df = combine_file(directory)
    court_surface(df)

def court_surface(df):
    winner = df.groupby(['winner_name', 'surface'], as_index=False).size()

    loser = df.groupby(['loser_name', 'surface'], as_index=False).size()

    winner_loser = winner.merge(loser, left_on=['winner_name', 'surface'], right_on=['loser_name', 'surface'], how='inner')
    winner_loser['surface_total'] = winner_loser['size_x'] + winner_loser['size_y']
    winner_loser['total_matches'] = winner_loser['surface_total'].groupby(winner_loser['winner_name']).transform('sum')
    winner_loser = winner_loser.rename(columns={'winner_name': 'name', 'size_x': 'won', 'size_y': 'lost'})
    winner_loser = winner_loser.drop(['loser_name'], axis=1)
    winner_loser['win_rate'] = round((winner_loser['won'] / winner_loser['surface_total']) * 100, 2)
    winner_loser.to_csv('winner_loser.csv')

    grass_court = winner_loser[winner_loser['surface'] == 'Grass']
    grass_court_top10 = grass_court.nlargest(10, 'won')
    fig1 = px.bar(grass_court_top10, x='name', y='won', color_discrete_sequence =['green'], hover_data=['surface_total', 'win_rate'],
                 labels={
                     'name': 'Player Name',
                     'won': 'Games Won',
                     'surface_total': 'Total Matches on Grass',
                     'win_rate': 'Winning Percentage on Grass'
                 })
    fig1.update_layout(title_text='Players With the Most Wins on Grass Court', title_x=0.5)
    fig1.show()

    hard_court = winner_loser[winner_loser['surface'] == 'Hard']
    hard_court_top10 = hard_court.nlargest(10, 'won')
    # print(hard_court_top10)
    fig2 = px.bar(hard_court_top10, x='name', y='won', color_discrete_sequence =['blue'], hover_data=['surface_total', 'win_rate'],
                 labels={
                     'name': 'Player Name',
                     'won': 'Games Won',
                     'surface_total': 'Total Matches on Hard',
                     'win_rate': 'Winning Percentage on Hard'
                 })
    fig2.update_layout(title='Players With the Most Wins on Hard Court', title_x=0.5)
    fig2.show()

    clay_court = winner_loser[winner_loser['surface'] == 'Clay'] #fig 3
    clay_court_top10 = clay_court.nlargest(10, 'won')
    fig3 = px.bar(clay_court_top10, x='name', y='won', color_discrete_sequence =['red'], hover_data=['surface_total', 'win_rate'],
                 labels={
                     'name': 'Player Name',
                     'won': 'Games Won',
                     'surface_total': 'Total Matches on Clay',
                     'win_rate': 'Winning Percentage on Clay'
                 })
    fig3.update_layout(title_text='Players With the Most Wins on Clay Court', title_x=0.5)
    fig3.show()

    carpet_court = winner_loser[winner_loser['surface'] == 'Carpet']
    carpet_court_top10 = carpet_court.nlargest(10, 'won')
    fig4 = px.bar(carpet_court_top10, x='name', y='won', color_discrete_sequence =['grey'], hover_data=['surface_total', 'win_rate'],
                 labels={
                     'name': 'Player Name',
                     'won': 'Games Won',
                     'surface_total': 'Total Matches on Carpet',
                     'win_rate': 'Winning Percentage on Carpet'
                 })
    fig4.update_layout(title='Players With the Most Wins on Carpet Court', title_x=0.5)
    fig4.show()


if __name__ == '__main__':
    main()
