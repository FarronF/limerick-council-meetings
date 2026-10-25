import argparse
from datetime import datetime
import os
import shutil

from tools.download.main import download_meeting_files
from tools.logging.file_logger import FileLoggerSingleton
from tools.process.main import process_meetings


def main():
    parser = argparse.ArgumentParser(
        description="Download council meeting PDFs and convert them to Markdown."
    )
    parser.add_argument("--start-year", type=int, default=2014, help="Start year (e.g., 2023)")
    parser.add_argument("--start-month", type=int, default=1, help="Start month (1-12)")
    parser.add_argument(
        "--end-year", type=int, default=datetime.now().year, help="End year (e.g., 2024)"
    )
    parser.add_argument(
        "--end-month", type=int, default=datetime.now().month, help="End month (1-12)"
    )
    parser.add_argument(
        "--meeting-filter",
        nargs="+",
        type=str,
        default=None,
        help="Filter meetings by name (case insensitive).",
    )
    parser.add_argument(
        "--file-filter",
        nargs="*",
        type=str,
        default=["agenda", "minutes"],
        help="Filter files by name. Pass this option without values to disable filtering.",
    )
    parser.add_argument(
        "--download-location",
        type=str,
        default="./data/downloaded",
        help="Location to save downloaded files.",
    )
    parser.add_argument(
        "--output-location",
        type=str,
        default="./data/processed",
        help="Location to save processed Markdown files.",
    )
    parser.add_argument(
        "--logs-location", type=str, default="./.logs", help="Location to save logs."
    )
    parser.add_argument(
        "--dont-download", action="store_true", help="Process existing downloads only."
    )
    parser.add_argument(
        "--dont-process", action="store_true", help="Download files without processing them."
    )
    parser.add_argument(
        "--delete-downloads-after-complete",
        action="store_true",
        help="Delete the entire download location after processing.",
    )
    args = parser.parse_args()

    if not args.file_filter:
        args.file_filter = None

    script_start_time = datetime.now()
    run_id = script_start_time.strftime("%Y-%m-%d_%H-%M-%S")
    FileLoggerSingleton(run_id, args.logs_location)

    if not args.dont_download:
        download_meeting_files(
            start_year=args.start_year,
            start_month=args.start_month,
            end_year=args.end_year,
            end_month=args.end_month,
            meeting_filter=args.meeting_filter,
            file_filter=args.file_filter,
            download_location=args.download_location,
        )

    if not args.dont_process:
        process_meetings(
            start_year=args.start_year,
            start_month=args.start_month,
            end_year=args.end_year,
            end_month=args.end_month,
            meeting_filter=args.meeting_filter,
            file_filter=args.file_filter,
            download_location=args.download_location,
            output_location=args.output_location,
        )

    if args.delete_downloads_after_complete:
        if os.path.exists(args.download_location):
            print(f"Removing download location {args.download_location}")
            shutil.rmtree(args.download_location)
        else:
            print(
                f"Download location {args.download_location} does not exist, skipping deletion."
            )


if __name__ == "__main__":
    main()
