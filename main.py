
import streamlit as st
import json

# File for saving/loading the library
FILE_NAME = "library.json"

# Load library from file
def load_library():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save library to file
def save_library(library):
    with open(FILE_NAME, "w") as file:
        json.dump(library, file, indent=4)

# Load the library (global variable)
library = load_library()

st.set_page_config(page_title="📖 HG Illuminarium", layout="wide")

st.title("📚 HG Illuminarium")
st.sidebar.title("📚 HG Illuminarium")
# Sidebar Menu
tabs = ["Add Book", "Remove Book", "Search Book", "View Library", "Statistics"]
choice = st.sidebar.radio("Select an option", tabs)


# ➤ **ADD BOOK**
if choice == "Add Book":
    
    st.header("📖 Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=1000, max_value=9999, step=1)
    genre = st.text_input("Genre")
    content = st.text_area("Book Content (Optional)")
    read_status = st.checkbox("Have you read this book?")
    
    if st.button("Add Book"):
        if title and author:
            book = {
                "Title": title,
                "Author": author,
                "Year": int(year),
                "Genre": genre,
                "Content": content,
                "Read": read_status
            }
            library.append(book)
            save_library(library)
            st.success(f"Book '{title}' added successfully!")
            st.rerun()
        else:
            st.warning("Title and Author are required!")

# ➤ **REMOVE BOOK**
elif choice == "Remove Book":
    st.header("🗑️ Remove a Book")
    titles = [book["Title"] for book in library]
    
    if titles:
        book_to_remove = st.selectbox("Select a book to remove", titles)
        
        if st.button("Remove Book"):
            # ✅ No need for global declaration here
            library = [book for book in library if book["Title"] != book_to_remove]
            save_library(library)
            st.success(f"Book '{book_to_remove}' removed successfully!")
            st.rerun()
    else:
        st.warning("No books available to remove.")

# ➤ **SEARCH BOOK**
elif choice == "Search Book":
    st.header("🔍 Search for a Book")
    search_term = st.text_input("Enter Title or Author")
    
    if st.button("Search"):
        results = [book for book in library if search_term.lower() in book["Title"].lower() or search_term.lower() in book["Author"].lower()]
        
        if results:
            st.write("### Matching Books:")
            for book in results:
                st.write(f"**{book['Title']}** by {book['Author']} ({book['Year']}) - {book['Genre']} - {'✅ Read' if book['Read'] else '❌ Unread'}")
                if book["Content"]:
                    with st.expander("View Content"):
                        st.write(book["Content"])
        else:
            st.warning("No matching books found.")

# ➤ **VIEW LIBRARY**
elif choice == "View Library":
    st.header("📚 Your Library")
    
    if library:
        for book in library:
            st.write(f"**{book['Title']}** by {book['Author']} ({book['Year']}) - {book['Genre']} - {'✅ Read' if book['Read'] else '❌ Unread'}")
            if book["Content"]:
                with st.expander("View Content"):
                    st.write(book["Content"])
    else:
        st.info("Your library is empty.")

# ➤ **STATISTICS**
elif choice == "Statistics":
    st.header("📊 Library Statistics")
    total_books = len(library)
    read_books = sum(1 for book in library if book["Read"])
    read_percentage = (read_books / total_books) * 100 if total_books > 0 else 0
    
    st.write(f"**Total Books:** {total_books}")
    st.write(f"**Percentage Read:** {read_percentage:.2f}%")

# ➤ **FOOTER**
st.markdown("---")
st.markdown("🩵 **Created by Hadiqa Gohar** 🩵")
