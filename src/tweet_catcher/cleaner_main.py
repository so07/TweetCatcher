import argparse

from .tweet_cleaner import tweet_cleaner
from .tweet_utils import logger, set_logging_verbosity, write_df_by_date
from .clargs import add_parser_debug, add_parser_date

lang_supported = [
    "af",
    "ar",
    "bg",
    "bn",
    "ca",
    "cs",
    "cy",
    "da",
    "de",
    "el",
    "en",
    "es",
    "et",
    "fa",
    "fi",
    "fr",
    "gu",
    "he",
    "hi",
    "hr",
    "hu",
    "id",
    "it",
    "ja",
    "kn",
    "ko",
    "lt",
    "lv",
    "mk",
    "ml",
    "mr",
    "ne",
    "nl",
    "no",
    "pa",
    "pl",
    "pt",
    "ro",
    "ru",
    "sk",
    "sl",
    "so",
    "sq",
    "sv",
    "sw",
    "ta",
    "te",
    "th",
    "tl",
    "tr",
    "uk",
    "ur",
    "vi",
    "zh-cn",
    "zh-tw",
]


def main():

    parser = argparse.ArgumentParser(
        prog="tweet_cleaner",
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    add_parser_date(parser)
    add_parser_debug(parser)

    parser.add_argument(
        "--path",
        "-p",
        dest="search_path",
        default="tweet_search",
        help="directory where search csv file with tweets. (default %(default)s)",
    )

    parser.add_argument(
        "--pattern",
        "-P",
        dest="search_pattern",
        default=None,
        help="pattern of csv file to clean. (default %(default)s)",
    )

    parser.add_argument(
        "--output",
        "-o",
        dest="output",
        default="tweet_clean",
        help="directory where clean tweet data are stored. (default %(default)s)",
    )

    parser.add_argument(
        "--language",
        "-l",
        dest="language",
        metavar="lang",
        default=None,
        choices=lang_supported,
        help=f"language. (default %(default)s).\nSupported languages {lang_supported}",
    )

    args = parser.parse_args()

    set_logging_verbosity(args.verbose)

    logger.debug(args)

    df = tweet_cleaner(
        args.search_path,
        args.search_pattern,
        args.language,
        args.verbose,
    )

    write_df_by_date(df, args.output)


if __name__ == "__main__":
    main()
