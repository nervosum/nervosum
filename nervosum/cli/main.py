#!/usr/bin/env python

import importlib

from nervosum.cli.nervosum_parser import generate_parser


def main() -> None:
    p = generate_parser()
    args = p.parse_args()
    module = importlib.import_module(args.nervosum_module)
    module.execute(args)  # type: ignore


if __name__ == "__main__":
    main()
