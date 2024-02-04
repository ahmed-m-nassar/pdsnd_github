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
    cities = ['chicago', 'new york city', 'washington']
    months = ['all','january', 'february', 'march', 'april', 'may', 'june']
    days   = ['all','saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday' , 'friday']

    city = input("Please enter name of the city to analyze ['chicago' or 'new york city' or 'washington'] \n ").lower()
    while city not in cities :
        city = input("Wrong city name , please enter a correct city name :")
    
    month = input("Please enter name of the month to filter by, or 'all' to apply no month filter  ['all','january', 'february', 'march', 'april', 'may', 'june'] \n").lower()
    while month not in months :
        month = input("Wrong month name , please enter a correct month name").lower()
    
    day = input("Please enter name of the day of week to filter by, or 'all' to apply no day filter ['all','saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday' , 'friday'] \n ").lower()
    while day not in days :
        day = input("Wrong day name ").lower()

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
    df = pd.read_csv('./' + CITY_DATA[city])

    # convert the Start Time column to datetime
    #df['Start Time'] = 

    # extract month and day of week from Start Time to create new columns
    df['month'] = pd.to_datetime(df['Start Time']).dt.month
    df['day_of_week'] = pd.to_datetime(df['Start Time']).dt.dayofweek
     
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday' , 'friday' , 'saturday', 'sunday']
        day = days.index(day)
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day ]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print('Most common month is : ' +  months[df['month'].mode()[0] - 1] )

    # display the most common day of week
    days = ['monday', 'tuesday', 'wednesday', 'thursday' , 'friday' , 'saturday', 'sunday']
    print('Most common day of week is : ' +  days[df['day_of_week'].mode()[0]] )


    # display the most common start hour
    df['hour'] = pd.to_datetime(df['Start Time']).dt.hour
    print('Most common start hour is : ' + str(df['hour'].mode()[0]) )
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most commonly used start station is : ' + str(df['Start Station'].mode()[0]) )


    # display most commonly used end station
    print('Most commonly used end station is : ' + str(df['End Station'].mode()[0]) )

    # display most frequent combination of start station and end station trip
    print('most frequent combination of start station and end station trip is :' + str(df.groupby(['Start Station','End Station']).size().idxmax()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    seconds_to_hours = lambda x : x//3600
    remaining_minutes = lambda x : (x%3600) // 60
    remaining_seconds = lambda x :(x%3600)%60
        
    df['Travel Time'] =   pd.to_datetime(df['End Time']) -  pd.to_datetime(df['Start Time'])
    total_travel_time_in_seconds = df['Travel Time'].sum().total_seconds()
    mean_travel_time_in_seconds = df['Travel Time'].mean().total_seconds()
    
    #displaying total travel time
    print('Total travel time : {} hours , {} minutes and {} seconds'.format(seconds_to_hours(total_travel_time_in_seconds) ,
                                        remaining_minutes(total_travel_time_in_seconds) ,remaining_seconds(total_travel_time_in_seconds)))
    # TO DO: display mean travel time
    print('Mean travel time : {} hours , {} minutes and {} seconds'.format(seconds_to_hours(mean_travel_time_in_seconds) ,
                                        remaining_minutes(mean_travel_time_in_seconds) ,remaining_seconds(mean_travel_time_in_seconds)))
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts())

    print('\n \n ')
    
    # Display counts of gender
    if city != 'washington':
        print(df['Gender'].value_counts())

        # Display earliest, most recent, and most common year of birth
        print('Earliest year of birth : ' + str(int(df['Birth Year'].min())))
        print('Most recent year of birth : ' + str(int(df['Birth Year'].max())))
        print('Most common year of birth : ' + str(int(df['Birth Year'].mode())))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        
        view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?")
        start_loc = 0
        while view_data != 'no':
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5
            view_data = input("Do you wish to continue? , type 'no' to stop , otherwise we will continue : ").lower()

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
