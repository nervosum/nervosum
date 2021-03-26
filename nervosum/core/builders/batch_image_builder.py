import os

from nervosum.config import NervosumConfig
from nervosum.core import utils
from nervosum.core.builders.image_builder import ImageBuilder, logger


class BatchImageBuilder(ImageBuilder):
    mode = "batch"

    def generate_wrapper_files(self, config: NervosumConfig) -> None:
        logger.info("Copying wrapper files")

        wrapper_requirements = utils.render_template(
            self.mode, "wrapper-requirements.txt"
        )

        wrapper_file = utils.render_template(
            self.mode,
            "wrapper.py.j2",
            src=config.src.replace("/", ".").rstrip("."),
            model_module=config.interface.model_module,
            model_class=config.interface.model_class,
        )

        dockerfile = utils.render_template(
            self.mode,
            "Dockerfile.j2",
            requirements_file=config.requirements,
            platform_tag=config.platform_tag,
        )

        utils.write_to_file(
            os.path.join(self.target_dir, "pydzipimport_linux.py"),
            utils.get_pkg_file("batch", "pydzipimport_linux.py").decode(
                "utf-8"
            ),
        )

        utils.write_to_file(
            os.path.join(self.target_dir, "wrapper.py"), wrapper_file
        )
        utils.write_to_file(
            os.path.join(self.target_dir, "wrapper-requirements.txt"),
            wrapper_requirements,
        )
        utils.write_to_file(
            os.path.join(self.target_dir, "Dockerfile"), dockerfile
        )
