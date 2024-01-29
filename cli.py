import argparse
from rich.console import Console
from utils.logging import Logger
from utils.file_handling import AudioHandler, sync_files


class ArgParser:
    def __init__(self):
        self.console = Console()
        self.parser = argparse.ArgumentParser(
            description="CLI for audio transcription and processing."
        )
        self._add_arguments()

    def _add_arguments(self):
        self.parser.add_argument(
            "--verbose", action="store_true", help="Enable verbose output."
        )
        subparsers = self.parser.add_subparsers(help="sub-command help", dest="command")

        parser_transcribe = subparsers.add_parser(
            "transcribe", help="Transcribe audio files."
        )
        parser_transcribe.add_argument(
            "input_path", help="Path to the audio file or directory to transcribe."
        )
        parser_transcribe.add_argument(
            "-o",
            "--output",
            default="data/processed",
            help="Output directory for the files. Default is 'data/processed'.",
        )
        parser_transcribe.add_argument(
            "--relocate_files",
            choices=["true", "false"],
            default="true",
            help="Whether to move transcribed audio files to the output directory upon completion. Accepts 'true' or 'false'; default is 'true'.",
        )
        parser_transcribe.add_argument(
            "-f",
            "--format",
            choices=["srt", "json", "lrc"],
            default="srt",
            help="Output format: 'srt', 'json', 'lrc'.",
        )
        parser_transcribe.add_argument(
            "--speaker_count",
            type=int,
            help="Set minimum and maximum number of speakers.",
        )
        parser_transcribe.add_argument(
            "--device_index", type=int, help="Index of the device to use."
        )
        parser_transcribe.add_argument(
            "--prompt", type=str, help="Initial prompt to use."
        )
        parser_transcribe.set_defaults(func=self.handle_transcription)

        # File import
        parser_pull = subparsers.add_parser(
            "pull", help="Synchronize files/folders to a local directory."
        )
        parser_pull.add_argument(
            "source_dirs", nargs="+", help="List of source directories to synchronize."
        )
        parser_pull.add_argument(
            "-d",
            "--destination",
            default="data/imports",
            help="Destination directory for the files. Default is 'data/imports'.",
        )
        parser_pull.set_defaults(func=self.handle_pull)

    def handle_pull(self, args, logger):
        logger.start_session(args)

        sync_files(args.source_dirs, args.destination, logger=logger)

        logger.end_session()
        logger.save_log()

    def handle_transcription(self, args, logger):
        audio_handler = AudioHandler(args, logger, self.console)
        audio_handler.transcribe()

    def parse_args(self):
        return self.parser.parse_args()


def main():
    arg_parser = ArgParser()
    args = arg_parser.parse_args()

    if args.verbose:
        print("Verbose mode enabled.")

    if args.command is None:
        arg_parser.parser.print_help()
    else:
        logger = Logger("logs/log.json")
        # Call the appropriate handler based on the command
        if hasattr(args, "func"):
            args.func(args, logger)
        else:
            arg_parser.parser.print_help()
            print("\nNo valid command provided.")


if __name__ == "__main__":
    main()