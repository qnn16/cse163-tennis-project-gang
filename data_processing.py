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


def main():
    # directory = 'data/'
    # data = combine_file(directory)
    # print(tennis.first_set_win(data))
    # tennis.court_surface(data)
    # tennis.hand_dominance(data)
    # tennis.predict_match_outcome(data)

    # empty = 'testdata4/'
    # empty_set = combine_file(empty)
    # assert tennis.first_set_win(empty_set) is None

    test_directory = 'testdata2/'
    data2_test = combine_file(test_directory)
    assert tennis.first_set_win(data2_test) == 78.78
    tennis.court_surface(data2_test)
    tennis.hand_dominance(data2_test)

    # test3_directory = 'testdata3/'
    # data3_test = combine_file(test3_directory)
    # assert tennis.first_set_win(data3_test) == 85.71
    # tennis.court_surface(data3_test) # this has key error
    # tennis.hand_dominance(data3_test)


if __name__ == '__main__':
    main()
