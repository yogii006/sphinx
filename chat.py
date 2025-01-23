import streamlit as st
import sys
print(sys.path)
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

from langchain_community.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain_community.vectorstores import FAISS
# from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms import HuggingFaceHub




from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
# from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain_community.embeddings import HuggingFaceInstructEmbeddings

# from langchain.vectorstores import FAISS

from langchain_community.vectorstores import FAISS

# from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
# from langchain.llms import HuggingFaceHub
from langchain_community.llms import HuggingFaceHub

from sentence_transformers import SentenceTransformer


# Function to extract the menu structure and crawl pages
def extract_and_crawl(base_url):
    urls_n = [base_url] if base_url else []
    urls_v = []
    all_text = '''Sphinx is actively engaged in the following verticals:
            Automotive
            Industrial Equipment
            Power & Energy
            White Goods Industry, etc.
            The agent can also provide relevant links for detailed information. For example:

            Automotive: https://www.sphinxworldbiz.com/automotive/
            Industrial Equipment: https://www.sphinxworldbiz.com/industrial-equipment/'''
    try:
        response = requests.get(base_url)
        # response.raise_for_status()
        # soup = BeautifulSoup(response.content, 'html.parser')

        # # Step 1: Extract menu structure
        # # st.write("Extracting menu structure...")
        # menu_items = soup.find_all('li', class_=re.compile(r'^menu-item'))  # Matches all menu items
        # menu_structure = []

        # for menu_item in menu_items:
        #     # Extract main menu item name and link
        #     anchor = menu_item.find('a')  # Find the anchor tag inside the menu item
        #     if not anchor:
        #         continue
            
        #     main_menu_name = anchor.get_text(strip=True)
        #     main_menu_link = urljoin(base_url, anchor['href'])  # Ensure links are absolute

        #     # Check for nested sub-menus
        #     sub_menu_items = menu_item.find_all('li', class_=re.compile(r'^menu-item'))
        #     sub_menu_list = [
        #         {
        #             'name': sub_item.find('a').get_text(strip=True),
        #             'link': urljoin(base_url, sub_item.find('a')['href'])
        #         }
        #         for sub_item in sub_menu_items if sub_item.find('a')
        #     ]

        #     # Add to the menu structure
        #     menu_structure.append({
        #         'name': main_menu_name,
        #         'link': main_menu_link,
        #         'sub_menu': sub_menu_list
        #     })

        # # Step 2: Crawl the website
        # # st.write("Starting crawling process...")
        # unique_sentences = set()  # Set to store unique sentences

        # while urls_n:
        #     current_url = urls_n.pop(0)
        #     urls_v.append(current_url)
        #     st.sidebar.write(f"Crawling: {current_url}")

        #     try:
        #         response = requests.get(current_url)
        #         response.raise_for_status()
        #         soup = BeautifulSoup(response.content, 'html.parser')

        #         # Extract text content
        #         text_chunks = [p.get_text() for p in soup.find_all('p')]
        #         cleaned_text = " ".join(text_chunks)
        #         cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

        #         # Add unique sentences
        #         sentences = cleaned_text.split('. ')
        #         for sentence in sentences:
        #             unique_sentences.add(sentence.strip())

        #         # Extract additional URLs
        #         image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.pdf')
        #         for a_tag in soup.find_all('a', href=True):
        #             href = a_tag.get('href')
        #             if href and not href.lower().endswith(image_extensions):
        #                 full_url = urljoin(base_url, href)
        #                 if full_url.startswith(base_url) and full_url not in urls_v and full_url not in urls_n:
        #                     urls_n.append(full_url)
        #     except requests.RequestException as e:
        #         # st.write(f"Error processing {current_url}: {e}")
        #         print(f"Error processing {current_url}: {e}")

        # # Combine unique sentences into a single text
        # all_text = ". ".join(unique_sentences) + "."
        # # st.write("Crawling complete!")
        # # st.write(f"Total Unique Sentences: {len(unique_sentences)}")
       

    except Exception as e:
        # st.write(f"Error: {e}")
        print(f"Error: {e}")
    return all_text




def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

from langchain.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import FAISS

def get_vectorstore(text_chunks):
    model_name = "sentence-transformers/all-MiniLM-L6-v2"  # You can choose a different model
    try:
        # Initialize SentenceTransformer model
        embedding_model = SentenceTransformerEmbeddings(model_name=model_name)
        
        # Create vectorstore using SentenceTransformer embeddings
        vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embedding_model)
        
        return vectorstore
    except Exception as e:
        print(f"Error loading model {model_name}: {e}")
        raise


def get_conversation_chain(vectorstore):
    llm = HuggingFaceHub(
        repo_id="google/flan-t5-small", 
        model_kwargs={"temperature": 0.5, "max_length": 512}
    )

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)

def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDFs",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)

    # with st.sidebar:
    #     st.subheader("Your documents")
    #     pdf_docs = st.file_uploader(
    #         "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
    #     if st.button("Process"):
    #         with st.spinner("Processing"):
    #             # get pdf text
    #             raw_text = get_pdf_text(pdf_docs)

    #             # get the text chunks
    #             text_chunks = get_text_chunks(raw_text)

    #             # create vector store
    #             vectorstore = get_vectorstore(text_chunks)

    #             # create conversation chain
    #             st.session_state.conversation = get_conversation_chain(
    #                 vectorstore)
    with st.sidebar:
        st.subheader("Just crawl")
        # pdf_docs = st.file_uploader(
        #     "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        url = st.text_input("Enter the base URL:", "https://www.sphinxworldbiz.com/")
        if st.button("Process"):
            with st.spinner("Processing"):
                # get pdf text
                raw_text = extract_and_crawl(base_url=url)

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(
                    vectorstore)


if __name__ == '__main__':
    main()