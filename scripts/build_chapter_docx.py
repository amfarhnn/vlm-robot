from __future__ import annotations

from pathlib import Path

import build_chapter_3_docx as docx_builder


ROOT = Path(__file__).resolve().parents[1]


def build(markdown_path: Path, drawio_dir: Path, docx_path: Path) -> None:
    docx_builder.MARKDOWN_PATH = markdown_path
    docx_builder.DRAWIO_DIR = drawio_dir
    docx_builder.EXPORT_DIR = drawio_dir / "exported"
    docx_builder.DOCX_PATH = docx_path
    caption_to_image = docx_builder.render_all_drawio()
    embedded_count = docx_builder.build_docx(caption_to_image)
    print(f"Built {docx_path.name}: embedded {embedded_count} Draw.io images")


def main() -> None:
    build(
        ROOT / "literature_review.md",
        ROOT / "drawio" / "chapter_2",
        ROOT / "chapter_2_literature_review.docx",
    )
    build(
        ROOT / "chapter_3_methodology.md",
        ROOT / "drawio" / "chapter_3",
        ROOT / "chapter_3_methodology.docx",
    )


if __name__ == "__main__":
    main()
