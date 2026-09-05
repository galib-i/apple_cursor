import glob
import json
import os

import resvg_py


def render_svg(svg_path, out_path, colour_replacements):
    """Render a single SVG to PNG with colour replacements applied."""
    with open(svg_path, "r") as sf:
        svg_data = sf.read()

    # Apply colour replacements
    for colour_repl in colour_replacements:
        svg_data = svg_data.replace(colour_repl["match"], colour_repl["replace"])
        svg_data = svg_data.replace(
            colour_repl["match"].lower(), colour_repl["replace"]
        )

    # Render SVG to PNG
    png_data = resvg_py.svg_to_bytes(svg_string=svg_data)

    with open(out_path, "wb") as pf:
        pf.write(png_data)


def main():
    with open("render.json", "r") as f:
        config = json.load(f)

    for theme, settings in config.items():
        in_dir = settings["dir"]
        out_dir = settings["out"]
        colours = settings["colors"]
        os.makedirs(out_dir, exist_ok=True)
        print(f"  -> Rendering theme: {theme} into {out_dir}/")

        # Render top-level SVGs (e.g. svg/hand1.svg → bitmaps/macOS/hand1.png)
        for svg_path in glob.glob(os.path.join(in_dir, "*.svg")):
            out_name = os.path.basename(svg_path).replace(".svg", ".png")
            render_svg(svg_path, os.path.join(out_dir, out_name), colours)

        # Render animated cursor frames in subdirectories
        # (e.g. svg/left_ptr_watch/left_ptr_watch-01.svg → bitmaps/macOS/left_ptr_watch-01.png)
        for subdir in glob.glob(os.path.join(in_dir, "*/")):
            for svg_path in glob.glob(os.path.join(subdir, "*.svg")):
                out_name = os.path.basename(svg_path).replace(".svg", ".png")
                render_svg(svg_path, os.path.join(out_dir, out_name), colours)


if __name__ == "__main__":
    main()
