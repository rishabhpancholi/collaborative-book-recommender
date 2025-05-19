import streamlit as st
import pandas as pd
import numpy as np
import requests
import html

# Set page layout to wide for better visual presentation
st.set_page_config(layout="wide")

st.title('Book Recommendation System')

# Sidebar navigation
page = st.sidebar.radio("Navigate", ["Popular", "Recommend"])

# ===========================
# -------- Popular ----------
# ===========================
if page == 'Popular':
    st.header('Most Popular Books')
    try:
        # Fetch popular books from backend
        url = 'https://collaborative-book-recommender.onrender.com/popular'
        response = requests.get(url)

        if response.status_code == 200:
            # Convert JSON response to DataFrame
            data = response.json()
            popular_df = pd.DataFrame(data)

            # Display books in rows of 5
            for i in range(0, len(popular_df), 5):
                # Create 5 columns with 0.1 width spacers between them
                cols = st.columns([1, 0.1, 1, 0.1, 1, 0.1, 1, 0.1, 1])
                for j in range(5):
                    if i + j < len(popular_df):
                        with cols[j * 2]:  # Only use non-spacer columns
                            raw_title = popular_df['title'][i + j]
                            title = html.unescape(raw_title)

                            # Display book cover
                            image_url = popular_df[popular_df['title']==raw_title]['image_url'].values[0]
                            st.markdown(f"<img src = '{image_url}' style='height: 50vh; width: 100%;'>", unsafe_allow_html=True)

                            # Add spacing
                            st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

                            # Display book title
                            st.write(title)

                # Add red divider and spacing between rows
                st.markdown("<div style='height:1px; background-color:blue;'></div>", unsafe_allow_html=True)
                st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
        else:
            st.write('Oops! Something went wrong!')
    except Exception as e:
        st.write(f'Error: {e}')

# ===========================
# -------- Recommend --------
# ===========================
elif page == 'Recommend':
    st.header('Choose one book from the list')
    try:
        # Fetch full book dataset from backend
        url = 'https://collaborative-book-recommender.onrender.com'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            books_df = pd.DataFrame(data)

            # Create dropdown with pretty titles (title cased)
            titles = books_df.sort_values(by='avg_rating', ascending=False)['title']
            titles_display = [html.unescape(title).title() for title in titles]
            title_map = dict(zip(titles_display, titles))  # Map displayed title to raw title

            selected_book = st.selectbox('Select a Book:', titles_display)
            raw_title = title_map[selected_book]  # Get raw title for backend queries

            if st.button('Recommend'):
                st.header('Book Details')
                
                # Create 2-column layout with slight spacing
                col1, sp1, col2 = st.columns([1.1, 0.1, 5])

                with col1:
                    # Display selected book cover
                    image_url = books_df[books_df['title']==raw_title]['image_url'].values[0]
                    st.markdown(f"<img src = '{image_url}' style='height: 50vh; width: 100%;'>", unsafe_allow_html=True)

                with col2:
                    # Add vertical spacing to align with image
                    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
                    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
                    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

                    # Show book details
                    title = html.unescape(raw_title)
                    st.header(title.title())

                    # Add spacing
                    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
                    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
                    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

                    # Show author
                    author = books_df[books_df['title']==raw_title]['author'].values[0]
                    st.subheader(f'Written by: {author.title()}')

                    # Add spacing
                    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
                    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
                    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

                    # Show publish year
                    publish_year = books_df[books_df['title']==raw_title]['publish_year'].values[0]
                    st.subheader(f'Published in : {publish_year}')

                # Divider after book details
                st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
                st.markdown("<div style='height:1px; background-color:blue;'></div>", unsafe_allow_html=True)
                st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

                # Recommended books section
                st.header('You Might Also Like These')
                try:
                    # Fetch recommended books from backend
                    url = f'https://collaborative-book-recommender.onrender.com/recommend/{raw_title}'
                    response = requests.get(url)

                    if response.status_code == 200:
                        data = response.json()
                        recommended_books_df = pd.DataFrame(data)

                        # Display 5 recommended books in a row
                        cols = st.columns([1, 0.1, 1, 0.1, 1, 0.1, 1, 0.1, 1])
                        for i in range(5):
                            with cols[i * 2]:
                                raw_title = recommended_books_df['title'][i]
                                title = html.unescape(raw_title)

                                # Show book cover
                                image_url = recommended_books_df[recommended_books_df['title']==raw_title]['image_url'].values[0]
                                st.markdown(f"<img src = '{image_url}' style='height: 50vh; width: 100%;'>", unsafe_allow_html=True)

                                # Add spacing and show title
                                st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
                                st.write(title)
                    else:
                        st.write('Oops! Something went wrong!')
                except Exception as e:
                    st.write(f'Error: {e}')
                
                # Add red divider and spacing between rows
                st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
                st.markdown("<div style='height:1px; background-color:blue;'></div>", unsafe_allow_html=True)
                st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
        else:
            st.write('Oops! Something went wrong!')
    except Exception as e:
        st.write(f'Error: {e}')


