from nervosum.config import NervosumConfig
from nervosum.core.builders.image_builder import ImageBuilder


class DefaultImageBuilder(ImageBuilder):
    def generate_wrapper_files(self, config: NervosumConfig):
        pass


def test_image_builder() -> None:
    IB = DefaultImageBuilder(source_dir="source_dir", target_dir="target_dir")
    assert IB.source_dir == "source_dir"
    assert IB.target_dir == "target_dir"
