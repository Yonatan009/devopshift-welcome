# user_input.py
# Collect deployment parameters from the user (plain prompts)

AMI_OPTIONS = {
    "1": "ami-0eb9d6fc9fab44d24",  # Amazon Linux 2023 (us-east-2)
    "2": "ami-0d1b5a8c13042c939",  # Ubuntu 22.04 LTS   (us-east-2)
}

INSTANCE_TYPES = {"1": "t3.small", "2": "t3.medium"}
DEFAULT_REGION = "us-east-2"

# Fixed values from instructor
VPC_ID = "vpc-0a691b1cda1dea4be"
SUBNET_A_ID = "subnet-09a9b4fe4e74051b3"
SUBNET_B_ID = "subnet-05860172a9327d826"

def prompt() -> dict | None:
    """
    Ask the user for AMI, instance type, region, and ALB name.
    Returns a dict suitable for Jinja2: template.render(**context)
    """
    try:
        # AMI
        print("Choose AMI:")
        print(" 1) Amazon Linux 2023")
        print(" 2) Ubuntu 22.04")
        ami_choice = input("Select (1/2): ").strip()
        ami = AMI_OPTIONS.get(ami_choice, AMI_OPTIONS["1"])

        # Instance type
        print("\nChoose instance type:")
        print(" 1) t3.small")
        print(" 2) t3.medium")
        inst_choice = input("Select (1/2): ").strip()
        instance_type = INSTANCE_TYPES.get(inst_choice, INSTANCE_TYPES["1"])

        # Region (only us-east-2 is accepted)
        region = input("\nAWS region [us-east-2]: ").strip() or DEFAULT_REGION
        if region != DEFAULT_REGION:
            print(f"Only {DEFAULT_REGION} is supported. Using default.")
            region = DEFAULT_REGION

        # Load Balancer name
        lb_name = input("\nALB name [my-alb]: ").strip() or "my-alb"

        az1, az2 = f"{region}a", f"{region}b"

        return {
            "ami": ami,
            "instance_type": instance_type,
            "region": region,
            "az1": az1,
            "az2": az2,
            "availability_zone": az1,
            "lb_name": lb_name,
            "vpc_id": VPC_ID,
            "subnet_a_id": SUBNET_A_ID,
            "subnet_b_id": SUBNET_B_ID
        }

    except KeyboardInterrupt:
        print("\nAborted.")
        return None