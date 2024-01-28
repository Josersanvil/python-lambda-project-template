import argparse

from app.main import main


def get_args_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser("Application main script.")
    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="The log level to use.",
    )
    return parser


if __name__ == "__main__":
    parser = get_args_parser()
    args = parser.parse_args()
    main(
        log_level=args.log_level,
    )
