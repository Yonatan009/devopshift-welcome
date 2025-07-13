import json
from pathlib import Path
import boto3

class AWSValidator:
    def __init__(self, region: str):
        self.ec2 = boto3.client("ec2", region_name=region)
        self.elb = boto3.client("elbv2", region_name=region)

    def validate(self, tf_outputs: dict, path: str = "../outputs/aws_validation.json") -> dict:
        inst_id = tf_outputs["instance_id"]["value"]
        alb_dns = tf_outputs["alb_dns"]["value"]

        inst = self.ec2.describe_instances(InstanceIds=[inst_id])["Reservations"][0]["Instances"][0]
        data = {
            "instance_id": inst_id,
            "instance_state": inst["State"]["Name"],
            "public_ip": inst.get("PublicIpAddress", "N/A"),
            "load_balancer_dns": alb_dns,
        }
        Path(path).write_text(json.dumps(data, indent=2))
        return data
