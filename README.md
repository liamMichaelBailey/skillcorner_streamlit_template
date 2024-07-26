# Skillcorner Vizualisation Tool

A tool that allows users to create visualizations through an intuitive user interface,
enabling effortless data exploration and presentation. Users can build charts, graphs,
and tables without coding, making complex data insights accessible and visually appealing
for informed decision-making.

## How to Run the Application

Having opened the relevant project through your IDE, open the terminal and run the command 'streamlit run main.py'.
This will open a localhost environment through your web-browser and allow you to access the application. 

## How to Deploy the Application

Once having ran the application, on the upper-right of the page there will be a 'Deploy' button. 
Click on this button and follow the further instructions that are displayed. 

# Instructions to use the Skillcorner Vizualisation Tool

## 1) Logging In

To log in to the app enter your SkillCorner API credentials into the username & password fields on the
sidebar. The username & password are the same as used to access the SkillCorner Web
Query Tool. Once successfully authenticated, the user’s competition edition (competition & season
combination) access will be displayed in the sidebar.

## 2) Requesting the Data

The first step of using the tool is to request the data for the desired competition & season.
The application will request the data at match by match performance level with a minimum
performance duration threshold of 30 minutes. Once the request is complete the data can be grouped
& filtered into player, team & competition benchmarks.

## 3) Grouping and Filtering the Data

Once the match by match performance data is returned from the API, the user can group the data into
player, team or competition level benchmarks. Use the “group data by” field to aggregate the
data at the desired level (this can be changed at any time). Some common data groupings are below:

● player, team, group → data by player in high level positional groups (Hakimi playing in the full
back group).

● player, team, position → data by player & positions (E.g. Hakimi playing in the RWB position).

● team, competition → data by team in each competition (E.g. PSG playing in Ligue 1)

● team, group → data by team in each positional group (E.g. PSG Midfield average)

● competition → data by competition (E.g. Ligue 1 average)

● competition, group → data by competition & positional group (E.g. Ligue 1 Full Back average)

After grouping the data, the user can filter the sample on various conditions. To do so select
group in the 'filter data' column & then the positions that need to be analysed. Data can be filtered by 
fields such as group, position, player birthdate, team, competition & the number of events in the benchmark sample.

## 4) Plotting the Data

Following the data being grouped & filtered to create a sample of benchmarks it can be plotted in
four different types of charts: scatter plot, bar chart, summary table, and radar plot. Each chart is generated in a similar
fashion & can be downloaded as a high resolution PNG file. To start the user selects a metric to rank the
players by from the 'select metric' drop down menu. The text edit field to the right allows the user
to edit the label that will be plotted on the chart. By default the metric label will be the standard
metric name.

All the chart types include options to highlight particular data points of interest. A text value
can be selected that will be used to label data points. Usually the label would be player_name,
short_name, team_name or competition_name depending on how the data is organised. The bar plot
has two further options to highlight data points in SkillCorners primary or secondary green colours.

For each plot additional formatting options can be toggled on/off. There are options to rotate the plot
to use vertical bars, add each data point’s value as text to the end of the bar & include information of the data sample.

Lastly, when the user has selected all of their data points and formatting options, the 'Create Plot' button
should be pressed to create the user's plot.

Note this is an adhoc dashboard with the aim to support a small group of users to quickly visualise SkillCorner. 
If something more powerful & substantial is required we are happy to investigate options.
