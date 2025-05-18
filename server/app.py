from flask import Flask,jsonify
from flask_cors import CORS
from helper import get_recommendations
import pickle

app = Flask(__name__)

# Connecting with the streamlit frontend
CORS(app,origins=['http://localhost:8502'])

#Load the data from pickle
with open('artifacts/popular.pkl','rb') as f:
    popular_df = pickle.load(f)
    popular_df['author'] = popular_df['author'].apply(lambda x: x.encode('latin1').decode('utf-8') if isinstance(x, str) else x)
    popular_df['title'] = popular_df['title'].apply(lambda x: x.encode('latin1').decode('utf-8') if isinstance(x, str) else x)

with open('artifacts/books.pkl','rb') as f:
    books_df = pickle.load(f)
    books_df['author'] = books_df['author'].apply(lambda x: x.encode('latin1').decode('utf-8') if isinstance(x, str) else x)
    books_df['title'] = books_df['title'].apply(lambda x: x.encode('latin1').decode('utf-8') if isinstance(x, str) else x)


with open('artifacts/pt.pkl','rb') as f:
    pt = pickle.load(f)

with open('artifacts/similarity.pkl','rb') as f:
    similarity = pickle.load(f)

# All the books data
@app.route('/',methods=['GET'])
def show_books():
    return jsonify(books_df.to_dict(orient='records'))

# Getting popular books
@app.route('/popular',methods = ['GET'])
def show_popular():
    return jsonify(popular_df.to_dict(orient='records'))

# Getting recommended books
@app.route('/recommend/<book_name>',methods = ['GET'])
def recommend(book_name):
    recommendations = get_recommendations(book_name,books_df,pt,similarity)
    return jsonify(recommendations)

# Run the app
if __name__=='__main__':
    app.run(debug=True)




