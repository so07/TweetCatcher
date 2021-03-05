import re
import datetime

__version__ = "0.3.1"


def add_parser_debug(parser):

    parser_group = parser.add_argument_group("execution options")

    parser_group.add_argument(
        "--version",
        action="version",
        version="%(prog)s " + __version__,
        help="print version information",
    )

    parser_group.add_argument(
        "-v", "--verbose", action="count", default=0, help="increase verbosity"
    )

    parser_group.add_argument(
        "--debug", "--dry-run", dest="dry_run", action="store_true", help="dry-run mode"
    )


def add_parser_date(parser):
    def _date(s):

        fmt_day = "%Y-%m-%d"
        fmt_time = "%H:%M:%S"
        fmt_minutes = "%H:%M"
        sep = "T"

        for fmt in (
            fmt_day,
            fmt_time,
            fmt_day + sep + fmt_time,
            fmt_day + sep + fmt_minutes,
        ):
            try:
                return datetime.datetime.strptime(s, fmt)
            except:
                pass
        else:
            raise ValueError("invalid date {}".format(s))

    def _freq(s):

        if s is None:
            return None, None

        digit = int(re.findall(r"\d+", s)[0])

        freq_str = s.upper()

        if "y" in s.lower():
            freq_time = datetime.timedelta(days=365 * digit)
        if "d" in s.lower():
            freq_time = datetime.timedelta(days=digit)
        if "h" in s.lower():
            freq_time = datetime.timedelta(hours=digit)
        if "m" in s.lower():
            freq_str = str(digit) + "T"
            freq_time = datetime.timedelta(minutes=digit)
        if "s" in s.lower():
            freq_time = datetime.timedelta(seconds=digit)

        return freq_str, freq_time

    parser_group = parser.add_argument_group("date options")

    parser_group.add_argument(
        "--from",
        dest="from_date",
        type=_date,
        default=datetime.datetime(1970, 1, 1).isoformat(sep="T", timespec="minutes"),
        metavar="1985-10-26T01:20:00",
        help="start date in format 1985-10-26T01:20:00",
    )

    parser_group.add_argument(
        "--to",
        dest="to_date",
        type=_date,
        default=datetime.datetime.now().isoformat(sep="T", timespec="minutes"),
        metavar="2015-10-21T07:28:00",
        help="until date in format 2015-10-21T07:28:00",
    )

    parser_group.add_argument(
        "--freq",
        dest="freq",
        type=_freq,
        default=(None, None),
        metavar="xY, xD, xH, xM, xS",
        help="data frequency.\ny/Y for years, d/D for days, h/H for hours, m/M for minutes, s/S for seconds.\n'30M' data frequency with time interval of 30 minutes.",
    )


def add_parser_output(parser):

    parser_group = parser.add_argument_group("output options")

    parser_group.add_argument(
        "--output-path",
        "-o",
        dest="output",
        default="tweet_clean",
        help="directory where tweet data are stored. (default %(default)s)",
    )

    parser_group.add_argument(
        "--output-prefix",
        dest="output_prefix",
        default="",
        help="prefix to output file. (default %(default)s)",
    )


def add_parser_input(parser):

    parser_group = parser.add_argument_group("input options")

    parser_group.add_argument(
        "--path",
        "-p",
        dest="search_path",
        nargs="+",
        default="tweet_search",
        help="directory where search data files with tweets. (default %(default)s)",
    )

    parser_group.add_argument(
        "--pattern",
        "-P",
        dest="search_pattern",
        default=None,
        help="pattern of file to clean. (default %(default)s)",
    )


def add_parser_format(parser):

    parser_group = parser.add_argument_group("format options")

    parser_group.add_argument(
        "--format",
        "-f",
        dest="format",
        default="csv",
        choices=["json", "csv"],
        help="output file format. (default %(default)s)",
    )

    parser_group.add_argument(
        "--sep",
        dest="separator",
        default=",",
        help="output file columns separator. (default %(default)s)",
    )
