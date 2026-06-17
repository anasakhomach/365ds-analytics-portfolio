# Tracking User Engagement with SQL, Excel, and Python Project Instructions

Source DOCX: `Tracking User Engagement with SQL, Excel, and Python Project.docx`

Comparing and Analyzing Student Engagement Between Q2 2021 and Q2 2022 freeadvanced

With Hristina Hristova

- Type: Career Track project

- Duration: 25 Hours

- Status: In Progress

## Description

## Solution

## Discussion

## Case Description

Background: Throughout this Tracking User Engagement with SQL, Excel, and Python project, you’ll work with a real dataset from our company’s data. The project requires you to analyze whether the new additions to the platform (new courses, exams, and career tracks) have increased student engagement.

## You are given the following information

Holder (student ID) and issuance date of certificates issued in Q2 2022

Student ID and registration date of students registered between January 1, 2020 and June 30, 2022

Student ID, product type, purchase date, and refund date (if applicable) of purchases made between January 1, 2020 and June 30, 2022

Student watching (student ID), time watched, and date of courses watched in Q2 2021 and Q2 2022

We have, of course, restrictеd the dataset volume and made sure to protect our customers’ privacy.

Hypothesis: The first half of 2022 was expected to be profitable for the company. The reason was the hypothesized increased student engagement after the release of several new features on the company’s website at end-2021. These include enrolling in career tracks and testing your knowledge through practice, course, and career track exams. Of course, we have also expanded our course library to increase user engagement and the platform’s audience as more topics are covered. By comparing different metrics, we can measure the effectiveness of these new features and the overall engagement of our users.

Guidelines: Every data scientist has their preferred methodology. Two data scientists solving a task may obtain the same result using different tools. This implies that throughout this project, analyzing the data correctly and extracting meaningful results is more important than your approach.Nevertheless, we provide optional guidance with the tools taught in the courses from the Data Science career track.

## Project requirements

For this Tracking User Engagement with SQL, Excel, and Python project, you’ll be working with MySQL Workbench 8.0 (or later), Excel 2007 (or later), and Python 3, where you’ll need to prepare the following libraries:

pandas

matplotlib

statsmodels

scikit-learn

seaborn (optional)

The file is an SQL database containing information on student purchases, activity, and certificate issuance.

## Project content

1 Project file

Guided and unguided instructions Up to 10 XP

## Part 1: Data Preparation with SQL – Creating a View

## Part 2: Data Preparation with SQL – Splitting Into Periods

## Part 3: Data Preparation with SQL – Certificates Issued

## Part 4: Data Preprocessing with Python – Removing Outliers

## Part 5: Data Analysis with Excel – Hypothesis Testing

## Part 6: Data Analysis with Excel – Correlation Coefficients

## Part 7: Dependencies and Probabilities

## Part 8: Data Prediction with Python

Quiz Up to 50 XP

## Featured tools

## Topics covered

Relational DatabasesMachine learningProgrammingData PreprocessingMathematicsData Analysis

## Related tracks

## To complete this project you need expertise on the following topic(s)

Data Scientist

Data Preparation with SQL – Creating a View

Throughout this Tracking User Engagement with SQL, Excel, and Python project, you’ll work with a real dataset from our company’s data. The project requires you to analyze whether the new additions to the platform (new courses, exams, and career tracks) have increased student engagement.

The first half of 2022 was expected to be profitable for the company. The reason was the hypothesized increased student engagement after the release of several new features on the company’s website at end-2021. These include enrolling in career tracks and testing your knowledge through practice, course, and career track exams. Of course, we have also expanded our course library to increase user engagement and the platform’s audience as more topics are covered. By comparing different metrics, we can measure the effectiveness of these new features and the overall engagement of our users.

I. Calculating a Subscription’s End Date

Use the student_purchases table from the data_scientist_project database to create a result set with the following columns:

purchase_id

student_id

plan_id

date_start

date_end

date_refunded

The date_start column is the renamed date_purchased column from the database, adjusted for consistency with the subsequent date_end column.

To calculate the end date of a subscription (date_end), add one month, three months, or 12 months to the start date of a subscription for a Monthly (represented as 0 in the plan_id column), Quarterly (1), or an Annual (2) purchase, respectively.

The only exception is the lifetime subscription (denoted by 3), which has no end date. Refunds will be handled in the following task: II. Re-Calculating a Subscription’s End Date.

Hint 1: Research MySQL’s DATE_ADD function.

Hint 2: You can refer to the Customer Engagement Analysis with SQL and Tableau course (the Retrieving Relevant Data from The Database section), which explains this query in detail.

Sanity Check: Ensure your table has 18,207 rows—i.e., you’ve found each subscription’s start and end dates.

To complete the task, follow the instructions below.

Identify the fields to include in your result set: You’ll want to include all fields from the original table in your result set, but you’ll also need to create two new ones: date_start and date_end. date_start will be the date_purchased field from the original table, but date_end must be calculated.Note the skeleton of the code:

SELECT

???,

???,

???,

??? AS date_start,

??? AS date_end,

???

FROM

student_purchases;

Calculate the subscription end date: You’ll need to use the plan_id field to calculate the date_end field. Depending on the plan_id, you’ll add a different number of months to the date_purchased field. To handle the varying number of months to add, you can use a CASE statement inside your calculation.Note the skeleton of the code:

SELECT

???,

???,

???,

??? AS date_start,

CASE

WHEN plan_id = 0 THEN ???

WHEN plan_id = 1 THEN ???

WHEN plan_id = 2 THEN ???

WHEN plan_id = 3 THEN ???

END AS date_end,

???

FROM

student_purchases;

II. Re-Calculating a Subscription’s End Date

Using the query from the previous task (I. Calculating a Subscription’s End Date) as a sub-query, create a new one retrieving the following columns:

purchase_id

student_id

plan_id

date_start

date_end

Re-calculate the date_end column so that if an order was refunded—indicated by a non-NULL value in the date_refunded field—the student’s subscription terminates at the refund date.

Sanity Check: Ensure your view has 18,207 rows.

To complete the task, follow the instructions below.

Identify the fields to include in your result set: Include the necessary fields from the sub-query created in the previous task.

SELECT

???,

???,

???,

date_start,

date_end

FROM

(

-- Sub-query created in the task "I. Calculating a Subscription's End Date"

) a;

Handle refunds: If a refund occurred, the subscription end date should be the refund date instead of the calculated end date. To handle this, use an IF statement or a similar control structure.

SELECT

???,

???,

???,

date_start,

IF(date_refunded IS NULL,

???,

???) AS date_end

FROM

(

-- Sub-query created in the task "I. Calculating a Subscription's End Date"

) a;

III. Creating Two ‘paid’ Columns and a MySQL View

Using the query you designed in the previous task (II. Re-Calculating a Subscription’s End Date), create a new SQL query that, when executed, stores in the data_scientist_project schema a view called purchases_info which we’ll use in subsequent parts. The view should include the following columns:

purchase_id

student_id

plan_id

date_start

date_end

paid_q2_2021

paid_q2_2022

The paid_q2_2021 and paid_q2_2022 columns contain binary values indicating whether a student had an active subscription during the respective year’s second quarter (April 1 to June 30, inclusive). A 0 in the column indicates a free-plan student in Q2, while a 1 represents an active subscription in that period.

Refer to the following instructions to complete the task.

Identify the fields to include in your result set: Select all fields from the sub-query created in II. Re-Calculating a Subscription’s End Date. Include two new fields: paid_q2_2021 and paid_q2_2022.

SELECT

???,

??? AS paid_q2_2021,

??? AS paid_q2_2022

FROM

(

-- Sub-query created in the task "II. Re-Calculating a Subscription's End Date"

) b;

Identify if a student has an active subscription: Use, for example, a CASE statement and check if a subscription period falls inside Q2—i.e.:

If the end date is before April 1, the student will have had a free plan (indicated by 0).

If the start date is after June 30, the student will have had a free plan (indicated by 0).

In all other cases, the student will have had an active subscription (indicated by 1).

SELECT

???,

CASE

WHEN ??? THEN 0

WHEN ??? THEN 0

ELSE 1

END AS paid_q2_2021,

CASE

WHEN ??? THEN 0

WHEN ??? THEN 0

ELSE 1

END AS paid_q2_2022

FROM

(

-- Sub-query created in the task "II. Re-Calculating a Subscription's End Date"

) b;

Create the view: Add the following code lines at the beginning of your query to create the view. Refresh the schema and ensure the view has appeared under Views in the data_scientist_project database.

DROP VIEW IF EXISTS purchases_info;

CREATE VIEW purchases_info AS

SELECT

???,

CASE

WHEN ??? THEN 0

WHEN ??? THEN 0

ELSE 1

END AS paid_q2_2021,

CASE

WHEN ??? THEN 0

WHEN ??? THEN 0

ELSE 1

END AS paid_q2_2022

FROM

(

-- Sub-query created in the task "II. Re-Calculating a Subscription's End Date"

) b;

Data Preparation with SQL – Splitting Into Periods

Great job! We created a view in the schema called purchases_info, which stores information about students’ subscriptions and whether these subscription periods overlap with the second quarters of 2021 or 2022. Now, we’ll utilize purchases_info to classify students as free-plan and paying in Q2 2021 and Q2 2022.

I. Calculating Total Minutes Watched in Q2 2021 and Q2 2022

We’re now interested in analyzing the engagement of our users in terms of the total minutes watched during Q2 2021 and Q2 2022 separately. Additionally, we want to identify which users were paid subscribers during each of these periods.

## Your task is to write an SQL query that returns the following columns

student_id – a list of student IDs

minutes_watched – the total minutes students have watched in both periods—return a separate table for each period

The information about the minutes watched by each student is available in the student_video_watched table.

Sanity Check: Ensure you have 7,639 rows in the result set representing students who watched a lecture in Q2 2021. Then, confirm you have 8,841 rows in the result set representing students who watched a lecture in Q2 2022.

Follow the instructions below to complete the task.

Identify the necessary fields: Select the student_id field from the student_video_watched table and calculate the total minutes watched. Round the result to two decimal places.

SELECT

student_id,

??? AS minutes_watched

FROM

student_video_watched;

Aggregate by student: Perform the aggregation such that you calculate the minutes watched for each student.

SELECT

student_id,

??? AS minutes_watched

FROM

student_video_watched

GROUP BY student_id;

Add a condition: Add a condition that filters 2021 and 2022.

SELECT

student_id,

??? AS minutes_watched

FROM

student_video_watched

WHERE

???

GROUP BY student_id;

II. Creating a ‘paid’ Column

Now, use the query you designed in the previous task (I. Calculating Total Minutes Watched in Q2 2021 and Q2 2022) to create a result set with the following columns:

student_id

minutes_watched

paid_in_q2

The last column indicates whether a student had an active subscription in Q2 (represented by 1) or not (represented by 0).

Retrieve the following four datasets and store them in the corresponding CSV files:

Students engaged in Q2 2021 who haven’t had a paid subscription in Q2 2021 (minutes_watched_2021_paid_0.csv)

Students engaged in Q2 2022 who haven’t had a paid subscription in Q2 2022 (minutes_watched_2022_paid_0.csv)

Students engaged in Q2 2021 who have been paid subscribers in Q2 2021 (minutes_watched_2021_paid_1.csv)

Students engaged in Q2 2022 who have been paid subscribers in Q2 2022 (minutes_watched_2022_paid_1.csv)

Note: Remember that the same student can have multiple subscription records in the purchases_info view.

Sanity check: Ensure you retrieve the following number of rows for each case, respectively:

5,334

6,055

2,305

2,786

Follow the instructions below to complete the task.

Identify the tables: We need the information from the sub-query we created in the previous task (I. Calculating Total Minutes Watched in Q2 2021 and Q2 2022) and the purchases_info view. Consider joining the sub-query and the view such that you retrieve all records from the sub-query regardless of whether a student has a record in purchases_info or has never purchased a subscription.

SELECT

???

FROM

(

-- Sub-query created in the task 'I. Calculating Total Minutes Watched in Q2 2021 and Q2 2022'

) a

??? purchases_info i ON ???;

Retrieve the necessary columns and create the paid_in_q2 one: Retrieve the student_id and miutes_watched columns. Use an IF statement to check if a student has a record in the purchases_info view. Aggregate the results such that you obtain one record per student.

SELECT

???,

???,

IF(???) AS paid_in_q2

FROM

(

-- Sub-query created in the task 'I. Calculating Total Minutes Watched in Q2 2021 and Q2 2022'

) a

??? purchases_info i ON ???

GROUP BY

???;

Create the four data sources: Filter the data to obtain all four datasets described in the task.

SELECT

???,

???,

IF(???) AS paid_in_q2

FROM

(

-- Sub-query created in the task 'I. Calculating Total Minutes Watched in Q2 2021 and Q2 2022'

) a

??? purchases_info i ON ???

GROUP BY

???

HAVING

paid_in_q2 = ???;

Data Preparation with SQL – Certificates Issued

In the previous two sections, you created a MySQL view and used it to classify students as free-plan or paying on a given date. In this short task, you’ll retrieve information on the minutes watched and the certificates issued to a student. Later in the project, we’ll study the correlation between these two metrics.

I. Studying Minutes Watched and Certificates Issued

For this task, consider only the students who’ve been issued a certificate. Create an SQL query to extract the following information for each such student:

The student ID

The total minutes watched

The total number of certificates issued

Assign the corresponding value for students with no minutes recorded as 0. Save the resulting table as minutes_and_certificates.csv for later use.

Sanity Check: Ensure your table has a total of 658 rows.

To execute the task, follow the instructions below.

Create a sub-query: Select the student_id column from the student_certificates table. Then, count the number of certificates each student has been issued and store the result in a column called certificates_issued.

SELECT

student_id,

??? AS certificates_issued

FROM

student_certificates

???;

Join tables: Use an appropriate JOIN clause to join the sub-query with the student_video_watched table.

SELECT

???,

???,

???

FROM

(

-- Sub-query

) a

??? student_video_watched w ???

???;

Select the relevant fields: Select all records from the sub-query, retrieving the student_id and certificates_issued columns. For the students entering the sub-query, calculate the number of minutes watched and store the result in a column called minutes_watched. Note that a student with an issued certificate shouldn’t have necessarily watched a video, so their record in the minutes_watched column should be 0.

SELECT

???,

??? AS minutes_watched,

???

FROM

(

-- Sub-query

) a

??? student_video_watched w ???

???;

Data Preprocessing with Python – Removing Outliers

## Excellent work! You should now be equipped with the following CSV files

minutes_watched_2021_paid_0.csv

minutes_watched_2022_paid_0.csv

minutes_watched_2021_paid_1.csv

minutes_watched_2022_paid_1.csv

minutes_and_certificates.csv

We’re now ready to switch technologies and open Jupyter Notebook, where we’ll study the data with the help of distribution plots and remove the outliers so that they don’t skew the analysis we’ll perform later in this project. The following tasks will use the first four CSV files listed above.

I. Plotting the Distributions

Plot the distribution of the minutes_watched variable of each of the four datasets and examine its shape. Are the distributions skewed? If yes, how? What does this tell us about the distribution of minutes watched?

Hint: Research pandas’ kdeplot() method. You can create four subplots displaying all four distributions simultaneously for better clarity.

Follow the instructions below to execute the task.

Importing necessary libraries: Import the pandas library for data manipulation and matplotlib and seaborn for data visualization.

Loading the data: Load the CSV data files into four separate pandas DataFrames. Remember that pandas has a method read_csv(), which loads a CSV file and returns a DataFrame.

Initial data exploration: Examine the loaded data applying the head() method on the DataFrames to display the first few rows.

Plotting the distributions: To plot the distributions, you will use the seaborn method kdeplot(). It takes as an argument the column of the DataFrame you wish to plot. The column is selected using the DataFrame variable followed by the column name in square brackets.

II. Removing the Outliers

Remove the outliers of the data—for each of the four datasets, keep the values lower than the 99th percentile.

Once you’ve retrieved the final datasets, save them as four separate CSV files on your computer:

minutes_watched_2021_paid_0_no_outliers.csv

minutes_watched_2022_paid_0_no_outliers.csv

minutes_watched_2021_paid_1_no_outliers.csv

minutes_watched_2022_paid_1_no_outliers.csv

## Hint: To save a DataFrame as a CSV file, use the following line of code

df_name.to_csv('file_name.csv', index=False)

If you don’t specify a path at the beginning of the string, the CSV file will be stored in the same directory as your Jupyter Notebook document.

Follow the instructions below to execute the task.

Checking for outliers: First, you can use pandas’ quantile() method to calculate the 99th percentile of the minutes_watched column.

Removing outliers: Now that you have the 99th percentile value, you can use it to filter your DataFrame. You want to keep only those rows where minutes_watched is less than this value using, for example, conditional filtering.

Visualizing the filtered data: After removing the outliers, plot and study the new distributions.

Saving the data as a CSV file. Save the filtered data to a CSV file using pandas’ to_csv() method. Ensure you follow the same steps to process all four datasets. At the end of this exercise, you should have obtained the following CSV files:

minutes_watched_2021_paid_0_no_outliers.csv

minutes_watched_2022_paid_0_no_outliers.csv

minutes_watched_2021_paid_1_no_outliers.csv

minutes_watched_2022_paid_1_no_outliers.csv

Data Analysis with Excel – Hypothesis Testing

You’re making significant progress! In the previous part (Data Preprocessing with Python – Removing Outliers), we removed the outliers from four of the datasets and stored the results in the following CSV files:

minutes_watched_2021_paid_0_no_outliers.csv

minutes_watched_2022_paid_0_no_outliers.csv

minutes_watched_2021_paid_1_no_outliers.csv

minutes_watched_2022_paid_1_no_outliers.csv

Now, open a new Excel sheet and paste the content of each file into a separate tab within the same worksheet. Once you’ve done that, you are ready to proceed with the following tasks.

I. Calculating Mean and Median Values

Calculate the mean and median minutes watched by students in the four groups. How does the median compare with the mean in each group? Referring to the distribution plots you created in Data Preprocessing with Python – Removing Outliers, does this result meet your expectations?

To execute the task, follow the instructions below.

Insert the data: In separate Excel tabs, open all four CSV files.

Calculate the mean and median minutes: Apply the Excel functions AVERAGE and MEDIAN to the minutes_watched column to compute the mean and median values.

Compare with the distribution plots: Compare these metrics to see how engagement changed from Q2 2021 to Q2 2022 for free-plan and paying students. Referring to the skewness of the distribution plots, did the difference in mean and median values meet your expectations?

II. Calculating Confidence Intervals

For each of the four groups, find the minute interval for which you are 95% confident a random person will fall in that interval. Assume a normal distribution.

What conclusions can you draw about students’ engagement in Q2 2021 and Q2 2022 for both free-plan and paying students?

Optional: Create a confidence interval bar chart to support your arguments better.

To execute the task, follow the instructions below.

Determine the size of your sample (n): Use Excel’s COUNT function to find the number of observations in your data.

Calculate the standard error: Calculate this value by dividing the standard deviation (STDEV.S) by the square root (SQRT) of the sample size.

Calculate the margin of error: Perform this calculation by multiplying the critical value—assuming a normal distribution—with the standard error.

Calculate the confidence interval: Subtract the margin of error from the mean to get the lower bound and add it to the mean to get the upper bound.

III. Performing Hypothesis Testing

You want to reach a data-driven decision on whether the new features (courses, career tracks, and exams) contribute to the increased number of minutes watched on the platform for free-plan and paying students—i.e., increased student engagement in their study process. You use hypothesis testing on both groups (free-plan and paying) for 2021 and 2022.

## Let your null and alternative hypotheses (respectively) be

The engagement (minutes watched) in Q2 2021 is higher than or equal to the one in Q2 2022

. We test free-plan and paying students separately.

The engagement (minutes watched) in Q2 2021 is lower than the one in Q2 2022

. We test free-plan and paying students separately.

## Additionally, make the following assumptions

Assume a normal distribution.

For free-plan students, perform a two-sample t-test assuming equal variances.

For paying students, perform a two-sample t-test assuming unequal variances.

Optional: Perform a two-sample f-test for variances to support the assumptions.

What conclusion can you draw from this test? Comment on the results of committing a Type I or a Type II error in this study. Which one would result in higher costs to the company?

Note the following instructions for free-plan students where the variances are assumed equal.

Prepare your data: Have one row for the metrics of students engaged in Q2 2021 and another for the metrics of students engaged in Q2 2022. Do this separately for free-plan and paying students.

Calculate the pooled variance

Data Analysis with Excel – Correlation Coefficients

You’re approaching the end of the Excel part of the project. In the previous part (Data Analysis with Excel – Hypothesis Testing), you performed a hypothesis analysis and concluded whether the additions to the platform had increased the minutes watched by students.

Now, you’ll analyze the correlation between the minutes watched on the platform and the certificates issued. You’ll work with the minutes_and_certificates.csv file created in the Data Preparation with SQL – Certificates Issued part.

I. Calculating Correlation Coefficients

Find the correlation coefficient between the minutes watched and the certificates issued. Interpret the results.

Optional: Create a scatter plot to support your arguments better.

To execute the task, follow the instructions below.

Load the data into Excel: First, you must have your CSV data in Excel.

Calculate the correlation coefficient: You want to find the correlation between the minutes watched and certificates issued. Select the two columns and use Excel’s built-in function (CORREL) to perform the calculation.

Create a scatter plot (Optional): You can make a scatter plot to interpret the results better.

Interpret the correlation coefficient: Recall which correlation coefficient values indicate a strong or weak correlation. What do positive and negative values represent?

Dependencies and Probabilities

In this part of the project, we analyze the engaged students on the platform. Return to the data_scientist_project database and consider all students who’ve watched a lecture in Q2 2021 and those who’ve watched a lecture in Q2 2022 as two sets. Let the universal set be all students who’ve watched a lecture on the platform—the union of the two sets defined above. Don’t omit any outliers we’ve removed during this project.

II. Calculating Probabilities

What is the probability that a student has watched a lecture in Q2 2021, given that they’ve watched a lecture in Q2 2022?

To complete the task, follow the instructions below.

Define the task: The question asks for the conditional probability that a student watched a lecture in Q2 2021 given that they watched a lecture in Q2 2022.

Identify the relevant data: You’ll need to know the following two critical pieces of information to solve this problem.

The number of students who watched a lecture in Q2 2022 will be the denominator of your probability calculation because these are the conditions under which we calculate the probability.

The number of students who watched a lecture in Q2 2021 and Q2 2022 will be the numerator of your probability calculation because these are the cases we’re interested in.

Data Prediction with Python

Congratulations! You’ve applied various technologies like SQL, Python, Excel, and pure theory to extract, preprocess, analyze, and compare data concerning student engagement in Q2 2021 and Q2 2022. You’ve now reached the final part of this project, which deals with applying machine learning techniques. Use the minutes_and_certificates.csv file you extracted in the Data Preparation with SQL – Certificates Issued part. Let’s begin!

I. Creating a Linear Regression

This part aims to perform a linear regression using the minutes_watched column as a predictor and certificates_issued as a target. Having done that, answer the following:

What is the linear equation that explains the behavior of the relationship?

What is the R-squared value of the regression? How would you interpret it?

What is the predicted number of certificates taken by a student who has watched 1200 minutes of content? (Round your result up to the nearest integer.)

Note: Use 20% of your data as a test set. Use the number 365 as a random state.

To complete the task, follow the instructions below.

## Import the relevant libraries

pandas library,

matplotlib library,

LinearRegression model from the sklearn.linear_model module,

train_test_split method from the sklearn.model_selection module,

seaborn library (optional).

Data import: Use the pandas read_csv() method to import your CSV file containing the dataset. This will return a DataFrame you can store in a variable (e.g., raw_data).

Copy the data: Create a copy of the data to avoid accidentally modifying it; call the new variable data.

Data preview: You can use the head() method to preview your data quickly, including the column names and the first few rows.

Define the input and target variables: Divide your dataset into features (input variable) and target variable.

Split the data into training and testing sets: It’s good practice to split your data into training and testing sets to avoid overfitting and understand how your model will perform on new data. As instructed in the task, allocate 20% of the data to a test set and use 365 as a random seed—ensuring the train-test split is the same each time.

Reshape the data: Since we create a model with a single feature, the training and test inputs need to be converted to NumPy ndarrays and then reshaped.

Create and train the model: Create an instance of sklearn’s LinearRegression model and then fit it on the training data.

Linear equation: After you fit the regression model to the training data, print the value of the slope (denoted by

Calculating the R-squared: Print the value of the R-squared metric and interpret the number.

Prediction: Once the model is fitted, you can make predictions using the predict() method.

Visualization: To visualize the model performance, you can create a scatter plot where the

-axis represents the actual test values, and the

-axis is the predicted values.

## Quiz

## Question 1

Consider your solution to Data Preparation with SQL – Creating a View. Which of the following pieces of code would successfully modify the date_end column if a refund is made?

IF(date_end IS NULL, date_refunded, date_end) AS date_end

IF(date_refunded IS NULL, date_refunded, date_end) AS date_end

IF(date_refunded IS NULL, date_end, NULL) AS date_end

IF(date_refunded IS NULL, date_end, date_refunded) AS date_end

## Question 2

Consider your solutions to Data Preparation with SQL – Splitting Into Periods. Which of the following pieces of code would correctly calculate the minutes watched from seconds watched and round the result to two decimal places?

ROUND(2, SUM(seconds_watched) / 60)

ROUND(2, SUM(seconds_watched))/60

ROUND(SUM(seconds_watched) / 60, 2)

ROUND(SUM(seconds_watched), 2) / 60

## Question 3

Consider your solution to Data Preprocessing with Python – Removing Outliers. What can you say about the distribution of minutes watched in both periods?

The distribution is right-skewed

The distribution is left-skewed

The distribution is symmetrical

No conclusion can be drawn about the distribution

## Question 4

Consider your solution to Data Preprocessing with Python – Removing Outliers. Which of the following pieces of code would keep the values from the data DataFrame lower than the 99th percentile and store them in a new DataFrame called data_no_outliers?

data_no_outliers = data[data['minutes_watched'] = data['minutes_watched'].quantile(0.99)]

data_no_outliers = data[data['minutes_watched'] > data['minutes_watched'].quantile(0.99)]

data_no_outliers = data[data['minutes_watched'] < data['minutes_watched'].quantile(0.99)]

data_no_outliers = data[data['minutes_watched'].quantile(0.01)]

## Question 5

Consider your solution to Data Analysis with Excel – Hypothesis Testing. How does the sample size affect the confidence interval?

As the sample size increases, the confidence interval narrows, assuming the confidence level remains constant.

As the sample size increases, the confidence interval becomes wider, assuming the confidence level remains constant.

The sample size has no impact on the confidence interval.

The confidence interval is only affected by the sample size if the sample size is less than 30.

## Question 6

Consider your solution to Data Analysis with Excel – Hypothesis Testing. What conclusion can we draw based on the confidence intervals of the free-plan students who watched in Q2 2021 and Q2 2022?

The average minutes watched by students in Q2 2021 is higher than that of students in Q2 2022. This is because the lower limit of the confidence interval for Q2 2021 is less than the lower limit for Q2 2022.

The average minutes watched by students in Q2 2022 is higher than in Q2 2021. This is because the entire confidence interval for Q2 2022 is above the entire confidence interval for Q2 2021.

The average minutes watched by students in Q2 2022 is lower than that of students in Q2 2021. This is because the upper limit of the confidence interval for Q2 2022 is lower than the upper limit for Q2 2021.

There is no significant difference in the average minutes watched by students in Q2 2021 and Q2 2022. This is because the confidence intervals for both periods overlap.

## Question 7

Consider your solution to Data Analysis with Excel – Hypothesis Testing. What conclusion can we draw based on the confidence intervals of the paying students who watched in Q2 2021 and Q2 2022?

The students who watched a course in Q2 2021 had more minutes watched on average than students who watched a course in Q2 2022.

The students who watched a course in Q2 2022 had more minutes watched on average than students who watched a course in Q2 2021.

The students who watched a course in Q2 2021 and students who watched a course in Q2 2022 have the same average minutes watched.

We cannot make a valid conclusion about the differences in the average minutes watched between students who watched a course in Q2 2021 and students who watched a course in Q2 2022.

## Question 8

Consider your solution to Data Analysis with Excel – Hypothesis Testing. What is the approximate value of the t-statistic you obtain for free-plan students? Do you accept or reject the null hypothesis?

-4.0 – we accept the null hypothesis

-4.0 – we reject the null hypothesis

5.0 – we accept the null hypothesis

5.0 – we reject the null hypothesis

## Question 9

Consider your solution to Data Analysis with Excel – Hypothesis Testing. What is the approximate value of the t-statistic you obtain for paying students? Do you accept or reject the null hypothesis?

-4.0 – we accept the null hypothesis

-4.0 – we reject the null hypothesis

5.0 – we accept the null hypothesis

5.0 – we reject the null hypothesis

## Question 10

Consider your solution to Data Analysis with Excel – Hypothesis Testing. Which of the following comes closest to the value of the correlation coefficient between the minutes watched and the certificates issued?

0.5

0.6

0.7

0.8

## Question 13

Consider your solution to Dependencies and Probabilities. What can you say about the two events of watching a lecture in Q2 2021 and Q2 2022?

The two events are dependent.

The two events are independent.

It cannot be determined whether the two events are dependent.

## Question 14

Consider your solution to Dependencies and Probabilities. What is the approximate probability that a student has watched a lecture in Q2 2021, given that they’ve watched a lecture in Q2 2022?

5%

7%

10%

12%

## Question 16

Consider your solution to Data Prediction with Python. Which of the following comes closest to the R-squared value of the linear model?

0.2

0.3

0.4

0.5

## Question 17

Consider your solution to Data Prediction with Python. What is the predicted number of certificates taken by a student for whom the minutes watched equal 1200? Round your result up to the nearest integer.

1

2

3

4
