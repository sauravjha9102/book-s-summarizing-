import streamlit as st
from transformers import pipeline
import pyttsx3
import os

# Initialize the summarization pipeline with a more advanced model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", force_download=True)


def get_book_summary(book_name, author_name, min_words=200):
    prompt = f"Summarize the book '{book_name}' by {author_name}."
    summary = ""
    remaining_text = prompt
    while len(summary.split()) < min_words:
        part_summary = summarizer(remaining_text, max_length=150, min_length=100, do_sample=False)[0]['summary_text']
        summary += " " + part_summary
        remaining_text = remaining_text[len(part_summary):]  # Adjust to track the remaining text
    return summary.strip()

def text_to_audio(text, filename="book_summary.mp3"):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Set speech rate
    engine.setProperty('volume', 0.9)  # Set volume level
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Change voice if needed (e.g., to female voice)
    engine.save_to_file(text, filename)
    engine.runAndWait()
    return filename

# Streamlit UI
st.title("Book Summary Generator")
st.write("Enter the book's name and author's name to get a summary.")

book_name = st.text_input("Book Name")
author_name = st.text_input("Author Name")

if st.button("Get Summary"):
    if book_name and author_name:
        summary = get_book_summary(book_name, author_name)
        st.subheader("Summary")
        st.write(summary)

        audio_file = text_to_audio(summary)
        audio_path = os.path.join(os.getcwd(), audio_file)

        # Display audio player in Streamlit
        st.audio(audio_path)

        # Provide a download link
        with open(audio_path, "rb") as file:
            btn = st.download_button(
                label="Download Audio Summary",
                data=file,
                file_name=audio_file,
                mime="audio/mpeg"
            )
    else:
        st.error("Please enter both the book's name and the author's name.")
