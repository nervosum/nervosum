from nervosum.config import Config
from nervosum.core.builders.batch_image_builder import BatchImageBuilder
from nervosum.core.builders.flask_image_builder import FlaskImageBuilder
from nervosum.core.builders.image_builder import ImageBuilder


class Director:
    """
    The Director is only responsible for executing the building steps in a
    particular sequence. It is helpful when producing products according to a
    specific order or configuration. Strictly speaking, the Director class is
    optional, since the client can control builders directly.
    """

    def __init__(self) -> None:
        pass

    @property
    def builder(self) -> ImageBuilder:
        return self._builder

    @builder.setter
    def builder(self, builder: ImageBuilder) -> None:
        """
        The Director works with any builder instance that the client code
        passes to it. This way, the client code may alter the final type of
        the newly assembled product.

        Args:
            builder: Set an ImageBuilder instance
        """
        self._builder = builder

    def setup_builder(self, source_dir: str, target_dir: str, mode: str):
        if mode == "batch":
            self.builder = BatchImageBuilder(source_dir, target_dir)
        elif mode == "http":
            self.builder = FlaskImageBuilder(source_dir, target_dir)
        else:
            raise NotImplementedError(f"Currently no support for mode {mode}")

    """
    The Director can construct several product variations using the same
    building steps.
    """

    def build(self, config: Config) -> None:
        self.builder.copy_client_files()
        self.builder.generate_wrapper_files(config)
        self.builder.build_image(config)
