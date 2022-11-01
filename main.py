import streamlit as st
import pandas as pd
import helper
import preprocessor
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)
st.sidebar.title("Olympics Analysis")
st.sidebar.image("olympics.jpeg")
user_menu = st.sidebar.radio(
    "Select an option",
    ("Medal Tally", "Overall Analysis", "Country Wise Analysis", "Athlete wise analysis")
)

# st.dataframe(df)

if user_menu == "Medal Tally":
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    if selected_year == "Overall" and selected_country == "All":
        st.title("Overall Tally")
    elif selected_country == "All":
        st.title(f"Medal Tally in {selected_year}")
    elif selected_year == "Overall":
        st.title(f"Medal Tally of {selected_country}")
    else:
        st.title(f"Medal Tally of {selected_country} in {selected_year}")
    st.table(medal_tally)

elif user_menu == "Overall Analysis":
    editions = df["Year"].nunique() - 1
    cities = df["City"].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes = df['Name'].nunique()
    nations = df['region'].nunique()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)

    with col2:
        st.header("Hosts")
        st.title(cities)

    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)

    with col2:
        st.header("Nations")
        st.title(nations)

    with col3:
        st.header("Athletes")
        st.title(athletes)

    nation_over_time = helper.data_over_time(df, 'region')
    st.title("Participation Countries over the year")
    fig = px.line(nation_over_time, x="Edition", y='region')
    fig.update_layout(
        margin=dict(t=25, l=25, b=25, r=25),
        autosize=False,
        width=1400,
        height=800,
    )
    st.plotly_chart(fig)

    event_over_time = helper.data_over_time(df, 'Event')
    st.title("Events over the year")
    fig = px.line(event_over_time, x="Edition", y='Event')
    fig.update_layout(
        margin=dict(t=25, l=25, b=25, r=25),
        autosize=False,
        width=1400,
        height=800,
    )
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')
    st.title("Athletes over the year")
    fig = px.line(athletes_over_time, x="Edition", y='Name')
    fig.update_layout(
        margin=dict(t=25, l=25, b=25, r=25),
        autosize=False,
        width=1400,
        height=800,
    )
    st.plotly_chart(fig)

    st.title("No. of Events over years(Every Sports)")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', "Sport", "Event"])
    ax = sns.heatmap(x.pivot_table(index="Sport", columns="Year",
                                   values='Event', aggfunc='count').fillna(0).astype(int), annot=True)
    plt.xticks(rotation=45)

    st.pyplot(fig)

    st.title("Most Successful Athlete")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, "Overall")
    selected_sport = st.selectbox("Sport", sport_list)

    x = helper.most_successful(df, selected_sport)
    st.table(x)

elif user_menu == 'Country Wise Analysis':

    st.sidebar.title("Country Wise Analysis")
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox("Select a Country", country_list)

    medal_list = ['All', "Gold", "Silver", "Bronze"]
    selected_medal_type = st.sidebar.selectbox("Choose Medal", medal_list)

    country_df = helper.yearwise_medal_tally(df, selected_country, selected_medal_type)
    st.title(selected_country + " medal Tally over the year")
    fig = px.line(country_df, x="Year", y=selected_medal_type)
    fig.update_layout(
        margin=dict(t=25, l=25, b=25, r=25),
        autosize=False,
        width=1400,
        height=800,
    )
    st.plotly_chart(fig)

    st.title(selected_country + " excels in following sports")
    pt = helper.country_event_heatmap(df, selected_country, selected_medal_type)
    fig, ax = plt.subplots(figsize=(20, 20))

    ax = sns.heatmap(pt, annot=True, annot_kws={"size": 16})
    st.pyplot(fig)

    st.title("Top Athletes in " + selected_country)
    top_df = helper.most_successful_athletes_in_country(df, selected_country)
    st.table(top_df)

elif user_menu == "Athlete wise analysis":
    athlete_df = df.drop_duplicates(subset=["Name", 'region'])

    overall = athlete_df['Age'].dropna()
    gold_medalist = athlete_df[athlete_df['Medal'] == "Gold"]['Age'].dropna()
    silver_medalist = athlete_df[athlete_df['Medal'] == "Silver"]['Age'].dropna()
    bronze_medalist = athlete_df[athlete_df['Medal'] == "Bronze"]['Age'].dropna()

    fig = ff.create_distplot([overall, gold_medalist, silver_medalist, bronze_medalist],
                             ["Overall", "Gold Medalist", "Silver Medalist", "Bronze Medalist"], show_hist=False,
                             show_rug=False)
    fig.update_layout(
        margin=dict(t=25, l=25, b=25, r=25),
        autosize=False,
        width=1400,
        height=800,
    )
    st.title("Age Distribution of Athletes")
    st.plotly_chart(fig)

    famous_sport = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics', 'Swimming', 'Badminton', 'Sailing',
                    'Gymnastics', 'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling', 'Water Polo', 'Hockey',
                    'Rowing', 'Fencing', 'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing', 'Tennis',
                    'Golf', 'Softball', 'Archery', 'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                    'Rhythmic Gymnastics', 'Rugby Sevens', 'Beach Volleyball', 'Triathlon', 'Rugby', 'Lacrosse', 'Polo',
                    'Ice Hockey']

    x = []
    name = []
    for sport in famous_sport:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df["Medal"] == "Gold"]['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)

    fig.update_layout(
        margin=dict(t=25, l=25, b=25, r=25),
        autosize=False,
        width=1400,
        height=800,
    )
    st.title("Age Distribution of Athletes wrt sport")
    st.plotly_chart(fig)

    st.title("Height Vs Weight")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, "Overall")
    selected_sport = st.selectbox("Sport", sport_list)

    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()

    ax = sns.scatterplot(x=temp_df["Weight"],
                         y=temp_df["Height"],
                         hue=temp_df["Medal"],
                         style=temp_df['Sex'],
                         s=20, alpha=0.7)
    st.pyplot(fig)

    st.title("Men Vs Women Participation over the Years")

    selected_sport_in_men_vs_women = st.selectbox("Choose Sport", sport_list)

    final = helper.men_vs_women(df, selected_sport_in_men_vs_women)
    fig = px.line(final, x="Year", y=['Male', "Female"])
    fig.update_layout(
        margin=dict(t=25, l=25, b=25, r=25),
        autosize=False,
        width=1400,
        height=800,
    )
    st.plotly_chart(fig)