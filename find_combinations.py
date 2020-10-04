import sys
import pandas as pd
import numpy as np


def get_following_flight(df, flight):
	"""
	For a specific starter flight find the possible flight connections, acording to the defined constrains:
		- the source of the next flight should be the same as the destination of the starter flight 
		- the time between flights should be NO smaller than 1 hour (60 min)
		- the time between flights should be NO larger than 4 hours (240 min)

	Parameters:
	df (pandas.DataFrame): all the possible flights.
	flight (pandas.Series): starter flight we are searching possible connections from.
	
	Returns:
	pandas.DataFrame: all possible following connections for this flight.

	"""
	return df.loc[(df.source==flight.destination)\
							&((df.departure - flight.arrival)/np.timedelta64(1,'m') >= 60)\
							&((df.departure - flight.arrival)/np.timedelta64(1,'m') <= 240)]	


def combinations(df_main, df_search):
	"""
	Get all the possible trips (combinations of flights), given some main flights dataFrame (df_main)
	and specific starting point(s) to search from (df_search). Returns pandas.Series with a list of flights for each possible trip.

	Parameters:
	df_main (pandas.DataFrame): base dataframe to check flights information from.
	df_search (pandas.DataFrame): dataframe with flights that we are searching possible connections/trips from.
	
	Returns:
	pandas.Series: all possible trips. each entry is a list of flight(s) number(s).

	"""

	# all the possible trips will be stored here
	all_trips = pd.Series(dtype='object')
	for i, flight_start in df_search.iterrows():
		
		# First possible trip will be just this starter flight		
		all_trips.loc[len(all_trips)] = [flight_start.flight_number] 

		# Find all possible next flights		
		df_next = get_following_flight(df_main, flight_start)

		# If there are any following ("next") flights available, start searching for more trips/flights
		if not df_next.empty:
			
			# If in any of the following/next trips we arrive back at our starting point, each of this trips ends here		
			df_end = df_next.loc[df_next.destination == flight_start.source]
			
			for i_end, flight_end in df_end.iterrows():
				all_trips.loc[len(all_trips)] = [flight_start.flight_number, flight_end.flight_number] 
			
			# Only search for following/next flights, if we are NOT back at our starting point
			df_next = df_next.loc[df_next.destination != flight_start.source]
			
			# Loop through our next flights and search recursivly for possible following trips
			for i_next, flight_next in df_next.iterrows():
				# get all following trips
				trips_next = combinations(df_main, df_next.loc[[i_next]])
				for t in trips_next:
					# the following trips have to start with our starter flight
					all_trips.loc[len(all_trips)] = [flight_start.flight_number] + t

	return all_trips

def clean_data(trips, df_main, nr_bags):
	"""
	given some flights combinations, return list of trips with more details, such as total cost, flight total time and transfer total time.
	
	Parameters:
	
	trips (pandas.Series): series of lists with flights codes.
	df_main (pandas.DataFrame): base dataframe to check flights information from.
	
	Returns:
	list: list of dictionaries. each dictionary contains information regarding one specific trip and it's details. 

	"""

	# final cleaned trips will be stored here
	trips_cleaned = []
	for trip in trips:

		# find details of the flights of this trip
		df_trip = df_main.loc[df_main.flight_number.isin(trip)]
		df_trip = df_trip.sort_values(by='departure')
		
		# find all flights duration and all transfers duration
		time_diff = (df_trip.arrival - df_trip.departure)/np.timedelta64(1,'m')
		transfer_time_diff = (df_trip.departure[1:] - df_trip.arrival.shift(1)[1:])/np.timedelta64(1,'m')
		
		# date columns in string format, so they can possibly be json serializable in the future
		df_trip.arrival = df_trip.arrival.dt.strftime('%Y-%m-%d %H:%M')
		df_trip.departure = df_trip.departure.dt.strftime('%Y-%m-%d %H:%M')

		# append his trip to our main trips lists
		trips_cleaned.append({
			'number_of_bags': int(nr_bags),
			'source': df_trip.iloc[0].source,
			'destination': df_trip.iloc[-1].destination,
			'flights': [flight.to_dict() for i,flight in df_trip.iterrows()],
			'total_price': float(df_trip.price.sum() + nr_bags*df_trip.bag_price.sum()), # total price should include bags prices
			'flight_time': float(time_diff.sum()), 
			'transfer_time': float(transfer_time_diff.sum()),
			'number_of_transfers': int(len(df_trip)-1),
		})
	return trips_cleaned


def main(df=pd.DataFrame(), passenger_bags=[0,1,2]):
	""" Creates dictionary of possible trips given flights data and number(s) of bags the passanger want's to carry.

	Parameters:
	df (pandas.DataFrame): dataframe with flights info.
	passenger_bags (list): list of bags per passanger. Different sets of trips will be created for each one of this bags numbers. 
	
	Returns:
	dictionary: nested dictionary where the "main/parent keys" correspond to the number of bags allowed per passanger. 
				Each "main/parent value" is a list of all the trips possible with that number of bags.
	"""

	if df.empty:
		df = pd.read_csv('input.csv') # default name of input file

	# columns necessary to check all the possible flights combinations.
	cols_for_combinations = ['source', 'destination', 'departure', 'arrival', 'flight_number']	

	# Proper datetime format
	df.departure = pd.to_datetime(df.departure)
	df.arrival = pd.to_datetime(df.arrival)

	# All the final trips will be in this empty dictionary
	result = {}

	# Loop through each bag that the passenger will carry
	for nr_bags in passenger_bags:
		# Passanger with 'n' bag(s) can catch flights that allow 'n' bag(s) or more
		df_bags = df.loc[df.bags_allowed >= nr_bags].reset_index(drop=True)

		if not df_bags.empty:
			# gather all possible combinations for this number of bags
			trips = combinations(df_bags[cols_for_combinations], df_bags[cols_for_combinations])

			# organize data such that relevant information is more accessible
			result[nr_bags] = clean_data(trips, df_bags, nr_bags)

		else:
			# If there are now possible flights for this number of bags, there's no possible trips
			result[nr_bags] = []
	return result
	

if __name__ == '__main__':
	data = sys.stdin
	df = pd.read_csv(data)
	print(main(df))
