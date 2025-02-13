# UI Automation Tool

This project is a UI Automation Tool that converts images into code using the power of AI. It leverages Streamlit for the web interface and Google's Vertex AI for generating code from screenshots.

## Features

- Upload a screenshot and generate code using various frontend technologies.
- Supports HTML5 with Tailwind, CSS, Bootstrap5, React with Tailwind, and Ionic with Tailwind.
- Customizable UI with a clean and unique design.
- Download the generated code as an HTML file.

## Setup

1. Clone the repository:
    ```sh
   git clone https://github.com/gopinadh516/codegenerator.git
    cd codegenerator
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Set up your Google Cloud service account:
    - Place your service account JSON file in the project directory and name it [snap-code.json](http://_vscodecontentref_/2).

4. Run the Streamlit app:
    ```sh
    streamlit run app.py
    ```

## Usage

1. Open the Streamlit app in your browser.
2. Select the frontend technology from the dropdown menu.
3. Upload a screenshot (PNG, JPG, JPEG).
4. Click the "Submit" button to generate the code.
5. View the generated code in the middle section.
6. Download the generated code using the download button in the right section.

## Project Structure

- [app.py](http://_vscodecontentref_/3): Main application file containing the Streamlit app and code generation logic.
- [snap-code.json](http://_vscodecontentref_/4): Google Cloud service account JSON file.
- [README.md](http://_vscodecontentref_/5): Project documentation.

## Dependencies

- Streamlit
- Google Cloud AI Platform
- Vertex AI Generative Models
- Google OAuth2
- Base64

## License

This project is licensed under the MIT License. See the LICENSE file for details.