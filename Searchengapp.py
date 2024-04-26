import streamlit as st
import chromadb

# Set page background color to cream
st.markdown(
    """
    <style>
    .stApp {{
        background-color: #F1FAAD;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
# Set up Streamlit title and subheader
st.title('🎬🎞️ Subtitles Search Engine 🎥')
st.subheader('🔍 Empowering Users to Find the Right Content')

# Initialize ChromaDB client and collection
client = chromadb.PersistentClient(path="Embeddings")
client.heartbeat()
collection = client.get_collection(name="SubtitleSearch_Engine")

# Get user input for query
query_text = st.text_input('Enter your subtitles here:')

# Perform search when button is clicked
if st.button('Search'):
    # Display loading spinner
    with st.spinner():
        # Define function to find similar subtitles
        def similar_title(query_text):
            result = collection.query(
                query_texts=[query_text],
                include=["metadatas", "distances"],
                n_results=10
            )
            ids = result['ids'][0]
            distances = result['distances'][0]
            metadatas = result['metadatas'][0]
            sorted_data = sorted(zip(metadatas, ids, distances), key=lambda x: x[2], reverse=True)
            return sorted_data

        # Get search results
        result_data = similar_title(query_text)

        # Display top 10 most relevant subtitle names
        st.markdown(
        f'<div style="font-size: 20px; padding: 10px; background-color: #1f497d; color: white; border-radius: 5px;">'
        f'Here are the TOP 10 most relevant movie names matching your search:'
        f'</div>', unsafe_allow_html=True
        )
        for i, (metadata, ids, similarity_score) in enumerate(result_data, start=1):
            subtitle_name = metadata['name']
            subtitle_id = metadata['num']
            # Display result with index number and cosine similarity
            st.write(f"{i}. {subtitle_name}(https://www.opensubtitles.org/en/subtitles/{subtitle_id}) - Similarity Score: {similarity_score:.4f}")
