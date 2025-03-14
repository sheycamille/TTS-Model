import PyPDF2
import edge_tts
import asyncio
from pathlib import Path
import re
from tqdm.auto import tqdm
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading

class PDFToAudioConverter(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("PDF to Audio Converter")
        self.geometry("600x400")
        self.configure(padx=20, pady=20)

        # Create main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # PDF File Selection
        ttk.Label(self.main_frame, text="Select PDF File:").pack(anchor=tk.W)
        self.pdf_frame = ttk.Frame(self.main_frame)
        self.pdf_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.pdf_path_var = tk.StringVar()
        self.pdf_entry = ttk.Entry(self.pdf_frame, textvariable=self.pdf_path_var)
        self.pdf_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.pdf_button = ttk.Button(self.pdf_frame, text="Browse", command=self.browse_pdf)
        self.pdf_button.pack(side=tk.RIGHT, padx=(5, 0))

        # Output File Selection
        ttk.Label(self.main_frame, text="Select Output Location:").pack(anchor=tk.W)
        self.output_frame = ttk.Frame(self.main_frame)
        self.output_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.output_path_var = tk.StringVar()
        self.output_entry = ttk.Entry(self.output_frame, textvariable=self.output_path_var)
        self.output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.output_button = ttk.Button(self.output_frame, text="Browse", command=self.browse_output)
        self.output_button.pack(side=tk.RIGHT, padx=(5, 0))

        # Voice Selection
        ttk.Label(self.main_frame, text="Select Voice:").pack(anchor=tk.W)
        self.voice_var = tk.StringVar(value="en-US-GuyNeural")
        self.voice_combo = ttk.Combobox(self.main_frame, textvariable=self.voice_var)
        self.voice_combo['values'] = [
            "en-US-GuyNeural",
            "en-GB-RyanNeural",
            "en-US-ChristopherNeural",
            "en-US-EricNeural"
        ]
        self.voice_combo.pack(fill=tk.X, pady=(0, 10))

        # Progress Bars
        self.pdf_progress = ttk.Progressbar(self.main_frame, mode='determinate')
        self.pdf_progress.pack(fill=tk.X, pady=(10, 5))
        
        self.audio_progress = ttk.Progressbar(self.main_frame, mode='determinate')
        self.audio_progress.pack(fill=tk.X, pady=(5, 10))

        # Status Label
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(self.main_frame, textvariable=self.status_var)
        self.status_label.pack(pady=(0, 10))

        # Convert Button
        self.convert_button = ttk.Button(self.main_frame, text="Convert to Audio", command=self.start_conversion)
        self.convert_button.pack(pady=(0, 10))

    def browse_pdf(self):
        filename = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if filename:
            self.pdf_path_var.set(filename)
            # Auto-set output path
            output_path = str(Path(filename).with_suffix('.mp3'))
            self.output_path_var.set(output_path)

    def browse_output(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".mp3",
            filetypes=[("MP3 files", "*.mp3")]
        )
        if filename:
            self.output_path_var.set(filename)

    def update_status(self, message):
        self.status_var.set(message)
        self.update_idletasks()

    async def convert_pdf_to_audio(self, pdf_path, output_path, voice):
        try:
            # Extract text from PDF
            self.update_status("Reading PDF...")
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                total_pages = len(pdf_reader.pages)
                
                for i, page in enumerate(pdf_reader.pages):
                    text += page.extract_text() + "\n"
                    progress = ((i + 1) / total_pages) * 100
                    self.pdf_progress['value'] = progress
                    self.update_idletasks()

            # Clean text
            text = re.sub(r'\s+', ' ', text).strip()

            # Convert to audio
            self.update_status("Converting to audio...")
            communicate = edge_tts.Communicate(text, voice)
            
            async def progress_callback(current_char: int, total_char: int):
                progress = (current_char / total_char) * 100
                self.audio_progress['value'] = progress
                self.update_idletasks()

            communicate.progress_callback = progress_callback
            await communicate.save(output_path)
            
            self.update_status("Conversion completed!")
            messagebox.showinfo("Success", "Audio file has been created successfully!")
            
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
            messagebox.showerror("Error", str(e))

    def start_conversion(self):
        pdf_path = self.pdf_path_var.get()
        output_path = self.output_path_var.get()
        voice = self.voice_var.get()

        if not pdf_path or not output_path:
            messagebox.showerror("Error", "Please select both PDF file and output location")
            return

        # Reset progress bars
        self.pdf_progress['value'] = 0
        self.audio_progress['value'] = 0
        
        # Disable buttons during conversion
        self.convert_button['state'] = 'disabled'
        
        # Run conversion in a separate thread
        def run_conversion():
            asyncio.run(self.convert_pdf_to_audio(pdf_path, output_path, voice))
            self.convert_button['state'] = 'normal'
        
        thread = threading.Thread(target=run_conversion)
        thread.start()

if __name__ == "__main__":
    app = PDFToAudioConverter()
    app.mainloop()