# PDF to Audio Converter

A Python-based application that converts PDF documents to audio files using Microsoft Edge's Text-to-Speech service.

## Features

- 📱 Android-compatible GUI interface
- 📖 PDF text extraction with progress tracking
- 🔊 High-quality text-to-speech conversion
- 🎭 Multiple voice options:
  - en-US-GuyNeural (Deep male voice)
  - en-GB-RyanNeural (British male voice)
  - en-US-ChristopherNeural (Male voice)
  - en-US-EricNeural (Male voice)
- 📊 Dual progress bars for PDF reading and audio conversion
- 💾 Automatic output file naming
- ⚡ Asynchronous processing
- 🔄 Real-time conversion status updates

## Requirements

- Python 3.11+
- PyPDF2
- edge-tts
- tqdm

## Installation

1. Clone the repository:
```bash
git clone [your-repository-url]
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```


## Usage

1. Launch the application
2. Click "Browse" to select your PDF file
3. Choose output location for the MP3 file
4. Select preferred voice from the dropdown menu
5. Click "Convert to Audio" to start the conversion
6. Monitor progress through the dual progress bars
7. Receive notification when conversion is complete

## Permissions Required

- Storage Read Permission (for PDF files)
- Storage Write Permission (for MP3 output)
- Internet Permission (for TTS service)

## Technical Details

- Uses Microsoft Edge's TTS service for high-quality voice synthesis
- Asynchronous processing to prevent UI freezing
- Efficient PDF text extraction with PyPDF2
- Real-time progress tracking for both PDF reading and audio conversion

## Known Limitations

- Requires internet connection for TTS conversion
- PDF must be text-searchable (OCR'd)
- Large PDFs may take longer to process

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.


## Acknowledgments

- Microsoft Edge TTS service
- PyPDF2 developers