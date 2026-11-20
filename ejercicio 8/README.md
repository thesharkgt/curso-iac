# Ejercicio 8: etiquetas y responsables por entorno

Este laboratorio continúa el catálogo del ejercicio 7. Mantiene las dos fichas ficticias `portal` y `ayuda`, y añade a cada una un mapa `etiquetas` con proyecto, entorno y equipo responsable.

## El recorrido del dato

La variable `responsable` tiene un valor predeterminado para pruebas. El escenario de integración define otro equipo. El valor pasa desde la configuración principal al módulo y termina dentro de `terraform_data.ficha.input`, donde la política Python puede revisarlo en el plan.

| Escenario | Ficha principal | Entorno | Responsable esperado |
| --- | --- | --- | --- |
| Predeterminado | `portal-demo` | `pruebas` | `equipo-lab` |
| Integración | `portal-interno` | `integracion` | `equipo-integracion` |

Es como anotar en una ficha interna de una empresa el nombre del proyecto, el entorno donde se usa y el equipo que debe atenderlo. En este ejercicio son datos de ejemplo dentro de `terraform_data`; no son etiquetas aplicadas a un servicio real.

## Qué comprueba la política

La política conserva las reglas del ejercicio 7: solo admite las fichas `portal` y `ayuda`, el tipo `terraform_data`, la acción `create`, los nombres y los entornos aprobados. También exige las tres etiquetas exactas, el proyecto `nexo-portal`, que la etiqueta de entorno coincida y que el equipo corresponda al entorno.

La comprobación de marcas desconocidas y sensibles recorre mapas y listas anidados. Un valor `false` dentro de `after_unknown` o `after_sensitive` no provoca un rechazo; un valor `true` sí.

Si se asigna `equipo-lab` a integración, OpenTofu todavía puede validar y calcular el plan: el texto es una cadena válida. La política debe rechazarlo con `POLÍTICA RECHAZADA: responsable no aprobado para integracion`. Al restaurar `equipo-integracion`, ambos escenarios vuelven a aprobarse.

## Comprobaciones observadas

- [Primera ejecución aprobada](https://github.com/thesharkgt/curso-iac/actions/runs/44729661219): formato, validación, los dos planes y las políticas pasaron.
- [Prueba del equipo equivocado](https://github.com/thesharkgt/curso-iac/actions/runs/44729777199): el formato, la validación y ambos planes pasaron; la política de integración rechazó `equipo-lab` con el mensaje esperado.
- [Corrección aprobada](https://github.com/thesharkgt/curso-iac/actions/runs/44729835861): ambos planes y ambas políticas volvieron a pasar.

La revisión con IA señaló que `tofu validate` comprueba la forma de los datos, pero no si el equipo tiene permiso para ese entorno. Se comprobó publicando el valor incorrecto: el plan de integración se creó con dos fichas, y el rechazo apareció en la política, no en la validación ni en el plan.

Decisión de diseño: una tabla explícita relaciona cada entorno permitido con su equipo responsable. Así se puede revisar la regla de forma sencilla y se evita usar un equipo por defecto para todos los entornos. Una recomendación para un sistema real sería proteger la política con revisión independiente y permisos de rama; no se implementa en este laboratorio.

## Validación y límites

El workflow `../.github/workflows/validacion-ejercicio-8.yml` comprueba formato, configuración, los dos planes y sus políticas en GitHub Actions. El laboratorio no ejecuta `tofu apply`, no despliega servicios y no crea etiquetas reales. Una política editable dentro de la misma rama sirve para aprender, pero no es por sí sola un control independiente de producción.
