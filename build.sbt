name := "nervosum"
Global / organization := "ai.nervosum"
Global / organizationHomepage := Some(url("https://github.com/orgs/nervosum"))

Global / scalaVersion := "2.11.12"

lazy val global = project
  .in(file("."))
  .aggregate(versionProject, cli)
  .dependsOn(versionProject, cli)

lazy val versionProject = project
  .enablePlugins(ScalaNativePlugin, GitVersioning, BuildInfoPlugin)
  .settings(
    com.typesafe.sbt.SbtGit.git.baseVersion := "0.0.1", // Upcoming version. See `README.md`

    buildInfoKeys := Seq[BuildInfoKey](name, version, scalaVersion, sbtVersion),
    buildInfoPackage := "ai.nervosum.buildinfo"
  )

lazy val cli = project
  .dependsOn(versionProject)
  .enablePlugins(ScalaNativePlugin)
  .settings(
    nativeLinkStubs := true,
    libraryDependencies += "org.rogach" %%% "scallop" % "3.5.1"
  )
