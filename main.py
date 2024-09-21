import streamlit as st
import requests
import base64
from io import BytesIO
import urllib.parse

# Function to fetch image data from Pixabay API
def fetch_images(search_term):
    api_key = "46093786-16a74134e123471b002587ac0"
    url = f"https://pixabay.com/api/?key={api_key}&q={search_term}&image_type=photo"
    result = requests.get(url)
    return result.json()

# Function to create a download link for an image
def get_image_download_link(img_url, filename, text):
    response = requests.get(img_url)
    img = BytesIO(response.content)
    b64 = base64.b64encode(img.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{b64}" download="{filename}">{text}</a>'
    return href

# Function to create social media share links (with WhatsApp)
def get_share_links(img_url, title):
    encoded_url = urllib.parse.quote(img_url)
    encoded_title = urllib.parse.quote(title)
    
    facebook_url = f"https://www.facebook.com/sharer/sharer.php?u={encoded_url}"
    twitter_url = f"https://twitter.com/intent/tweet?url={encoded_url}&text={encoded_title}"
    pinterest_url = f"https://pinterest.com/pin/create/button/?url={encoded_url}&media={encoded_url}&description={encoded_title}"
    whatsapp_url = f"https://api.whatsapp.com/send?text={encoded_title} {encoded_url}"
    
    return facebook_url, twitter_url, pinterest_url, whatsapp_url

# Function to display images with download and share links
def display_images(image_list):
    col1, col2 = st.columns(2)
    for i in range(0, len(image_list), 2):
        with col1:
            st.image(image_list[i]['webformatURL'], caption="Uploader: "+image_list[i]['user'], width=340)
            download_link = get_image_download_link(image_list[i]['largeImageURL'], f"image{i}.jpg", "Download Here")
            st.markdown(download_link, unsafe_allow_html=True)
            
            # Add share buttons
            facebook_url, twitter_url, pinterest_url, whatsapp_url = get_share_links(image_list[i]['largeImageURL'], f"Check out this image from Pixabay!")
            st.markdown(f """
            Share: 
            <a href="{facebook_url}" target="_blank">Facebook</a> | 
            <a href="{twitter_url}" target="_blank">Twitter</a> | 
            <a href="{pinterest_url}" target="_blank">Pinterest</a> | 
            <a href="{whatsapp_url}" target="_blank">WhatsApp</a>
            """, unsafe_allow_html=True)
        
        if i + 1 < len(image_list):
            with col2:
                st.image(image_list[i+1]['webformatURL'], caption="Uploader: "+image_list[i+1]['user'], width=340)
                download_link = get_image_download_link(image_list[i+1]['largeImageURL'], f"image{i+1}.jpg", "Download Here")
                st.markdown(download_link, unsafe_allow_html=True)
                
                # Add share buttons
                facebook_url, twitter_url, pinterest_url, whatsapp_url = get_share_links(image_list[i+1]['largeImageURL'], f"Check out this image from Pixabay!")
                st.markdown(f """
                Share: 
                <a href="{facebook_url}" target="_blank">Facebook</a> | 
                <a href="{twitter_url}" target="_blank">Twitter</a> | 
                <a href="{pinterest_url}" target="_blank">Pinterest</a> | 
                <a href="{whatsapp_url}" target="_blank">WhatsApp</a>
                """, unsafe_allow_html=True)

# Main function for the Streamlit app
def main():
    st.title("Pixabay Search Engine 📷")
    
    # User inputs the search keyword
    search_term = st.text_input("Enter the image search keyword")
    if st.button("Search"):
        if search_term:
            # Fetch image data based on search term
            image_data = fetch_images(search_term)
            
            if 'hits' in image_data:
                st.write(f"Displaying results for: {search_term}")
                display_images(image_data['hits'])
            else:
                st.write("No results found!")
        else:
            st.warning("Please enter a phrase in the search box!")

# Run the app
if __name__ == "__main__":
    main()
