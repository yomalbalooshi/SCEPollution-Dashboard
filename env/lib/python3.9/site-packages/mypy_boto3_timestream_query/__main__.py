"""
Main CLI entrypoint.
"""
import sys


def print_info() -> None:
    """
    Print package info to stdout.
    """
    print(
        "Type annotations for boto3.TimestreamQuery 1.22.0\nVersion:         1.22.0.post1\nBuilder"
        " version: 7.5.9\nDocs:           "
        " https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query//\nBoto3 docs:    "
        "  https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery\nOther"
        " services:  https://pypi.org/project/boto3-stubs/\nChangelog:      "
        " https://github.com/youtype/mypy_boto3_builder/releases"
    )


def print_version() -> None:
    """
    Print package version to stdout.
    """
    print("1.22.0.post1")


def main() -> None:
    """
    Main CLI entrypoint.
    """
    if "--version" in sys.argv:
        return print_version()
    print_info()


if __name__ == "__main__":
    main()
