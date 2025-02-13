# Installation Guide for UI Automation Tool

Follow these steps to set up and run the UI Automation Tool on your local machine.

## Prerequisites

- Python 3.7 or higher
- Git
- Google Cloud account with Vertex AI enabled

## Setup

1. **Clone the repository:**
    ```sh
    git clone https://github.com/your-repo/ui-automation-tool.git
    cd ui-automation-tool
    ```

2. **Create and activate a virtual environment (optional but recommended):**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required Python packages:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up your Google Cloud service account:**
    - Place your service account JSON file in the project directory and name it `snap-code.json`.

5. **Run the Streamlit app:**
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

## Troubleshooting

- Ensure all dependencies are installed correctly.
- Verify that the Google Cloud service account JSON file is correctly placed and named `snap-code.json`.
- Check the Streamlit app logs for any errors and resolve them accordingly.

## Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google Cloud Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)