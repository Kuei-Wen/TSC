# Auto Subtitle Generator

This script automatically generates subtitles for a video file in a specified language and merges them into the video.

## How it works

1.  **Extracts Audio:** The script first uses `ffmpeg` to extract the audio from the input video file.
2.  **Generates Subtitles:** It then uses OpenAI's `whisper` model to transcribe the audio and generate a subtitle file (`.srt`).
3.  **Merges Subtitles:** Finally, it uses `ffmpeg` again to merge the generated subtitle file into the original video, creating a new video file with embedded subtitles.

## Dependencies

This script requires the following dependencies:

-   **Python 3:** The programming language used to run the script.
-   **`openai-whisper`:** A Python package for automatic speech recognition.
-   **`ffmpeg`:** A command-line tool for handling video and audio.

### Installation

1.  **Install `openai-whisper`:**

    You can install the `whisper` library using `pip`. It's recommended to also install `torch` and `torchaudio` for GPU support if you have a compatible NVIDIA GPU, as this will significantly speed up the transcription process.

    ```bash
    pip install openai-whisper
    # For GPU support with PyTorch
    # pip install torch torchaudio --extra-index-url https://download.pytorch.org/whl/cu118
    ```
    For more details on installing with GPU support, please refer to the official PyTorch documentation.

2.  **Install `ffmpeg`:**

    `ffmpeg` is a system dependency that needs to be installed separately.

    -   **Windows:**
        1.  Download the latest build from the [ffmpeg website](https://ffmpeg.org/download.html).
        2.  Extract the downloaded archive.
        3.  Add the `bin` directory from the extracted folder to your system's `PATH` environment variable.

    -   **macOS (using Homebrew):**
        ```bash
        brew install ffmpeg
        ```

    -   **Linux (using apt):**
        ```bash
        sudo apt update && sudo apt install ffmpeg
        ```

    To verify that `ffmpeg` is installed correctly and available in your PATH, you can run `ffmpeg -version` in your terminal.

## How to Run the Script

Once you have installed the dependencies, you can run the `auto_subtitle.py` script from your terminal.

### Usage

```bash
python auto_subtitle.py <video_path> [-l <language>]
```

-   `<video_path>`: (Required) The path to the input video file (e.g., `my_video.mp4`).
-   `-l <language>`: (Optional) The language of the audio in the video. Use a two-letter ISO-639-1 language code (e.g., `en` for English, `es` for Spanish, `ja` for Japanese). If not specified, it defaults to English (`en`).

### Example

To generate English subtitles for a video named `presentation.mp4`:

```bash
python auto_subtitle.py presentation.mp4 -l en
```

The script will produce the following files:

-   `presentation.srt`: The generated subtitle file.
-   `presentation_subtitled.mp4`: The final video with the subtitles merged in.

A temporary audio file (`presentation_temp_audio.mp3`) will be created during the process but will be deleted automatically upon completion.
