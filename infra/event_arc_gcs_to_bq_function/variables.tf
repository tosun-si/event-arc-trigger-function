variable "project_id" {
  description = "Project ID, used to enforce providing a project id"
  type        = string
}

variable "env" {
  description = "Environment name among dev , uat, prod"
  type        = string
}
