import os
import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import streamlit.components.v1 as components
from pdf2image import convert_from_path
import pytesseract
import tempfile

# Load API key from environment variable
API_KEY = os.getenv("GOOGLE_API_KEY")

def configure_genai():
    """Configure the Gemini AI with the API key."""
    if not API_KEY:
        st.error("API Key is missing. Please set the GENAI_API_KEY environment variable.")
        return False
    try:
        genai.configure(api_key=API_KEY)
        return True
    except Exception as e:
        st.error(f"Error configuring Google API: {str(e)}")
        return False

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file, including scanned PDFs."""
    try:
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(pdf_file.read())
            temp_file_path = temp_file.name

        # Attempt to extract text using PyPDF2
        pdf_reader = PdfReader(temp_file_path)
        text = "\n".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())
        
        # If no text is extracted, use OCR
        if not text.strip():
            st.warning("No text could be extracted from the PDF. Attempting OCR...")
            images = convert_from_path(temp_file_path)  # Convert PDF pages to images
            ocr_text = ""
            for i, image in enumerate(images):
                ocr_text += pytesseract.image_to_string(image) + "\n"
            if not ocr_text.strip():
                st.error("OCR failed to extract text. Ensure the PDF contains readable text or images.")
                return None
            return ocr_text.strip()
        
        return text.strip()
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return None
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

def create_mindmap_markdown(text):
    """Generate mindmap markdown using Gemini AI."""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        max_chars = 30000
        if len(text) > max_chars:
            text = text[:max_chars] + "..."
            st.warning(f"Text was truncated to {max_chars} characters due to length limitations.")
        
        prompt = """
        Create a hierarchical markdown mindmap from the following text. 
        Use proper markdown heading syntax (# for main topics, ## for subtopics, ### for details).
        Focus on the main concepts and their relationships.
        Include relevant details and connections between ideas.
        Keep the structure clean and organized.
        
        Format the output exactly like this example:
        # Main Topic
        ## Subtopic 1
        ### Detail 1
        - Key point 1
        - Key point 2
        ### Detail 2
        ## Subtopic 2
        ### Detail 3
        ### Detail 4
        
        Text to analyze: {text}
        
        Respond only with the markdown mindmap, no additional text.
        """
        
        response = model.generate_content(prompt.format(text=text))
        if not response.text or not response.text.strip():
            st.error("Received empty response from Gemini AI")
            return None
        return response.text.strip()
    except Exception as e:
        st.error(f"Error generating mindmap: {str(e)}")
        return None

def create_markmap_html(markdown_content):
    """Create HTML with enhanced Markmap visualization."""
    markdown_content = markdown_content.replace('`', '\\`').replace('${', '\\${')
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            #mindmap {{
                width: 100%;
                height: 600px;
                margin: 0;
                padding: 0;
            }}
        </style>
        <script src="https://cdn.jsdelivr.net/npm/d3@6"></script>
        <script src="https://cdn.jsdelivr.net/npm/markmap-view"></script>
        <script src="https://cdn.jsdelivr.net/npm/markmap-lib@0.14.3/dist/browser/index.min.js"></script>
    </head>
    <body>
        <svg id="mindmap"></svg>
        <script>
            window.onload = async () => {{
                try {{
                    const markdown = `{markdown_content}`;
                    const transformer = new markmap.Transformer();
                    const {{root}} = transformer.transform(markdown);
                    const mm = new markmap.Markmap(document.querySelector('#mindmap'), {{
                        maxWidth: 300,
                        color: (node) => {{
                            const level = node.depth;
                            return ['#2196f3', '#4caf50', '#ff9800', '#f44336'][level % 4];
                        }},
                        paddingX: 16,
                        autoFit: true,
                        initialExpandLevel: 2,
                        duration: 500,
                    }});
                    mm.setData(root);
                    mm.fit();
                }} catch (error) {{
                    console.error('Error rendering mindmap:', error);
                    document.body.innerHTML = '<p style="color: red;">Error rendering mindmap. Please check the console for details.</p>';
                }}
            }};
        </script>
    </body>
    </html>
    """

def convert_html_to_pdf(html_content):
    """Convert HTML content to PDF."""
    try:
        from weasyprint import HTML
        pdf = HTML(string=html_content).write_pdf()
        return pdf
    except Exception as e:
        st.error(f"Error converting HTML to PDF: {str(e)}")
        return None

def generate_questions_from_text(text):
    """Generate questions from the given text using Google Generative AI."""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        prompt = """
        Based on the following text, generate a list of questions that test comprehension and understanding of the content. 
        Provide the questions in a numbered list format.

        Text:
        {text}

        Respond only with the list of questions.
        """
        response = model.generate_content(prompt.format(text=text))
        if not response.text or not response.text.strip():
            st.error("Received empty response from Gemini AI")
            return None
        return response.text.strip().split("\n")  # Split the response into a list of questions
    except Exception as e:
        st.error(f"Error generating questions: {str(e)}")
        return None

def main():
    st.set_page_config(layout="wide")
    st.title("📄 PDF to Mindmap Converter")
    st.markdown("Convert your PDF content into an interactive mindmap.")

    if not configure_genai():
        return

    uploaded_file = st.file_uploader("📥 Choose a PDF file", type="pdf")
    if uploaded_file is not None:
        with st.spinner("🔄 Processing PDF and generating mindmap..."):
            text = extract_text_from_pdf(uploaded_file)
            if text:
                st.info(f"✅ Successfully extracted {len(text)} characters from PDF")
                markdown_content = create_mindmap_markdown(text)
                if markdown_content:
                    tab1, tab2, tab3 = st.tabs(["📊 Mindmap", "📝 Markdown", "❓ Questions"])
                    
                    with tab1:
                        st.subheader("🌳 Interactive Mindmap")
                        html_content = create_markmap_html(markdown_content)
                        st.download_button(
                            label="⬇️ Download Mindmap",
                            data=html_content,
                            file_name="interactive_mindmap.html",
                            mime="text/html",
                            key="download_html"
                        )
                        components.html(html_content, height=700, scrolling=True)
                    
                    with tab2:
                        st.subheader("📝 Generated Markdown")
                        st.download_button(
                            label="⬇️ Download Markdown",
                            data=markdown_content,
                            file_name="mindmap.md",
                            mime="text/markdown",
                            key="download_markdown"
                        )
                        st.text_area("Markdown Content", markdown_content, height=400)

                    with tab3:
                        st.subheader("❓ Questions and Topic Importance")
                        if st.button("Generate Questions"):
                            with st.spinner("🔄 Generating questions and analyzing topic importance..."):
                                questions = generate_questions_from_text(text)
                                if questions:
                                    st.markdown("### Generated Questions:")
                                    for question in questions:
                                        st.markdown(f"- {question}")
                                else:
                                    st.error("Failed to generate questions. Please try again.")

if __name__ == "__main__":
    main()
