import os

from nervosum.config import Config
from nervosum.core.builders.image_builder import ImageBuilder, client, logger


class BatchImageBuilder(ImageBuilder):
    mode = "batch"

    def copy_client_files(self) -> None:
        logger.info("Copying client files")
        self.create_target_dir()
        self.copy_source_files_to_target_dir()

    def generate_wrapper_files(self, config: Config) -> None:
        logger.info("Copying wrapper files")

        wrapper_requirements = self.render_template(
            self.mode, "wrapper-requirements.txt"
        )

        wrapper_file = self.render_template(
            self.mode,
            "wrapper.py.j2",
            src=config.src.replace("/", ".").rstrip("."),
            model_module=config.interface.model_module,
            model_class=config.interface.model_class,
        )

        dockerfile = self.render_template(
            self.mode,
            "Dockerfile.j2",
            requirements_file=config.requirements,
            platform_tag=config.platform_tag,
        )
        self.write_to_file(
            "pydzipimport_linux.py",
            self.get_pkg_file("batch", "pydzipimport_linux.py").decode(
                "utf-8"
            ),
        )
        self.write_to_file("wrapper.py", wrapper_file)
        self.write_to_file("wrapper-requirements.txt", wrapper_requirements)
        self.write_to_file("Dockerfile", dockerfile)

    def build_image(self, config: Config) -> None:
        logger.info("Building docker image")

        os.chdir(self.target_dir)
        client.images.build(
            path=".",
            labels={
                "owner": "nervosum",
                "mode": self.mode,
                "name": config.name.lower(),
                "tag": config.tag,
            },
            tag=[f"nervosum/{config.name.lower()}:{config.tag}"],
            quiet=False,
        )
