import os

from nervosum.config import NervosumConfig
from nervosum.core import utils
from nervosum.core.builders.image_builder import ImageBuilder, logger


class FlaskImageBuilder(ImageBuilder):
    mode = "http"

    def generate_wrapper_files(self, config: NervosumConfig) -> None:
        logger.info("Copying wrapper files")

        wrapper_requirements = utils.render_template(
            self.mode, "wrapper-requirements.txt"
        )

        wrapper_file = utils.render_template(
            self.mode,
            "wrapper.py.j2",
            model_module=config.interface.model_module,
            model_class=config.interface.model_class,
            input_schema=config.input_schema,
            output_schema=config.output_schema,
            src=config.src.replace("/", ".").rstrip("."),
            metadata=None,
        )

        dockerfile = utils.render_template(
            self.mode, "Dockerfile.j2", requirements_file=config.requirements,
        )

        utils.write_to_file(
            os.path.join(self.target_dir, "wrapper.py"), wrapper_file
        )
        utils.write_to_file(
            os.path.join(self.target_dir, "wrapper_requirements.txt"),
            wrapper_requirements,
        )
        utils.write_to_file(
            os.path.join(self.target_dir, "Dockerfile"), dockerfile
        )
