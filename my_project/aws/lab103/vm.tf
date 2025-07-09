resource "aws_instance" "vm" {
 ami                         = var.ami
 instance_type               = var.vm_size
 vpc_security_group_ids      = [aws_security_group.sg.id]
 subnet_id  = "subnet-06acd0b316280afeb"

 tags = {
   Name = var.vm_name
 }

user_data = <<-CLOUD
  #cloud-config
  ssh_pwauth: true
  users:
    - default
    - name: ${var.admin_username}
      groups: sudo
      shell: /bin/bash
      sudo: ALL=(ALL) NOPASSWD:ALL
      lock_passwd: false
      passwd: ${var.admin_password}

  # מריץ פקודות פעם אחת אחרי שה-cloud-init מסיים להעלות את המערכת
  runcmd:
    - sed -i 's/^PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config
    - systemctl restart ssh
CLOUD
}


output "vm_public_ip" {
 value = aws_instance.vm.public_ip
}
