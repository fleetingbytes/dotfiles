#!/usr/bin/env python

import argparse
import json
from collections.abc import Mapping
from os import getenv
from pathlib import Path
from socket import gethostname
from tempfile import gettempdir

argument_parser = argparse.ArgumentParser("Generate dynamic chezmoi templates")
argument_parser.add_argument("source", type=str, metavar="STRING", help="Name of the setting")
argument_parser.add_argument("target", type=Path, metavar="STRING", help="Path to the output file")
cli_args = argument_parser.parse_args()


def on_termux() -> bool:
    expected_prefix = "/data/data/com.termux/files/usr"
    return all(
        (
            getenv("TERMUX_VERSION"),
            getenv("PREFIX") == expected_prefix,
            Path(expected_prefix).is_dir(),
        )
    )


def needs_fat_z() -> bool:
    hostname = gethostname()
    return hostname in set(("starlab-lite",))


def keyboard_options() -> str:
    options = ["caps:escape_shifted_capslock"]
    if needs_fat_z():
        options.append("fat_z")
    return ",".join(options)


def common_data() -> Mapping[str, str]:
    """
    Returns a dictionary with common data
    later to be added to any
    .json configuration file
    """
    home = Path(getenv("HOME", default=""))
    downloads_directory = home / "Downloads"
    if on_termux():
        downloads_directory = home / "storage" / "shared" / "Download"
    result = dict(
        (
            ("temporary_directory", gettempdir()),
            ("zdotdir", (home / ".config" / "zdotdir").as_posix()),
            ("youtube_downloads", (downloads_directory / "yt").as_posix()),
            ("on_termux", on_termux()),
            ("keyboard_options", keyboard_options()),
        )
    )
    return result


def main() -> None:
    source_file = Path(cli_args.source).with_suffix(".json")
    with open(source_file, encoding="utf-8") as js:
        source_json = json.load(js)
        source_json.update(common_data())
        with open(cli_args.target, mode="w", encoding="utf-8") as target_file:
            json.dump(source_json, target_file, indent=4)


if __name__ == "__main__":
    main()
