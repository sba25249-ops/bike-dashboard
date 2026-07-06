import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('Fremont Bridge Bicycle Counter Dashboard')

st.write(
    'This app shows bike traffic crossing the Fremont Bridge in Seattle, '
    'so you can see the best (and busiest) times to cycle.'
)

DATE_COLUMN = 'Date'
DATA_URL = 'fremont_bridge_cleaned.csv'

@st.cache_data
def load_data():
    data = pd.read_csv(DATA_URL)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text('Done! (using st.cache_data)')

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Average bicycles by hour of day')
hourly_avg = data.groupby('Hour')['Total'].mean()
st.bar_chart(hourly_avg)

st.subheader('Pick an hour to check')
hour_to_filter = st.slider('Hour of day', 0, 23, 8)

filtered_data = data[data['Hour'] == hour_to_filter]

st.write(
    f"Average bicycles at {hour_to_filter}:00 is about",
    round(filtered_data['Total'].mean())
)

st.subheader('Average bicycles by day of the week')

day_order = [
    'Monday', 'Tuesday', 'Wednesday',
    'Thursday', 'Friday', 'Saturday', 'Sunday'
]

day_avg = data.groupby('DayName')['Total'].mean().reindex(day_order)

fig, ax = plt.subplots()
ax.bar(day_avg.index, day_avg.values)
ax.set_xlabel('Day')
ax.set_ylabel('Average bicycles')
ax.set_title('Average bicycles by day of the week')
plt.xticks(rotation=45)

st.pyplot(fig)

st.subheader('Weekday vs weekend')

show_weekends = st.checkbox('Show weekends only (untick for weekdays only)')

if show_weekends:
    day_type_data = data[data['IsWeekend'] == True]
else:
    day_type_data = data[data['IsWeekend'] == False]

st.write('Average bicycles per hour:', round(day_type_data['Total'].mean()))

st.subheader('Bicycles over the year')

year_to_filter = st.slider(
    'Year',
    int(data['Year'].min()),
    int(data['Year'].max()),
    int(data['Year'].max())
)

year_data = data[data['Year'] == year_to_filter]

daily_totals = year_data.set_index(DATE_COLUMN)['Total'].resample('D').sum()

st.line_chart(daily_totals)