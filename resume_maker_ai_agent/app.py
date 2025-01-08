import warnings

import streamlit as st

from resume_maker_ai_agent.services.app_service import search_music

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


# Set page config
st.set_page_config(page_title="Music Search", page_icon="🎵", layout="wide")

# App title
st.title("🎵 Music Search Results")

search_query = st.sidebar.text_input("Enter song name or artist")

if search_query:
    # Show loading spinner
    with st.spinner("Searching for music..."):
        music_data = search_music(search_query)

    if music_data is None or len(music_data) == 0:
        st.warning("No music found. Please try again.")

    for item in music_data:
        try:
            song_id = item["song_info"]["song_url"].split("/")[-1]  # Get unique ID from URL
            song_title = item["song_info"]["title"].split(" - ")[0]
            musicians = item["song_info"]["musician"]
            artists = ", ".join(musicians[:2])
            release_date = item["song_info"]["release_date"]

            # Display song information in a row
            with st.container():
                # Create columns
                col1, col2, col3, col4 = st.columns([1, 2, 2, 2])

                # Column 1: Image
                with col1:
                    st.image(item["album_image_url"], width=100)

                # Column 2: Title and Artists
                with col2:
                    st.markdown(f"**{song_title}**")
                    st.markdown(f"*{artists} | {release_date}*")

                # Column 4: Audio Player
                with col4:
                    st.audio(item["song_info"]["downloadable_url"])
        except Exception as e:
            print(f"An error occurred: {e!s}")
            continue
