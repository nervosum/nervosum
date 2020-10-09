# Nervosum CLI

This is the command line interface for Nervosum.

## Prerequisites

* [Scala native](https://www.scala-native.org/en/v0.3.9-docs/user/setup.html)

## Running locally

To run the CLI locally, use this command:

```bash
sbt run
```

## Building the CLI

To build the CLI binary, run this command:

```bash
sbt nativeLink
```

This will create a binary called `target/scala-2.11/cli-out`.
