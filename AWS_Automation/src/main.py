import json
import sys
from pathlib import Path

from user_input import prompt 
from template_generator import TemplateGenerator 
from terraform_manager import TerraformManager 
from aws_validator import AWSValidator 


def main() -> None:
    # ≡≡ 1. קלט משתמש ≡≡1
    selection = prompt()                 
    context = selection

    # ≡≡ 2. רינדור תבנית ≡≡
    tpl = TemplateGenerator()
    tf_file: Path = tpl.render(context)
    print(f"\n✅ generated {tf_file}")

    # ≡≡ 3. Terraform init/plan/apply ≡≡
    tf_mgr = TerraformManager()
    try:
        outputs = tf_mgr.deploy()   
    except Exception as err:
        print("Terraform failed:", err)
        sys.exit(1)

    print("\n== Terraform outputs ==")
    print(json.dumps(outputs, indent=2))

    # ≡≡ 4. אימות ב-AWS (boto3) ≡≡
    try:
        validator = AWSValidator(selection.region)
        result = validator.validate(outputs)
        print("\n== AWS validation ==")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as err:
        print("AWS validation failed:", err)
        sys.exit(1)

    # ≡≡ 5. Destroy לבחירת המשתמש ≡≡
    try:
        answer = input("\nDestroy infra? (y/N): ").lower()
        if answer == "y":
            tf_mgr.destroy()
            print("✔ Infrastructure destroyed.")
        else:
            print("השארת את המשאבים פעילים – זכור שעלולים להיות חיובים.")
    except KeyboardInterrupt:
        print("\n(Interrupted) – no destroy executed.")


if __name__ == "__main__":
    main()
