# Nervosum CLI

This is the command line interface for Nervosum.

## Prerequisites

* [Scala native](https://www.scala-native.org/en/v0.3.9-docs/user/setup.html)

## Running locally

To run the CLI locally, cd to the root level and execute this command:

```bash
sbt cli/run
```

## Building the CLI

To build the CLI binary, cd to the root level and execute this command:

```bash
sbt cli/nativeLink
```

This will create a binary called `cli/target/scala-2.11/cli-out`.
