import argparse
from datetime import datetime
import os
import shutil

from tools.download.main import download_meeting_files
from tools.process.main import process_meetings
from tools.publish.main import find_processed_meetings, publish_processed_meetings
from tools.shared.file_logger import FileLoggerSingleton


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Download, process, and publish council meeting documents."
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
        help="Filter files by displayed text. Pass this option with no values to disable filtering.",
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
        "--dont-publish",
        action="store_true",
        help="Keep processed Markdown in the output location without publishing it.",
    )
    parser.add_argument(
        "--redownload-existing",
        action="store_true",
        help="Download PDFs again even when the local file already exists.",
    )
    parser.add_argument(
        "--reprocess-existing",
        action="store_true",
        help="Regenerate Markdown even when the output already exists.",
    )
    parser.add_argument(
        "--republish-existing",
        action="store_true",
        help="Overwrite published files with processed files and rerun post-processing.",
    )
    parser.add_argument(
        "--delete-downloads-after-complete",
        action="store_true",
        help="Delete the entire download location after processing.",
    )
    args = parser.parse_args(argv)

    if not args.file_filter:
        args.file_filter = None

    run_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
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
            redownload_existing=args.redownload_existing,
        )

    processed_meetings = []
    if not args.dont_process:
        processed_meetings = process_meetings(
            start_year=args.start_year,
            start_month=args.start_month,
            end_year=args.end_year,
            end_month=args.end_month,
            meeting_filter=args.meeting_filter,
            file_filter=args.file_filter,
            download_location=args.download_location,
            output_location=args.output_location,
            reprocess_existing=args.reprocess_existing,
        )
    elif args.republish_existing:
        processed_meetings = find_processed_meetings(
            processed_root=args.output_location,
            start_year=args.start_year,
            start_month=args.start_month,
            end_year=args.end_year,
            end_month=args.end_month,
            meeting_filter=args.meeting_filter,
        )
        print(f"Found {len(processed_meetings)} existing processed meeting(s) to republish.")

    if processed_meetings and not args.dont_publish:
        publish_processed_meetings(
            processed_meetings,
            processed_root=args.output_location,
            logs_location=args.logs_location,
            republish_existing=args.republish_existing,
        )

    if args.delete_downloads_after_complete:
        if os.path.exists(args.download_location):
            print(f"Removing download location {args.download_location}")
            shutil.rmtree(args.download_location)
        else:
            print(
                f"Download location {args.download_location} does not exist, skipping deletion."
            )
