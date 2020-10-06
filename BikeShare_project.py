# -*- coding: utf-8 -*-
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print("we have data for chicago, new york and washington only")
    # get user input for city (chicago, new york city, washington).
    #HINT: Use a while loop to handle invalid inputs
    cities = ["chicago", "new york","washington"]
    months = ["january","febreuary","march","april","may","june","all"]
    days = ["sunday","monday","tuesday","wednesday","thursday","friday","saturday","all"]
    city = ""
    month = ""
    day = ""



    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city not in cities:

        city = input("Enter the city name\n'New york'\n'Chicago'\n'Washington'\n").lower().strip()
        if city in cities:
            break

    # get user input for month (all, january, february, ... , june)
    while month not in months:
        month = input("Enter the month name\n 'january', 'febreuary', 'march'\n 'april', 'may', 'june'\n or 'all' to analyze the 6 months\n").lower().strip()
        if month in months:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day not in days:
        day = input("Enter the day of the week or 'all' to analyze all days: \n").lower().strip()
        if day in days:
            break

    print("You have choose ' {} ' to analyze by ' {} ' at week day ' {} '  ".format(city.title(), month.title(), day.title()))
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        # filter by day of week to create the new dataframe
        if day != 'all':
            df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    like most frequent month, most frequent day of the week and most frequent hour"""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    m_com_mon = df["month"].mode()[0]

    # display the most common day of week
    m_com_dow = df["day_of_week"].mode()[0]

    # display the most common start hour
    m_com_st = df["Start Time"].dt.hour.mode()[0]

    print("Most common month is:     {}".format(m_com_mon))
    print("Most common day of week:     {}".format(m_com_dow))
    print("Most common start hour:     {}".format(m_com_st))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    m_com_1stst = df["Start Station"].mode()[0]


    # display most commonly used end station
    m_com_endst = df["End Station"].mode()[0]

    # display most frequent combination of start station and end station trip
    #m_com_stend = df.groupby(['Start Station'])['End Station'].value_counts().mode
    m_com_stend = df.groupby(['Start Station','End Station']).size().nlargest(1)


    print("Most commonly useed start Station is:     {}".format(m_com_1stst))
    print("Most commonly used end Station is:     {}".format(m_com_endst))
    print("Most frequent combination of start and end stations as follow: \n", m_com_stend)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    trip_time = df["Trip Duration"].sum()

    # display mean travel time
    trip_avg = df["Trip Duration"].mean()
    print("Total travel time: ", trip_time)
    print("Mean travel time: ", trip_avg)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):

    """Displays statistics on bikeshare users... eg.
    users count by type and gender most frequent most recent and earliest year of birth"""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_count = df['User Type'].value_counts().to_frame()
    print('\nUser types:\n',user_count  )
    try:
    # Display counts of gender
            user_gender = df.groupby(["Gender"])["Gender"].count()
            print("Count by user Gender : ", user_gender)
    # Display earliest, most recent, and most common year of birth
            yob_mode = df["Birth Year"].mode()[0]
            yob_min = df["Birth Year"].min()
            yob_max = df["Birth Year"].max()
            print("The earliest year of birth is :     {}\n The Most recent year is :     {}\n The most common year of birth is :     {} ".format(yob_min, yob_max, yob_mode))
    except KeyError:

             print("There is no Gender data for Washington!")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(city):
    """ask the customer after the analysis if he would like to see raw data.
    input:yes = show data OR no = no data and go to the restart question
    output: raw data extracted from the DataFrame 5 raws at a time as the customer
    can choose to repeat by typing yes again if choose no will be directed to the restart question"""
    user_choice = ["yes","no"]

    raw_data = input("If you like to check 5 rows of raw Data kindly type 'yes' or 'no'\n ").lower().strip()
    while raw_data not in user_choice:
        print("NOT A VALID INPUT!")

        raw_data = input("If you like to check 5 rows of raw Data kindly type 'yes' or 'no'\n ").lower().strip()
        pass

    while raw_data == "yes":

                try:

                    for chunk in pd.read_csv(CITY_DATA[city], chunksize=5):
                        print(chunk)
                        raw_data = input("Do you like to check 5 more! kindly type yes or no\n").lower().strip()
                        if raw_data != "yes":
                            print("Thank you")
                            break
                    break
                except KeyboardInterrupt:
                    print("Thank you")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower().strip()
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
