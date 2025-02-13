import streamlit as st
import base64
from google.cloud import aiplatform
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel, Part, SafetySetting
import os
import time

# Set the path to your service account JSON file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './snap-code.json'

# Initialize Google Cloud project
project_id = "snapcode-434710"
aiplatform.init(project=project_id)

# Initialize the Gemini model
model = GenerativeModel("gemini-2.0-flash-001")

# Enable wide mode
st.set_page_config(layout="wide")

# Custom CSS for a clean, unique UI with your colors
st.markdown(f"""
    <style>
        .block-container {{
            padding: 2rem;
        }}
            a {{
            text-decoration:none !important;
            }}
        .main-header {{
            text-align: center;
            background-color: #142850;
            color: #fff !important;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            margin-bottom: 20px;
        }}
        .main-header h1 {{
            font-size: 2.2rem;
            margin: 0;
            padding-top:0;
            color:#fff;  
        }}
        .main-header p {{
            color: #DDE6ED;
             margin-bottom: 0px;
        }}
        .stButton button, .download-btn {{
            background-color: #142850;
            color: white !important;
            border-radius: 10px;
            padding: 10px;
            width: 100%;
             text-decoration:none !importat;
          
        }}
        .stButton button:hover {{
            background-color: #142850;
        }}
            .element-container img{{
              width:400px !important;
            height:300px !important;
            object-fit:cover;
            }}
        .image-preview, .code-display {{
            padding: 20px;
            background-color: #DDE6ED;
            border-radius: 10px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        }}
    </style>
""", unsafe_allow_html=True)

# Header section
st.markdown("""
    <div class="main-header">
        <h1>UI Automation Tool</h1>
        <p>Turn images into code with the power of AI</p>
    </div>
""", unsafe_allow_html=True)

# Function to get the appropriate prompt based on the selected frontend
def get_prompt(frontend):
    base_prompt = "Task: You are an expert web developer tasked with creating a single-page app from a given screenshot using the specified technology stack. Ensure the app precisely matches the screenshot visually, including layout structure, grid, container, fluid-containers, rows, columns, background color, text color, font size, font family, padding, margin, and alignment. dobule check the colour code and should match with given screenshot visually, im expecting 100% match"
    
    if frontend == "HTML5 + Tailwind":
        return """You are an expert HTML5 and Tailwind developer. 
        You take screenshots of a reference web page from the user, and then build single page apps 
        using Tailwind, HTML, and JS.
        - Make sure the app looks exactly like the screenshot.
        - cross check the layout style, container, grid, or fluid layout
        - Pay close attention to background color, text color, font size, font family, padding, margin, border, etc.
        - For images, use placeholder images from https://placehold.co and include a detailed description of the image in the alt text.
        - Use this script to include Tailwind: <script src="https://cdn.tailwindcss.com"></script>
        -Do not include markdown ```html at the start or end.
        -make sure optmize the css inside the <style> tag and minimize and make it to singleline the  CSS.
        Return the full code in <html></html> tags.
        """

    elif frontend == "HTML5 + CSS":
        return base_prompt + """
        You are an expert html5 and CSS developer. 
        You take screenshots of a reference web page from the user, and then build single page apps 
        using CSS, HTML, and JS.
        - Make sure the app looks exactly like the screenshot.
         - cross check the layout style, container, grid, or fluid layout
        - Pay close attention to background color, text color, font size, font family, padding, margin, border, etc.
        - For images, use placeholder images from https://placehold.co and include a detailed description of the image in the alt text.
        -Do not include markdown ```html "```" or "```html" at the start or end.
        -make sure optmize the css inside the <style> tag and minimize and make it to singleline the  CSS.
        -Return the full code in <html></html> tags.
        """

    elif frontend == "HTML5 + Bootstrap5":
        return """You are an expert html5 and Bootstrap developer. 
        You take screenshots of a reference web page from the user, and then build single page apps 
        using Bootstrap, HTML, and JS.
        - Make sure the app looks exactly like the screenshot.
         - cross check the layout style, container, grid, or fluid layout
        - Dont' include helper classes in <style> tags, use boostrap html helper classes.
        - Pay close attention to background color, text color, font size, font family, padding, margin, border, etc.
        - For images, use placeholder images from https://placehold.co and include a detailed description of the image in the alt text.
        - Use Bootstrap 5: <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
         -Do not include markdown ```html "```" or "```html"  ```html ```at the start or end.
        - If you include bootstrap.min.css in <link> tag dont repeat css in <style> tag
        - Minimize the css  inside the <style> tag by only including mandataory styles. use bootstrap classes for layout, such as rows and columns, ad ensure responsiveness
        - Return the full code in <html></html> tags.
        """

    elif frontend == "React + Tailwind":
        return base_prompt + """
        You are an expert React/Tailwind developer. 
        You take screenshots of a reference web page from the user, and then build single page apps 
        using React and Tailwind CSS.
        - Make sure the app looks exactly like the screenshot.
         - cross check the layout style, container, grid, or fluid layout
        - Pay close attention to background color, text color, font size, font family, padding, margin, border, etc.
        - Use these scripts to include React and Tailwind:
          <script src="https://unpkg.com/react/umd/react.development.js"></script>
          <script src="https://unpkg.com/react-dom/umd/react-dom.development.js"></script>
          <script src="https://unpkg.com/@babel/standalone/babel.js"></script>
          <script src="https://cdn.tailwindcss.com"></script>
        - Return the full code in <html></html> tags.
        - Do not include markdown "```" or "```html" at the start or end.
        - Make sure optmize the css inside the <style> tag and minimize and make it to singleline the  CSS.
        """

    elif frontend == "Ionic + Tailwind":
        return base_prompt + """
        You are an expert Ionic/Tailwind developer. 
        You take screenshots of a reference web page from the user, and then build single page apps 
        using Ionic and Tailwind CSS.
        - Make sure the app looks exactly like the screenshot.
        - Pay close attention to background color, text color, font size, font family, padding, margin, border, etc.
        - Use these scripts to include Ionic and Tailwind:
          <script type="module" src="https://cdn.jsdelivr.net/npm/@ionic/core/dist/ionic/ionic.esm.js"></script>
          <script nomodule src="https://cdn.jsdelivr.net/npm/@ionic/core/dist/ionic/ionic.js"></script>
          <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@ionic/core/css/ionic.bundle.css" />
          <script src="https://cdn.tailwindcss.com"></script>
        - Return the full code in <html></html> tags.
        - Do not include markdown "```" or "```html" at the start or end.
        - Make sure optmize the css inside the <style> tag and minimize and make it to singleline the  CSS.
       
        """

    return ""


# Download button function
def download_button(code, filename="generated_code.html"):
    b64 = base64.b64encode(code.encode()).decode()  # Encode the code to base64
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}" class="download-btn">Download the generated code</a>'
    st.markdown(href, unsafe_allow_html=True)

# Create a 40:60 column layout
col1, col2, col3 = st.columns([1, 2.5, 1], gap="medium")

# Left side: File upload and technology selection (40%)
with col1:
    st.markdown("### Technology Selection")

    # Frontend technology selection
    frontend_options = ["HTML5 + Tailwind", "HTML5 + CSS", "HTML5 + Bootstrap5", "React + Tailwind", "Ionic + Tailwind", "Vz Brand"]
    selected_frontend = st.selectbox("Select Technology:", frontend_options)
   # Submit button
    submit = st.button("Submit")
# Middle section: Image Upload and Code Generation
with col2:
    st.markdown("### Upload Screenshot and Generate Code")

    # Image preview section
    uploaded_image = st.file_uploader("Upload a screenshot (PNG, JPG, JPEG):", type=["png", "jpg", "jpeg"])

    if uploaded_image:
        # Display uploaded image
        st.image(uploaded_image, caption="Uploaded Screenshot", use_column_width=True)

 

    # Code generation logic
    if uploaded_image and submit:
        try:
            # Convert the uploaded image to base64
            image_data = base64.b64encode(uploaded_image.read()).decode('utf-8')
            image_part = Part.from_data(mime_type=uploaded_image.type, data=base64.b64decode(image_data))

            # Get the appropriate prompt based on the selected frontend
            prompt = get_prompt(selected_frontend)

            if not prompt:
                st.error("Prompt generation failed. Please check the selected frontend.")
            else:
                st.info("Generating code...")

                # Progress status
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.02)
                    progress_bar.progress(i + 1)

                generation_config = {
                    "max_output_tokens": 8192,
                    "temperature": 1,
                    "top_p": 0.95,
                }

                safety_settings = [
                    SafetySetting(
                        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
                    ),
                    SafetySetting(
                        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
                    ),
                    SafetySetting(
                        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
                    ),
                    SafetySetting(
                        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
                        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
                    ),
                ]

                # Generate code based on the image and selected frontend prompt
                responses = model.generate_content(
                    [image_part, prompt],
                    generation_config=generation_config,
                    safety_settings=safety_settings,
                    stream=True,
                )

                # Combine all parts of the generated response
                result = "".join([response.text for response in responses])

                # Display the generated code
                st.code(result, language='html' if 'HTML5' in selected_frontend else 'jsx')

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.balloons()

# Right side: Actions section
with col3:
    st.markdown("### Actions")

    # Add a download button to download the generated code
    if 'result' in locals() and result:
        download_button(result)
