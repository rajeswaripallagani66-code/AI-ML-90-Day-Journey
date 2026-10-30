variable "region" {
  default = "ap-south-1"
}
variable "vpc_id" {
  default = ""
}
variable "subnet_ids" {
  type    = list(string)
  default = []
}