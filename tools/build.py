import math
import shutil
import zipfile

from pixel_font_builder import FontBuilder, WeightName, SerifStyle, SlantStyle, WidthStyle, Glyph, opentype
from pixel_font_knife import glyph_file_util

from tools import path_define


def main():
    if path_define.build_dir.exists():
        shutil.rmtree(path_define.build_dir)
    path_define.outputs_dir.mkdir(parents=True)
    path_define.releases_dir.mkdir(parents=True)

    context = glyph_file_util.load_context(path_define.glyphs_dir)
    glyph_file_util.normalize_context(context, path_define.glyphs_dir)

    builder = FontBuilder()
    builder.font_metric.font_size = 10
    builder.font_metric.horizontal_layout.ascent = 10
    builder.font_metric.horizontal_layout.descent = 0
    builder.font_metric.vertical_layout.ascent = 5
    builder.font_metric.vertical_layout.descent = -5
    builder.font_metric.x_height = 7
    builder.font_metric.cap_height = 9

    builder.meta_info.version = '1.1.0'
    builder.meta_info.family_name = 'Vertical Sans'
    builder.meta_info.weight_name = WeightName.BOLD
    builder.meta_info.serif_style = SerifStyle.SANS_SERIF
    builder.meta_info.slant_style = SlantStyle.NORMAL
    builder.meta_info.width_style = WidthStyle.PROPORTIONAL
    builder.meta_info.manufacturer = 'Aloteri'
    builder.meta_info.designer = 'Aloteri'
    builder.meta_info.description = 'Vertical Sans Pixel Font.'
    builder.meta_info.copyright_info = "Copyright (c) 2023-2024, Aloteri (aloteri@foxmail.com), with Reserved Font Name 'Vertical'."
    builder.meta_info.license_info = 'This Font Software is licensed under the SIL Open Font License, Version 1.1.'
    builder.meta_info.vendor_url = 'https://github.com/archive-chan/vertical-sans'
    builder.meta_info.designer_url = 'https://github.com/archive-chan'
    builder.meta_info.license_url = 'https://openfontlicense.org'

    character_mapping = glyph_file_util.get_character_mapping(context)
    builder.character_mapping.update(character_mapping)

    glyph_sequence = glyph_file_util.get_glyph_sequence(context)
    for glyph_file in glyph_sequence:
        horizontal_offset_y = (builder.font_metric.horizontal_layout.ascent + builder.font_metric.horizontal_layout.descent - glyph_file.height) // 2
        vertical_offset_x = -math.ceil(glyph_file.width / 2)
        builder.glyphs.append(Glyph(
            name=glyph_file.glyph_name,
            horizontal_offset=(0, horizontal_offset_y),
            advance_width=glyph_file.width,
            vertical_offset=(vertical_offset_x, 0),
            advance_height=builder.font_metric.font_size,
            bitmap=glyph_file.bitmap.data,
        ))

    builder.save_otf(path_define.outputs_dir.joinpath('VerticalSans.otf'))
    builder.save_otf(path_define.outputs_dir.joinpath('VerticalSans.woff2'), flavor=opentype.Flavor.WOFF2)
    builder.save_ttf(path_define.outputs_dir.joinpath('VerticalSans.ttf'))
    builder.save_bdf(path_define.outputs_dir.joinpath('VerticalSans.bdf'))
    builder.save_pcf(path_define.outputs_dir.joinpath('VerticalSans.pcf'))

    builder.meta_info.family_name = 'Vertical Sans SquareDot'
    builder.opentype_config.outlines_painter = opentype.SquareDotOutlinesPainter()
    builder.save_otf(path_define.outputs_dir.joinpath('VerticalSans-SquareDot.otf'))
    builder.save_otf(path_define.outputs_dir.joinpath('VerticalSans-SquareDot.woff2'), flavor=opentype.Flavor.WOFF2)
    builder.save_ttf(path_define.outputs_dir.joinpath('VerticalSans-SquareDot.ttf'))
    builder.save_bdf(path_define.outputs_dir.joinpath('VerticalSans-SquareDot.bdf'))
    builder.save_pcf(path_define.outputs_dir.joinpath('VerticalSans-SquareDot.pcf'))

    builder.meta_info.family_name = 'Vertical Sans CircleDot'
    builder.opentype_config.outlines_painter = opentype.CircleDotOutlinesPainter()
    builder.save_otf(path_define.outputs_dir.joinpath('VerticalSans-CircleDot.otf'))
    builder.save_otf(path_define.outputs_dir.joinpath('VerticalSans-CircleDot.woff2'), flavor=opentype.Flavor.WOFF2)
    builder.save_ttf(path_define.outputs_dir.joinpath('VerticalSans-CircleDot.ttf'))
    builder.save_bdf(path_define.outputs_dir.joinpath('VerticalSans-CircleDot.bdf'))
    builder.save_pcf(path_define.outputs_dir.joinpath('VerticalSans-CircleDot.pcf'))

    with zipfile.ZipFile(path_define.releases_dir.joinpath(f'VerticalSans-Bold-v{builder.meta_info.version}.zip'), 'w') as file:
        file.write(path_define.project_root_dir.joinpath('LICENSE'), 'OFL.txt')
        for font_file_path in path_define.outputs_dir.iterdir():
            if font_file_path.suffix in ('.otf', '.woff2', '.ttf', '.bdf', '.pcf'):
                file.write(font_file_path, font_file_path.name)

    if path_define.www_fonts_dir.exists():
        shutil.rmtree(path_define.www_fonts_dir)
    path_define.www_fonts_dir.mkdir(parents=True)

    for font_file_path in path_define.outputs_dir.iterdir():
        if font_file_path.suffix == '.woff2':
            shutil.copyfile(font_file_path, path_define.www_fonts_dir.joinpath(font_file_path.name))


if __name__ == '__main__':
    main()
