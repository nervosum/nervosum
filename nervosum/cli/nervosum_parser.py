import argparse
from textwrap import dedent


def parse_args(args=None) -> argparse.Namespace:
    p = generate_parser()
    return p.parse_args(args)


def generate_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="nervosum is a tool to help you deploy python ML models"
    )

    sub_parsers = p.add_subparsers(metavar="commands", dest="cmd",)

    sub_parsers.required = True
    configure_parser_build(sub_parsers)
    configure_parser_run(sub_parsers)
    configure_parser_list(sub_parsers)
    return p


def configure_parser_build(sub_parsers: argparse._SubParsersAction) -> None:
    help = "Build a model class into a docker image"
    descr = help

    example = dedent(
        """
    Examples:
        nervosum build -c config.yaml .
    """
    )
    p = sub_parsers.add_parser(
        "build", description=descr, help=help, epilog=example,
    )
    p.add_argument(
        "dir", help="Path to model dir",
    )
    p.add_argument(
        "--c",
        "-c",
        action="store",
        default="nervosum.yaml",
        help="Path to config file",
    )

    p.set_defaults(nervosum_module="nervosum.core.build")


def configure_parser_run(sub_parsers: argparse._SubParsersAction) -> None:
    help = "Run a docker image"
    descr = help

    example = dedent(
        """
    Examples:
        nervosum run
    """
    )
    p = sub_parsers.add_parser(
        "run", description=descr, help=help, epilog=example,
    )
    p.add_argument(
        "-t", "--tag", action="store", help="Tag of image to run",
    )
    p.add_argument(
        "-n", "--name", action="store", help="Name of image to run",
    )
    p.add_argument(
        "-e",
        "--env",
        action="append",
        help="Environment variable(s) to pass to container. -e ENV=value",
    )
    p.add_argument(
        "-v",
        "--volume",
        action="append",
        help="Volume(s) to mount. -v local:container",
    )

    p.set_defaults(nervosum_module="nervosum.core.run")


def configure_parser_list(sub_parsers: argparse._SubParsersAction) -> None:
    help = "List nervosum images"
    descr = help

    example = dedent(
        """
    Examples:
        nervosum list -f classifier
    """
    )

    p = sub_parsers.add_parser(
        "ls", description=descr, help=help, epilog=example,
    )

    p.add_argument(
        "-f",
        "--filter",
        action="append",
        help="Filter on a specific label given to the image",
    )

    p.set_defaults(nervosum_module="nervosum.core.list")
