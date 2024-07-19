# Meeting Summarizer and Plan of Action Generator using NLP

This project leverages advanced Natural Language Processing (NLP) techniques to provide comprehensive meeting summaries and actionable plans. It processes video/audio files to extract key information, analyze sentiment and tone, and generate summaries. Additionally, it includes a feature to send emails with the summarized information to respective recipients.
<img width="960" alt="app1" src="<img width="960" alt="5" src="https://github.com/user-attachments/assets/7b528a01-6020-4760-8adf-7d54fb5f51be">
">


## Features

- **Video/Audio Processing**: Converts video files to audio using `ffmpeg` and removes silent regions using `pydub`.
- **Transcription**: Uses OpenAI's Whisper base-model to transcribe audio files into text.
- **Summarization**: Utilizes OpenAI's GPT-3.5 Turbo model to generate meeting summaries.
- **Sentiment and Tone Analysis**: Analyzes the sentiment and tone of the meeting content.
- **Plan of Action**: Generates a plan of action based on the meeting content.
- **Email Sending**: Sends the summarized information and plan of action to predefined recipients using the `smtplib` library.

## Project Screenshots

### Summarizer
![Summarizer](<img width="960" alt="3" src="https://github.com/user-attachments/assets/fdc2aa75-735f-494b-9385-c6a21dbc8b58">

)


### Audio Processing and Text Preprocessing

#### Audio Processing
The project utilizes several audio processing techniques to prepare meeting recordings for analysis and summarization:

- **Conversion to Audio**: Video files are converted to audio using `ffmpeg`, facilitating easier processing of the meeting content without visual data.
- **Silent Region Removal**: `pydub` is employed to remove silent regions from the audio files. This preprocessing step helps in focusing the analysis on meaningful speech segments, improving the accuracy of transcription and subsequent NLP tasks.

#### Text Preprocessing
Before applying Natural Language Processing (NLP) techniques to extract meeting summaries and plans of action, the transcribed text undergoes preprocessing to enhance the quality of analysis:

- **Tokenization**: The transcribed text is segmented into individual tokens (words or phrases) to facilitate further analysis.
- **Stopword Removal**: Common stopwords (e.g., "the", "is", "and") are removed from the text to reduce noise and improve the relevance of extracted information.

These preprocessing steps are crucial for optimizing the performance of the summarization and sentiment analysis models, ensuring that the generated summaries are concise, relevant, and accurately reflect the content and sentiment of the meetings.

## Installation

1. Clone the repository:
   

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Install `ffmpeg`:
    - For Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.
    - For macOS: Use Homebrew:
        ```bash
        brew install ffmpeg
        ```
    - For Linux:
        ```bash
        sudo apt-get install ffmpeg
        ```

## Usage

1. Place your video files in the `input_videos` directory.
2. Run the main script:
    ```bash
    python Meeting_Summarizer.py
    ```
3. The processed audio, transcriptions, summaries, and plans of action will be saved in the respective directories.
4. The email will be sent to the predefined recipients with the summarized information and plan of action.

## Configuration

Modify the script to set up your email credentials and recipients.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- OpenAI for the Whisper and GPT-3.5 Turbo models.
- The developers of `ffmpeg`.
- Infosys for the internship opportunity and project support.

---
