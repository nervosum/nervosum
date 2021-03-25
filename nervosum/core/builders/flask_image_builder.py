import os

from nervosum.config import Config
from nervosum.core.builders.image_builder import ImageBuilder, client, logger


class FlaskImageBuilder(ImageBuilder):
    mode = "http"

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

    def generate_wrapper_files(self, config: Config) -> None:
        logger.info("Copying wrapper files")

        wrapper_requirements = self.render_template(
            self.mode, "wrapper-requirements.txt"
        )

        wrapper_file = self.render_template(
            self.mode,
            "wrapper.py.j2",
            model_module=config.interface.model_module,
            model_class=config.interface.model_class,
            input_schema=config.input_schema,
            output_schema=config.output_schema,
            metadata=None,
        )

        dockerfile = self.render_template(
            self.mode, "Dockerfile.j2", requirements_file=config.requirements,
        )

        self.write_to_file("wrapper.py", wrapper_file)
        self.write_to_file("wrapper_requirements.txt", wrapper_requirements)
        self.write_to_file("Dockerfile", dockerfile)

    def copy_client_files(self) -> None:
        logger.info("Copying client files")
        self.create_target_dir()
        self.copy_source_files_to_target_dir()
