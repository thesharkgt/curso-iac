# Ejercicio 7: catálogo de fichas reutilizable

Proyecto del ejercicio 7, derivado del módulo ficticio del ejercicio 5 y de las reglas de gobierno documentadas en el ejercicio 6. No modifica `ejercicio-5-local` ni los archivos Terraform de la raíz; añade un workflow independiente en `.github/workflows/` para validar esta carpeta.

## Catálogo de fichas

El mapa `local.catalogo` contiene exactamente las claves `portal` y `ayuda`. Un único bloque `module "fichas"` usa `for_each` para crear una instancia lógica del módulo local por clave; `each.value` entrega el nombre de cada ficha.

La salida `resumen` construye un mapa que conserva esas claves y muestra los valores previstos de cada instancia. La política Python solo admite las direcciones `module.fichas["portal"].terraform_data.ficha` y `module.fichas["ayuda"].terraform_data.ficha`, además de conservar las reglas del ejercicio 6: dos recursos `terraform_data`, acción `create`, entradas conocidas `nombre` y `entorno`, nombre con prefijo `portal-`, ayuda llamada `portal-ayuda` y entornos iguales entre `desarrollo`, `pruebas` e `integracion`.

Si se añade una tercera entrada `informes`, `tofu validate` y el plan pueden aceptarla como configuración, pero la política rechaza el plan porque el catálogo aprobado contiene exactamente portal y ayuda. Retirar esa entrada restaura el catálogo aprobado.

## Escenarios y comprobación

- Valores por defecto: `portal-demo` y `portal-ayuda` en `pruebas`.
- `escenario-integracion.tfvars`: `portal-interno` y `portal-ayuda` en `integracion`.
- El workflow independiente `../.github/workflows/validacion-ejercicio-7.yml` comprueba formato, validación, los dos planes y sus políticas en GitHub Actions.

## Evidencia en GitHub Actions

- [Catálogo de dos fichas aprobado](https://github.com/thesharkgt/curso-iac/actions/runs/44708809085).
- [Prueba de tercera ficha rechazada por la política](https://github.com/thesharkgt/curso-iac/actions/runs/44708979455).
- [Corrección: catálogo de dos fichas aprobado](https://github.com/thesharkgt/curso-iac/actions/runs/44709241053).

La ejecución roja es intencionada: formato, validación y plan pasaron; falló la política del plan predeterminado con `POLÍTICA RECHAZADA: se esperan exactamente las fichas portal y ayuda`.

Para validar en un entorno con OpenTofu y Python ya disponibles:

```powershell
tofu init -backend=false -input=false
tofu fmt -check -diff -recursive
tofu validate -no-color
tofu plan -input=false -no-color -out=plan-predeterminado.tfplan
tofu show -json -plan=plan-predeterminado.tfplan | python politica_plan.py
```

Para el escenario de integración, guarda el plan como `plan-integracion.tfplan` usando `-var-file=escenario-integracion.tfvars` y pásalo a `tofu show -json` de la misma forma. El plan solo calcula cambios: este ejercicio no ejecuta `tofu apply`, no despliega infraestructura cloud y no crea una plataforma de autoservicio real.
