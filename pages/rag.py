import streamlit as st
import os
from PIL import Image
from ragalchemy.agents.pptx import PPTQnA


st.set_page_config(page_title="PPT Summarizer", page_icon="📈")

with st.sidebar.form(key ='UploadFile'):
    image = Image.open('./documentation/images/logo.png')
    st.image(image)

    uploaded_file_path = st.text_input('Enter pptx file path')
    
    option = st.selectbox(
        "What best describes your data?",
        ("Healthcare", "Finance", "Report"),
    )
    submit = st.form_submit_button(label = 'Upload 📁')


if submit and uploaded_file_path:
    pass
    # pptx_file = r"C:\Users\AU39525\Downloads\PowerPoint Parser- LLM Hackathon\Data for Participants\DTC_Trends.pptx"
    # ex = PPTQnA(pptx_file)
    # for s in ex.summarize_stream():
    #     st.text(s["Summary"])
    #     st.divider()