resource "aws_security_group" "sg" {
  name        = "allow-ssh-only"
  description = "Allow SSH only" 

  ingress {
    description = "SSH from anywhere"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # זמנית - אח״כ תוכל להגביל ל-IP שלך
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}