# Ejercicio 5: módulo local reutilizable

Proyecto autocontenido del ejercicio 5. Usa `terraform_data` para representar dos fichas ficticias: la principal (`portal`) y la de ayuda (`ayuda`). No configura proveedores cloud ni crea VMs, redes o servicios reales.

## Contenido

- `modulo_ficha/`: recurso ficticio, entradas obligatorias y salida `resumen`.
- `main.tf` y `outputs.tf`: dos instancias del módulo y su resumen conjunto.
- `variables.tf`: valores predeterminados del escenario de pruebas.
- `escenario-integracion.tfvars`: valores del escenario de integración.
- `../.github/workflows/validacion.yml`: workflow de la raíz del repositorio que ejecuta formato recursivo, validación, planes y evidencia sobre esta carpeta.

## Ejecución y límites

No se requiere instalar OpenTofu en este equipo para conservar o revisar el proyecto. El workflow configura OpenTofu en un runner temporal de GitHub Actions; para obtener esos resultados hay que publicar el proyecto en un repositorio habilitado para Actions. No se ha ejecutado `tofu init`, `tofu plan` ni `tofu apply` localmente. `apply` no forma parte de este ejercicio.

La ejecución verde [de referencia](https://github.com/thesharkgt/curso-iac/actions/runs/44293713887) confirmó ambos escenarios: dos recursos `terraform_data` por plan (2 to add, 0 to change, 0 to destroy), sin cambios ni destrucciones. Por defecto: `portal-demo/pruebas` y `portal-ayuda/pruebas`; integración: `portal-interno/integracion` y `portal-ayuda/integracion`. Son resultados de planes; no se ejecutó `apply`.

## Arquitectura ficticia

- Necesidad: representar un portal y una ficha de ayuda sin desplegar infraestructura real.
- Reutilización: ambas fichas usan el módulo local `modulo_ficha`.
- Entradas: `nombre` y `entorno`, ambas obligatorias en cada llamada al módulo y validadas.
- Escenarios: valores predeterminados de pruebas y variante de integración en `escenario-integracion.tfvars`.
- Evidencias: GitHub Actions está configurado para revisar formato, validar y generar planes y un artefacto de evidencia.
- Limitación: no se ejecuta `apply`; `terraform_data` es una representación ficticia, no una VM, red ni aplicación.
