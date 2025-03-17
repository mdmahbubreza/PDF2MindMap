# PDF2FlowChart

PDF2FlowChart is a web application that converts a PDF document into a hierarchical mindmap (flowchart) visualization. It extracts text from your PDF, uses Google's Generative AI to generate a structured markdown mindmap, and then renders an interactive visualization using Markmap.

## Features

- **PDF Text Extraction:** Uses [PyPDF2](https://pypi.org/project/PyPDF2/) to extract text from PDF files.
- **Mindmap Generation:** Leverages [Google Generative AI](https://developers.generativeai.google/) (Gemini AI) to convert extracted text into a hierarchical markdown mindmap.
- **Interactive Visualization:** Displays an interactive mindmap using [Markmap](https://markmap.js.org/) and D3.js.
- **Streamlit Interface:** Provides an easy-to-use web interface with [Streamlit](https://streamlit.io/).

## Prerequisites

- **Python 3.7+**
- Required Python libraries:
  - `streamlit`
  - `google-generativeai`
  - `PyPDF2`
- A valid Google API key for the Generative AI service. Replace the placeholder in the code with your API key.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/mdmahbubreza/PDF2FlowChart.git
   cd PDF2FlowChart
   ```

2. **Create a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   If a `requirements.txt` file is not provided, you can install dependencies manually:

   ```bash
   pip install streamlit google-generativeai PyPDF2
   ```

## Configuration

Before running the application, open the `app.py` file and replace the placeholder API key with your actual Google API key:

```python
API_KEY = "PASTE API KEY"  # Replace with your Google API key
```

## Usage

1. **Run the Application:**

   ```bash
   streamlit run app.py
   ```

2. **Upload a PDF File:**
   - Once the application is running, use the file uploader to select your PDF.
   - The app will extract text from the PDF and generate a markdown mindmap.

3. **View the Results:**
   - The generated mindmap will be displayed interactively.
   - You can switch between the rendered mindmap and the markdown text.
   - A download button is available to save the generated markdown as `mindmap.md`.

## How It Works

1. **Text Extraction:**  
   The application reads your PDF file and extracts text from each page using PyPDF2.

2. **Mindmap Creation:**  
   The extracted text is sent to the Google Generative AI model (Gemini AI) with a prompt to generate a structured markdown mindmap. The prompt is designed to output a hierarchical format using markdown headings.

3. **Visualization:**  
   The markdown output is converted into an interactive flowchart using Markmap and D3.js, allowing you to visually explore the main concepts and their relationships.

## Troubleshooting

- **Empty PDF Extraction:**  
  If no text is extracted, ensure that the PDF is not a scanned image. You may need to use OCR tools for scanned documents.

- **API Key Issues:**  
  Make sure your Google API key is valid and correctly configured in `app.py`.

- **Text Length Warning:**  
  The application limits the text input to 30,000 characters. If your document exceeds this length, the text will be truncated, and a warning will be displayed.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve the project.

## License

This project is open source and available under the [MIT License](./LICENSE).
