# subtitle_writer.py

def write_srt(text: str, output_path: str):
    """
    Writes basic SRT file with one line of subtitle per second (approx).

    Args:
        text (str): Text to convert into subtitles.
        output_path (str): Where to save the .srt file.
    """
    lines = text.split(". ")
    with open(output_path, "w", encoding="utf-8") as f:
        for i, line in enumerate(lines):
            start = i
            end = i + 1
            f.write(f"{i+1}\n")
            f.write(f"00:00:{start:02d},000 --> 00:00:{end:02d},000\n")
            f.write(line.strip() + "\n\n")

