from pathlib import Path

project_root_dir = Path(__file__).parent.joinpath('..').resolve()

assets_dir = project_root_dir.joinpath('assets')
glyphs_dir = assets_dir.joinpath('glyphs')

build_dir = project_root_dir.joinpath('build')
outputs_dir = build_dir.joinpath('outputs')
releases_dir = build_dir.joinpath('releases')

www_dir = project_root_dir.joinpath('www')
www_fonts_dir = www_dir.joinpath('fonts')
