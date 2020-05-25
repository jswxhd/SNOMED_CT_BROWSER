import nltk
#nltk.download('stopwords')
#nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.decomposition import TruncatedSVD
import math
import numpy as np



#my_documents=["Shipment of gold damaged in a fire","Delivery of silver arrived in a silver truck",
#"Shipment of gold arrived in a truck"]
		
def text_preprocess(texts):
	token_texts = nltk.word_tokenize(texts,language = 'english')
	st2 = PorterStemmer()
	english_stopwords = stopwords.words("english")
	token_stem_stopword=[]
	
	for each in token_texts:
		if each not in english_stopwords:
			token_stem_stopword.append(st2.stem(each))

	new_text = ' '.join(token_stem_stopword)
		
	return new_text


def topic_model(documents,keyword):
	new_documents=[]
	for each in documents:
		new_documents.append(text_preprocess(each))
	
	new_documents.append(keyword)
		
	vectorizer = TfidfVectorizer()   
	vector = vectorizer.fit_transform(new_documents)    
	#word = vectorizer.get_feature_names()
	svd_model = TruncatedSVD(n_components=3, algorithm='randomized', n_iter=10, random_state=1)
	result_vector = svd_model.fit_transform(vector[:-1])
	keyword_vector = svd_model.transform(vector[-1])

	return result_vector,keyword_vector


#这个方法没有做stem
def topic_model_2(documents):	
	vectorizer = TfidfVectorizer(stop_words = 'english')   
	vector = vectorizer.fit_transform(documents)    
	#word = vectorizer.get_feature_names()
	svd_model = TruncatedSVD(n_components=2, algorithm='randomized', n_iter=10, random_state=1)
	new_vector = svd_model.fit_transform(vector)
	#print(word)
	#query_vector = svd_model.transform(query)

	return new_vector


def dot_product(v1, v2):
	return sum(a * b for a,b in zip(v1,v2))

def distance(vector):
	return math.sqrt(dot_product(vector, vector))

def cos_sim(v1, v2):
	return dot_product(v1, v2) / distance(v1) * distance(v2)

def get_similarity_group(document_list, keyword):
	sim_list = []
	result_matrix, keyword_matrix = topic_model(document_list,keyword)
	for i in range(0,len(result_matrix)):
		sim_list.append(cos_sim(result_matrix[i],keyword_matrix[0]))

	return sim_list
		
#a,b = topic_model(my_documents,'ship of fire')
#print(a,b)
#get_similarity_group(my_documents,'silver')

		
	
	
