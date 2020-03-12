import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

listOfCities = ['chicago', 'new york city', 'washington']
listOfMonths = ['january', 'february', 'march', 'april', 'may', 'june']
listOfDays = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
#    listOfCities = ['chicago', 'new york city', 'washington']
#    listOfMonths = ['january', 'february', 'march', 'april', 'may', 'june']
#    listOfDays = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid input

    while True:
        cityInput = input("Would you like to see data for Chicago, New York City or Washington?\n")
        cityInput = cityInput.lower()
        if cityInput in listOfCities:
            city  = cityInput
            break
        else:
            print("I don't understand your choice, please try re-entering the city.\n")

    # get user input for month (all, january, february, ... , june)
    filterLoop = 0
    while filterLoop != 1:
        filterInput = input("\nWould you like to filter by month, day or not at all?  Type \"none\" for no time filter.\n")
        filterInput = filterInput.lower()
        if filterInput == 'month':
            monthInput = input("\nWhich month? January, February, March, April, May or June?\n")
            monthInput = monthInput.lower()
            iMonth = 0
            while iMonth != 1:
                if monthInput in listOfMonths:
                    month = monthInput
                    iMonth = 1
                    day = 'all'
                    print('Filtering by month:', month.title())
                    filterLoop = 1
                else:
                    print("Invalid month, please try re-entering the month.\n")
    # get user input for day of week (all, monday, tuesday, ... sunday)
        elif filterInput == 'day':
            dayInput = 0
            month = 'all'
            while dayInput < 1 or dayInput > 7:
                try:
                    dayInput = int(input("\nwhich day? Please enter your response as an integer (1=Sun, 2=Mon, 3=Tue, 4=Wed, 5=Thur, 6=Fri, 7=Sat).\n"))
                    if dayInput >= 1 and dayInput <= 7:
                        day = listOfDays[dayInput-1]
                        print(day.title())
                        filterLoop = 1
                except ValueError:
                    print("Enter a valid integer")
        elif filterInput == 'none':
            day = 'all'
            month = 'all'
            filterLoop = 1
        else:
            print("Invalid filter, please try re-entering the filter.\n")

#    print("City: {}; Month: {}; Day: {}\n".format(city.title(), month.title(), day.title()))
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = listOfMonths.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    print('Most Frequent Month:', listOfMonths[df['month'].mode()[0]-1].title())

    # display the most common day of week
    df['day'] = df['Start Time'].dt.dayofweek
    popular_day = df['day'].mode()[0]
    print('Most Frequent Day of Week:', listOfDays[popular_day].title())

    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # find the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour: {}:00'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("\nMost used start station: ",df['Start Station'].value_counts().idxmax())

    # display most commonly used end station
    print("Most used end station: ",df['End Station'].value_counts().idxmax())

    # display most frequent combination of start station and end station trip
    print("\nMost frequent combination of start and end station: \n", df.groupby(['Start Station','End Station']).size().idxmax())
    # this only returns index of first occurance, not all if there are multiple with same count
    # however the instruction is singular so it is accurate but maybe not complete

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total Travel Time: ", df['Trip Duration'].sum())

    # display mean travel time
    print("Mean Travel Time: ", df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df.columns:
        print("User Type Counts:\n",df['User Type'].value_counts().to_string(header=None))
    else:
        print("Now User Type information available.\n")

    # Display counts of gender
    if 'Gender' in df.columns:
        print("\nCounts by Gender:\n",df['Gender'].value_counts().to_string(header=None))
        print("Unknown   ",df['Gender'].isnull().values.sum())
    else:
        print("No Gender information available.\n")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print("\nBirth year stats:\nEarliest: {}".format(int(df['Birth Year'].min())))
        print("Most Recent: {}".format(int(df['Birth Year'].max())))
        print("Most Common: {}".format(int(df['Birth Year'].mode())))
    else:
        print("No Birth Year information available.\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays raw data on bikeshare users."""
    initialRow = 0
    endRow = 4
    rawDisplay = 'c'
    while rawDisplay != 'q':
        #code review suggestion
        while initialRow <= endRow and endRow <= len(df.index)
        #while initialRow <= endRow:
            print('\nRow {}\n{}'.format(initialRow,df.iloc[initialRow,:].to_string(header=None)))
            initialRow = initialRow + 1
        rawDisplay = input('Hit Enter to continue, enter \"q\" to quit\n')
        if rawDisplay == 'q':
            break
        else:
            endRow = endRow + 5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        rawdata = input('\nWould you like to view raw data? Enter yes or no.\n')
        if rawdata.lower() == 'yes':
            print('rawdata:',rawdata)
            raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
