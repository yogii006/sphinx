import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import streamlit as st

# Input URL
base_url = st.text_input("Enter the base URL:", "https://www.sphinxworldbiz.com/")
urls_n = [base_url] if base_url else []
urls_v = []

# Initialize session state for storing conversation history
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# Function to extract the menu structure and crawl pages
def extract_and_crawl(base_url):
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Step 1: Extract menu structure
        st.write("Extracting menu structure...")
        menu_items = soup.find_all('li', class_=re.compile(r'^menu-item'))  # Matches all menu items
        menu_structure = []

        for menu_item in menu_items:
            # Extract main menu item name and link
            anchor = menu_item.find('a')  # Find the anchor tag inside the menu item
            if not anchor:
                continue
            
            main_menu_name = anchor.get_text(strip=True)
            main_menu_link = urljoin(base_url, anchor['href'])  # Ensure links are absolute

            # Check for nested sub-menus
            sub_menu_items = menu_item.find_all('li', class_=re.compile(r'^menu-item'))
            sub_menu_list = [
                {
                    'name': sub_item.find('a').get_text(strip=True),
                    'link': urljoin(base_url, sub_item.find('a')['href'])
                }
                for sub_item in sub_menu_items if sub_item.find('a')
            ]

            # Add to the menu structure
            menu_structure.append({
                'name': main_menu_name,
                'link': main_menu_link,
                'sub_menu': sub_menu_list
            })

        # Step 2: Crawl the website
        st.write("Starting crawling process...")
        unique_sentences = set()  # Set to store unique sentences

        while urls_n:
            current_url = urls_n.pop(0)
            urls_v.append(current_url)
            st.sidebar.write(f"Crawling: {current_url}")

            try:
                response = requests.get(current_url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')

                # Extract text content
                text_chunks = [p.get_text() for p in soup.find_all('p')]
                cleaned_text = " ".join(text_chunks)
                cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

                # Add unique sentences
                sentences = cleaned_text.split('. ')
                for sentence in sentences:
                    unique_sentences.add(sentence.strip())

                # Extract additional URLs
                image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.pdf')
                for a_tag in soup.find_all('a', href=True):
                    href = a_tag.get('href')
                    if href and not href.lower().endswith(image_extensions):
                        full_url = urljoin(base_url, href)
                        if full_url.startswith(base_url) and full_url not in urls_v and full_url not in urls_n:
                            urls_n.append(full_url)
            except requests.RequestException as e:
                st.write(f"Error processing {current_url}: {e}")

        # Combine unique sentences into a single text
        all_text = ". ".join(unique_sentences) + "."
        st.write("Crawling complete!")
        st.write(f"Total Unique Sentences: {len(unique_sentences)}")
       

    except Exception as e:
        st.write(f"Error: {e}")
    return all_text

st.write(extract_and_crawl(base_url))
