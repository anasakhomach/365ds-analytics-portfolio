# Customer Engagement Analysis with SQL and Tableau Project Instructions

Source DOCX: `Customer Engagement Analysis with SQL and Tableau Project.docx`

A Practical Approach to Analyzing and Visualizing Customer Engagement Metrics freeintermediate

With Hristina Hristova

- Type: Course project

- Duration: 10 Hours

## Description

## Solution

## Discussion

## Case Description

Overview: Our Customer Engagement Analysis with SQL and Tableau project offers an exceptional opportunity to enhance and expand your professional portfolio. Your task is to build a three-page dashboard including key metrics and visualizations that aims to show student engagement with the 365 platform and identify critical areas of improvement.

Objective: The following is a list of the questions we want our dashboard to answer:

Which courses are the most watched by students, and how are they rated?

How many students register each month, and what fraction are also onboarded?

How do students engage with the platform (minutes and average minutes watched) based on student type (free-plan or paying)?

Do students watch more content with time, and does it vary seasonally?

Which countries have the most students registered, and does this number scale proportionally with the number of minutes watched per country?

Discuss your findings, uncover valuable insights, and gain meaningful experience working on a real-life database.

## Project requirements

For this Customer Engagement Analysis with SQL and Tableau project, you’ll work with Tableau Public 2022.4 or newer and optionally MySQL Workbench 8.0.

Customer Engagement.twbx – a Tableau workbook containing two pre-loaded data sources

dashboard_skeleton.pdf – a skeleton of the dashboard containing the names of the charts described in the project

365_database.sql – Optional: If you fancy a challenge, you can practice your SQL skills by retrieving the pre-loaded Tableau data sources using the provided SQL database

## Project content

3 Project files

Guided and unguided instructions Up to 10 XP

## Part 1: Sketching the Dashboard

## Part 2: Retrieving Courses Information with SQL

## Part 3: Retrieving Purchases Information with SQL

## Part 4: Retrieving Students Information with SQL

## Part 5: Creating the Table in Tableau

## Part 6: Creating the Charts in Tableau

## Part 7: Creating the KPIs in Tableau

## Part 8: Creating the Dashboard in Tableau

## Part 9: Interpreting the Results

Quiz Up to 25 XP

## Featured tools

## Topics covered

ProgrammingData visualizationRelational DatabasesData Analysis

## Related courses

## To complete this project you need expertise on the following topic(s)

Customer Engagement Analysis with SQL and Tableau

Sketching the Dashboard

Our Customer Engagement Analysis with SQL and Tableau project offers an exceptional opportunity to enhance and expand your professional portfolio. Your task is to build a three-page dashboard—including key metrics and visualizations that aim to show student engagement with the 365 platform and identify critical areas of improvement.

But how do we define engagement on the 365 platform? For this project, we’ll discuss engagement in the following way. Students are engaged on a particular day if they have watched a lecture. Using this definition, let’s introduce one more term: onboarding. Students are onboarded if they have watched a lecture on the 365 platform at least once.

Your goal is to have the following questions answered by the end of this project:

Which courses are the most watched by students, and how are they rated?

How many students register each month, and what fraction are onboarded?

How do students engage with the platform (minutes and average minutes watched) based on student type (free-plan or paid)?

Do students watch more content with time, and does it vary seasonally?

Which countries have the most students registered, and does this number scale proportionally with the number of minutes watched per country?

In the dashboard_skeleton.pdf file, we’ve created a skeleton of the dashboard where you can locate the Charts, Tables, KPIs, and Parameters. For now, you’re only asked to get familiar with the structure of the dashboard. By the end of this project, you’ll have had it constructed in Tableau and then used it to answer the questions posed above.

Charts

## The bar-and-line chart from page 1 should represent the minutes watched

Let the height of the bars communicate the number of minutes watched.

The line should represent the average number of minutes watched.

Visualize the chart monthly.

The left funnel chart from page 2 should visualize the total number of users from a given country:

Display the first five countries with the most significant number of users.

Depict each country as a horizontal bar.

Let the bar length represent the number of students from that country.

Sort the chart in descending order.

The right funnel chart from page 2 should visualize the minutes watched on the platform by users from a given country:

Display the first five countries with the most significant number of minutes watched.

Depict each country as a horizontal bar.

Let the length of the bar represent the minutes watched by each country.

Sort the chart in descending order according to the number of users.

The stacked bar chart from page 3 should represent the number of registered and onboarded users:

Let the height of the bar represent the number of newly registered users.

The number of students in each bar who have also been onboarded should be colored differently so we can visually assess how this number compares to the total number of registered users.

Visualize the chart monthly.

Tables

The five-column table from page 3 should display the top five most watched courses based on total minutes watched:

Let the first column show the courses’ names.

Let the second column show the total number of minutes watched from each course.

Let the third column show the average minutes watched—the total number of minutes divided by the unique number of users who have watched the course.

Let the fourth column show the number of ratings for each course.

Let the fifth and final column show the average rating for each course—the sum of all ratings divided by the number of ratings.

KPIs

The Registered Students field from page 1 must show the number of registered users on the platform.

The Minutes Watched field from page 1 must show the number of minutes watched on the platform.

The Average Minutes Watched field from page 1 must show the number of minutes watched on the platform divided by the number of unique users who have watched.

The Onboarded Students field from page 3 must show the percentage of registered users onboarded out of all registered users.

Retrieving Courses Information with SQL

In this section, your task is to retrieve the data source files imported into the Tableau workbook. You can do this in MySQL by importing the database from the 365_database.sql file and then designing the relevant queries.

Note: The data sources you will extract in this and the following two tasks (Retrieving Purchases Information with SQL and Retrieving Purchases Information with SQL) are already imported into the Customer Engagement.twbx file. These three tasks are not compulsory for completing the project, and you can jump directly to the Creating the Table in Tableau section. Nevertheless, solving them is an excellent opportunity to put your SQL skills into practice and solidify your knowledge on the subject.

Use the tables 365_course_info, 365_student_learning, and 365_course_ratings from the 365_database to retrieve a new table with the following fields:

course_id – the unique identification of a course

course_title – the title of the course

total_minutes_watched – all minutes watched from the course for the entire period

average_minutes – all minutes watched from the course for the entire period divided by the number of students who’ve started the course

number_of_ratings – the number of ratings the course has received

average_rating – the sum of all the course’s ratings divided by the number of students who rated it.

Save the retrieved table as sql-task1-courses.csv

Note: Ensure your final result set consists of 46 rows—the number of courses in the 365_course_info table.

Execute the instructions to complete the task. Remember to replace the question marks with the appropriate values and statements. At each stage, think about the information you have and what you need to calculate. Remember to make use of aggregate functions like SUM, COUNT, and AVG, and be careful with the JOIN operations to ensure you’re combining the tables correctly.

Create a common table expression (CTE) that calculates the total minutes watched and the total number of students for each course. Here, the SQL GROUP BY clause would be helpful to group the data by each course.

Enclose the sub-query within parentheses and prefix it with a WITH clause. Assign the alias title_total_minutes to this temporary result set.

## Note the skeleton of this sub-query

WITH title_total_minutes AS

(

SELECT

course_id,

course_title,

ROUND(SUM(???), 2) AS total_minutes_watched,

COUNT(DISTINCT ???) AS num_students

FROM

???

JOIN

??? USING (course_id)

GROUP BY course_id

),

Create another CTE that calculates the average minutes watched for each course by using the result from the previous step (total_minutes_watched and num_students).

Enclose the sub-query within parentheses and assign the alias title_average_minutes to this temporary result set.

## Note the skeleton of this query

title_average_minutes AS

(

SELECT

course_id,

course_title,

total_minutes_watched,

ROUND(???, 2) AS average_minutes

FROM

???

),

Create a third CTE that calculates the number of ratings and the average rating for each course. Group the data by course. If there are no ratings for a course, the average rating should be 0.

Enclose the sub-query within parentheses and assign the alias title_ratings to this temporary result set.

## Note the skeleton of this query

title_ratings AS

(

SELECT

course_id,

course_title,

total_minutes_watched,

average_minutes,

??? AS number_of_ratings,

??? AS average_rating

FROM

???

LEFT JOIN

??? USING (course_id)

GROUP BY course_id

)

Retrieve the title_ratings result set and save it as sql-task1-courses.csv.

Retrieving Purchases Information with SQL

So far, we’ve studied the dashboard skeleton and created the first of two CSV data source files. Now, using the 365_student_purchases table, create a new SQL query that, when executed, stores in the 365_database schema a view called purchases_info, which we’ll use in subsequent tasks. This view should contain information about the time intervals each student was a paid subscriber to our platform with the following columns:

purchase_id

student_id

purchase_type

date_start (the date the subscription started)

date_end (the date the subscription ended)

To calculate the end date of a subscription (date_end), add one month, three months, or 12 months to the start date of a subscription for a Monthly (represented as 0 in the plan_id column), Quarterly (1), or an Annual (2) purchase, respectively.

Note: Ensure you have 3,041 rows in your purchases_info view—i.e., you’ve found each subscription’s start and end dates.

Execute the instructions below to complete the task. Remember to replace the question marks with the appropriate values and statements.

First, ensure you’ve dropped the purchases_info view before creating it.

DROP VIEW IF EXISTS purchases_info;

CREATE VIEW purchases_info AS

Select specific fields from the 365_student_purchases table. The date_start column is created by renaming the date_purchased column accordingly.

DROP VIEW IF EXISTS purchases_info;

CREATE VIEW purchases_info AS

SELECT

???,

???,

???,

date_purchased AS date_start,

FROM

365_student_purchases;

Calculate date_end, based on date_purchased and purchase_type. You can use a CASE statement for this, with each condition corresponding to a different type of purchase (Monthly, Quarterly, Annual).

DROP VIEW IF EXISTS purchases_info;

CREATE VIEW purchases_info AS

SELECT

???,

???,

???,

date_purchased AS date_start,

CASE

WHEN

purchase_type = 'Monthly'

THEN

???

WHEN

purchase_type = 'Quarterly'

THEN

???

WHEN

purchase_type = 'Annual'

THEN

???

END AS date_end

FROM

365_student_purchases;

Retrieving Students Information with SQL

Great job creating the purchases_info view! Now, use this result together with the 365_student_purchases, 365_student_info, and 365_student_learning tables from the database to retrieve a new temporary result set containing the following fields:

student_id – a list of student IDs

student_country – the country of origin they’ve entered into the platform

date_registered – registration date of the students

date_watched – the date they’ve watched a course

minutes_watched – the minutes they’ve watched from that course on that day

onboarded – whether they have a record in the 365_student_learning table (0 – no, 1 – yes)

paid – whether they’ve had an active subscription on the day of watching the course (0 – no, 1 – yes)

The table should include the daily minutes each student watches for each course. If they have never watched a video, they need only one entry in the table with NULL under date_watched and 0 under minutes_watched.

Save the retrieved result set as sql-task3-courses.csv

Note: The table should have 81,532 rows. Ensure the sum of your minutes_watched column returns the same result as the sum of the minutes_watched column from the 365_student_learning table.

Refer to the instructions below to complete the task.

Create a query that appropriately joins the 365_student_info and the 365_student_learning tables, retrieving all records from the first table. Select all columns from 365_student_info and the date_watched column from the 365_student_learning table. Note that the date_watched column can be NULL if a student from the 365_student_info hasn’t watched any lectures.

SELECT

???,

???

FROM

365_student_info i

???

365_student_learning l USING(???)

Create a column called minutes_watched to calculate the total minutes a student watches daily. Note that if a student hasn’t watched any lectures—i.e., they don’t have any record in the 365_student_learning table—their sum of watched minutes should be 0.

SELECT

???,

???,

IF(??? IS NULL, ???, ???) AS minutes_watched,

FROM

365_student_info i

???

365_student_learning l USING(???)

GROUP BY ???, ???

Create another column called onboarded, evaluated at 0 if a student has no record in the 365_student_learning table. Otherwise, it is 1.

SELECT

???,

???,

IF(??? IS NULL, ???, ???) AS minutes_watched,

IF(??? IS NULL, ???, ???) AS onboarded

FROM

365_student_info i

???

365_student_learning l USING(???)

GROUP BY ???, ???

Use the query you derived as a subquery (aliased a), which you need to appropriately join with the purchases_info view so that all records from a are retrieved. Select all columns from a. Create a new column (call it paid), which is evaluated at 1 if a lecture is watched between the subscription’s start date and the same subscription’s end date. Otherwise, consider it at 0.

SELECT

???,

IF(???) AS paid

FROM

( -- First sub-query

) a

LEFT JOIN

purchases_info p USING (student_id)

Use the query created at step 4 as a new subquery; call it b. Select the first six columns from b. Then, select the maximum value of the paid column for a single student_id – date_watched pair. This would determine if a student was a paid member on the date specified by the date_watched column.

SELECT

???,

...

???,

??? AS paid

FROM

( -- Second sub-query

) b

GROUP BY ???, ???;

Retrieving Students Information with SQL

Great job creating the purchases_info view! Now, use this result together with the 365_student_purchases, 365_student_info, and 365_student_learning tables from the database to retrieve a new temporary result set containing the following fields:

student_id – a list of student IDs

student_country – the country of origin they’ve entered into the platform

date_registered – registration date of the students

date_watched – the date they’ve watched a course

minutes_watched – the minutes they’ve watched from that course on that day

onboarded – whether they have a record in the 365_student_learning table (0 – no, 1 – yes)

paid – whether they’ve had an active subscription on the day of watching the course (0 – no, 1 – yes)

The table should include the daily minutes each student watches for each course. If they have never watched a video, they need only one entry in the table with NULL under date_watched and 0 under minutes_watched.

Save the retrieved result set as sql-task3-courses.csv

Note: The table should have 81,532 rows. Ensure the sum of your minutes_watched column returns the same result as the sum of the minutes_watched column from the 365_student_learning table.

Refer to the instructions below to complete the task.

Create a query that appropriately joins the 365_student_info and the 365_student_learning tables, retrieving all records from the first table. Select all columns from 365_student_info and the date_watched column from the 365_student_learning table. Note that the date_watched column can be NULL if a student from the 365_student_info hasn’t watched any lectures.

SELECT

???,

???

FROM

365_student_info i

???

365_student_learning l USING(???)

Create a column called minutes_watched to calculate the total minutes a student watches daily. Note that if a student hasn’t watched any lectures—i.e., they don’t have any record in the 365_student_learning table—their sum of watched minutes should be 0.

SELECT

???,

???,

IF(??? IS NULL, ???, ???) AS minutes_watched,

FROM

365_student_info i

???

365_student_learning l USING(???)

GROUP BY ???, ???

Create another column called onboarded, evaluated at 0 if a student has no record in the 365_student_learning table. Otherwise, it is 1.

SELECT

???,

???,

IF(??? IS NULL, ???, ???) AS minutes_watched,

IF(??? IS NULL, ???, ???) AS onboarded

FROM

365_student_info i

???

365_student_learning l USING(???)

GROUP BY ???, ???

Use the query you derived as a subquery (aliased a), which you need to appropriately join with the purchases_info view so that all records from a are retrieved. Select all columns from a. Create a new column (call it paid), which is evaluated at 1 if a lecture is watched between the subscription’s start date and the same subscription’s end date. Otherwise, consider it at 0.

SELECT

???,

IF(???) AS paid

FROM

( -- First sub-query

) a

LEFT JOIN

purchases_info p USING (student_id)

Use the query created at step 4 as a new subquery; call it b. Select the first six columns from b. Then, select the maximum value of the paid column for a single student_id – date_watched pair. This would determine if a student was a paid member on the date specified by the date_watched column.

SELECT

???,

...

???,

??? AS paid

FROM

( -- Second sub-query

) b

GROUP BY ???, ???;

Creating the Charts in Tableau

Great job on completing one of the visualizations entering the dashboard. Your next task is to use the sql-task3-students.csv data source to construct the following funnel, combo, and stacked bar charts.

Total Number of Registered Students (Funnel Chart)

Create the left funnel from page 2 displaying the total number of registered students by country.

Display the first five countries with the most significant number of users.

Depict each country as a horizontal bar.

Let the bar length represent the number of students from that country.

Sort the chart in descending order.

Create and apply a registration month parameter and a user-type parameter (Free, Paid, or Both).

Use the following instructions to carry out the task.

Create a horizontal bar chart that shows the number of users from each country. The first step is to drag the Student Country pill to the Rows shelf. Ensure the Student Id field is under Measures and drag it to the Columns shelf selecting the COUNTD function.

Sort the chart by the number of students in descending order.

Display only the top five countries by the number of students.

To construct the registration month parameter, create a custom date that only includes the month of the registration date.

Next, create a Registration Month parameter that uses the Date Registered (Months) custom date. Ensure the Data type is Date, and the Display format is Custom (mmm yy).

To establish the connection between the parameter and the funnel chart, create a calculated field, Registration Date Filter, which ensures that the Date Registered (Months) custom date equals the value of the Registration Month parameter.

Drag the Registration Date Filter calculated field to the Filters shelf and select True.

Right-click the Registration Month parameter and select Show Parameter. For convenience, change its type to a Slider, and ensure it works as expected.

To construct the user-type parameter, create a new parameter of an integer data type and make a list of allowable values:

0 – Representing Free-plan students (aliased Free)

1 – Representing Paying students (aliased Paid)

2 – Representing both types of students (aliased All)

Ensure the current value is different from All, which will be helpful in the final step.

Next, create a calculated field connecting the parameter and the funnel chart.

Finally, drag the User Type Filter calculated field to the Filters shelf and select True—had the parameter’s Current value been All, the False option would not have appeared. Show the User Type parameter and make sure it works as expected.

Total Number of Minutes Watched (Funnel Chart)

Create the right funnel from page 2 displaying the total number of minutes watched by country.

Display the first five countries with the most significant minutes watched.

Depict each country as a horizontal bar.

Let the length of the bar represent the minutes watched by each country.

Sort the chart in descending order according to the number of users.

Create and apply a registration month and a user-type parameter (Free, Paid, or Both).

To complete the task, follow the instructions below.

Analogously, create a horizontal bar chart that shows the number of minutes watched from each country. The first step is to drag the Student Country pill to the Rows shelf and the SUM of the Minutes Watched measure to the Columns shelf. Right-click on the Student Country pill to sort the chart by the total number of minutes watched in descending order.

Display only the top five countries by the number of minutes watched.

Drag the Registration Date Filter and the User Type Filter calculated fields to the Filters shelf and select True in both cases. Then, show the corresponding parameters on the screen and make sure they work as expected.

Total Number of Minutes and Average Minutes Watched (Combo Chart)

Create the combo chart displaying the total number of minutes watched (bar chart) and the average number of minutes watched (line chart) monthly. Apply a student-type parameter (Free, Paid, or Both).

To complete the task, follow the instructions below.

Create a bar chart with 12 bars, each representing a different month of the year. Drag the month of the Date Watched pill to the Columns shelf. Right-click on the pill and ensure it’s a Discrete field.

Drag the Minutes Watched pill to the Rows shelf. By default, the function Tableau will apply is the SUM function. Change the type of chart to a bar chart. The height of the bars now represents the number of minutes watched during a given month.

Create a pill in the Rows shelf that sums the Minutes Watched field and divides it by the distinct count of the Student Id field. Change the type of chart to a line chart. You’ve now created a chart whose values represent the average minutes watched in a given month.

To overlay the two charts, right-click on the

y

y

-axis of the line chart and select Dual Axis. Alternatively, right-click on the second pill in the Rows shelf and select Dual Axis.

Drag the User Type Filter calculated field to the Filters shelf and select True. Then, show the corresponding parameter on the screen and make sure it works as expected.

Fraction of Onboarded Students (Stacked Bar Chart)

## Create the stacked bar chart as follows

Let the height of the bar represent the number of newly registered users.

The number of students in each bar who have also been onboarded should be colored differently so we can visually assess how this number compares to the total number of registered users.

Visualize the chart monthly.

Refer to the instructions below to complete the task.

Place the distinct count of students onto Rows as a continuous measure.

Place the date of registration onto Columns as a discrete month.

Ensure the type of visualization is a bar chart.

Ensure the Onboarded pill is under Dimensions and drag it onto the Color mark to color the portion of registered and onboarded students.

Drag the distinct count of students onto the Label property.

Right-click on the field dragged in the previous step and select Add Table Calculation.

Represent the count as Percent of Total, computed using Cell—thereby displaying the onboarded and not-onboarded students as a percentage of all registered users in a month.

Creating the KPIs in Tableau

You’re making significant progress and are one task away from combining all visualizations into a three-page dashboard. You’re now tasked with creating four key performance indicators (KPIs) using the sql-task3-students.csv data source.

Number of Registered Students

Create the KPI displaying the number of registered students. Apply registration start- and end-date parameters and a student-type parameter (Free, Paid, or Both).

To complete the task, follow the instructions below.

Drag the distinct count of students onto the Text property.

Create a parameter and a calculated field that filters out between Free, Paid, and Both types of students.

Create two parameters: one sets the minimum registration date (call it Start Date), and another establishes the maximum (call it End Date). Create a calculated field (call it Registration Date Filter 2) that connects the parameters and the data source. Then drag the calculation to the Filters shelf and select True.

Number of Minutes Watched

Create the KPI displaying the number of minutes watched on the platform. Apply date start and end parameters for the date watched and a student-type parameter (Free, Paid, or Both).

Use the following insrtuctions to carry out the task.

Drag the sum of all minutes watched onto the Text property.

Drag the User Type Filter calculated field to the Filters shelf and select True. Show the User Type parameter on the screen and make sure it works as expected.

Use the Start Date and End Date parameters to create a filter that confines the watch date. To do that, create a new calculated field (Date Watched Filter) that connects the two parameters and the data source. Then drag that calculation to the Filters shelf and select True. Show the parameters on the screen and ensure they work as expected.

Average Number of Minutes Watched

Create the KPI displaying the average number of minutes watched on the platform. Apply date start and end parameters for the date watched and a student-type parameter (Free, Paid, or Both).

To complete the task, follow the instructions below.

Drag the sum of all minutes watched divided by the distinct count of students onto the Text property.

Drag the User Type Filter calculated field to the Filters shelf and select True. Show the User Type parameter on the screen and make sure it works as expected.

Drag the Date Watched Filter calculated field to the Filters shelf and select True. Show the Start Date and End Date parameters on the screen and make sure they work as expected.

Percentage of Onboarded Students

Create the KPI displaying the percentage of onboarded students from registered ones.

Refer to the instructions below to complete the task.

Create a calculated field called Onboarded Students and include the following formula:

COUNTD(IF [Onboarded] = 1 THEN [Student Id] END)/COUNTD([Student Id])

The numerator of this expression, COUNTD(IF [Onboarded] = 1 THEN [Student Id] END), counts the students who have been onboarded on the 365 platform. The denominator, COUNTD([Student Id]), counts the distinct number of students on the platform.

Drag the calculated field onto the Text property.

Creating the Dashboard in Tableau

Excellent work! Now that you’ve created the table, all four charts, and the four KPIs, you’re ready to combine all nine visualizations into a three-page dashboard according to the dashboard sketch.

For this part, you’ll be given guidance only on constructing the first page of the dashboard. You’ll then build the other two pages similarly, adhering to the dashboard skeleton file and the instructions below.

Create the Item Hierarchy

The first part of creating a dashboard is determining what item hierarchy to implement. Creating a good order and organizing your elements in containers would make aligning them in the dashboard much easier later.

## We see on this first page three distinct elements arranged vertically

The title of the page, together with three navigation buttons

KPIs and parameters to their left

A combo chart.

Therefore, we’ll first place a container storing three elements vertically. But what would they be? We can see that the topmost and middle parts contain elements arranged horizontally. The top has the title and the buttons placed one next to each other. The same applies to the parameters and KPIs in the second vertical element. This first vertical container will, therefore, store two horizontal ones.

The bottom element is a single combo chart. Here, we can choose between putting the chart at the bottom or placing it inside a vertical or a horizontal container. I’ve set the combo chart inside a horizontal container.

All right, let’s concentrate on the top horizontal container. It stores a text object and then three navigation buttons that seem to be distributed evenly within a separate horizontal container. This container will, therefore, contain a text object and another horizontal container, which, in turn, will keep the navigation buttons.

Then, we have the second horizontal container storing parameters and three KPIs from left to right. Notice that vertical is the most optimal way to arrange each element. All three parameters (Start Date, End Date, User Type) will be set vertically, and all three KPIs will also have a vertical arrangement, with the title at the top and the value at the bottom.

Our item hierarchy is now clear. We can proceed with realizing it in Tableau.

Arrange the Dashboard According to Hierarchy

Next to the worksheets containing all visualizations, create a new dashboard, and call it Page 1. Change its size to a Generic Desktop (1366

×

×

768). Ensure you’re working with a Floating layout and drag a vertical container onto the screen.

Resize it to have the exact dimensions we’ve given our dashboard and position it at coordinates

x

x

and

y

y

equal to zero.

Next, place three horizontal containers on top of each other inside this vertical container. Pressing Shift while dropping the elements makes finding and positioning them easier. Ensure the item hierarchy looks as expected.

Give the top horizontal container a height of 130 pixels. Then, place a text object and a horizontal object inside. Give this second horizontal object a width of 430 pixels.

Inside the horizontal object, place three navigation buttons. Distribute their contents evenly within the container.

Next, proceed with the second horizontal object inside the vertical container, where we’ll store the parameters and the KPIs. First, ensure you evenly distribute four vertical containers inside the horizontal one. Change the height of the horizontal container to 200 pixels.

Place a text object inside the second, third, and fourth containers. Style them to your liking.

Place the sheet displaying the respective KPI below each text object.

You might’ve noticed that the bottom horizontal container—which we reserved for the combo chart—now stores the parameters of these KPIs. Tableau positioned them there while we needed them in the leftmost vertical container inside the second horizontal object. So, we need to drag the parameters and place them in their desired position.

Finally, place the combo chart in the bottom horizontal container. Note that the container might’ve disappeared after we removed all its parameters. But don’t worry, add it again. Remove all unnecessary legends that might’ve appeared after introducing the combo chart to the dashboard.

Style Your Dashboard

Stylize the dashboard professionally in a way that you find best. What you see in the PDF file suggests how it could look. But feel free to experiment.

Configure the Buttons to Navigate to Different Pages

Once you’ve created all three dashboard pages, configure the buttons of each page to lead to the respective place—configuring nine navigation buttons in total.

Interpreting the Results

The dashboard turned out great! You’re now at the final and critical task of analyzing the results. Please return to the questions we posed at the beginning of the project. Using the dashboard you created, how would you answer each of them, and what conclusions can you draw?

Which courses are the most watched by students, and how are they rated?Hint: Use the table you created in Tableau to answer this question.

How many students register each month, and what fraction are also onboarded?Hint: Use the Registered Students’ and Onboarded Students’ KPIs and the stacked bar chart you created in Tableau to answer this question.

How do students engage with the platform (minutes and average minutes watched) based on student type (free-plan or paying)?Hint: Use the Minutes Watched and Average Minutes Watched KPIs you created in Tableau to answer this question.

Do students watch more content with time, and does it vary seasonally?Hint: Use the combo chart you created in Tableau to answer this question.

Which countries have the most students registered, and does this number scale proportionally with the number of minutes watched per country?Hint: Use the funnels you created in Tableau to answer this question.

## Quiz

## Question 1

Using the table you created in Tableau, which is the second course with the most minutes watched on the platform?

SQL

Statistics

Introduction to Data and Data Science

Python Programmer Bootcamp

## Question 2

Use one of the funnels you created, with the user type parameter set to All, and locate the country with the most registered students in August 2022. What is the approximate number of these students?

300

500

700

1000

## Question 3

Employ one of the funnels you created, with the registration month parameter set to September and the user type parameter to All. Which is the fifth topmost country with the most representatives on the platform?

United States

India

Nigeria

Canada

## Question 4

Using one of the funnels you created, which country has the highest number of minutes watched by free-plan students registered in July?

United States

India

Nigeria

Canada

## Question 5

Utilizing one of the funnels you made, which country has the highest number of minutes watched by paying students registered in July?

United States

India

Nigeria

Canada

## Question 6

Using the monthly combo chart you created, which of the following comes closest to the highest average number of minutes watched by paying students?

190

230

290

310

## Question 7

Using the monthly combo chart you created, which of the following comes closest to the highest number of minutes watched by free-plan students?

41,000

146,000

172,000

319,000

## Question 8

Using the stacked bar chart you created, which month has the lowest onboarding rate?

April

May

June

July

## Question 9

Using the KPIs you created, what is the approximate onboarding rate on the platform?

0.25

0.3

0.45

0.5

## Question 10

How much more do paying students watch compared to free-plan ones? Considering the entire analysis period and the ‘average minutes watched’ KPI, what is the approximate value of the following fraction?
