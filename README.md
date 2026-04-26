# Digitalización de facturas físicas mediante OCR propio

Proyecto de grado — Universidad Manuela Beltrán (en desarrollo, entrega finales 2026)

---

## El problema

A pesar de que existe normativa que regula la facturación electrónica, en Colombia todavía hay un volumen considerable de empresas que operan con facturas físicas en su día a día. Digitalizarlas implica hoy depender de servicios externos como Tesseract o APIs de visión de terceros, lo que genera dependencia tecnológica y limita la adaptación a formatos locales específicos.

La pregunta que guía este proyecto es si es viable construir un motor de OCR propio, entrenado sobre facturas físicas colombianas, que no dependa de ningún servicio externo y que pueda extraer y validar los campos relevantes de forma autónoma.

---

## Qué estamos construyendo

Un sistema que recibe imágenes de facturas físicas y extrae automáticamente sus campos (fecha, NIT, total, líneas de detalle, entre otros) usando un modelo de visión por computadora entrenado por el equipo, sin Tesseract ni APIs de reconocimiento externas.

El sistema además valida los resultados extraídos y los almacena de forma estructurada para su consulta posterior.

---

## Stack

- Python como lenguaje principal
- Visión por computadora para el motor de OCR
- Alembic para migraciones y versionado del esquema de base de datos
- Esquema de base de datos con tablas diferenciadas para resultados OCR y validaciones
- Arquitectura dividida en fases con reportes de auditoría por etapa

---

## Estado actual

El proyecto está en desarrollo activo. Tenemos avances funcionales en extracción y validación de campos. La entrega final está prevista para finales de 2026.

La estructura del repositorio refleja el proceso de construcción por fases, con documentación de auditoría y listas de verificación por entorno (local y producción en Render).

---

## Equipo

Proyecto desarrollado por tres estudiantes de ingeniería de la Universidad Manuela Beltrán como trabajo de grado.
