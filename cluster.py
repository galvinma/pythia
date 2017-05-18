import numpy as np
import pandas as pd
import math
from kmodes import kmodes


def cluster():
	# Find population size
	population = session.query(func.count(User.id))
	# Get a list of all interests (ids)
	interests = []
	get_interest_ids = session.query(Interests).filter(Interests.id != None)
	for interest in get_interest_ids.all():
		interests.append(interest.id)
	# Get list of all users (ids)
	users = []
	get_user_ids = session.query(User).filter(User.id != None)
	for user in get_user_ids.all():
		users.append(user.id)
	# Get a list of all user-interest combinations
	user_interests = []
	get_user_interests = session.query(UserInterests).filter(UserInterests.user_id != None)
	for pair in get_user_interests.all():
		user_interests.append([UserInterests.user_id, UserInterests.interest_id)
	# Generate np zeros matrix of interests x users
	data = pd.DataFrame(np.zeros((len(users)),len(interests)), index=users, columns=interests)
	# Fill in user interests
	for pair in user_interests:
		row = pair[0]
		col = pair[1]
		data.set_value(row, col, 1)

	# Find maximum and minimum number of clusters
	# Max cluster size = 500 people
	# Min cluster size = 25 people
	# Total Population (tp) = K (# of clusters) * cs (average cluster size)
	k_min = math.floor(population/500)
	k_max = math.floor(population/25)
	# Item in list k represents an attempt to find the best fit number of clusters  
	k = []
	# Create optimal spacing based on estimate of k_min
	i = k_min
	while i < 50 and i < k_max:
		k.append(i)
		i += 1
	while i < 100 and i < k_max:
		k.append(i)
		i += 5
	while i < 250 and i < k_max:
		k.append(i)
		i += 10
	while i < 500 and i < k_max:
		k.append(i)
		i += 25
	while i < 1000 and i < k_max:
		k.append(i)
		i += 50
	while i < 2000 and i < k_max:
		k.append(i)
		i += 100
	while i < 5000 and i < k_max:
		k.append(i)
		i += 2000
	while i < 10000 and i < k_max:
		k.append(i)
		i += 500

	# Define ks as a dictionary of {Cluser : Silhouette Score}
	ks = {}

	for clusters in k:
		kmodes_cao = kmodes.KModes(n_clusters=4, init='Cao', verbose=1)
		kmodes_cao.fit(x)