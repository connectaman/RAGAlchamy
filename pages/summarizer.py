import streamlit as st
import os
from PIL import Image
from ragalchemy.agents.pptx import PPTSummarizer


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
    pptx_file = r"C:\Users\AU39525\Downloads\PowerPoint Parser- LLM Hackathon\Data for Participants\DTC_Trends.pptx"
    ex = PPTSummarizer(pptx_file)
    
    st.header("PPT Metadata")
    col1,col2 = st.columns(2)
    with col1:
        st.text("PPT Title")
    with col2:
        st.text(ex.title)
        
    col1,col2 = st.columns(2)
    with col1:
        st.text("PPT Author")
    with col2:
        st.text(ex.author)
        
    col1,col2 = st.columns(2)
    with col1:
        st.text("PPT Subject")
    with col2:
        st.text(ex.subject)
        
    col1,col2 = st.columns(2)
    with col1:
        st.text("PPT Keywords")
    with col2:
        st.text(ex.keywords)
        
    col1,col2 = st.columns(2)
    with col1:
        st.text("PPT Last Modified By")
    with col2:
        st.text(ex.last_modified_by)
        
    col1,col2 = st.columns(2)
    with col1:
        st.text("PPT Created At")
    with col2:
        st.text(ex.created)
        
    col1,col2 = st.columns(2)
    with col1:
        st.text("PPT Modified At")
    with col2:
        st.text(ex.modified)
        
            
    st.divider()
    
    st.header("PPT Slide Wise Summary")
    for s in ex.summarize_stream():
        st.text(s["Summary"])
        st.divider()