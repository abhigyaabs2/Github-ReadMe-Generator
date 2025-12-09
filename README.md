📝 GitHub README Generator (Streamlit + LangChain)

A powerful and easy-to-use AI-powered GitHub README Generator built with Streamlit, LangChain, and OpenAI GPT.
This tool analyzes your project files or pasted code and automatically generates a clean, professional, and customizable README.md for your repository.

Perfect for developers who want to save time writing documentation and maintain high-quality project READMEs.

---

🚀 Features
✅ AI-Generated README.md

Automatically generates detailed and professional README files using OpenAI GPT models.

📁 Upload Multiple Project Files

Upload .py, .js, .json, .txt, .md, .html, .css, .java, .cpp, .c, .go, .rs, .php, and more.

---

🎨 Customizable Styles

Choose your README style:

Professional

Minimalist

Detailed

Open Source

---

🏷️ Optional Sections

Badges

---

🧠 Project Context Understanding

Include metadata like project name, description, and instructions.

📥 Downloadable README

One-click download of generated .md file.

🔄 Refinement Mode

Ask the AI to modify or refine the README with additional feedback.

🖼️ Demo UI

The app includes:

A modern UI with a gradient header

Sidebar for configuration

Tabs for upload/paste code

Markdown preview

Download button for README

📦 Tech Stack

Python 3.10+

Streamlit – UI Framework

LangChain – Prompt templating & LLM orchestration

OpenAI GPT (via langchain-openai)

python-dotenv – Secure API key handling

---

🛠️ Installation
1️⃣ Clone the Repository
git clone https://github.com/abhigyaabs2/Github-ReadMe-Generator.git
cd Github-ReadMe-Generator

2️⃣ Create Virtual Environment (Recommended)
conda create -n readmegen python=3.11 -y
conda activate readmegen


or

python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

3️⃣ Install Dependencies
streamlit
langchain
langchain-openai
python-dotenv

🔑 Environment Variables

Create a .env file in the root folder:

OPENAI_API_KEY=your_api_key_here


Or enter the key manually in the Streamlit sidebar.

▶️ Run the App
streamlit run github.py

---

📁 Project Structure
📦 readme-generator
 ┣ 📜 github.py           # Main Streamlit application
 ┣ 📜 .env                # API key (ignored in GitHub)
 ┣ 📜 README.md           # Documentation
 ┣ 📜 requirements.txt    # Dependencies
 ┗ 📁 assets/             # Optional: screenshots, icons

🔍 How It Works

You upload files or paste your project code

App extracts & merges content for analysis

LangChain constructs a prompt with:

Your files

Metadata

README style

OpenAI generates a structured README.md

You view, edit, download, or refine the output

---

📘 Output Format

The generated README includes:

Title

Badges (optional)

Table of Contents (optional)

Overview

Features

Tech Stack

Installation

Usage

Project Structure

Configuration

Screenshots (optional)

Contributing

License

Contact

---

🤝 Contributing

Contributions are welcome!
Feel free to fork this project and submit a PR.

📄 License

This project is licensed under the MIT License.
