import pickle
import streamlit as st
import base64

# Function to set background
def set_background(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        color: #f8f8f8;
    }}
    .stSelectbox label, .stTextInput label {{
        color: #ffffff !important;
    }}
    .stSelectbox div, .stTextInput input {{
        background-color: rgba(0,0,0,0.6);
        color: #ffffff;
    }}
    .stButton>button {{
        background-color: #8B4513;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
        border: 2px solid #fff;
    }}
    .stButton>button:hover {{
        background-color: #A0522D;
        color: #fff;
    }}
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
        color: #fff !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Set the background
set_background("book2.jpg")

# Load models and data
popular_df = pickle.load(open('model/popular.pkl', 'rb'))
pt = pickle.load(open('model/pt.pkl', 'rb'))
books = pickle.load(open('model/books.pkl', 'rb'))
similarity_scores = pickle.load(open('model/similarity_scores.pkl', 'rb'))

st.markdown("""
<div style="background-color: rgba(0, 0, 0, 0.7); padding: 20px; border-radius: 15px; text-align: center; border: 2px solid white;">
    <h1 style="color: #FFD700; font-family: 'Trebuchet MS', sans-serif;">📚 Book Recommender System</h1>
</div>
""", unsafe_allow_html=True)


# Dropdown to select a book
book_list = popular_df['Book-Title'].values
selected_book = st.selectbox("Type or select a book from the dropdown", book_list)

# Recommendation function
def recommend(book_name):
    index = pt.index.get_loc(book_name)
    distances = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)

    recommended_book_names = []
    recommended_book_posters = []

    for i in distances[1:6]:
        book_title = pt.index[i[0]]
        recommended_book_names.append(book_title)
        book_info = books[books['Book-Title'] == book_title].drop_duplicates('Book-Title').iloc[0]
        recommended_book_posters.append(book_info['Image-URL-M'])

    return recommended_book_names, recommended_book_posters
if st.button('Show Recommendation'):
    names, posters = recommend(selected_book)
    col1, col2, col3, col4, col5 = st.columns(5)

    cols = [col1, col2, col3, col4, col5]
    for i in range(5):
        with cols[i]:
            # Display image
            st.image(posters[i])

            # Create a clickable expander for book details
            with st.expander(f"📘 {names[i]}"):
                book_info = books[books['Book-Title'] == names[i]].drop_duplicates('Book-Title').iloc[0]
                st.markdown(f"""
                <div style="color:white;">
                <strong>Title:</strong> {book_info['Book-Title']}<br>
                <strong>Author:</strong> {book_info['Book-Author']}<br>
                <strong>Year:</strong> {book_info['Year-Of-Publication']}<br>
                <strong>Publisher:</strong> {book_info['Publisher']}<br>
                <img src="{book_info['Image-URL-L']}" width="100%" />
                </div>
                """, unsafe_allow_html=True)