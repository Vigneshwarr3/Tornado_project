import streamlit as st

# creates webpage to explain the data and assumptions
st.title("Extra information for our project and our data")

# our project
st.header("About our project")
st.write("This is our final project for INFO H-501.  In this project, we were tasked with creating \
        a Streamlit app that serves a social or human-centered purpose.  We chose to explore tornados \
        and provide a webpage that allows users to have customizable querying to see how tornados \
        have changed over time.")
# put a link in here
st.write("Here is a link to our GitHub for this project: https://github.com/Vigneshwarr3/Tornado_project")
st.write("We hope you enjoy this project!  If there are any problems, comments, or additional features \
        you'd like for us to add, please reach out to us on GitHub!")

# for the tornados
st.header("About our data")
st.write("Our data comes from  NOAA's National Weather Service (https://www.spc.noaa.gov/wcm/#data) \
        and has tornado information \
         from 1950-2023.  We also pulled additional information such as CPI from the St. Louis FRED \
         for inflation measurements, and information like state population and area sizes \
         from Wikipedia.  There are limitations in our data, along with certain ways to interpret \
         the data that we will include below.")

st.subheader("Population")
st.write("Population data for the US is collected every decade as a census.  Apart from the inherent \
         limitations of a census at this scale, we had to estimate the population growth between \
         censuses.  We decided to fill in these missing years by using linear interpolation.  This \
         will help smooth the growth over years so you don't see jumps or dips in certain \
         visualizations, but obviously these values are estimates.")

st.subheader("Damage")
st.write("Since this data began in 1950, the technology we have to make more accurate estimates \
         for individual tornado damages has increased.  Before 1996, damage was measured \
         logarithmically.  Specifically, it was recorded as an integer n where n is between \
         5*10^(n) and 5*10(n+1).  This posed a serious problem when it came to making estimates.")
st.write("If we knew damage from a tornado was between $5m and $50m, what number do we use?  \
         This is a very big range, and choosing a value too low or too high can distort our data.  \
         We tried many ways to make an 'average' or 'middle' number to use, some of which \
         were finding the average area under the exponential curve or using the middle damage \
         value in the range.  We ended up estimating the damages using a magnitude of n + 0.5.  \
         So if the value was between $5m and $50m, or 5*10^(n) and 5*10(n+1), we estimated the \
         damage as 5*10^(n+0.5).")
st.write("Obviously, these are all just estimates.  The actual values will never be known.  Data \
         collected after 1996 are just estimates as well.  If the differences are orders of \
         magnitude apart, there may be a difference beyond approximation differences.  However, if \
         certain values are close together, there may not be much statistically significant differences.")

st.subheader("Inflation")
st.write("All inflation data was gathered from the St. Louis FRED in September 2024.  Likewise, \
         we chose to create the base inflation period as 8/24.  All adjusted damage amounts are \
         adjusted to the equivalent monetary value of this period.")
st.write("This is an imperfect metric.  Beyond the imperfections of CPI for US Household Goods, \
         tornados destroy more than simple household goods.  Using alternative inflation metrics \
         such as changes in residential properties yielded similar magnitudes in adjustments, but had \
         considerable less historical information to use.  Although some benefit could have been gained \
         looking at property inflation instead of a more generalized inflation, we made the decision to \
         stick with CPI.")

st.subheader("Tracking tornados and technology")
st.write("Tracking tornados is an imperfect science, but an improving one.  When our data began \
         collection in 1950, there were major reporting and recording networks in a handful of states \
         near tornado alley.  As time and technology improved, we began recording more tornados across \
         the country.  This especially improved thanks to advances in Doppler radar and satellite \
         imaging.  These major advances became commonplace in the 1990s, so one might assume \
         that there was less under-reporting of tornados during and after the 1990s.")
st.write("Even with these technological improvements, they are not perfect.  We rely greatly \
         on live reporters to verify tornado existence, and the quality of such can \
         vary over time and location.")

st.subheader("Technology increases and comparisons")
st.write("We have shared some notable limitations to our data and how to best interpret some \
         estimates presented.  This is not an exhaustive list though.  As technology improves, \
         there runs risks of over-reporting tornados, classification definitions can become \
         outdated and make long term comparisons tricky, and many other small changes can create \
         small, but compounding differences to new data that makes comparison less and less accurate.  \
         Don't let this fool you though, there is a lot of information that can still be gleaned \
         despite its shortcomings, and I hope you enjoy exploring the data and learning things \
         about tornados in the US you might not have known!")
