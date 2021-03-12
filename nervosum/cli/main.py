#!/usr/bin/env python

from nervosum.cli.nervosum_argument_parser import generate_parser
import importlib

def main():
    p = generate_parser()
    args = p.parse_args()
    module = importlib.import_module(args.nervosum_module)
    module.execute(args, p)

if __name__ == "__main__":
    main()
