def medal(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', "Games", "Year", "City", 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('NOC').sum()[['Gold', "Silver", "Bronze"]].sort_values('Gold',
                                                                                             ascending=False).reset_index()
    medal_tally["total"] = medal_tally["Gold"] + medal_tally["Silver"] + medal_tally["Bronze"]
    medal_tally['Gold'] = medal_tally['Gold'].astype("int")
    medal_tally['Silver'] = medal_tally['Silver'].astype("int")
    medal_tally['Bronze'] = medal_tally['Bronze'].astype("int")
    medal_tally['total'] = medal_tally['total'].astype("int")

    return medal_tally


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    countries = df['region'].dropna().unique().tolist()
    countries.sort()
    countries.insert(0, "All")

    return years, countries


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', "Games", "Year", "City", 'Sport', 'Event', 'Medal'])
    if year == "Overall" and country == "All":
        temp_df = medal_df
        x = temp_df.groupby('region').sum()[['Gold', "Silver", "Bronze"]].sort_values(['Gold', 'Silver', 'Bronze'],
                                                                                      ascending=False).reset_index()
    elif year == "Overall":
        temp_df = medal_df[medal_df['region'] == country]
        x = temp_df.groupby('Year').sum()[['Gold', "Silver", "Bronze"]].sort_values('Year').reset_index()
    elif country == "All":
        temp_df = medal_df[medal_df['Year'] == year]
        x = temp_df.groupby('region').sum()[['Gold', "Silver", "Bronze"]].sort_values(['Gold', 'Silver', 'Bronze'],
                                                                                      ascending=False).reset_index()
    else:
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]
        x = temp_df.groupby('region').sum()[['Gold', "Silver", "Bronze"]].sort_values(['Gold', 'Silver', 'Bronze'],
                                                                                      ascending=False).reset_index()
    x["Gold"] = x["Gold"].astype(int)
    x["Silver"] = x["Silver"].astype(int)
    x["Bronze"] = x["Bronze"].astype(int)
    x["total"] = x["Gold"] + x["Silver"] + x["Bronze"]
    return x


def data_over_time(df, col):
    nation_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('index')
    nation_over_time.rename(columns={'index': 'Edition', 'Year': col}, inplace=True)
    return nation_over_time


def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != "Overall":
        temp_df = temp_df[temp_df["Sport"] == sport]

    temp_df = \
        temp_df["Name"].value_counts().reset_index().head(15).merge(df, left_on="index", right_on="Name", how="left")[
            ["index", "Name_x", "Sport", "region"]].drop_duplicates('index')
    temp_df.rename(columns={'index': "Name", "Name_x": 'Medals'}, inplace=True)
    temp_df.reset_index(drop=True, inplace=True)
    return temp_df


def yearwise_medal_tally(df, country, medal):
    temp_df = df.dropna(subset=["Medal"])
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    new_df = temp_df[temp_df["region"] == country]
    if medal != "All":
        final_df = new_df.groupby("Year").sum()[medal].reset_index()
    else:
        final_df = new_df.groupby("Year").count()["Medal"].reset_index()
        final_df.rename(columns={"Medal": medal}, inplace=True)
    return final_df


def country_event_heatmap(df, country, medal):
    temp_df = df.dropna(subset=["Medal"])
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    new_df = temp_df[temp_df["region"] == country]
    if medal != "All":
        pt = new_df.pivot_table(index='Sport', columns=['Year'], values=medal, aggfunc='sum').fillna(0)
    else:
        pt = new_df.pivot_table(index='Sport', columns=['Year'], values="Medal", aggfunc='count').fillna(0)
    return pt


def most_successful_athletes_in_country(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df["region"] == country]

    temp_df = \
        temp_df["Name"].value_counts().reset_index().head(15).merge(df, left_on="index", right_on="Name", how="left")[
            ["index", "Name_x", "Sport"]].drop_duplicates('index').reset_index()
    temp_df.rename(columns={'index': "Name", "Name_x": 'Medals'}, inplace=True)
    temp_df.drop(['level_0'], axis=1, inplace=True)
    return temp_df


def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset=["Name", 'region'])
    athlete_df["Medal"].fillna("No Medal", inplace=True)
    if sport != "Overall":
        temp_df = athlete_df[athlete_df["Sport"] == sport]
    else:
        return athlete_df
    return temp_df


def men_vs_women(df, sport):
    athlete_df = df.drop_duplicates(subset=["Name", 'region'])
    if sport != "Overall":
        athlete_df = athlete_df[athlete_df["Sport"] == sport]
    men = athlete_df[athlete_df["Sex"] == "M"].groupby('Year').count()["Name"].reset_index()
    women = athlete_df[athlete_df["Sex"] == "F"].groupby('Year').count()["Name"].reset_index()
    final_df = men.merge(women, on="Year", how='left')
    final_df.rename(columns={"Name_x": "Male", "Name_y": "Female"}, inplace=True)
    final_df = final_df.fillna(0).astype(int)
    return final_df
