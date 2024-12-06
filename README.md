Link to streamlit app: tornado.streamlit.app

----- OVERVIEW -----
Tornados have changed a lot over the years.  We are better able to track them, assess their damages, and importantly assess how they are changing.  Many
people are aware of the destruction of Tornado Alley, but not everyone may be so cognizent on how the geographic tornado hotspot has shifted east recently.
Using our website, citizens of the US can analyze their geographic area over desired periods of time and see how tornados have impacted their communities.
We provide a host of information about fatalities, destruction, and frequency based on metrics of time, population size, and geographic area.  Utilizing these
features, in addition to insights we hand chose to provide, can give citizens a better understanding of the history of tornados and what might be in store for
them moving forward such as changes in frequency, changes in safety, and changes in destruction.


----- DATA DESCRIPTION -----
The main data we used came from the NOAA's National Weather Service (https://www.spc.noaa.gov/wcm/#data)
This data contained every recorded instance of a tornado from 1950 to 2023, with each row represented as a certain tornado in a given US county (meaning a tornado
that stretched multiple counties would be recorded as several rows), and different columns provided details such as an id, state affected, county affected, magnitude,
damages, fatalities, injuries, and many others.
-- Cleaning the data: --
  Technology greatly improved over time, and so did the methodology of reporting tornado information.  Even though our measurements were improved, we couldn't go
back in time to change them, so, for example, damages were represented differently before 1996 than they were after.  Our team came up with ways to best convert
pre-1996 data to something comparable to the estimates made today.  Other values changed slightly such as updating a few time values that were not successfully 
converted to CST, but for the most part column values were well taken care before downloading.
  We did have to aggregate our data though.  We excluded certain column values we didn't care about, and then grouped together tornados by a unique ID and the state
they were in.  This has its pros and cons.  For most every tornado case, this became more accurate.  Its easier to understand different instances of tornados, you
can see their total damages through counties, and you only lose some information such as a "progress check" that shows at what time it moved into a new county, for
example.  The big drawback comes to potential user confusion when looking at state by state data when a tornado, particuarly a massive/deadly/costly one, moves
across state lines.  Without the state aggregation, the damages in two states would only be counted in one, so one state would be seen as overstated in damage and
the other understated.  With the aggregation, this over/understatement is fixed, but users may wrongly conclude that a single damaging torando was instead
two separate instances of slightly less damaging tornado.  Although this may be an unlikely occurance, we found instances of these while testing out data.
-- Additional information appended: --
  We added additional information to give further insight into analysis.  We used CPI data from the St. Louis FRED to make inflation adjusted damage amounts so
historical damages could be better compared.  We also added in population per state for a given year along with the area of states found from Wikipedia.  
This allowed us to make new information such as a variable per x residents, x square miles, and compare that from year to year.  Examples of the benefits of these
could be that total deaths have increased, but when looking at changes in population, less people are dying proportionally.  As well, some states may seem like
a tornado hotspot, like Texas, but when adjusting for their massive land area, it is less severe.


----- Algorithm Description -----
No algorithms were used for this project beyond implmentation of cleaning, merging, and aggregating as explained above.


----- TOOLS USED -----
  The project's tools can be broken into two categories: running the streamlit app, and creating the data used for analysis.
-- Running Streamlit: --
  Backblaze to store tornado information
  Botocore for exceptions
  Dotenv and utils.b2
-- Creating the tornado data: --
  Pandas for data manipulation, much of which has been explained above.
  MatPlotLib and Seaborn for standard two dimentional plots comparing two variables.
  Folium to create map visualization.


----- ETHICAL CONCERNS -----
  Perhaps the only significant ethical concern is going to come from estimates and changes in technology.  More information is presented as a page on our website.
There are a lot of limiations when it comes to tornado collection, even more so historically.  Before Doppler radar and satelite imaging, people needed to verify
tornados, and alternative approaches were limited.  Even today, some manual verification is still needed.  Users may think that tornado frequency is changing
substantially over time, but in reality the only thing changing might just be our technology to track tornados.
  Other similar issues arise when looking at how tornados are classified, damages, wind speed, etc.  Things that would have had precendent for being labeled one
way may no longer be as new technology can disprove assumptions.  Its possible that a tornado fifty years ago could have very different metrics in terms of category,
wind speed, duration, and lengh if it appeared today.
  If we didn't provide these details, or perhaps a warning as to the estimates we used, users may assume everything we are providing is strictly factual, which its
not.  It is the most reliable data set available, and its certainly not useless, but strict statistical analysis or finding small changes over time may not be
applicable, and any attempt to do so will be doomed to provide an innaccurate finding.  This is the reason we will be providing some external information in our
website warning users that the figures they see are estimates, and fortunately in this area we are not giving any sort of recommendation in terms of how users
should conduct their life or changes in policies.  We are simply giving users enchanced information for their own research and curiousity, so concerns that this
will mislead and create negative implications on people's lives is not likely, let alone potentially severe.



