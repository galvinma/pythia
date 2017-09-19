import numpy as np
import pandas as pd
import math
from kmodes import kmodes
	
# Similarity function compares two DataFrame objects and returns a similarity score
	# ex. 
	# a = [1,0,0,0], b = [1,1,0,0]
	# delta = abs(a - b) = [0,1,0,0]
	# similarity = sum(delta) = 1
# Lower similarity scores imply a object is more similar

def similarity(object_one, object_two):
	delta = pd.DataFrame(object_one-object_two).abs()
	similarity = 0
	for i in delta:
		similarity += i
	return similarity

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

	# Define ks as a list of [Cluster : Mean Silhouette Score]
	ks = []

	for num in k:
		# init kmodes algo with num clusters
		kmodes_cao = kmodes.KModes(n_clusters=num, init='Cao')
		kmodes_cao.fit_predict(data)

		# Create a DataFrame linking cluster id to cluster centroid
		# NOTE: Default DataFrame index will match Kmodes cluster label
		clusters = pd.DataFrame(kmodes_cao.cluster_centroids_)

		# Create a DataFrame linking user id to cluster label
		user_cluster = pd.DataFrame(index=data.index)
		user_cluster['clusters'] = kmodes_cao.labels_

		# Create a Dictionary with the user id as the key. Value for each key \\
		# is a list: [[Interest list], Cluster ID, [Cluster]]
	

		# Calculate the silhouette coefficient for each point
		#
		# For the ith obj, calculate its average distance to all other objects in the cluster \\
		# Call this value, "ai".
		#
		# For the ith obj, and any cluster not containing the obj, calculate the object's average \\
		# distance to all the objects in the given cluster. Find the minimum such value with \\
		# respect to all clusters; call this value, "bi"
		#
		# For the ith obj, the silhouette coefficient is defined as:
		# si = (bi-ai)/max(ai,bi)






		# Pass user and associated cluster to similarity function
		# 
		# This is incorrect. Not quite sure what I was trying to do here, but keeping for reference for now
		for index, row in user_cluster.iterrows():
			cluster = clusters.iloc[row['clusters']]
			user = data.iloc[index]
			# Find similarity between user and cluster
			sim = similarity(user, cluster)
			 
