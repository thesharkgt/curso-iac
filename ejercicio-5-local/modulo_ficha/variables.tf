variable "nombre" {
  description = "Nombre ficticio de la ficha"
  type        = string

  validation {
    condition     = startswith(var.nombre, "portal-")
    error_message = "El nombre debe empezar por portal-."
  }
}

variable "entorno" {
  description = "Entorno ficticio de la ficha"
  type        = string

  validation {
    condition     = contains(["desarrollo", "pruebas", "integracion"], var.entorno)
    error_message = "Usa desarrollo, pruebas o integracion."
  }
}
