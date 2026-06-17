# Real Estate Market Analysis with Python Project Instructions

Source DOCX: `Real Estate Market Analysis with Python Project.docx`

Investigating Property Transactions and Customer Satisfaction freeadvanced

With Elitsa Kaloyanova

- Type: Career Track project

- Duration: 18 Hours

## Description

## Solution

## Discussion

## Case Description

Background: The real estate market is a complex and dynamic entity of great interest for professionals in the field, investors, policymakers, and data analysts that wish to thoroughly understand the market conditions and customer behavior and make informed decisions. In our Real Estate Market Analysis with Python project, the client—a leading company in the industry—has collected data on properties and their customers and wishes you to help them with the real estate analysis.

Project Objective: This Real Estate Market Analysis with Python project aims for you to preprocess, analyze, and visualize the real estate property data, thereby generating meaningful insights about property transactions and customer profiles.

## Project requirements

For this Real Estate Market Analysis with Python project, you’ll need Python v.3 and Jupyter Notebook installed.

## You’ll need to have the following Python libraries installed

pandas

NumPy

Matplotlib

datetime

seaborn (optional)

The data in this Real Estate Market Analysis with Python project is divided into two main tables. The first dataset contains details about the properties, including ID, building details, sale date, etc. The second dataset comprises customer details, such as customer ID, entity, name, surname, and more.

## Project content

2 Project files

Guided and unguided instructions Up to 10 XP

## Part 1: Data Preprocessing

## Part 2: Descriptive Statistics

## Part 3: Data Analysis

## Part 4: Data Visualization

## Part 5: Data Interpretation

Quiz Up to 50 XP

## Featured tools

## Topics covered

Data AnalysisData visualizationData processing

## Related tracks

## To complete this project you need expertise on the following topic(s)

Data Analyst

Investigating Property Transactions and Customer Satisfaction freeadvanced

With Elitsa Kaloyanova

- Type: Career Track project

- Duration: 18 Hours

## Description

## Solution

## Discussion

## Case Description

Background: The real estate market is a complex and dynamic entity of great interest for professionals in the field, investors, policymakers, and data analysts that wish to thoroughly understand the market conditions and customer behavior and make informed decisions. In our Real Estate Market Analysis with Python project, the client—a leading company in the industry—has collected data on properties and their customers and wishes you to help them with the real estate analysis.

Project Objective: This Real Estate Market Analysis with Python project aims for you to preprocess, analyze, and visualize the real estate property data, thereby generating meaningful insights about property transactions and customer profiles.

## Project requirements

For this Real Estate Market Analysis with Python project, you’ll need Python v.3 and Jupyter Notebook installed.

## You’ll need to have the following Python libraries installed

pandas

NumPy

Matplotlib

datetime

seaborn (optional)

The data in this Real Estate Market Analysis with Python project is divided into two main tables. The first dataset contains details about the properties, including ID, building details, sale date, etc. The second dataset comprises customer details, such as customer ID, entity, name, surname, and more.

## Project content

2 Project files

Guided and unguided instructions Up to 10 XP

## Part 1: Data Preprocessing

## Part 2: Descriptive Statistics

## Part 3: Data Analysis

## Part 4: Data Visualization

## Part 5: Data Interpretation

Quiz Up to 50 XP

## Featured tools

## Topics covered

Data AnalysisData visualizationData processing

## Related tracks

## To complete this project you need expertise on the following topic(s)

Data Analyst

Descriptive Statistics

Now that we have successfully merged the two datasets, we can turn our attention to the next part of the analysis: descriptive statistics.A comprehensive statistical analysis will be conducted to understand the distribution of the key variables.

What are each variable's main characteristics—specifically the numerical ones?

What are the sales and overall performance by building type?

What are the sales and overall performance by country and state?

Breakdown by Building

First, we focus on the buildings’ variable and their different types. Here you must examine the totals and averages breakdown by building.

Start by examining how many building types there are in the data set.

Select columns of interest which to examine the totals by building type. Make a list with those variables, including building as the index variable. They are sold and mortgage .

Find the total number of sold properties, and how many of them had mortgages per building type.

Select columns of interest to examine the averages by building type and consider that they may not be the exact columns you used for the totals. They are area, price, and deal satisfaction.

Determine the average values of area , price , and deal satisfaction per building type.

Breakdown by Country

On the country level, perform the same analysis you did for the building types by choosing columns of interest and using summary statistics for the totals and averages. Make note that the breakdown of calculations by country will give you the frequency distribution by country.

Breakdown by State

Determine the frequency distribution by state, like you did for the countries table. In addition, create a table containing the relative frequency and the cumulative frequency by state.

Note: You can calculate the cumulative frequency using the .cumsum() pandas method.

Data Analysis

Now that you’ve successfully merged the two datasets and have tackled descriptive statistics, thus successfully completing an vital part of the project, it’s time to focus on the analysis of key variables.This phase will include a more in-depth analysis of the data to uncover trends, correlations, and hidden insights. Start by analyzing the customers' age (and age intervals) and perform the same analysis for the properties’ prices. Ultimately, find out more about the relationship between age and price.

Analyzing Age

Calculate age at the time of purchase. The first step of the analysis is determining the age of customers at the time of sale. As there isn’t such a variable in the data, you must work out the customers’ ages from the information given in the data.

Create age interval categories. After calculating the customers' ages, you must create age intervals to evaluate group behavior. Separate the age into 10 intervals of equal length, or otherwise create the following intervals:

(19.0, 25.0], (25.0, 31.0], (31.0, 36.0], (36.0, 42.0], (42.0, 48.0], (48.0, 54.0], (54.0, 59.0], (59.0, 65.0], (65.0, 71.0], (71.0, 76.0]

Break down by age intervals. Finally, using summary statistics, determine how many properties have been sold by age intervals.

Analyzing Properties

To analyze the properties, you must perform similar steps to the age analysis. Create 10 bins for the price intervals to answer the quiz questions successfully. But remember that the correct number of bins may vary in real-world situations.

Relationship between Properties and Age

To conclude this data analysis part of the project, you must examine the relationship between the properties and age variable. Discover the covariance and correlation between the two variables.

Data Visualization

The final part of the project is all about data visualization. Here is where all of our hard work pays off! Ensure you’ve cleaned and preprocessed the data and completed all the descriptive statistics and data analysis tasks because they’ll also serve you well in this part. You’re now ready to answer the client’s following critical questions regarding the data.

What is the average deal satisfaction for each country? How does it look by state?

What is the monthly revenue of the company?

How many apartments are sold in each state?

What is the age distribution for customers? (Use the same age intervals or number of bins from the data analysis stage.)

What are the yearly sales for each building?

## To answer these questions, you can create the following visualizations

Deal Satisfaction by Country – A bar chart or a heat map that represents average deal satisfaction by country

Revenue Graph – A time-series graph showing the total revenue over time

Apartments Sold by State – A pareto chart, in which the bar shows the absolute frequency of buildings sold by state, and the line chart displays the cumulative frequency

Age Distribution Histogram – A histogram displaying the age distribution of customers

Sales per Year by Building Type – A stacked bar graph or a line graph showing the yearly sales for each building type

Think about the previous analysis you've conducted on the relevant variables, such as the descriptive statistics by state and the deal satisfaction by country. Many of the visualizations can be created based on already existing tables.

Data Interpretation

The last step of the project is to think about the data interpretation.

Based on the data analysis, what can you conclude about the customer profile, as well as the building characteristics?

## You need to ask questions such as

Which customer age bracket has the most buyers potential?

What is the most sought after building?

What is the highest priced building?

Once you’ve formulated these questions and other relevant questions, consider how to leverage into a real-estate development strategy.

## Quiz

## Question 1

Which method is commonly used to combine two datasets into one Python?

.merge()

.concatenate()

.join()

.combine()

## Question 2

What is the average area of building type 1 in the data set in squared feet?

267

284

928

1943

## Question 3

What is the most common property type sold?

Apartment

Detached House

Townhouse

Office

## Question 4

Which building has the highest average property price?

Building 1

Building 2

Building 3

Building 4

## Question 5

What is the average cost of a building in Mexico?

$205,098

$257,183

$270,096

$338,181

## Question 6

Based on the data, which state has the second-highest number of properties sold?

California

Colorado

Nevada

Oregon

## Question 7

Based on the customer demographics, what is the most common age range of property buyers?

31-36

36-42

42-48

48-54

## Question 8

Considering you have split the price variable into 10 equal intervals, how many unsold properties are there in the last interval $496,201–$538,272:

1

4

6

20

## Question 9

What is the correlation between the customer's age and the property price?

Positive correlation

Negative correlation

No correlation

Immeasurable from the data

## Question 10

Which of the following countries has the highest average deal satisfaction?

Belgium

Canada

Mexico

US

## Question 11

Looking at the histogram of age distribution, what can you infer about the shape of the distribution?

Positively skewed

Negatively skewed

Normal distribution

Bimodal distribution

## Question 12

Which building had the highest sales in 2004 according to the data?

Building 1

Building 2

Building 3

Building 4

## Question 13

Which of the following states account for 82% of the company revenue?

California, Nevada, Colorado

California, Nevada, Oregon

Nevada, Colorado

Utah, Nevada, Colorado

## Question 14

Which of the following years brought in the highest revenue?

2004

2007

2008

2009

## Question 15

Referring to the stacked area chart showing the total number of sales per year by building, which building showed a significant decrease in sales over the years?

Building 1

Building 2

Building 3

Building 4
