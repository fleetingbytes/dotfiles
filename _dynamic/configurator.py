#!/usr/bin/env python

import json
import argparse
from pathlib import Path
from typing import Mapping
import socket
import os


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


def dynamic_data() -> Mapping[str, str]:
    """
    Core function to generate a dict with values depending on some circumstances.
    In the .tmpl files just use this to get access to the dynamic values:
    {{ $dyn := include "_dynamic/dyn_config.json" | mustFromJson -}}
    and then you can access a value like this:
    {{ $dyn.some_value }}
    but mosly you will need to enclose the value in quotes anyway, like this:
    {{ $dyn.some_value | quote }}
    In PowerShell scripts you will also need to replace double backslashes:
    $bootstrap_path = {{ $dyn.bootstrap_path | quote }} -replace "\\\\", "\" # dynamic JSON delivers double backslashes
    """
    edit = dict()
    edit["command"] = f"vim"
    edit["args"] = "[]"
    host = socket.gethostname()
    home = Path(os.getenv("HOME", default=""))
    username = os.getenv("USER", default="")
    age = dict()
    age["identity"] = (home / ".ssh" / "age_identitiy.key").as_posix()
    age["recipient"] = f"age1gvwgc4w2tlgp7fd6qx96ygx0h2gsf7x5qc4xkczdk0sjl0zl7dsqgfnar3"
    environments_path = home / "envs"
    src_path = home / "src"
    bootstrap_path = src_path / "bootstrap"
    result = dict((
        ("edit", edit),
        ("age", age),
        ("env", environments_path.as_posix()),
        ("src", src_path.as_posix()),
        ("bootstrap_path", bootstrap_path.as_posix()),
        ))
    return result


def main() -> None:
    source_file = Path(cli_args.source).with_suffix(".json")
    with open(source_file, mode="r", encoding="utf-8") as js:
        source_json = json.load(js)
        source_json.update(dynamic_data())
        with open(cli_args.target, mode="w", encoding="utf-8") as target_file:
            json.dump(source_json, target_file, indent=4)


if __name__ == "__main__":
    main()
