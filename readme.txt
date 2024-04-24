				Jeff_Partyka's RAG Demo
				-----------------------

_________________________________________________________________________

How do I run this demo?

-Be sure that you are running some version of Python 3.10 or Python 3.11. I have not tested against any other version of Python.

-Open a terminal and cd into the '/code' directory.  You should see a file called 'requirements.txt'

-You will need to install the Python libraries and their specific versions located in 'requirements.txt'. You can do this either by installing each library one at a time like so:

pip install python_library==version_number

Or you could install all of them at once like so:

pip install -r requirements.txt

_________________________________________________________________________

What files are included in this demo?

    Files at the top directory level
    --------------------------------
    -readme.txt: This file!
    
    -Evaluation_Questions.txt: The file being used to evaluate the RAG solution

    -Sr_LLM_RAG_Assessment_Instruction.docx: Contains project instructions

    -Overview_of_RAG_Solution.pptx: A slide deck containing a higher-level, product-level 
     overview of the RAG solution. 

    -Evaluation_Results.pptx: A slide deck containing some results I generated 
     against the questions contained in 'Evaluation_Questions.txt'


    Python Scripts in code folder
    -----------------------------

    -tifin_rag_demo.py: This is the python script that is the basis of the demo. It is a 
     Streamlit web application that will allow anyone to ask questions and get answers from 
     "Investment_Case_For_Disruptive_Innovation.pdf"

    -GPTUtils.py: A helper class that can makes calls to either GPT 3.5 Turbo or GPT-4

    -GPTPromptTemplate.py: A file containing a multiline string that serves as a prompt template 
     for GPT LLMs to use in synthesizing answers from documents retrieved from the VectorDB in r
     response to a user question. 

    -CleanData.py: A helper class that removes stop words, punctuation, contractions and non-
     ASCII characters from the text extracted from the PDF file 
     "Investment_Case_For_Disruptive_Innovation.pdf"

    -requirements.txt: This file contains all Python libraries and their versions that are used 
     in this project that are not part of the Python Standard Library

 
    Files in code/documents folder
    -------------------------

    -Investment_Case_For_Disruptive_Innovation.pdf: This is the file from which we are 
     extracting text and asking/answering questions.

    Files in code/keys folder
    --------------------

    -openai_api_key.txt: This file contains the OpenAI API key that we use to query GPT 3.5 
     Turbo and/or GPT-4. It is one of my personal OpenAI API keys, but I will delete it once 
     this project is evaluated. Don't worry, I have other keys that I can use :-)

_________________________________________________________________________


