# 📚 AI Book Maker

An intelligent book creation tool that uses GPT-4O and Perplexity AI to automatically generate well-researched, structured books on any topic.

## 🌟 Features

- **Automated Book Outline Generation**: Creates detailed chapter structures with research questions
- **Parallel Research Processing**: Efficiently researches multiple chapters simultaneously
- **Smart Chapter Writing**: Converts research into coherent, engaging chapters
- **Real-time Progress Updates**: Colorful console output showing progress
- **Beautiful Markdown Output**: Final book is formatted in clean, readable markdown

## 🔧 Prerequisites

- Python 3.7+
- OpenAI API key
- Perplexity API key

## ⚡ Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd book-maker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Windows:
   ```cmd
   set OPENAI_API_KEY=your-openai-key
   set PERPLEXITY_API_KEY=your-perplexity-key
   ```
   
   Linux/Mac:
   ```bash
   export OPENAI_API_KEY=your-openai-key
   export PERPLEXITY_API_KEY=your-perplexity-key
   ```

4. **Run the book maker**
   ```bash
   python book_maker.py
   ```

## 🎯 Detailed Process Flow

1. **Book Outline Generation**
   - GPT-4O receives your topic and generates a structured outline
   - Returns a JSON object containing:
     ```json
     {
       "title": "Book Title",
       "chapters": [
         {
           "title": "Chapter Title",
           "description": "Brief chapter overview",
           "research_questions": [
             "Specific question 1?",
             "Specific question 2?",
             "..."
           ]
         }
       ]
     }
     ```

2. **Research Process**
   - Questions for each chapter are processed in parallel
   - For each chapter:
     ```python
     research_data = await perplexity_client.research(questions)
     ```
   - Batching system:
     - Processes 10 chapters simultaneously (configurable)
     - Implements rate limiting (1 second between batches)
     - Handles API throttling gracefully

3. **Chapter Writing**
   - Research data is fed to GPT-4O-Mini
   - Each chapter is written sequentially to maintain narrative flow
   - Real-time updates:
     ```markdown
     🎯 Generating outline...
     📚 Researching Chapter 1...
     ✍️ Writing Chapter 1...
     📝 Updating book.md...
     ```

4. **Output Generation**
   - Markdown file is updated after each chapter
   - Progress is visible in real-time
   - Colored console output shows status

## 📋 Output Format

The generated book will be saved in markdown format with:
- Book title
- Numbered chapters
- Well-formatted content
- Clean hierarchy

Example structure:
```markdown
# Book Title

## Chapter 1: Chapter Title
[Chapter content...]

## Chapter 2: Chapter Title
[Chapter content...]
```

## ⚙️ Configuration

Key constants in `book_maker.py`:
- `MAX_PARALLEL_REQUESTS`: Number of concurrent research requests (default: 10)
- `SLEEP_BETWEEN_REQUESTS`: Delay between batch requests in seconds (default: 1)
- `OUTPUT_FILE`: Output file name (default: "book.md")

## 🚨 Error Handling

The script includes comprehensive error handling:
- API connection issues
- File writing errors
- JSON parsing errors
- All errors are displayed with descriptive colored messages

## 📝 Notes

- The quality of the book depends on the API response quality
- Longer books will take more time to generate
- Keep your API keys secure and never commit them to version control
- Research questions are automatically generated based on chapter context
- Each chapter typically generates 3-5 focused research questions
- Research data is processed and synthesized before writing

## 🔒 API Key Security

Always use environment variables for API keys. Never hardcode them in the script. 