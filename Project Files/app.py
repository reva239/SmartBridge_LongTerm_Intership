import streamlit as st
import google.generativeai as genai
import random
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Validate API key-
api_key = os.environ.get("GOOGLE_GEMINI_API_KEY")
if not api_key:
    st.error("GOOGLE_GEMINI_API_KEY environment variable is not set. Please configure it to use this app.")
    st.stop()

genai.configure(api_key=api_key)

# Page configuration
st.set_page_config(
    page_title="Flavour Fusion - AI Recipe Blogging",
    page_icon="🍳",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #0b1220 0%, #111827 100%);
        color: #e5e7eb;
    }
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #1f2937 0%, #111827 55%, #0f172a 100%);
        padding: 2rem;
        border-radius: 12px;
        color: #f9fafb;
        margin-bottom: 2rem;
        border: 1px solid #374151;
        box-shadow: 0 8px 22px rgba(0, 0, 0, 0.35);
    }
    .section-card {
        background-color: rgba(17, 24, 39, 0.75);
        border: 1px solid #374151;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 1rem;
        color: #d1d5db;
    }
    .section-title {
        margin: 0 0 0.35rem 0;
        font-size: 1.05rem;
        color: #f3f4f6;
    }
    .section-subtitle {
        margin: 0;
        font-size: 0.9rem;
        color: #9ca3af;
    }
    .recipe-container {
        background-color: #111827;
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid #374151;
        border-left: 4px solid #22d3ee;
        margin-top: 1rem;
        color: #e5e7eb;
    }
    .stTextInput > div > div > input,
    .stNumberInput input,
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #1f2937 !important;
        color: #f3f4f6 !important;
        border: 1px solid #4b5563 !important;
        border-radius: 10px !important;
    }
    .stTextInput label,
    .stNumberInput label,
    .stSelectbox label {
        color: #d1d5db !important;
    }
    .stDownloadButton > button,
    .stButton > button {
        background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%);
        color: #ffffff;
        border: none;
        border-radius: 10px;
        font-weight: 600;
    }
    .stDownloadButton > button:hover,
    .stButton > button:hover {
        background: linear-gradient(135deg, #0284c7 0%, #1d4ed8 100%);
    }
    .stAlert {
        background-color: #1f2937;
        border: 1px solid #374151;
    }
    .stCaption {
        color: #9ca3af !important;
    }
    hr {
        border: none;
        border-top: 1px solid #374151;
        margin: 1.2rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for recipe history
if "recipe_history" not in st.session_state:
    st.session_state.recipe_history = []

# Generation configuration
generation_config = {
    "temperature": 0.75,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

def get_joke():
    """Get a random programming or food-related joke."""
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why don't skeletons fight each other? They don't have the guts.",
        "What do you call fake spaghetti? An impasta!",
        "Why did the bicycle fall over? Because it was two-tired!",
        "Why did the math book look sad? Because it had too many problems.",
        "What do you call cheese that isn't yours? Nacho cheese!",
        "Why can't your nose be 12 inches long? Because then it would be a foot!",
        "Why did the golfer bring two pairs of pants? In case he got a hole in one!",
        "What do you call a bear with no teeth? A gummy bear!",
        "Why did the cookie go to the doctor? Because it felt crumbly!",
        "What did the chef say when he criticized the pasta? 'It was an impasta!'"
    ]
    return random.choice(jokes)

# gemini-1.5-flash model is not supported for generateContention tasks, using gemini-2.5-flash instead
@st.cache_resource
def get_model():
    """Initialize the generative model with caching."""
    return genai.GenerativeModel("gemini-2.5-flash", generation_config=generation_config)

def recipe_generator(user_input, word_count, cuisine_type=None):
    """
    Generate a recipe using Google Generative AI.
    
    Args:
        user_input (str): The recipe topic/ingredient
        word_count (int): Desired word count
        cuisine_type (str): Optional cuisine type filter
    
    Returns:
        str: Generated recipe or empty string if failed
    """
    model = get_model()
    
    # Enhanced prompt for better recipes
    prompt = f"""Write a detailed and engaging recipe blog post about '{user_input}' 
    with approximately {word_count} words. {f'Focus on {cuisine_type} cuisine.' if cuisine_type else ''}
    
    Include:
    - Brief introduction about the dish
    - Ingredients list with quantities
    - Step-by-step cooking instructions
    - Tips and tricks
    - Serving suggestions
    - Nutritional information (approximate)
    - Storage and reheating instructions
    
    Make it engaging, informative, and easy to follow."""
    
    try:
        with st.spinner("🍳 Cooking up your recipe..."):
            chat_session = model.start_chat(history=[])
            response = chat_session.send_message(prompt)
            return response.text
    except Exception as e:
        st.error(f"❌ Error generating recipe: {str(e)}")
        return ""

def save_recipe_to_history(topic, recipe, word_count, cuisine):
    """Save generated recipe to session history."""
    st.session_state.recipe_history.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "topic": topic,
        "cuisine": cuisine,
        "word_count": word_count,
        "recipe": recipe
    })

def download_recipe(recipe_text, filename="recipe.txt"):
    """Generate download link for recipe."""
    return recipe_text.encode('utf-8')

# Main header
st.markdown("""
    <div class="main-header">
        <h1>🍳 Flavour Fusion</h1>
        <p style="font-size: 1.2rem; margin: 0;">AI-Driven Recipe Blogging</p>
        <p style="font-size: 0.9rem; margin: 0.5rem 0 0 0;">Create unique, customized recipes powered by Google Gemini AI</p>
    </div>
""", unsafe_allow_html=True)

# Default settings (no sidebar needed)
show_joke = True
save_history = True

# Main content
st.markdown("""
    <div class="section-card">
        <h3 class="section-title">✨ Build Your Recipe Blog Post</h3>
        <p class="section-subtitle">Choose a topic, cuisine style, and word count, then generate a complete, ready-to-use recipe article.</p>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    user_input = st.text_input(
        "🌶️ Recipe Topic",
        placeholder="e.g., Spicy Thai Curry",
        help="Enter the main ingredient or recipe type"
    )

with col2:
    word_count = st.number_input(
        "📝 Word Count",
        min_value=100,
        max_value=5000,
        value=500,
        step=100,
        help="Desired length of the recipe in words"
    )

cuisine_type = st.selectbox(
    "🍽️ Cuisine Type (Optional)",
    ["Any", "Italian", "Indian", "Chinese", "Mexican", "Mediterranean", "Asian Fusion", "American", "French"]
)

st.markdown("<hr>", unsafe_allow_html=True)

# Generate button
if st.button("🚀 Generate Recipe", use_container_width=True, type="primary"):
    if not user_input.strip():
        st.warning("⚠️ Please enter a recipe topic to generate a recipe!")
    else:
        # Show joke if enabled
        if show_joke:
            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown("😂")
            with col2:
                st.info(f"**Joke Time:** {get_joke()}")
        
        # Generate recipe
        cuisine_filter = None if cuisine_type == "Any" else cuisine_type
        recipe = recipe_generator(user_input, word_count, cuisine_filter)
        
        if recipe:
            # Save to history
            if save_history:
                save_recipe_to_history(user_input, recipe, word_count, cuisine_type)
            
            # Display recipe
            st.success("✨ Your recipe has been generated successfully!")
            
            st.markdown("""
                <div class="recipe-container">
            """, unsafe_allow_html=True)
            
            st.markdown(f"### 📖 Recipe: {user_input.title()}")
            if cuisine_type != "Any":
                st.caption(f"🍽️ Cuisine: {cuisine_type} | 📝 Word Count: {word_count}")
            
            st.markdown(recipe)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Download button
            recipe_bytes = download_recipe(recipe)
            st.download_button(
                label="📥 Download Recipe",
                data=recipe_bytes,
                file_name=f"{user_input.replace(' ', '_')}_recipe.txt",
                mime="text/plain"
            )
