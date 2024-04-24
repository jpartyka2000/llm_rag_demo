import streamlit as st
import sys
import os
import chromadb
import random
import tika
import nltk
import copy

#be sure to download and use punkt tokenizer, which works across many languages and punctuation patterns
nltk.download('punkt')

from pypdf import PdfReader
from datetime import datetime
from nltk.tokenize import sent_tokenize, word_tokenize

from CleanData import CleanData
from GPTUtils import GPTUtils
from GPTPromptTemplate import gpt_prompt_template_str

def process_pdf_file(session_state, progress_bar, percent_complete_widget):
        
    reader = PdfReader(session_state.uploaded_file)
    
    progress_increment = int(100.0 / len(reader.pages))
    percent_complete = 0

        
    try:
        current_obj_id = len(session_state.collection.get()['ids']) + 1
    except Exception:
        current_obj_id = 1

    for pageidx, page in enumerate(reader.pages, 1):

        this_page_text = page.extract_text()

        #st.subheader(this_page_text)
        #st.subheader('-------')

        #break content into individual sentences
        sentences_list = sent_tokenize(this_page_text)

        metadata_dict_list = []
        id_list = []

        for i in range(len(sentences_list)):

            #populate metadata_dict and id_list for insertion into Chromadb collection
            metadata_dict_list.append({"source":"page_" + str(pageidx)})
            id_list.append("id" + str(current_obj_id))

            #clean this sentence to improve retrieval accuracy
            #sentences_list[i] = session_state.data_cleaning_object.clean_text(sentences_list[i])

            #print(sentences_list[i])

            current_obj_id += 1

        #add pdf pages to document collection in chromadb
        session_state.collection.add(
        documents=sentences_list,
        metadatas=metadata_dict_list,
        ids=id_list)
        
        #update progress bar
        percent_complete += progress_increment
        progress_bar.progress(percent_complete)
        percent_complete_widget.text(str(percent_complete) + " percent complete")
        
    try:
        current_obj_id = len(session_state.collection.get()['ids'])
        #st.subheader(current_obj_id)
    except Exception:
        pass
    
    #finalize progress bar
    progress_bar.progress(100)
    percent_complete_widget.text("100 percent complete.")

    
def process_pptx_file():
    pass

def process_docx_file():
    pass
    
    
def main():
    st.title("TIFIN RAG Web App Demo")

    menu = ["Upload File", "Ask a Question", "Evaluation", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    #initialize session state variables
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None
    
    if 'uploaded_file_name' not in st.session_state:
        st.session_state.uploaded_file_name = ""
    
    if 'uploaded_file_status_msg' not in st.session_state or 'file_uploaded_status' not in st.session_state or st.session_state.file_uploaded_status == False:
        st.session_state.uploaded_file_status_msg = "<p style=\"color: red;\">File has has not been uploaded</p>"
    elif st.session_state.file_uploaded_status == True:
        st.session_state.uploaded_file_status_msg = "<p style=\"color: green;\">File has been successfully uploaded!</p>"
        
    #Store data cleaning object, GPTUtils object and chromadb instance in st.session_state
    if 'data_cleaning_object' not in st.session_state:
        st.session_state.data_cleaning_object = CleanData()
    
    if 'gpt_utils_object' not in st.session_state:
        st.session_state.gpt_utils_object = GPTUtils()
    
    if 'chromadb_client' not in st.session_state:
        st.session_state.chromadb_client = chromadb.PersistentClient(path='chromadb_demo')
        
        #we will always delete any preexisting collection at the beginning of the app execution
        try:
            st.session_state.chromadb_client.delete_collection(name="jeff_partyka_collection")
        except Exception:
            pass
        
        #create a new collection
        st.session_state.collection = st.session_state.chromadb_client.create_collection(name="jeff_partyka_collection")
        
        #and set the current_object_id in the collection to 1
        st.session_state.current_object_id = 1


    if choice == "Upload File":
        st.subheader("Upload File")
        st.markdown(st.session_state.uploaded_file_status_msg, unsafe_allow_html=True)

        uploaded_file = st.file_uploader("Upload File", type=['pdf','pptx','docx'])
        
        if st.button("Process Data File"):
            
            if uploaded_file is not None:
                
                progress_bar = st.progress(0)
                percent_complete_widget = st.empty()
                
                #indicate that file has been successfully uploaded
                st.session_state.file_uploaded_status = True
                
                st.session_state.uploaded_file = uploaded_file
                st.session_state.uploaded_file_name = uploaded_file.name
 
                #if the file is a PDF file, extract text using pypdf
                #otherwise, use tika to extract text
                if st.session_state.uploaded_file_name[-4:] == '.pdf':
                    process_pdf_file(st.session_state, progress_bar, percent_complete_widget)
                
                elif st.session_state.uploaded_file_name[-5:] == '.pptx':
                    st.subheader("A PPTX FILE!")
                
                elif st.session_state.uploaded_file_name[-5:] == '.docx':
                    st.subheader("A DOCX FILE!")
                
                #st.session_state.uploaded_file_status_msg = 
                st.markdown("<p style=\"color: green;\">File has been successfully uploaded!</p>", unsafe_allow_html=True)
                st.subheader("Go to the 'Ask a Question' page in the left dropdown menu and ask your data questions.")
                

            else:
                
                pass


    elif choice == "Ask a Question":
        st.subheader("Ask a Question")
        st.markdown(st.session_state.uploaded_file_status_msg, unsafe_allow_html=True)
        
        if st.session_state.uploaded_file is not None:
            
            #create simple UI involving 2 text boxes: one for the question, another for the answer returned by chromadb + GPT-3.5 Turbo
            prompt_text_area = st.text_area("Ask Your Data a Question:", height=300, value="")
            
            #add 2 radio buttons for querying either gpt 3.5 Turbo or gpt-4
            gpt_model = st.radio(
                "Pick the GPT model you want to use",
                ["GPT-3.5-Turbo", "GPT-4"])
            
            #ranking_metric = st.radio(
            #    "Choose the similaity metric you want to use",
            #    ["l2", "ip","cosine"])
            
            num_results = st.text_input("Enter the number of neighbors to fetch from Vector DB:", value=8)
                        
            if st.button("Ask Away"):
                
                #first, we need to query the chromadb document collection for matching sentences
                #through the entire PDF
                
                results_str = st.session_state.collection.query(
                    query_texts = [prompt_text_area],
                    n_results=int(num_results)
                )
                
                #extract the metadata and document for the N results. We will use 3 different ranking algorithms. 
                #(1): Use the top result for the simple re-ranking measure
                #(2): Use the top result + any other results returned that are on the same page
                #(3); Use all results
                
                #For any approach, I will send the candidate info as background context for GPT 3.5 Turbo/GPT-4 to use as part of answer synthesis
                
                #first, combine all document results into one string
                document_list = results_str['documents'][0]
                
                combined_document_str = ""
                
                for this_document_str in document_list:
                    combined_document_str += this_document_str
                
                #I will implement approach #3, and likely will not be able to implement the other 2 approaches due to time constraints
                #first, copy gpt_prompt_template_str for use in this question
                
                this_question_prompt_template_str = copy.deepcopy(gpt_prompt_template_str)
                
                #replace template placeholders with values
                this_question_prompt_template_str = this_question_prompt_template_str.replace("{background_context}", combined_document_str)
                this_question_prompt_template_str = this_question_prompt_template_str.replace("{user_question}", prompt_text_area)
                
                call_gpt_turbo_param = True
                
                #get GPT model to use
                if gpt_model == "GPT-4":
                    call_gpt_turbo_param = False
                
                #send to GPT LLM
                gpt_response = st.session_state.gpt_utils_object.call_gpt(prompt_text_area, this_question_prompt_template_str,call_gpt_turbo=call_gpt_turbo_param)
                
                answer_text_area = st.text_area("GPT Says:", height=300, value=gpt_response)
                
                                    

            
            
     
    elif choice == "Evaluation":
        st.subheader("Evaluation")
        st.markdown(st.session_state.uploaded_file_status_msg, unsafe_allow_html=True)
        
    else:
        st.subheader("About")
        st.info("TIFIN RAG Demo Built with Streamlit 1.32.0")
        st.subheader("Authors")
        st.info("Jeffrey Partyka")


if __name__ == '__main__':
    main()