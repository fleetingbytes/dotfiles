#!/usr/bin/env python

import json
import argparse
from pathlib import Path
from typing import Mapping
from socket import gethostname
from os import getenv
from tempfile import gettempdir


argument_parser = argparse.ArgumentParser("Generate dynamic chezmoi templates")
argument_parser.add_argument(
        "source",
        type=str,
        metavar="STRING",
        help="Name of the setting"
    )
argument_parser.add_argument(
        "target",
        type=Path,
        metavar="STRING",
        help="Path to the output file"
    )
cli_args = argument_parser.parse_args()


def on_termux() -> bool:
    expected_prefix =  "/data/data/com.termux/files/usr"
    return all((
        getenv("TERMUX_VERSION"),
        getenv("PREFIX") == expected_prefix,
        Path(expected_prefix).is_dir(),
    ))


def common_data() -> Mapping[str, str]:
    """
    Returns a dictionary with common data
    later to be added to any
    .json configuration file
    """
    host = gethostname()
    home = Path(getenv("HOME", default=""))
    username = getenv("USER", default="dotfiles_user")
    downloads_directory = home / "Downloads"
    if on_termux():
        downloads_directory = home / "storage" / "shared" / "Download"
    result = dict((
        ("temporary_directory", gettempdir())
        ("zdotdir", (home / ".config" / "zdotdir").as_posix())
        ("youtube_downloads", (downloads_directory / "yt").as_posix())
        ))
    return result


def main() -> None:
    source_file = Path(cli_args.source).with_suffix(".json")
    with open(source_file, mode="r", encoding="utf-8") as js:
        source_json = json.load(js)
        source_json.update(common_data())
        with open(cli_args.target, mode="w", encoding="utf-8") as target_file:
            json.dump(source_json, target_file, indent=4)


if __name__ == "__main__":
    main()
