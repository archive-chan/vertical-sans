import logging
import os

from pixel_font_builder import FontBuilder, Glyph, SerifMode, WidthMode

from utils import fs_util, glyph_util

project_root_dir = os.path.dirname(__file__)
glyphs_dir = os.path.join(project_root_dir, 'assets', 'glyphs')
outputs_dir = os.path.join(project_root_dir, 'build', 'outputs')

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('build')


def _collect_glyph_files():
    character_mapping = {}
    glyph_file_paths = {}

    for glyph_file_dir, glyph_file_name in fs_util.walk_files(glyphs_dir):
        if not glyph_file_name.endswith('.png'):
            continue
        glyph_file_path = os.path.join(glyph_file_dir, glyph_file_name)
        if glyph_file_name == 'notdef.png':
            glyph_file_paths['.notdef'] = glyph_file_path
        else:
            hex_name = glyph_file_name.removesuffix('.png')
            code_point = int(hex_name, 16)
            glyph_name = f'uni{code_point:04X}'
            character_mapping[code_point] = glyph_name
            glyph_file_paths[glyph_name] = glyph_file_path

    return character_mapping, glyph_file_paths


def _create_builder(character_mapping: dict[int, str], glyph_file_paths: dict[str, str]) -> FontBuilder:
    builder = FontBuilder(
        size=10,
        ascent=10,
        descent=0,
        x_height=7,
        cap_height=9,
    )

    builder.character_mapping.update(character_mapping)
    for glyph_name, glyph_file_path in glyph_file_paths.items():
        glyph_data, glyph_width, glyph_height = glyph_util.load_glyph_data_from_png(glyph_file_path)
        builder.add_glyph(Glyph(
            name=glyph_name,
            advance_width=glyph_width,
            offset=(0, 0),
            data=glyph_data,
        ))

    builder.meta_infos.version = '1.1.0'
    builder.meta_infos.family_name = 'Vertical Sans'
    builder.meta_infos.style_name = 'Bold'
    builder.meta_infos.serif_mode = SerifMode.SANS_SERIF
    builder.meta_infos.width_mode = WidthMode.PROPORTIONAL
    builder.meta_infos.manufacturer = 'Aloteri'
    builder.meta_infos.designer = 'Aloteri'
    builder.meta_infos.description = 'Vertical Sans Pixel Font.'
    builder.meta_infos.copyright_info = 'Copyright (c) 2023, Aloteri'
    builder.meta_infos.license_info = 'This Font Software is licensed under the SIL Open Font License, Version 1.1.'
    builder.meta_infos.vendor_url = 'https://github.com/aloteri-archive/vertical-sans'
    builder.meta_infos.designer_url = 'https://github.com/aloteri-archive'
    builder.meta_infos.license_url = 'https://scripts.sil.org/OFL'

    return builder


def _make_font_files():
    character_mapping, glyph_file_paths = _collect_glyph_files()
    builder = _create_builder(character_mapping, glyph_file_paths)

    otf_builder = builder.to_otf_builder()
    otf_file_path = os.path.join(outputs_dir, 'VerticalSans.otf')
    otf_builder.save(otf_file_path)
    logger.info("Make font file: '%s'", otf_file_path)

    otf_builder.font.flavor = 'woff2'
    woff2_file_path = os.path.join(outputs_dir, 'VerticalSans.woff2')
    otf_builder.save(woff2_file_path)
    logger.info("Make font file: '%s'", woff2_file_path)

    ttf_file_path = os.path.join(outputs_dir, 'VerticalSans.ttf')
    builder.save_ttf(ttf_file_path)
    logger.info("Make font file: '%s'", ttf_file_path)

    bdf_file_path = os.path.join(outputs_dir, 'VerticalSans.bdf')
    builder.save_bdf(bdf_file_path)
    logger.info("Make font file: '%s'", bdf_file_path)


def main():
    fs_util.delete_dir(outputs_dir)
    fs_util.make_dirs(outputs_dir)
    _make_font_files()


if __name__ == '__main__':
    main()
