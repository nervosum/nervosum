# Nervosum

Nervosum aims to become a machine learning platform in which we incorporate lessons learned from productionalizing machine learned models in various contexts. It offers tooling and platform components to unify a local workflow of data scientists with CI/CD best practices from the software engineering field.

## Reference Architecture

![Reference Architecture](docs/reference-architecture.png)

* **nervosum-cli** - A commandline tool to wrap trained ML-models in a docker image.
* **nervosum-deployer** - A deployment component that can be triggered by `nervosum-cli` to deploy a wrapped model to the platform infrastructre.
* **nervosum-runtime** - The component which interfaces deployed models with the wider IT-landscape. It makes models accessible through HTTP and Kafka.

## Release process

We haven't set up automatic releases (see [#9](https://github.com/nervosum/nervosum/issues/9)).

### Version
The [sbt-git](https://github.com/sbt/sbt-git) plugin determines the build version. The version will be
* If the current git commit has a tag `[vx.y.z]` then the version will be `[x.y.z]`
* If not, the version will be `baseVersion-commitHash`. Where `baseVersion` is defined in `build.sbt` and `commitHash` is the commit hash of HEAD. 

In any case, if there are uncommitted changes, `-SNAPSHOT` is appended.
