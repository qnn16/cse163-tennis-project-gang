# Analysis on Men's Professional Tennis Match Outcomes
#### By Steven and Quang Nguyen

### Research Questions

-   **How does the surface of the court affect the outcome of the match? Does this give an advantage to a player?**
    > In certain cases, we noticed in tournaments there are different types of courts that these tournaments are runned on like grass, hard and clay courts. So, we are computing the result of the match based on the surface of the court. With this we can see if having a different surface gives an advantage to some players when playing on those courts.
-   **How does winning the first set affect the outcome of the match? Is there a correlation to a higher chance of winning the game by winning the first set?**
    > During a tennis match, with momentum being a factor of winning a set, we wanted to see if the momentum of winning the first set helps a player get the win the overall match. We are trying to compute the match outcome based on the order of sets won during the match.
-   **When facing an opponent with a certain dominant hand, how does it change the outcome of the match? Is the match better matched if they both have the same dominant hand or opposite or etc.?**
    > During a tennis match, with the chances of going against an opponent with a different dominant hand. This could impact the gameplay of the players since the ball could be sliced and curve a different direction. Also there is a chance of having an opponent that is ambidextrous. So with this we are trying to find the chances of winning when a player is going against the opponent with a certain dominant hand.

## [Dataset](https://github.com/JeffSackmann/tennis_atp)
#### - Within this dataset, it contains information about each and every match based on the year the tennis game was played. Within each dataset, it will contain information about:
    - The tournament played at (name of tournament, draw size, data played)
    - Surface
    - Winner and loser
    - Age of the player
    - Score, minutes played, number of aces
    - Ranks and rank points

## Challenge Goals
> We are using machine learning as one of our challenge goals in order to predict the match outcome based on information provided about the match including first serves won/lost, order of sets won/lost, and surface type. Our project will meet this goal because of all available specific statistical information about each match and the abundance of it for each year from 1968-2021.
> We are also planning to use a new library, plotly, to report and graph our findings such as win/loss statistics, rank points, and tournament statistics with an interactive user interface. Our project will meet this goal because of our familiarity with making graphs and plots within python and the amount of data that is included within our chosen dataset.

## Motivation and Background
> In the world of sports, there are players who are exceptional enough to reach the peak level of their certain sport and play against the best. However, even then, there are players who continue to dominate even amongst the greatest players of their generation. From firsthand experience of playing and watching high-level competitive tennis, we would think about what allows a certain player to be better than another and ultimately defeat them in a match. Based on these thoughts, our motivation came from the curiosity of different variables that could benefit one person over the other, such as technique or even the environment. These attributes are reflected in the game analytics and with variables like the surface type of the court and the dominant hands of each player in a match. With this knowledge, we could possibly obtain information that could give players a better idea of what to expect in a match and how to possibly tweak their training so that they’re able to pinpoint weaknesses of their opponents and themselves in order to make it to the top level.

## Methodology
> To answer the question on if certain court surfaces are advantageous for certain players, we would group all of the matches by each court surface and player based on their name. From there, we need to look at the total amount of wins and losses that they had on each court to compute the average win percentage for each player on each court. With this information, we’re able to see how each player fairs on the different court surfaces and can come to a conclusion about each player’s most dominant and weakest court. From then, we can create an interactive barchart plot that allows the user to select a court surface to display the top 10 players with the most wins on that specific surface along with the total number of wins.

> Similarly, we’re also computing the statistics including the match outcome, aces, and sets won for all of the matches based on a player’s dominant hand and how they fared up against a player who did or didn’t share the same dominant hand. We plan on taking all the possible matchup combinations, as in a left-handed player facing another left-handed player, a right-handed player vs a right-handed player, and players who do not share the same hand dominance, and dividing the match wins by the total number of matches for each hand combination to find the win-rate. We can then add up the total number of aces in each combination provided by the column already calculated in the dataset. However, calculating the number of sets won was a bit more difficult since the only data involving the score itself is the actual scoreboard. To do this, we would need to split the score of the sets based on the empty space in between each set and calculate the winner based on the higher score by iterating through each set. Fortunately, the scores are presented in a manner that always has the data for the winner on the left hand side and loser on the right, so we could create new columns that display the number of sets won and assign them to each player based on the positions of the score. We can graph the information such as the match outcome, aces, and sets won on a bar chart for each separate hand combination and look for patterns on if hand dominance plays a role in determining the winner.

> We are trying to create a machine learning algorithm through regression to predict the outcome of the matches based on winning the first set of a tennis match leading to a win as an outcome. First we want to filter the data, having columns containing the winner’s information, with their name and match stats from aces, first serve won, and amount of double faults. With the filter set, we would also remove any missing data. In the machine learning algorithm, we are making our label the first set won, then the features being the rest of the columns other than the label. Then while creating the regression model, we want to split the data so it is 80:20 ratio, making the majority of the dataset for training and the rest for testing. Then with the model, we use it to calculate the mean squared error. With the score we could see if we could predict the outcome based on the first set win of the match.

## Results

### Work Plan and Evaluation
- **Collaboration**
    - When developing and testing our code, we plan to coordinate times for us to work on the project together and will be sharing access to the source code so that we can simultaneously do work on Visual Studio Code.
- **Clean up and combine data (5 hours)**
    - Combining all the csv files for each year into one dataframe 
    - Removing columns that are not needed
    - Create dataframes
- **Make model to predict match outcome (12 hours)**
    - Training set and testing set for ML
- **Analysis for court surfaces and match outcomes based on hand dominance (4 hours)**
    - Compute the wins when the first set is won
    - Running tests to see if the program is properly running
- **Results (4 hours)**
    - Graphs presenting the findings
- **Evaluation**
    - blank

## License

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" href="http://purl.org/dc/dcmitype/Dataset" property="dct:title" rel="dct:type">Tennis databases, files, and algorithms</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="http://www.tennisabstract.com/" property="cc:attributionName" rel="cc:attributionURL">Jeff Sackmann / Tennis Abstract</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.<br />Based on a work at <a xmlns:dct="http://purl.org/dc/terms/" href="https://github.com/JeffSackmann" rel="dct:source">https://github.com/JeffSackmann</a>.
