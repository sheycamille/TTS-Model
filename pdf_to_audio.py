import PyPDF2
import edge_tts
import asyncio
from pathlib import Path
import re
from tqdm.auto import tqdm

async def convert_pdf_to_audio(pdf_path, output_path, voice="en-US-GuyNeural"):  # Deep male voice
    """Convert PDF to MP3 using Edge TTS"""
    
    # Extract text from PDF
    def extract_text_from_pdf(pdf_path):
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            print("Extracting text from PDF...")
            for page in tqdm(pdf_reader.pages, desc="Reading pages", unit="page"):
                text += page.extract_text() + "\n"
        return text

    # Clean text
    def clean_text(text):
        # Remove extra whitespace and special characters
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text

    try:
        # Extract and clean text
        text = extract_text_from_pdf(pdf_path)
        text = clean_text(text)

        # Get approximate duration (1 word ≈ 0.3 seconds)
        words = len(text.split())
        estimated_seconds = words * 0.3

        print("Converting to audio... This may take a while...")
        with tqdm(total=100, desc="Converting to audio", unit="%") as pbar:
            communicate = edge_tts.Communicate(text, voice)
            
            # Create a progress callback
            async def progress_callback(current_char: int, total_char: int):
                progress = (current_char / total_char) * 100
                pbar.n = int(progress)
                pbar.refresh()

            # Add progress callback to the communicate object
            communicate.progress_callback = progress_callback
            await communicate.save(output_path)
        
        print(f"\nAudio saved to: {output_path}")
        print(f"Estimated duration: {int(estimated_seconds/60)} minutes and {int(estimated_seconds%60)} seconds")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Example usage
    pdf_file = "C:/Users/T580/Downloads/The Subtle Art of Not Giving a Fck A Counterintuitive Approach to Living a Good Life by Mark Manson.pdf"  # Replace with your PDF path
    output_file = "C:/Users/T580/Downloads/Audio/The Subtle Art of Not Giving a Fck A Counterintuitive Approach to Living a Good Life by Mark Manson.mp3"  # Replace with your desired output path
    
    # Run the conversion
    asyncio.run(convert_pdf_to_audio(pdf_file, output_file))