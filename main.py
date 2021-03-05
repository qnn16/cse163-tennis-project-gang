import pandas as pd
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
    directory = r'C:\Users\steve\OneDrive\Documents\GitHub\cse163-tennis-project-gang\data'
    print(combine_file(directory))


if __name__ == '__main__':
    main()
