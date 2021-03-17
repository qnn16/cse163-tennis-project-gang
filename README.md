# Analysis on Men's Professional Tennis Matches

Our project uses all of the requisite Python packages and versions
that was provided by the `environment.yaml` file on the CSE163 course page.

We use the plotly library in our project which is not already included in the `environment.yaml` file
To install plotly this line of code can be ran in the terminal\
`pip install plotly`

To reproduce our project results, clone the repository and run the `data_processing.py` file.
Our data is included in csv format in the `data` folder.

The expected results should be a win percentage calculated by a player's first set win
that is printed in the terminal. There should also be a maximum of 10 graphs depending
on the data, that opens in a different browser. Lastly, our machine learning function
should print out accuracy scores for the training and testing models in the terminal.
We also included testing functions within the `data_processing.py` file that tests our main functions from the `tennis.py` file on different and smaller datasets. We decided to comment them out in the main function so that the person who's running our files will not get overwhelmed by 20+ simultaneous plotly graphs. However, they are welcome to uncomment them and check them individually.
