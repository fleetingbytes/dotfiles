#!/usr/bin/env python

import json
import argparse
from pathlib import Path
from typing import Mapping
from socket import gethostname
from os import getenv


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


def common_data() -> Mapping[str, str]:
    """
    Returns a dictionary with common data
    later to be added to any
    .json configuration file
    """
    host = gethostname()
    home = Path(getenv("HOME", default=""))
    username = getenv("USER", default="")
    environments_path = home / "envs"
    src_path = home / "src"
    bootstrap_path = src_path / "bootstrap"
    result = dict((
        ("env", environments_path.as_posix()),
        ("src", src_path.as_posix()),
        ("bootstrap_path", bootstrap_path.as_posix()),
        ))
    return result


def main() -> None:
    source_file = Path(cli_args.source).with_suffix(".json")
    with open(source_file, mode="r", encoding="utf-8") as js:
        source_json = json.load(js)
        # add common data
        source_json.update(common_data())
        with open(cli_args.target, mode="w", encoding="utf-8") as target_file:
            json.dump(source_json, target_file, indent=4)


if __name__ == "__main__":
    main()
