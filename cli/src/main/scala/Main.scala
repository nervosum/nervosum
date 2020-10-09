import org.rogach.scallop._

object Main {
  def main(args: Array[String]): Unit = {
    val conf = new Conf(args)

    conf.subcommand match {
      case Some(conf.build) =>
        println("Building...")
      case Some(_) => conf.printHelp()
      case None => conf.printHelp()
    }
  }

  class Conf(arguments: Seq[String]) extends ScallopConf(arguments) {
    val build: Subcommand = new Subcommand("build")
    build.descr("Builds a Docker image for a model")

    version("Nervosum CLI 0.0.1")
    addSubcommand(build)
    verify()
  }
}
