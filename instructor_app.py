import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load instructor data
instructors = pd.read_csv('instructor_data.csv')
import pickle
# topics_matrix1 = pickle.load(topics_matrix,open('topics_matrix.pkl','rb'))
# similarity_matrix = pickle.load(similarity_matrix,open('similarity_matrix.pkl','rb'))
#instructors = pickle.load(instructors,open('instructors.pkl','rb'))


# Vectorize topic interests
vectorizer = CountVectorizer()
topics_matrix = vectorizer.fit_transform(instructors['Topic_of_interests'].apply(lambda x: ''.join(x)))
similarity_matrix = cosine_similarity(topics_matrix, topics_matrix)

# Function to recommend similar instructors
def recommend_similar_instructors(instructor_id, top_n=5):
    instructor_index = instructors[instructors['Instructor ID'] == instructor_id].index[0]
    similarity_scores = similarity_matrix[instructor_index]
    similar_instructors_indices = similarity_scores.argsort()[-top_n-1:-1][::-1]
    similar_instructors = instructors.iloc[similar_instructors_indices]
    return similar_instructors[['Instructor ID', 'Instructor name', 'Topic_of_interests','E-mail ID']]

# Streamlit app
st.header("Instructor Recommendations")

# User input for instructor ID
instructor_id_input = st.text_input("Enter Instructor ID:")
if not instructor_id_input:
    st.warning("Please enter an Instructor ID.")
    st.stop()

# Recommendations button
if st.button("Show Recommendations"):
    # Display recommendations
    try:
        recommendations = recommend_similar_instructors(instructor_id=instructor_id_input)
        st.table(recommendations)
    except IndexError:
        st.warning("Instructor ID not found. Please enter a valid ID.")
