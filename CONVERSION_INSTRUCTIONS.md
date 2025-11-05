
# INSTRUCCIONES PARA CONVERTIR ARCHIVOS A PDF

## 🎯 Objetivo
Convertir los archivos .txt generados a PDFs profesionales para el curso.

## 📋 Método 1: Usando Microsoft Word/Google Docs (Recomendado)

1. Abrir cada archivo .txt en Microsoft Word o Google Docs
2. Aplicar formato profesional:
   - Fuente: Georgia o Times New Roman, 12pt
   - Márgenes: 2cm en todos los lados
   - Espaciado: 1.5 líneas
   - Títulos en negrita y tamaño 14pt
3. Archivo -> Guardar como -> PDF
4. Repetir para cada archivo

## 📋 Método 2: Usando Convertidores Online

1. Ir a https://smallpdf.com/word-to-pdf o similar
2. Subir cada archivo .txt
3. Convertir a PDF
4. Descargar los PDFs

## 📋 Método 3: Automatizado con Scripts

Si tienes acceso a herramientas de línea de comandos:

```bash
# Usando pandoc (si está instalado)
for file in materials/**/*_updated.txt; do
    pandoc "$file" -o "${file%.txt}.pdf" --pdf-engine=xelatex
done

# O usando wkhtmltopdf
for file in materials/**/*_updated.txt; do
    a2ps "$file" -o - | ps2pdf - "${file%.txt}.pdf"
done
```

## 📁 Archivos a Convertir

- materials/cuadernos/S2_Espanol_Intensivo_updated.txt
- materials/cuadernos/S5_Espanol_Intensivo_updated.txt
- materials/cuadernos/S10_Espanol_Intensivo_updated.txt
- materials/cuadernos/S3_Espanol_Intensivo_updated.txt
- materials/cuadernos/S11_Espanol_Intensivo_updated.txt
- materials/cuadernos/S4_Espanol_Intensivo_updated.txt
- materials/cuadernos/S12_Espanol_Intensivo_updated.txt
- materials/cuadernos/S7_Espanol_Intensivo_updated.txt
- materials/cuadernos/S8_Espanol_Intensivo_updated.txt
- materials/cuadernos/S9_Espanol_Intensivo_updated.txt
- materials/cuadernos/S6_Espanol_Intensivo_updated.txt
- materials/cuadernos/S1_Espanol_Intensivo_updated.txt
- materials/plantillas/ejercicios_basicos_updated.txt
- materials/vocabulario/flashcards_sesion1-6_updated.txt
- materials/tarjetas/nombres_personajes_updated.txt

## ✅ Verificación Final

1. Verificar que todos los PDFs tengan las fechas correctas (noviembre 2025)
2. Verificar que el formato sea profesional y legible
3. Probar que los PDFs se abren correctamente
4. Subir los nuevos PDFs al repositorio

## 🚀 Subida a GitHub

```bash
git add .
git commit -m "Updated course materials to November 2025 with new PDFs"
git push origin main
```
