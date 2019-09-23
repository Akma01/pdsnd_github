import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
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

    cities = list(CITY_DATA.keys())
    city = ''
    while city not in cities:
        city = input("Would you like to see data for Chicago, New York City, or Washington?").lower()

    print('-'*40)
    print("You requested data for", city.title())
    print("\n")


    months = ['all', 1,2,3,4,5,6]
    month = ''
    while month not in months:
        try:
            month = int(input("Which month? January, February, March, April, May, June? Please select as an integer through 1 to 6!"))
        except ValueError:
            print("Please enter an integer through 1 to 6! January = 1")
            continue
        if month not in range(1,7):
            print("Please enter an integer through 1 to 6! The data is given only from January through June.")
            continue
        else:
            break

    print('-'*40)

    if month == 1:
        print("You requested data for January")
    elif month == 2:
        print("You requested data for February")
    elif month == 3:
        print("You requested data for March")
    elif month == 4:
        print("You requested data for April")
    elif month == 5:
        print("You requested data for May")
    else:
        print("You requested data for June")

    print("\n")



    days = ['all', "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day = ''
    while day not in days:
        day = input("Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday?").title()
        if day not in days:
            print("Please select a proper weekday name!")
            continue
        else:
            break

    print('-'*40)
    print("You requested data for", day.title())


    return city, month, day
    print("\n")




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


    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df["End Time"] = pd.to_datetime(df['End Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df["hour"] = df["Start Time"].dt.hour

    if month != 'all':
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    popular_hour = df["hour"].mode()[0]
    print('Most Frequent Start Hour:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()


    popular_station = df["Start Station"].mode()[0]
    print('Most Frequent Start Station:', popular_station)



    popular_end_station = df["End Station"].mode()[0]
    print('Most Frequent End Station:', popular_end_station)



    popular_trip_from_start_to_end  = df.groupby(["Start Station", "End Station"]).size().idxmax()
    print('Most Common Trip From Start to End:', popular_trip_from_start_to_end)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df["travel_time"] = df["End Time"] - df["Start Time"]

    total_travel_time = df["travel_time"].sum()
    print("Total Travel Time:", total_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    try:
        user_type = df["User Type"].value_counts()
        print("Count of User Type:\n", user_type)
        print("\n")


        early_year = df["Birth Year"].min()
        print("Earliest Year of Birth:", early_year)

        recent_year = df["Birth Year"].max()
        print("Most Recent Year of Birth:", recent_year)

        common_year = df["Birth Year"].mode()
        print("Most Common Year of Birth:", common_year)

    except KeyError:
        print("Gender and Birth Year columns don't exist for Washington.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)



        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
