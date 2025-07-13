import json
from pathlib import Path
from typing import Dict, Any
from python_terraform import Terraform


class TerraformManager:
    def __init__(self, working_dir: str = "../outputs"):
        base = Path(__file__).resolve().parent
        full_path = base / working_dir
        self.tf = Terraform(working_dir=str(full_path))
        self.working_dir = full_path

    def deploy(self) -> Dict[str, Any]:
        print("\nRunning: terraform init")
        self._run("init")

        print("\nRunning: terraform plan")
        self._run("plan", extra_args=["-out=plan.out"])  # חשוב: arg אחד עם =

        print("\nRunning: terraform apply")
        self._run("apply", extra_args=["plan.out"], skip_plan=True)

        print("\nGetting Terraform outputs")
        return self._get_outputs()

    def destroy(self) -> None:
        print("\nRunning: terraform destroy")
        ret_code, stdout, stderr = self.tf.destroy(auto_approve=True)

        print(stdout.decode() if isinstance(stdout, bytes) else stdout)

        if ret_code != 0:
            err_msg = stderr.decode() if isinstance(stderr, bytes) else stderr
            raise RuntimeError(f"Terraform destroy failed:\n{err_msg}")

    def _run(self, cmd: str, extra_args=None, **kwargs) -> None:
        extra_args = extra_args or []
        fn = getattr(self.tf, cmd)

        ret_code, stdout, stderr = fn(*extra_args, **kwargs)

        print(stdout.decode() if isinstance(stdout, bytes) else stdout)

        if ret_code not in [0, 2]:  # <-- פתרון כאן
            print(stderr.decode() if isinstance(stderr, bytes) else stderr)
            raise RuntimeError(f"Terraform {cmd} failed")

    def _get_outputs(self) -> Dict[str, Any]:
        _, raw = self.tf.output(json=True)
        outputs = json.loads(raw)
        return {
            "instance_id": outputs.get("instance_id", {}).get("value", "N/A"),
            "alb_dns": outputs.get("alb_dns", {}).get("value", "N/A"),
            "public_ip": outputs.get("instance_public_ip", {}).get("value", "N/A"),
        }
