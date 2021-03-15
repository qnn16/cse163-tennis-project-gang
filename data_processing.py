"""
Name: Quang and Steven Nguyen
CSE 163 Project: Analysis on Men’s Tennis Match Outcomes
In this file, we have a function that combines all the files
in our data folder and returns them as a single dataframe.
It also runs the functions from our tennis file and includes
test functions using other datasets.
"""
import os
import pandas as pd
import glob
import tennis


def combine_file(directory):
    """
    In this function, it takes a directory and returns a new dataframe
    combining all the csv files into one.
    It will ignore any empty csv files in the directory and if the directory
    only contains empty csv files, the function will return None
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


def main_data(directory):
    """
    Tests the main dataset from 1968-2021
    """
    data = combine_file(directory)
    print(tennis.first_set_win(data))
    tennis.court_surface(data)
    tennis.hand_dominance(data)
    tennis.predict_match_outcome(data)


def test_empty(directory):
    """
    Tests empty file
    """
    empty_set = combine_file(directory)
    assert tennis.first_set_win(empty_set) is None


def test_data2(directory):
    """
    Tests data file 2
    """
    test_data = combine_file(directory)
    assert tennis.first_set_win(test_data) == 78.78
    tennis.court_surface(test_data)
    tennis.hand_dominance(test_data)


def test_data3(directory):
    """
    Tests data file 3
    """
    test_data = combine_file(directory)
    assert tennis.first_set_win(test_data) == 71.79
    tennis.court_surface(test_data)
    tennis.hand_dominance(test_data)


def main():
    main_data('data/')
    test_empty('testdata4/')
    test_data2('testdata2/')
    test_data3('testdata3/')


if __name__ == '__main__':
    main()
