
# Chat with PDFs and Websites

This project allows you to chat with information extracted from multiple PDFs or a website. The application uses Streamlit for the web interface and Langchain for processing the text data.

## Features

- **PDF Chat**: Upload multiple PDF files and ask questions related to the content.
- **Website Crawling and Chat**: Enter a website URL, crawl it, and chat with the content extracted from the web pages.
- **Customizable**: Use different language models to interact with the extracted data.
- **Embedding and Vector Store**: Utilize embeddings to store and retrieve text chunks efficiently for faster responses.

## Requirements

Ensure you have the following Python packages installed:

```bash
pip install streamlit langchain beautifulsoup4 requests sentence-transformers langchain_community PyPDF2 python-dotenv faiss-cpu
```

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/chat-with-pdfs-and-websites.git
   cd chat-with-pdfs-and-websites
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file to store environment variables (e.g., API keys if needed). You can load environment variables using the `dotenv` package.

4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

5. Open the app in your browser at `http://localhost:8501/`.

## How It Works

### 1. **Chat with PDFs**
   - Users can upload multiple PDF files.
   - The content of the PDFs is extracted and split into chunks.
   - The chunks are then embedded into a vector store for efficient querying.
   - A conversation chain is created using a language model (e.g., `flan-t5-small`).

### 2. **Chat with Website Content**
   - Users can input a website URL.
   - The website is crawled, and all unique textual content (text, paragraphs) is extracted.
   - The extracted content is processed, split into chunks, and stored in a vector store.
   - A conversational model is used to interact with the extracted content.
   - **Note**: Crawling a website can take **8-10 minutes** depending on the website's size and structure.

## Configuration

- **Environment Variables**: This project uses the `dotenv` library to manage environment variables, such as API keys for language models and other configurations.
  
- **Langchain**: The project uses Langchain for conversation and vector store management. It leverages different embeddings models like Sentence Transformers, HuggingFace embeddings, and FAISS vector stores.

### Example `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
HUGGINGFACE_API_KEY=your_huggingface_api_key
```

## Usage

1. **Chat with PDFs**:
   - Upload one or more PDF files via the sidebar.
   - Ask questions related to the content of the PDFs.

2. **Chat with Websites**:
   - Enter the URL of the website you want to crawl.
   - The system will crawl the website and extract text for conversation.
   - Ask questions based on the website content.

## Technologies Used

- **Streamlit**: For creating the web application interface.
- **Langchain**: For managing conversation chains, embeddings, and vector stores.
- **BeautifulSoup**: For crawling and extracting data from websites.
- **Sentence Transformers**: For generating embeddings from text.
- **FAISS**: For creating efficient vector stores.
- **PyPDF2**: For extracting text from PDFs.
- **HuggingFace Models**: For text generation and retrieval.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
