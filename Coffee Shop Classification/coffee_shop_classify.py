import os
import pandas as pd 
import numpy as np 
import re
import warnings

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.linear_model import RidgeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.ensemble import RandomForestClassifier

# Turn off warnings
warnings.filterwarnings('ignore')

# Set working directory and import initial dataset
path = 'I:\Projects\Leisure & Restaurants\CoffeeShops'
file = 'allshopes_Postcode info_UK.csv'

os.chdir(path)
data = pd.read_csv(file)

# Category labels
shopping_centre = ['shop(ping?)\s(centre|ctr|park)', 'mall', 'the\s\w+', 'supermarket', \
				   'outlet', 'arcade', 'complex', 'village', '(?<!health)(?<!garden)\scentre']
retail_park = ['(retail|business)\spark', 'industrial\sestate', 'garden\scentre', \
			   'plaza', 'drive\sthru']
transport_hub = ['train', 'airport', '(?<!gas)(?<!service)(?<!petrol)\sstation', 'bus', \
				 'subway', 'transit', 'termin(al|us)', 'arrivals', 'departures', 'quay',
				 'port', 'ferry']
service_station = ['motorway', 'petrol|gas|service\sstation', 'services', 'service\sarea', \
				   '(east|west|north|south)bound', 'grand central']
other = ['hospital', 'school', 'health\scentre', 'cinema', 'hotel', 'c\/o', 'university', \
		 'premier inn']

category = {'Shopping Centre': shopping_centre, 'Retail Park': retail_park, 
			'Transport Hub': transport_hub, 'Service Station': service_station, 
			'Other': other}

# Helper function for cleaning text
# Retain stopwords for n-gram vectorization
def clean_data(line):
	# Remove numbers and punctuation
	words = re.sub('[^a-zA-Z]', ' ' , line)
	# Lowercase words
	words = words.lower().split()
	# Remove additional whitespace
	words = " ".join(words)
	# Return value
	return words

# Helper function for creating labels
def label_data(line, dictionary, df, df_cat):
	for key in dictionary.keys():
		for exp in dictionary[key]:
			if bool(re.search(exp, line)):
				return key

# Clean and label initial data
data['Category'] = ''
for x in np.arange(len(data)):
	data['Store Location'][x] = clean_data(data['Store Location'][x])
	data['Category'][x] = label_data(data['Store Location'][x], category, data, 'Category')
	if data['Category'][x] is None:
		data['Category'][x] = 'High Street'

# Divide the data into training and testing sets
train_data, test_data = train_test_split(np.arange(len(data)), train_size=0.8, random_state=41)

train = data.iloc[train_data]
test = data.iloc[test_data]

# Create list of all locations
clean_train = []
for loc in train['Store Location']:
	clean_train.append(loc)

clean_test = []
for loc in test['Store Location']:
	clean_test.append(loc)

# TD-IDF vectorizer to downweight words frequent among all documents
# Using unigrams, bigrams, and trigrams to test relevance of word groups
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1,3), sublinear_tf=True)

#  training and testing data 
train_data_features = vectorizer.fit_transform(clean_train)
test_data_features = vectorizer.fit_transform(clean_test)

# Fit the model and predict results
models = {'KNeighbors': KNeighborsClassifier(), 'SVC': svm.SVC(), 'Linear SVC': LinearSVC(), \
		  'SGDClassifier': SGDClassifier(), 'Perceptron': Perceptron(), \
		  'Passive Aggressive Classifier': PassiveAggressiveClassifier(), \
		  'RidgeClassifier': RidgeClassifier(), 'Nearest Centroid': NearestCentroid(), \
		  'Random Forest Classifier': RandomForestClassifier(), \
		  'Bernoulli NB': BernoulliNB(), 'Multinomial NB': MultinomialNB()}

def fit_and_predict(model):
	model.fit(train_data_features, train['Category'])
	predict = model.predict(test_data_features)
	accuracy = accuracy_score(test['Category'], predict)
	return accuracy

for key, value in models.items():
	model = value
	accuracy = fit_and_predict(model)
	print(key, ':', accuracy)