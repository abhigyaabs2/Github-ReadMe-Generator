import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv
import zipfile
import tempfile

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="GitHub README Generator",
    page_icon="📝",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .stDownloadButton button {
        width: 100%;
        background-color: #28a745;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header"><h1>📝 GitHub README Generator</h1><p>Upload your project files and get a professional README.md instantly!</p></div>', unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Key input
    default_api_key = os.getenv("OPENAI_API_KEY", "")
    api_key = st.text_input(
        "OpenAI API Key",
        value=default_api_key,
        type="password",
        help="Enter your OpenAI API key or set it in .env file"
    )
    
    if default_api_key:
        st.success("✅ API key loaded from environment")
    
    st.markdown("---")
    
    # README Style Options
    st.subheader("📋 README Style")
    readme_style = st.selectbox(
        "Choose style",
        ["Professional", "Minimalist", "Detailed", "Open Source"]
    )
    
    include_badges = st.checkbox("Include badges", value=True)
    include_toc = st.checkbox("Include Table of Contents", value=True)
    include_screenshots = st.checkbox("Include screenshot placeholders", value=False)
    
    st.markdown("---")
    
    # Project metadata
    st.subheader("📊 Project Info (Optional)")
    project_name = st.text_input("Project Name", placeholder="my-awesome-project")
    project_description = st.text_area(
        "Brief Description",
        placeholder="A brief description of your project...",
        height=100
    )
    
    st.markdown("---")
    st.markdown("### 💡 Tips:")
    st.markdown("""
    - Upload multiple files for better analysis
    - Include main code files and dependencies
    - Supported: .py, .js, .json, .txt, .md
    - Max file size: 200MB total
    """)

# Main content area
tab1, tab2 = st.tabs(["📁 Upload Files", "✍️ Paste Code"])

with tab1:
    st.markdown("### Upload Project Files")
    uploaded_files = st.file_uploader(
        "Choose files from your project",
        accept_multiple_files=True,
        type=['py', 'js', 'jsx', 'ts', 'tsx', 'json', 'txt', 'md', 'html', 'css', 'java', 'cpp', 'c', 'go', 'rs', 'rb', 'php'],
        help="Upload your main code files, package.json, requirements.txt, etc."
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) uploaded")
        with st.expander("📄 View uploaded files"):
            for file in uploaded_files:
                st.text(f"• {file.name} ({file.size} bytes)")

with tab2:
    st.markdown("### Paste Your Code")
    code_input = st.text_area(
        "Paste your main code file or project structure",
        height=400,
        placeholder="""Paste your code here, for example:

# main.py
import streamlit as st

def main():
    st.title("My App")
    
if __name__ == "__main__":
    main()
"""
    )

# Additional context
st.markdown("### 📝 Additional Context (Optional)")
additional_context = st.text_area(
    "Add any special instructions or information",
    placeholder="e.g., 'This is a machine learning project for image classification', 'Focus on deployment instructions', etc.",
    height=100
)

# Generate README button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    generate_button = st.button(
        "🚀 Generate README",
        type="primary",
        use_container_width=True
    )

# Generate README logic
if generate_button:
    # Validation
    if not api_key:
        st.error("⚠️ Please provide your OpenAI API key in the sidebar")
    elif not uploaded_files and not code_input:
        st.error("⚠️ Please upload files or paste code to analyze")
    else:
        with st.spinner("🤖 AI is analyzing your project and generating README..."):
            try:
                # Prepare project content
                project_content = ""
                
                # Process uploaded files
                if uploaded_files:
                    project_content += "=== PROJECT FILES ===\n\n"
                    for file in uploaded_files:
                        try:
                            content = file.read().decode('utf-8', errors='ignore')
                            project_content += f"--- {file.name} ---\n{content}\n\n"
                        except Exception as e:
                            st.warning(f"⚠️ Could not read {file.name}: {str(e)}")
                
                # Add pasted code
                if code_input:
                    project_content += f"=== PASTED CODE ===\n{code_input}\n\n"
                
                # Add metadata
                metadata = f"""
Project Name: {project_name if project_name else 'Not provided'}
Project Description: {project_description if project_description else 'Not provided'}
Additional Context: {additional_context if additional_context else 'None'}
README Style: {readme_style}
Include Badges: {include_badges}
Include TOC: {include_toc}
Include Screenshots: {include_screenshots}
"""
                
                # Initialize LLM
                llm = ChatOpenAI(
                    model="gpt-4o-mini",
                    temperature=0.7,
                    api_key=api_key
                )
                
                # Create prompt based on style
                style_instructions = {
                    "Professional": "Create a professional, corporate-style README with clear sections and formal language.",
                    "Minimalist": "Create a clean, minimal README with only essential information. Keep it concise.",
                    "Detailed": "Create a comprehensive README with detailed explanations, examples, and troubleshooting sections.",
                    "Open Source": "Create an open-source friendly README with contribution guidelines, code of conduct references, and community-focused language."
                }
                
                system_prompt = f"""You are an expert technical writer specializing in GitHub README files. 
Analyze the provided project files and generate a professional, well-structured README.md file.

Style Guide: {style_instructions[readme_style]}

README Structure:
1. Project Title with description
2. {"Badges (build status, version, license, etc.)" if include_badges else ""}
3. {"Table of Contents" if include_toc else ""}
4. About / Overview
5. Key Features (bullet points)
6. Tech Stack / Built With
7. Getting Started
   - Prerequisites
   - Installation
8. Usage (with code examples if possible)
9. Project Structure (if complex)
10. Configuration (if applicable)
11. {"Screenshots section with placeholders" if include_screenshots else ""}
12. Roadmap / Future Enhancements
13. Contributing
14. License
15. Contact / Author
16. Acknowledgments

Important Guidelines:
- Use proper Markdown formatting
- Include code blocks with syntax highlighting
- Make installation steps clear and numbered
- Add emojis for visual appeal (but not excessive)
- Infer tech stack from file extensions and imports
- Generate realistic examples based on the code
- Be specific about what the project does
- Include placeholder text for sections that need user input (like screenshots)
"""
                
                user_prompt = f"""Analyze this project and generate a complete README.md:

{metadata}

PROJECT CONTENT:
{project_content[:15000]}

Generate a complete, professional README.md file. Make it engaging, informative, and properly formatted."""
                
                prompt = ChatPromptTemplate.from_messages([
                    ("system", system_prompt),
                    ("user", user_prompt)
                ])
                
                # Create and run chain
                chain = prompt | llm | StrOutputParser()
                readme_content = chain.invoke({})
                
                # Display success
                st.success("✅ README.md generated successfully!")
                st.markdown("---")
                
                # Show preview
                st.subheader("📄 Generated README.md")
                
                # Create tabs for preview
                preview_tab, markdown_tab, download_tab = st.tabs(["👁️ Preview", "📝 Markdown", "📥 Download"])
                
                with preview_tab:
                    st.markdown(readme_content)
                
                with markdown_tab:
                    st.code(readme_content, language="markdown")
                
                with download_tab:
                    st.download_button(
                        label="📥 Download README.md",
                        data=readme_content,
                        file_name="README.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                    
                    st.info("💡 Tip: Review and customize the README before adding to your repository!")
                
                # Option to regenerate with changes
                st.markdown("---")
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("🔄 Regenerate with Different Style", use_container_width=True):
                        st.rerun()
                
                with col2:
                    feedback = st.text_area(
                        "Need changes? Describe what to modify:",
                        placeholder="e.g., 'Make it more technical', 'Add Docker instructions', etc.",
                        height=100
                    )
                    
                    if feedback and st.button("✨ Refine README", use_container_width=True):
                        with st.spinner("🔧 Refining README..."):
                            refine_prompt = ChatPromptTemplate.from_messages([
                                ("system", "You are a technical writer. Modify the README based on user feedback."),
                                ("user", f"""Original README:
{readme_content}

User Feedback:
{feedback}

Generate an improved version incorporating the feedback.""")
                            ])
                            
                            refine_chain = refine_prompt | llm | StrOutputParser()
                            refined_readme = refine_chain.invoke({})
                            
                            st.markdown("### ✨ Refined README")
                            st.markdown(refined_readme)
                            
                            st.download_button(
                                label="📥 Download Refined README.md",
                                data=refined_readme,
                                file_name="README_refined.md",
                                mime="text/markdown",
                                use_container_width=True
                            )
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Make sure your API key is valid and you have credits available")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Built with ❤️ using LangChain 🦜🔗 and Streamlit</p>
    <p style='font-size: 0.9em;'>💡 Tip: Always review and customize the generated README before publishing!</p>
</div>
""", unsafe_allow_html=True)