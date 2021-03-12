#!/usr/bin/env python

import importlib

from nervosum.cli.nervosum_argument_parser import generate_parser


def main():
    p = generate_parser()
    args = p.parse_args()
    module = importlib.import_module(args.nervosum_module)
    module.execute(args, p)


if __name__ == "__main__":
    main()
