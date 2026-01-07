# ✍️ AI Literary Composer

An intelligent literary creation tool powered by AI that transforms your ideas into masterful works across multiple genres and formats.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🌟 Features

- **Multiple Personas**: Choose from 5 specialized writers
  - 🎭 **Poet** - Sonnets, Haikus, Free Verse
  - 📚 **Manga Writer** - Scripts, Character Profiles, World Building
  - 📖 **Novelist** - Short Stories, Novel Chapters, Plot Outlines
  - 🎓 **Academic** - Thesis Abstracts, Research Summaries
  - 📰 **Journalist** - News Articles, Editorials, Interview Scripts

- **Customizable Creativity**: Adjust temperature (0.0-1.0) to control output style
- **Specialized Templates**: Each literature type has professionally crafted prompts
- **Instant Download**: Export your generated works as text files
- **Clean UI**: Intuitive interface with real-time generation

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Groq API key ([Get one here](https://console.groq.com))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YuvrajJais9257/langchain_course_tutorials.git
cd langchain_course_tutorials
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**

Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

4. **Run the application**
```bash
streamlit run app.py
```

5. **Open your browser**

Navigate to `http://localhost:8501`

## 📁 Project Structure

```
literary_composer/
├── app.py                    # Main Streamlit application
├── constants/
│   ├── __init__.py          # Package initializer
│   └── templates.py         # All personas and prompt templates
├── .env                      # Environment variables (not in repo)
├── .gitignore               # Git ignore file
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## 🎯 Usage

1. **Select a Specialist**: Choose from Poet, Manga Writer, Novelist, Academic, or Journalist
2. **Pick Literature Type**: Select the specific format you want to generate
3. **Adjust Creativity**: Use the temperature slider to control creativity level
   - Lower (0.0-0.3): More focused and deterministic
   - Medium (0.4-0.7): Balanced creativity
   - Higher (0.8-1.0): More creative and diverse
4. **Enter Your Theme**: Describe what you want the work to be about
5. **Generate**: Click the button and watch AI create your masterpiece
6. **Download**: Save your generated work as a text file

## 💡 Examples

### Poet - Haiku
**Input**: "Cherry blossoms in spring"

**Output**:
```
Pink petals flutter—
whispers of fleeting beauty,
spring's gentle goodbye.
```

### Manga Writer - Character Profile
**Input**: "A time-traveling detective"

**Output**: Detailed character breakdown with appearance, backstory, abilities, and character arc.

### Novelist - Short Story
**Input**: "A chance encounter on a rainy night"

**Output**: Complete short story with vivid prose and emotional depth.

## 🛠️ Technologies Used

- **[Streamlit](https://streamlit.io/)** - Web application framework
- **[LangChain](https://www.langchain.com/)** - LLM orchestration
- **[Groq](https://groq.com/)** - Fast LLM inference
- **[Python-dotenv](https://github.com/theskumar/python-dotenv)** - Environment management

## ⚙️ Configuration

### Adding New Personas

Edit `constants/templates.py`:

```python
PERSONA_MAP = {
    "Your New Persona": ["Format 1", "Format 2", "Format 3"],
    # ... existing personas
}

TEMPLATES = {
    "Your New Persona": {
        "Format 1": ChatPromptTemplate.from_messages([
            ("system", "Your specialized system prompt here"),
            ("human", "Theme: {theme}")
        ]),
        # ... more formats
    }
}
```

### Changing the LLM Model

In `app.py`, modify the model parameter:

```python
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",  # Change this
    temperature=temp
)
```

Available Groq models:
- `llama-3.3-70b-versatile`
- `mixtral-8x7b-32768`
- `gemma-7b-it`

## 🎨 Customization

### Styling the Output Display

Modify the display section in `app.py`:

```python
st.markdown(
    f"""
    <div style='background-color: #your-color; 
                padding: 20px; 
                border-radius: 10px;'>
        {st.session_state.generated_work}
    </div>
    """,
    unsafe_allow_html=True
)
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Ideas for Contribution
- Add new personas (Screenwriter, Copywriter, Technical Writer)
- Implement multi-language support
- Add export formats (PDF, DOCX, Markdown)
- Create custom themes for the UI
- Add collaboration features

## 🐛 Known Issues

- Very long outputs may take time to generate
- API rate limits apply based on your Groq plan

## 📧 Contact

Jaiswal Yuvraj - [@jaiswal_yuvraj](https://yuvrajjaiswal-dev.vercel.app/) - yuvraj8257@gmail.com

Project Link: [https://github.com/YuvrajJais9257/langchain_course_tutorials.git](https://github.com/YuvrajJais9257/langchain_course_tutorials)

## 🙏 Acknowledgments
- [Groq](https://groq.com/) for lightning-fast inference
- [Streamlit](https://streamlit.io/) for the amazing framework
- All the writers and artists who inspire creativity

## 📊 Roadmap

- [ ] Add more personas (Screenwriter, Copywriter)
- [ ] Implement user authentication and history
- [ ] Add collaborative editing features
- [ ] Export to multiple formats (PDF, DOCX)
- [ ] Multi-language support
- [ ] Fine-tuned models for specific genres
- [ ] Mobile app version

---

**Made with ❤️ and AI**

*"Every great writer was once a beginner with an idea."*