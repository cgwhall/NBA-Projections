
# Final Project Write-up

REPO: datasci-harris/final-project-nba_prediction_modeling

## Table of Contents:

#### 1.) [Introduction](#introduction)
#### 2.) [Research question](#research-question)
#### 3.) [Approach](#approach)
#### 4.) [Coding](#coding)
#### 5.) [Weaknesses](#weaknesses)
#### 6.) [Results](#results)
---

## Introduction

This write-up outlines the most important aspects of our final project. It includes why we chose our topic, the methodologies we employed, how our models performed, and our thoughts on how this project could be further developed in the future. 

## Research question

To what extent is an NBA player’s past performance predictive of his future performance? 

## Approach

In order to answer this question, we examine three statistical categories that are commonly used to evaluate a player’s productivity and efficiency: points, assists, and rebounds. As player productivity at the “per game” level is highly dependent on the minutes per game an individual plays, we standardized each statistical category to a “per minute” basis to account for role changes throughout a player’s career. For each statistical category, we ran four variations of an OLS model to predict our dependent variable (i.e., productivity per minute) on our independent variables, which include seasons played, sentiment scores of tweets, and coach/team performance. While our model allows us to predict a player’s productivity for any season included in our dataframe, we focus our analysis on the 2021-22 season (i.e., the most recently completed season).

## Coding

Broadly speaking, our code falls into one of four categories: data wrangling and cleaning, natural language processing (NLP), visualizations, and modeling. Each of these categories is outlined below:

- **Data wrangling and cleaning:** We obtained data by scraping [Basketball-Reference.com](https://www.basketball-reference.com/) and [Twitter](https://twitter.com/home). The data from Basketball-Reference.com served as our primary dataframe, while data acquired from Twitter was merged onto the Basketball-Reference.com dataframe, complementing it. In addition to general data cleaning (e.g., treating missing values, removing irrelevant columns, and dropping players with small sample sizes), a primary challenge in preparing the data for our model was matching each season in which a player appeared in our data to the number of seasons they had played (e.g., in the 2022 season, player X has been in the league for Y year, where Y is unique to that specific player). We overcame this problem by writing a function that took in the entire dataframe, and for each player, filtered and sorted the dataframe to only observations with that player, reset the index, and then used the index and an iterator to populate a “year” column, which indicated how many years in the league a player had by a given season. 

- **Natural language processing (NLP):** We used NLP to gauge the sentiment of tweets posted by beat reporters in the lead-up to several seasons, starting with the 2009-10 season and ending with the 2022-23 season. Specifically, we examined tweets posted between September 1 and October 15, focusing on tweets in which the names of the players in our dataframe appeared. We found the Twitter handles of the beat reporters whose tweets we analyzed at [Fansided.com](https://fansided.com/2018/10/11/nba-twitter-beat-writers/). By using the Spacy library in conjunction with the SNScrape library, we were able to scrape tweets and determine average sentiment scores for every player in each season we chose to analyze. 

- **Visualizations:** Our interactive visualizations were created using Shiny and give users the ability to **1)** compare two players’ productivities with respect to a particular statistic over the course of their careers, and **2)** see how well each of our models predicted the productivity of specific players for different sample sizes of players. Our static plots were created using Matplotlib. These figures illustrate **1)** the accuracy of our models’ predictions as they pertain to points per minute, and **2)** the error seen in each of our models when predicting points, assists, and rebounds. 

- **Modeling:** We employed four different OLS models.

  - **Simple model (Model 1):** 
    - *Stat per minute* = α + β<sub>1</sub>*year* + β<sub>2</sub>*year*<sup>2</sup> + μ


  - **Simple model with cluster fixed effects (Model 2 - this model grouped players according to relevant characteristics):** Ideally, clustering would account for year-over-year trends and employ machine learning techniques to determine best cluster fit. While we were unable to achieve that, we were able to leverage player peak productivity to cluster. Using different percentile clusters, we can restrict or open these group sizes. In our analysis, we used 20 clusters: 
    - *Stat per minute* = α + β<sub>1</sub>*year* + β<sub>2</sub>*year*<sup>2</sup> + Σ<sup>I</sup><sub>i=1</sub> δ<sub>i</sub>*cluster* + μ

  - **Simple player fixed-effects model (Model 3):** 
    - *Stat per minute* = α + β<sub>1</sub>*year* + β<sub>2</sub>*year*<sup>2</sup> + Σ<sup>I</sup><sub>i=1</sub> δ<sub>i</sub>*player* + μ

  - **Player fixed-effects model with sentiment score and team performance (Model 4):** 
    - *Stat per minute* = α + β<sub>1</sub>*year* + β<sub>2</sub>*year*<sup>2</sup> + β<sub>3</sub>*sentiment* + β<sub>4</sub>*team*<sup>2</sup> + μ

   - **Results:** The player fixed-effects model was the most accurate. 

## Weaknesses 

Two weaknesses that our analysis suffered from are detailed below.

- **Weakness 1:** Our use of NLP was fairly unsophisticated. By using the Spacy and SNScrape libraries, we were able to calculate a sentiment score for each tweet that we scraped—but that’s as far as we went. Obviously, this is not an especially rigorous use of NLP. If time wasn’t a constraint, we would have considered using other tactics to strengthen this part of our project. For example, we could have tried to give higher scores to tweets that referenced certain words and phrases, such as “all-star” and “hot streak.” We also could have explored ways to ensure that tweets referring to players by their nicknames weren’t ignored (e.g., our code didn’t scrape tweets in which Lebron James was referred to as “Lebron”; the same applies to other players with regularly-used nicknames). Another factor we didn’t address is how sentiment scores can be skewed by how frequently (or unfrequently) players are referenced in tweets. 

- **Weakness 2:** Our study’s scope is narrow. This is made apparent in our data and the seasons on which we chose to focus. In terms of our data, we didn’t analyze every player in the league. In fact, we dropped hundreds, including rookies and players whose playing time per season didn’t surpass a certain threshold. We dropped these players because we thought they could pose problems to our models. A more rigorous analysis would have accounted for them. Regarding the seasons on which we focused, we limited ourselves to the 2021-2022 season. Ideally, we would have broadened our scope to other seasons.

## Results

As noted above, our player fixed-effects model proved to be the most accurate based on average absolute error. If this project were taken up again in the future, certain tactics could be employed to make the analysis more robust. For starters, as briefly alluded to in the “Weaknesses” section, the analysis could be strengthened by leveraging NLP in a more nuanced manner, finding workarounds to ensure that every player in the NBA is examined, and expanding the scope of the study to include a greater range of seasons. It might also be worth investigating how performance is impacted by factors like trades, changes in position, contract adjustments, and the like.  Additionally, it would be interesting to see if it’s possible to generalize the code created for this project such that it could be used to make predictions about athletes in other leagues (e.g., the NFL, MLB, NHL, etc.) The world of sports is awash with data, making it ripe for further study. 
