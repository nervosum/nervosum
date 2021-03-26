#!/usr/bin/env python

import importlib

from nervosum.cli import nervosum_parser


def main() -> None:
    args = nervosum_parser.parse_args()
    module = importlib.import_module(args.nervosum_module)
    module.execute(args)  # type: ignore


if __name__ == "__main__":
    main()
