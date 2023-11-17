import os
import sys
from pathlib import Path

import ir_filter


def os_system(cmd):
    print(f'Run: {cmd}')
    os.system(cmd)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python markdown2latex.py YOUR_WORKSPACE_DIRECTORY')
        exit(1)

    workspace_dir = Path(sys.argv[1])
    print(f'Picked: workspace_dir={workspace_dir}')

    path_build_dir = workspace_dir / "build"
    path_build_dir.mkdir(parents=True, exist_ok=True)

    path_markdown_dir = workspace_dir / "markdown"

    for path_markdown_md in path_markdown_dir.glob('*.md'):
        path_stage_1_json = path_build_dir / "stage_1.json"
        path_stage_2_json = path_build_dir / "stage_2.json"
        path_template_tex = workspace_dir / "template.tex"
        path_output_tex = path_build_dir / f'{path_markdown_md.stem}.tex'

        os_system(f'pandoc '
                  f'-f markdown '
                  f'-t json '
                  f'{path_markdown_md} '
                  f'-o {path_stage_1_json}')

        print('Run: ir_filter')
        ir_filter.run(
            template_dir=workspace_dir,
            input_stream=path_stage_1_json.open('r'),
            output_stream=path_stage_2_json.open('w'),
        )

        os_system(f'pandoc '
                  f'-f json '
                  f'-t latex '
                  f'--template={path_template_tex} '
                  f'--highlight-style=tango '
                  f'{path_stage_2_json} '
                  f'-o {path_output_tex}')

        path_stage_1_json.unlink()
        path_stage_2_json.unlink()
