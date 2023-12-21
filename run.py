import argparse
import os
import shutil
from transcribe.transcribe import call_whisperx, convert_to_lrc


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Transcribe audio and convert to various formats."
    )
    parser.add_argument(
        "input_path", help="Path to the audio file or directory to transcribe."
    )
    parser.add_argument(
        "-o",
        "--output",
        default="data/processed",
        help="Output directory for the files. Default is 'data/processed'.",
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=["srt", "json", "lrc"],
        default="srt",
        help="Output format: 'srt', 'json', 'lrc'.",
    )
    return parser.parse_args()


def create_temp_directory():
    temp_dir = "tmp"
    os.makedirs(temp_dir, exist_ok=True)
    return temp_dir


if __name__ == "__main__":
    args = parse_arguments()

    if not os.path.exists(args.input_path):
        raise FileNotFoundError(f"Input path {args.input_path} does not exist.")

    temp_dir = create_temp_directory() if args.format == "lrc" else args.output

    call_whisperx(
        args.input_path,
        args.output,
        output_format=args.format if args.format else "srt",
    )

    # Convert to LRC format if specified, then remove the temporary directory
    if args.format == "lrc":
        convert_to_lrc(temp_dir, args.output)
        shutil.rmtree(temp_dir)
