import os
import json
import asyncio
from typing import List, Dict
from termcolor import cprint
from openai import AsyncOpenAI
import markdown
import time

# Constants
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
OUTPUT_FILE = "book.md"
MAX_PARALLEL_REQUESTS = 10  # Adjust based on API limits
SLEEP_BETWEEN_REQUESTS = 1  # Seconds to wait between API calls

# Initialize API clients
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)
perplexity_client = AsyncOpenAI(
    api_key=PERPLEXITY_API_KEY, 
    base_url="https://api.perplexity.ai"
)

async def get_book_outline(topic: str) -> Dict:
    """Get detailed book outline using GPT-4-O."""
    try:
        cprint("🎯 Generating detailed book outline...", "cyan")
        response = await openai_client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional book outline creator. Create a detailed book outline with "
                        "chapters and research questions for each chapter. Return as JSON with format: "
                        "{'title': str, 'chapters': [{'title': str, 'description': str, "
                        "'research_questions': [str]}]}"
                    )
                },
                {"role": "user", "content": f"Create a detailed book outline about: {topic}"}
            ]
        )
        outline = json.loads(response.choices[0].message.content)
        cprint("✅ Book outline generated successfully!", "green")
        return outline
    except Exception as e:
        cprint(f"❌ Error generating book outline: {str(e)}", "red")
        raise

async def research_chapter(chapter: Dict) -> Dict:
    """Research a single chapter using Perplexity API."""
    try:
        questions = " ".join(chapter["research_questions"])
        cprint(f"🔍 Researching chapter: {chapter['title']}", "yellow")
        
        response = await perplexity_client.chat.completions.create(
            model="llama-3.1-sonar-large-128k-online",
            messages=[
                {
                    "role": "system",
                    "content": "You are a thorough researcher. Provide detailed, factual answers."
                },
                {
                    "role": "user",
                    "content": f"Research and provide detailed information for: {questions}"
                }
            ]
        )
        
        return {
            "title": chapter["title"],
            "research_data": response.choices[0].message.content
        }
    except Exception as e:
        cprint(f"❌ Error researching chapter {chapter['title']}: {str(e)}", "red")
        raise

async def write_chapter(chapter_title: str, research_data: str) -> str:
    """Write a chapter using GPT-4-O-Mini with research context."""
    try:
        cprint(f"✍️ Writing chapter: {chapter_title}", "magenta")
        
        response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional book writer. Write an engaging and informative "
                        "chapter based on the provided research data."
                    )
                },
                {
                    "role": "user",
                    "content": f"Write a chapter titled '{chapter_title}' based on this research:\n{research_data}"
                }
            ]
        )
        
        return response.choices[0].message.content
    except Exception as e:
        cprint(f"❌ Error writing chapter {chapter_title}: {str(e)}", "red")
        raise

async def process_chapters_in_batches(chapters: List[Dict]) -> List[Dict]:
    """Process chapters in parallel batches."""
    results = []
    for i in range(0, len(chapters), MAX_PARALLEL_REQUESTS):
        batch = chapters[i:i + MAX_PARALLEL_REQUESTS]
        batch_results = await asyncio.gather(
            *(research_chapter(chapter) for chapter in batch)
        )
        results.extend(batch_results)
        await asyncio.sleep(SLEEP_BETWEEN_REQUESTS)
    return results

def format_book_content(title: str, chapters: List[Dict]) -> str:
    """Format the book content with beautiful markdown."""
    content = f"# {title}\n\n"
    for idx, chapter in enumerate(chapters, 1):
        content += f"## Chapter {idx}: {chapter['title']}\n\n"
        content += f"{chapter['content']}\n\n"
    return content

async def create_book(topic: str):
    """Main function to create the book."""
    try:
        # Step 1: Generate book outline
        outline = await get_book_outline(topic)
        
        # Step 2: Research chapters in parallel
        cprint("📚 Starting parallel research for all chapters...", "blue")
        researched_chapters = await process_chapters_in_batches(outline["chapters"])
        
        # Step 3: Write chapters
        written_chapters = []
        for research in researched_chapters:
            chapter_content = await write_chapter(
                research["title"],
                research["research_data"]
            )
            written_chapters.append({
                "title": research["title"],
                "content": chapter_content
            })
            
            # Update the book file after each chapter
            book_content = format_book_content(outline["title"], written_chapters)
            try:
                with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                    f.write(book_content)
                cprint(f"📝 Updated {OUTPUT_FILE} with new chapter", "green")
            except Exception as e:
                cprint(f"❌ Error updating book file: {str(e)}", "red")
        
        cprint("✨ Book creation completed successfully!", "green")
        
    except Exception as e:
        cprint(f"❌ Fatal error in book creation: {str(e)}", "red")
        raise

if __name__ == "__main__":
    cprint("Enter the book topic: ", "cyan", end="")
    topic = input()
    asyncio.run(create_book(topic))