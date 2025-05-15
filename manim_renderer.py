from manim import *
import subprocess
from pathlib import Path
import os
from PIL import Image, ImageTk


class FormulaRendererManim:
    def __init__(self):
        pass

    
    def render_formula_to_image(self, formula, output_name="formula") :
        temp_file = Path("temp_render.py")

        code = f"""from manim import *

class FormulaScene(Scene):
    def construct(self):
        formula = MathTex(r"{formula}", font_size=36)
        self.add(formula)
        self.wait(0.1)                    
        """
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(code)

        cmd = [
            "manim",
            "-ql",
            "--format=png",
            str(temp_file),
            "FormulaScene"
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)
            img_path = f"{output_name}.png"
            if img_path.exists():
                return Image.open(img_path)
            return None
        except subprocess.CalledProcessError as e:
            print(f"Ошибка рендеринга: {e.stderr.decode()}")
            return None
        finally:
            try:
                temp_file.unlink()
            except:
                pass