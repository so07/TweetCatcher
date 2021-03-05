import argparse

from .tweet_cleaner import tweet_cleaner
from .tweet_utils import logger, set_logging_verbosity, write_df_by_date
from .clargs import (
    add_parser_debug,
    add_parser_date,
    add_parser_format,
    add_parser_input,
    add_parser_output,
)


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

    add_parser_input(parser)
    add_parser_output(parser)
    add_parser_date(parser)
    add_parser_format(parser)
    add_parser_debug(parser)

    parser.add_argument(
        "--language",
        "-l",
        dest="language",
        metavar="lang",
        default=None,
        choices=lang_supported,
        help=f"language. (default %(default)s).\nSupported languages {lang_supported}",
    )

    parser.add_argument(
        "--remove-duplicates",
        dest="remove_duplicates",
        action="store_true",
        help="remove duplicated tweets",
    )

    parser.add_argument(
        "--remove-keys",
        dest="remove_keys",
        action="store_true",
        help="remove useless keys (mentions, urls, reply_to)",
    )

    parser.add_argument(
        "--remove-emoticons",
        dest="remove_emoticons",
        action="store_true",
        help="remove emoticons",
    )

    args = parser.parse_args()

    set_logging_verbosity(args.verbose)

    logger.debug(args)

    df = tweet_cleaner(
        args.search_path,
        args.search_pattern,
        args.language,
        args.verbose,
        no_duplicates=args.remove_duplicates,
        no_useless_keys=args.remove_keys,
        no_emoticons=args.remove_emoticons,
    )

    write_df_by_date(
        df,
        args.output,
        prefix=args.output_prefix,
        format=args.format,
        sep=args.separator,
    )


if __name__ == "__main__":
    main()
