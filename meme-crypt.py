import os
import random
import textwrap
import requests
from PIL import Image, ImageDraw, ImageFont
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

# Define directories
TEMPLATE_DIR = "templates"
OUTPUT_DIR = "generated_memes"

# Ensure directories exist
os.makedirs(TEMPLATE_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_meme_templates():
    """
    Fetches meme templates from Imgflip API.
    Returns a list of dictionaries with 'name' and 'url' keys.
    """
    api_url = "https://api.imgflip.com/get_memes"
    meme_templates = []

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        if not data['success']:
            print("Failed to fetch memes from Imgflip API.")
            return meme_templates

        memes = data['data']['memes']
        print(f"Fetched {len(memes)} meme templates from Imgflip.")

        for meme in memes:
            name = meme['name']
            url = meme['url']
            meme_templates.append({'name': name, 'url': url})

        return meme_templates

    except Exception as e:
        print(f"Error fetching meme templates: {e}")
        return meme_templates

def download_template(meme):
    """
    Downloads the meme template image if not already present.
    Returns the local file path of the template image.
    """
    name = meme['name']
    url = meme['url']
    # Sanitize filename
    filename = f"{name.lower().replace(' ', '_').replace(',', '').replace('\'', '').replace('?', '').replace(':', '').replace('/', '_')}.jpg"
    filepath = os.path.join(TEMPLATE_DIR, filename)

    if not os.path.isfile(filepath):
        try:
            print(f"Downloading meme template: {name}")
            img_data = requests.get(url, timeout=10)
            img_data.raise_for_status()
            with open(filepath, 'wb') as f:
                f.write(img_data.content)
            print(f"Downloaded and saved: {filename}")
        except Exception as e:
            print(f"Failed to download {name}: {e}")
            return None
    else:
        print(f"Template already exists: {filename}")

    return filepath

def generate_key_stream(message):
    """
    Generates a contextual key based on the input message using OpenAI's GPT with streaming.
    """
    prompt = (
        f"Given the following message, generate a contextual key that represents shared knowledge or context necessary to understand it.\n\n"
        f"Message: \"{message}\"\n\n"
        f"Contextual Key:"
    )
    
    key = ""
    
    try:
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )
        
        print("Generating key:", end=" ", flush=True)
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                key += delta.content
                print(delta.content, end="", flush=True)
                
        key = key.strip()
        print()
        return key
    except Exception as e:
        print(f"\nError generating key: {e}")
        return "General"

def select_template_llm(message, key, meme_templates):
    """
    Selects an appropriate meme template by providing the LLM with all available templates.
    Downloads the template image if it's not already downloaded.
    Returns the template name and its local file path.
    """
    template_list = "\n".join(f"- {meme['name']}" for meme in meme_templates)
    
    prompt = (
        f"You are a meme generator assistant. Given a message and a contextual key, select the most appropriate meme template from the following list.\n\n"
        f"Message: \"{message}\"\n"
        f"Contextual Key: \"{key}\"\n\n"
        f"Available Meme Templates:\n{template_list}\n\n"
        f"Please respond with the exact name of the most suitable meme template from the list above."
    )
    
    try:
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )
        
        chosen_template = ""
        print("Selecting meme template:", end=" ", flush=True)
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                chosen_template += delta.content
                print(delta.content, end="", flush=True)
        
        chosen_template = chosen_template.strip()
        print()
        # Find the meme in the list
        selected_meme = next((meme for meme in meme_templates if meme['name'].lower() == chosen_template.lower()), None)
        
        if selected_meme:
            # Download the template image if not already downloaded
            template_path = download_template(selected_meme)
            if template_path:
                return selected_meme['name'], template_path
            else:
                print("Failed to download the selected template. Falling back to random selection.")
        else:
            print(f"LLM selected an invalid template: '{chosen_template}'. Falling back to random selection.")
        
        # Fallback to random selection if LLM's choice is invalid
        return select_random_template(meme_templates)
        
    except Exception as e:
        print(f"Error selecting template: {e}. Falling back to random selection.")
        return select_random_template(meme_templates)

def select_random_template(meme_templates):
    """
    Selects a random meme template from the available templates.
    Downloads the template image if not already downloaded.
    Returns the template name and its local file path.
    """
    selected_meme = random.choice(meme_templates)
    print(f"Randomly selected template: {selected_meme['name']}")
    template_path = download_template(selected_meme)
    if template_path:
        return selected_meme['name'], template_path
    else:
        print("Failed to download the randomly selected template. Using default captions.")
        return selected_meme['name'], None

def generate_captions_stream(message, key, template_name):
    """
    Generates a caption for the meme using OpenAI's GPT with streaming.
    """
    prompt = (
        f"Create a meme caption for the '{template_name}' meme template.\n"
        f"The underlying message to convey is: \"{message}\"\n"
        f"The contextual key is: \"{key}\"\n\n"
        f"Provide an appropriate caption based on the template format."
    )
    
    caption = ""
    
    try:
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )
        
        print("Generating caption:", end=" ", flush=True)
        for chunk in stream:
            delta = chunk.choices[0].delta
            content = getattr(delta, 'content') or ''
            caption += content
            print(content, end="", flush=True)
        
        print()  # For newline after streaming
        caption = caption.strip() or "DEFAULT TEXT"
        return caption
    except Exception as e:
        print(f"\nError generating caption: {e}")
        return "DEFAULT TEXT"

def create_meme(template_path, caption, key):
    """
    Saves the image and caption separately inside a folder named after the key.
    """
    try:
        folder_path = os.path.join(OUTPUT_DIR, key)
        os.makedirs(folder_path, exist_ok=True)
        
        # Save image
        if template_path:
            img = Image.open(template_path)
        else:
            img = Image.new('RGB', (500, 500), color=(73, 109, 137))
        image_path = os.path.join(folder_path, "image.jpg")
        img.save(image_path)
        print(f"Image saved to {image_path}")
        
        # Save text
        text_path = os.path.join(folder_path, "caption.txt")
        with open(text_path, 'w') as f:
            f.write(caption)
        print(f"Caption saved to {text_path}")
    except Exception as e:
        print(f"Error saving meme components: {e}")

def main():
    """
    Main function to run the Enhanced Meme Generator.
    """
    print("\n🚀 Enhanced Meme Generator 3000 🚀\n")
    message = input("🔒 Secret message: ")
    if not message:
        print("❌ No message. Abort!")
        return

    print("\n🔑 Generating key...")
    key = generate_key_stream(message)
    print(f"🔑 Key: {key}")

    print("\n🖼️ Fetching meme templates...")
    meme_templates = fetch_meme_templates()
    if not meme_templates:
        print("❌ No templates. Abort!")
        return

    print("\n🤖 AI selecting template...")
    template_name, template_path = select_template_llm(message, key, meme_templates)
    print(f"🖼️ Template: {template_name or 'N/A'}")

    print("\n✍️ Generating caption...")
    caption = generate_captions_stream(message, key, template_name)
    print(f"📝 Caption: {caption}")

    print("\n💾 Saving meme components...")
    create_meme(template_path, caption, message[:20])
    print(f"✅ Meme components saved in folder: {os.path.join(OUTPUT_DIR, message[:20])}")

if __name__ == "__main__":
    main()
