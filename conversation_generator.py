#!/usr/bin/env python3
"""
Generador de prácticas de conversación interactivas para el curso de español
"""

from fpdf import FPDF
import json
import os

class ConversationPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, 'Practica de Conversacion - Curso Intensivo de Espanol', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.set_text_color(102, 102, 102)
        self.cell(0, 6, 'Nivel 3 CLM (A1.2-A2.1) - Universidad de Granada', 0, 1, 'C')
        self.ln(8)

    def footer(self):
        self.set_y(-20)
        self.set_font('Arial', 'I', 9)
        self.set_text_color(128, 128, 128)
        self.cell(0, 6, f'Pagina {self.page_no()} de {{nb}}', 0, 1, 'C')
        self.cell(0, 6, 'Profesor: Javier Benitez Lainez | Centro de Lenguas Modernas', 0, 0, 'C')

def create_conversation_practice():
    conversations = [
        {
            "title": "En el Restaurante",
            "context": "Estás en un restaurante español y quieres pedir comida",
            "dialogue": [
                {"person": "Camarero/a", "text": "¡Buenas tardes! ¿Qué van a tomar?"},
                {"person": "Tú", "text": "Hola, me gustaría ver el menú, por favor"},
                {"person": "Camarero/a", "text": "Claro, aquí tienen el menú. ¿Desean algo de beber?"},
                {"person": "Tú", "text": "Una agua mineral y una cerveza, por favor"},
                {"person": "Camarero/a", "text": "Perfecto. ¿Ya saben qué van a comer?"},
                {"person": "Tú", "text": "Sí, quiero la paella valenciana y mi amigo quiere la tortilla española"},
                {"person": "Camarero/a", "text": "Excelente elección. Enseguida lo traigo"},
                {"person": "Tú", "text": "Muchas gracias"},
                {"person": "Camarero/a", "text": "De nada"}
            ]
        },
        {
            "title": "Pidiendo Direcciones",
            "context": "Estás perdido en Granada y necesitas llegar a la Alhambra",
            "dialogue": [
                {"person": "Tú", "text": "Disculpe, ¿podría ayudarme?"},
                {"person": "Local", "text": "Claro que sí, ¿qué necesita?"},
                {"person": "Tú", "text": "Busco la Alhambra. ¿Sabe cómo llegar?"},
                {"person": "Local", "text": "¡Claro! Está muy cerca. Siga toda esta calle recta"},
                {"person": "Tú", "text": "¿Recto hasta el final?"},
                {"person": "Local", "text": "Sí, hasta el final. Luego gire a la derecha y verá los jardines"},
                {"person": "Tú", "text": "¿Cuánto tiempo se camina aproximadamente?"},
                {"person": "Local", "text": "Unos 15 minutos caminando"},
                {"person": "Tú", "text": "Muchísimas gracias por su ayuda"},
                {"person": "Local", "text": "De nada. ¡Que disfrute su visita!"}
            ]
        },
        {
            "title": "En la Tienda de Ropa",
            "context": "Quieres comprar ropa en una tienda española",
            "dialogue": [
                {"person": "Tú", "text": "Buenos días. ¿Están buscando algo?"},
                {"person": "Dependiente/a", "text": "Hola, sí. ¿Puedo ayudarle?"},
                {"person": "Tú", "text": "Busco una camisa azul, talla mediana"},
                {"person": "Dependiente/a", "text": "Claro, tenemos varios modelos. ¿Prefiere manga larga o corta?"},
                {"person": "Tú", "text": "Manga larga, por favor"},
                {"person": "Dependiente/a", "text": "¿Qué le parece esta? Es de algodón y muy cómoda"},
                {"person": "Tú", "text": "Me gusta. ¿Cuánto cuesta?"},
                {"person": "Dependiente/a", "text": "Son 35 euros"},
                {"person": "Tú", "text": "Está bien. ¿Aceptan tarjetas de crédito?"},
                {"person": "Dependiente/a", "text": "Sí, por supuesto. Pase por caja cuando quiera"}
            ]
        },
        {
            "title": "En el Supermercado",
            "context": "Haciendo la compra semanal",
            "dialogue": [
                {"person": "Tú", "text": "Hola, ¿dónde puedo encontrar el pan?"},
                {"person": "Empleado/a", "text": "En el pasillo 3, al fondo a la derecha"},
                {"person": "Tú", "text": "Perfecto. ¿Y los productos lácteos?"},
                {"person": "Empleado/a", "text": "En los refrigeradores, pasillo 1"},
                {"person": "Tú", "text": "¿Tienen leche deslactosada?"},
                {"person": "Empleado/a", "text": "Sí, tenemos varias marcas en el refrigerador azul"},
                {"person": "Tú", "text": "Gracias. ¿Dónde están las frutas y verduras?"},
                {"person": "Empleado/a", "text": "En la entrada, a su izquierda. Todo está fresco hoy"},
                {"person": "Tú", "text": "Maravilloso. ¿Hay alguna oferta especial?"},
                {"person": "Empleado/a", "text": "Sí, las manzanas están en 2x1 esta semana"}
            ]
        },
        {
            "title": "En la Farmacia",
            "context": "Necesitas comprar medicamentos",
            "dialogue": [
                {"person": "Tú", "text": "Buenos días, necesito ayuda"},
                {"person": "Farmacéutico/a", "text": "Hola, ¿qué necesita?"},
                {"person": "Tú", "text": "Tengo dolor de cabeza y fiebre"},
                {"person": "Farmacéutico/a", "text": "¿Desde cuándo tiene estos síntomas?"},
                {"person": "Tú", "text": "Desde ayer por la tarde"},
                {"person": "Farmacéutico/a", "text": "Le recomiendo ibuprofeno. ¿Es alérgico a algún medicamento?"},
                {"person": "Tú", "text": "No, no soy alérgico a nada"},
                {"person": "Farmacéutico/a", "text": "Perfecto. Tome una pastilla cada 8 horas con comida"},
                {"person": "Tú", "text": "¿Cuánto cuesta?"},
                {"person": "Farmacéutico/a", "text": "Son 4 euros el envase"},
                {"person": "Tú", "text": "Gracias por su ayuda"}
            ]
        }
    ]

    pdf = ConversationPDF()
    pdf.set_title('Practicas de Conversacion - Curso Intensivo de Espanol')
    pdf.set_author('Centro de Lenguas Modernas - Universidad de Granada')
    pdf.add_page()

    for i, conv in enumerate(conversations, 1):
        if i > 1:
            pdf.add_page()

        # Título y contexto
        pdf.set_font('Arial', 'B', 14)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 10, f'Conversacion {i}: {conv["title"]}', 0, 1, 'C')
        pdf.ln(5)

        pdf.set_font('Arial', '', 11)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 6, f'Contexto: {conv["context"]}')
        pdf.ln(8)

        # Diálogo
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(0, 8, 'Dialogo:', 0, 1)
        pdf.ln(3)

        for line in conv["dialogue"]:
            pdf.set_font('Arial', 'B', 10)
            pdf.set_text_color(0, 102, 204)
            pdf.cell(30, 6, line["person"] + ':', 0, 0)
            pdf.set_font('Arial', '', 10)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(0, 6, line["text"])
            pdf.ln(2)

        pdf.ln(5)

        # Sección de práctica
        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(139, 69, 19)
        pdf.cell(0, 8, 'Ejercicios de Practica:', 0, 1)
        pdf.ln(3)

        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(0, 0, 0)

        exercises = [
            "1. Practica este diálogo con un compañero/a",
            "2. Cambia algunas palabras o frases para hacerlo más personal",
            "3. Inventa una situación diferente usando el mismo vocabulario",
            "4. Graba tu voz y escucha tu pronunciación",
            "5. Escribe 3 preguntas adicionales para esta conversación"
        ]

        for exercise in exercises:
            pdf.multi_cell(0, 6, exercise)
            pdf.ln(2)

        pdf.ln(5)

        # Vocabulario útil
        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(139, 69, 19)
        pdf.cell(0, 8, 'Vocabulario Util:', 0, 1)
        pdf.ln(3)

        pdf.set_font('Arial', '', 10)

        vocab_sections = {
            "Saludos y cortesia": ["Hola", "Buenos dias/tardes/noches", "Por favor", "Gracias", "De nada"],
            "Preguntas basicas": ["¿Como...?", "¿Donde...?", "¿Cuando...?", "¿Cuanto...?", "¿Por favor?"]
        }

        for category, words in vocab_sections.items():
            pdf.set_font('Arial', 'B', 10)
            pdf.set_text_color(0, 102, 204)
            pdf.cell(0, 6, category + ':', 0, 1)
            pdf.set_font('Arial', '', 10)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(0, 6, ', '.join(words))
            pdf.ln(3)

    # Guardar PDF
    pdf.output('materials/conversaciones-practicas.pdf')
    print("✅ Created professional conversaciones-practicas.pdf")

def create_cultural_guide():
    pdf = FPDF()
    pdf.add_page()

    # Título
    pdf.set_font('Arial', 'B', 16)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 10, 'Guia Cultural de Granada', 0, 1, 'C')
    pdf.set_font('Arial', 'I', 10)
    pdf.set_text_color(102, 102, 102)
    pdf.cell(0, 6, 'Para estudiantes del Curso Intensivo de Espanol', 0, 1, 'C')
    pdf.ln(10)

    # Contenido cultural
    cultural_content = [
        {
            "title": "La Alhambra",
            "content": "El monumento más famoso de Granada. Construido durante el siglo XIII por los reyes nazaríes. Es imprescindible visitarlo. ¡Reserva tus entradas con antelación!"
        },
        {
            "title": "Las Tapas",
            "content": "En Granada, cuando pides una bebida, recibes una tapa gratuita. Es una tradición social. Algunas tapas típicas: tortilla, jamón serrano, albóndigas, pimientos."
        },
        {
            "title": "El Albaicín",
            "content": "Barrio antiguo con calles estrechas y casas blancas. Desde el Mirador de San Nicolás tienes las mejores vistas de la Alhambra. Es patrimonio de la humanidad."
        },
        {
            "title": "Los Sacromontes",
            "content": "Abadía construida en el siglo XVII. Famous for its caves and panoramic views of the city. Semana Santa celebrations are very important here."
        },
        {
            "title": "Fiestas Locales",
            "content": "Feria de Abril: Celebration with music, dancing, traditional food. Corpus Christi: Religious processions. Día de la Cruz: May 3rd, crosses decorated with flowers."
        }
    ]

    for section in cultural_content:
        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(139, 69, 19)
        pdf.cell(0, 8, section["title"], 0, 1)
        pdf.ln(3)

        pdf.set_font('Arial', '', 11)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 6, section["content"])
        pdf.ln(8)

    # Frases útiles para turistas
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 10, 'Frases Utiles para Turistas', 0, 1, 'C')
    pdf.ln(5)

    useful_phrases = [
        ("Disculpe, ¿sabe cómo llegar a...?", "Excuse me, do you know how to get to...?"),
        ("¿Cuánto cuesta la entrada?", "How much is the admission?"),
        ("¿Habla inglés?", "Do you speak English?"),
        ("¿Dónde puedo encontrar...?", "Where can I find...?"),
        ("¿A qué hora abre/cierra?", "What time does it open/close?"),
        ("La cuenta, por favor", "The bill, please"),
        ("¿Está incluido en el precio?", "Is it included in the price?"),
        ("¿Hay descuento para estudiantes?", "Is there a student discount?")
    ]

    for spanish, english in useful_phrases:
        pdf.set_font('Arial', 'B', 10)
        pdf.set_text_color(0, 102, 204)
        pdf.multi_cell(0, 6, f"ES: {spanish}")
        pdf.set_font('Arial', 'I', 10)
        pdf.set_text_color(102, 102, 102)
        pdf.multi_cell(0, 6, f"EN: {english}")
        pdf.ln(4)

    pdf.output('materials/guia-cultural-granada.pdf')
    print("✅ Created professional guia-cultural-granada.pdf")

if __name__ == "__main__":
    print("🎭 Creating conversation and cultural practice materials...")
    create_conversation_practice()
    create_cultural_guide()
    print("\n🌟 All interactive learning materials created successfully!")
    print("📚 Students now have comprehensive conversation practice and cultural guides")