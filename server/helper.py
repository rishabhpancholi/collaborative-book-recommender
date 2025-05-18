import numpy as np

def get_recommendations(book_name,books_df,pt,similarity):

    # Check if the book exists
    if book_name not in books_df['title'].values:
        return {"error": "Movie not found in dataset."}
    
    # Get the book id
    book_id = books_df[books_df['title']==book_name]['ISBN'].values[0]
    
    # Check if book id is in pivot table
    if book_id not in pt.index:
        return {"error": "Movie not found in pivot table."}

    # Get index of the book in pivot table
    book_index = np.where(pt.index == book_id)[0][0]

    # Get similar books (top 5 excluding itself)
    similar_items = sorted(list(enumerate(similarity[book_index])),key=lambda x:x[1],reverse=True)[1:6]

    similar_books = []
    # Get books details
    for i in similar_items:
        book_id = pt.index[i[0]]
        book_detail= {
            'ISBN':str(book_id),
            'author':str(books_df[books_df['ISBN']==book_id]['author'].values[0]),
            'avg_rating':str(books_df[books_df['ISBN']==book_id]['avg_rating'].values[0]),
            'image_url':str(books_df[books_df['ISBN']==book_id]['image_url'].values[0]),
            'num_of_ratings':str(books_df[books_df['ISBN']==book_id]['num_of_ratings'].values[0]),
            'publish_year':str(books_df[books_df['ISBN']==book_id]['publish_year'].values[0]),
            'title':str(books_df[books_df['ISBN']==book_id]['title'].values[0])
        }

        similar_books.append(book_detail)

    # Return similar books data    
    return similar_books