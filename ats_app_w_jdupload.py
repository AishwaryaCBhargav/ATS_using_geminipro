from dotenv import load_dotenv
import base64
load_dotenv()
import streamlit as st
import os
# import io
from PIL import Image 
# import pdf2image
import google.generativeai as genai
import PyPDF2 as pdf


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_cotent,prompt):
    model=genai.GenerativeModel('gemini-pro')  ##gemini-pro-vision used for pdf2img
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

## simpler version
def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

    
## Streamlit App

def main():
    st.set_page_config(page_title="ATS Resume EXpert")
    st.header("ATS Tracking System")
    # input_text=st.text_area("Job Description: ",key="input")
    # uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])

    st.subheader('Upload Job Description PDF')
    job_description_file = st.file_uploader('Upload JD file', type='pdf')

    st.subheader('Upload Resume PDF')
    resume_file = st.file_uploader('Upload Resume file', type='pdf')


    if job_description_file and resume_file:
        st.write("PDFs Uploaded Successfully")


    submit1 = st.button("Tell Me About the Resume")


    #Input prompt for the first submit button
    input_prompt1 = """
    You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
    Please share your professional evaluation on whether the candidate's profile aligns with the role. 
    Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
    """


    if submit1:
        if job_description_file and resume_file:
            job_desc_text = input_pdf_text(job_description_file)
            resume_text = input_pdf_text(resume_file)

            response=get_gemini_response(input_prompt1,resume_text,job_desc_text)
            st.subheader("The Repsonse is")
            st.write(response)
        else:
            st.write("Please upload the resume")

 
if __name__ == "__main__":
    main()

