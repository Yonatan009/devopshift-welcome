from pathlib import Path
from jinja2 import Environment, FileSystemLoader

class TemplateGenerator:
    def __init__(self, template_dir: str = "../templates", out_dir: str = "../outputs"):
        base = Path(__file__).resolve().parent
        self.env = Environment(loader=FileSystemLoader(base / template_dir))
        self.out_dir = base / out_dir
        self.out_dir.mkdir(parents=True, exist_ok=True)  # ← הוספנו parents=True

    def render(self, context: dict, template_name: str = "terraform_template.j2") -> Path:
        """Return path to rendered main.tf."""
        tf_text = self.env.get_template(template_name).render(**context)
        tf_path = self.out_dir / "main.tf"
        tf_path.write_text(tf_text)
        return tf_path
