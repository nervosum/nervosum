import com.typesafe.sbt.SbtGit.git.baseVersion

scalaVersion := "2.11.12"

enablePlugins(ScalaNativePlugin)
// Set to false or remove if you want to show stubs as linking errors
nativeLinkStubs := true

enablePlugins(GitVersioning)
baseVersion := "0.0.1" // Upcoming version. See `cli/README.md`

enablePlugins(BuildInfoPlugin)
buildInfoKeys := Seq[BuildInfoKey](name, version, scalaVersion, sbtVersion)
buildInfoPackage := "ai.nervosum.buildinfo"

libraryDependencies += "org.rogach" %%% "scallop" % "3.5.1"
