provider "aws" {
 region = var.region
}

variable "region" {
 default = "us-west-1"
}


variable "ami" {
 default = "ami-025a9b1af952cc749"
 }
variable "vm_name" {
 default = "vm-yonatan"
}

variable "admin_username" {
 default = "admin-user"
}

variable "admin_password" {
 default = "Password123!"
}

variable "vm_size" {
 default = "t2.micro"
}