#!/usr/bin/env python3
"""
Crear PDFs con signos de puntuación españoles correctos
Manteniendo ¿ y ¡ en lugar de reemplazarlos
"""

from fpdf import FPDF
import os

def preserve_spanish_text(text):
    """Conservar signos españoles y hacer compatible con PDF"""
    # Solo reemplazar caracteres problematicos, mantener los españoles
    replacements = {
        '•': '-',
        '·': '.',
        # Emojis a texto
        '📘': 'Guia', '🎯': 'Objetivos', '📚': 'Metodologia',
        '📝': 'Evaluacion', '💡': 'Recomendaciones', '🌟': 'Expresiones',
        '🗣️': 'Frases', '🎭': 'Reacciones', '🔢': 'Verbos', '✅': 'Soluciones'
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Asegurar que los signos españoles estén presentes
    # Convertir ? incorrecto a ¿ correcto cuando inicia pregunta
    import re
    # Patrón para encontrar preguntas que empiezan con ? en lugar de ¿
    text = re.sub(r'^(\s*)\?+', r'\1¿', text, flags=re.MULTILINE)
    text = re.sub(r'([.!?]\s+)\?+', r'\1¿', text)

    # Similar para exclamaciones
    text = re.sub(r'^(\s*)\!+', r'\1¡', text, flags=re.MULTILINE)
    text = re.sub(r'([.!?]\s+)\!+', r'\1¡', text)

    return text

class SpanishPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=25)
        self.set_margins(20, 30, 20)

    def header(self):
        self.set_font('Arial', 'B', 18)
        self.set_text_color(0, 51, 102)
        self.cell(0, 12, preserve_spanish_text(self.title), 0, 1, 'C')

        self.set_font('Arial', 'I', 11)
        self.set_text_color(102, 102, 102)
        self.cell(0, 6, 'Curso Intensivo de Español - Nivel 3 CLM (A1.2-A2.1)', 0, 1, 'C')

        self.set_text_color(0, 153, 51)
        self.set_font('Arial', 'B', 12)
        self.cell(0, 8, 'Periodo: 6 - 27 de noviembre de 2025 | Lunes a Jueves 8:30-10:30', 0, 1, 'C')

        self.ln(8)

    def footer(self):
        self.set_y(-25)
        self.set_font('Arial', 'I', 9)
        self.set_text_color(128, 128, 128)
        self.cell(0, 6, f'Página {self.page_no()} de {{nb}}', 0, 1, 'C')
        self.cell(0, 6, 'Profesor: Javier Benítez Láinez | Aula: A2', 0, 1, 'C')
        self.cell(0, 6, 'Universidad de Granada - Centro de Lenguas Modernas', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, preserve_spanish_text(title), 0, 1, 'L')
        self.ln(4)

    def chapter_body(self, text, font_size=11):
        self.set_font('Arial', '', font_size)
        self.set_text_color(0, 0, 0)
        # Dividir texto en líneas para manejar mejor los márgenes
        lines = preserve_spanish_text(text).split('\n')
        for line in lines:
            self.multi_cell(170, 6, line)
        self.ln(4)

def create_corrected_guia_curso():
    pdf = SpanishPDF()
    pdf.set_title('Guía del Curso - Curso Intensivo de Español')
    pdf.add_page()
    pdf.title = 'Guía del Curso'

    pdf.chapter_title("Información General del Curso")
    pdf.chapter_body("¡Bienvenidos al Curso Intensivo de Español Nivel 3 CLM!")
    pdf.chapter_body("• Nivel: A1.2-A2.1 (Inicial-Elemental)")
    pdf.chapter_body("• Duración: 4 semanas (40 horas totales)")
    pdf.chapter_body("• Horario: Lunes a Jueves de 8:30 a 10:30")
    pdf.chapter_body("• Profesor: Javier Benítez Láinez")
    pdf.chapter_body("• Aula: A2, Centro de Lenguas Modernas")
    pdf.chapter_body("• Estudiantes: Grupo reducido (9-10 personas)")

    pdf.chapter_title("Objetivos del Curso")
    pdf.chapter_body("Al finalizar este curso, los estudiantes podrán:")
    pdf.chapter_body("• Presentarse y presentar a otras personas")
    pdf.chapter_body("• ¿Cómo pedir y dar información personal básica?")
    pdf.chapter_body("• Describir lugares, personas y objetos")
    pdf.chapter_body("• ¿Cómo expresar gustos, preferencias y opiniones?")
    pdf.chapter_body("• Realizar compras y transacciones simples")
    pdf.chapter_body("• ¿Cómo pedir direcciones y orientación?")
    pdf.chapter_body("• Entender y usar expresiones de tiempo")

    pdf.chapter_title("Metodología")
    pdf.chapter_body("Nuestro método se basa en:")
    pdf.chapter_body("• Comunicación desde el primer día")
    pdf.chapter_body("• ¿Qué actividades prácticas y reales usamos?")
    pdf.chapter_body("• Trabajo en parejas y grupos pequeños")
    pdf.chapter_body("• Uso de materiales auténticos")
    pdf.chapter_body("• Integración de cultura española")
    pdf.chapter_body("• ¿Cómo ofrecemos retroalimentación constante?")

    pdf.add_page()
    pdf.chapter_title("Sistema de Evaluación")
    pdf.chapter_body("La evaluación será continua y se basará en:")
    pdf.chapter_body("• Participación en clase (30%)")
    pdf.chapter_body("• Actividades y ejercicios (30%)")
    pdf.chapter_body("• Proyectos y presentaciones (20%)")
    pdf.chapter_body("• Examen final (20%)")

    pdf.chapter_title("Recomendaciones para el Éxito")
    pdf.chapter_body("Para aprovechar al máximo el curso:")
    pdf.chapter_body("• Asiste puntualmente a todas las clases")
    pdf.chapter_body("• ¿Cómo participar activamente en las actividades?")
    pdf.chapter_body("• Estudia 15-20 minutos diariamente")
    pdf.chapter_body("• Practica con compañeros fuera de clase")
    pdf.chapter_body("• ¿Por qué no debes temer cometer errores?")
    pdf.chapter_body("• ¡Sumergete en la cultura local!")

    # Preguntas frecuentes con signos correctos
    pdf.add_page()
    pdf.chapter_title("Preguntas Frecuentes")

    faqs = [
        "¿Qué nivel de español necesito para empezar?",
        "El curso es para niveles A1.2-A2.1 (básico con conocimientos previos)",
        "",
        "¿Cuántos estudiantes habrá por clase?",
        "Grupos reducidos de 9-10 estudiantes para atención personalizada",
        "",
        "¿Necesito comprar algún material?",
        "No, todos los materiales están incluidos y disponibles online",
        "",
        "¿Habrá tareas para casa?",
        "Sí, pero serán breves y prácticas para reforzar lo aprendido en clase",
        "",
        "¿Recibiré un certificado al finalizar?",
        "Sí, recibirás un certificado del Centro de Lenguas Modernas"
    ]

    for faq in faqs:
        if faq:
            pdf.chapter_body(faq)

    pdf.output('materials/guia-curso.pdf')
    print("✅ Created guia-curso.pdf with CORRECT Spanish punctuation")

def create_corrected_vocabulario():
    pdf = SpanishPDF()
    pdf.set_title('Vocabulario Esencial - Curso Intensivo de Español')
    pdf.add_page()
    pdf.title = 'Vocabulario Esencial'

    vocabulary_with_questions = [
        ("Saludos y Presentaciones", [
            "¿Cómo estás? / ¿Qué tal?",
            "Buenos días/tardes/noches",
            "Me llamo...",
            "¿Cómo te llamas?",
            "Mucho gusto / Encantado/a"
        ]),
        ("Preguntas Personales", [
            "¿De dónde eres?",
            "Soy de...",
            "¿Cuántos años tienes?",
            "Tengo ... años",
            "¿Qué estudias?",
            "¿Dónde vives?"
        ]),
        ("En el Restaurante", [
            "¿Qué me recomienda?",
            "¿Traen menú del día?",
            "La cuenta, por favor",
            "¿Está delicioso!"
        ]),
        ("Direcciones y Transporte", [
            "¿Dónde está...?",
            "¿Cómo llego a...?",
            "¿A qué hora sale el autobús?",
            "¿Cuánto cuesta el billete?"
        ]),
        ("Compras", [
            "¿Cuánto cuesta?",
            "¿Tienen... en talla mediana?",
            "¿Podría probármelo?",
            "¿Hay descuento para estudiantes?"
        ]),
        ("Emergencias y Ayuda", [
            "¿Podría ayudarme, por favor?",
            "¿Habla inglés?",
            "No entiendo, ¿puede repetir?",
            "¿Dónde está la farmacia más cercana?"
        ])
    ]

    for category, phrases in vocabulary_with_questions:
        pdf.chapter_title(category)
        for phrase in phrases:
            pdf.chapter_body(f"• {phrase}")
        pdf.ln(2)

    # Expresiones útiles con preguntas
    pdf.add_page()
    pdf.chapter_title("Expresiones Útiles en Conversación")

    expressions = [
        ("Para pedir información", "¿Podría decirme...? / ¿Sabe usted...? / ¿Dónde encuentro...?"),
        ("Para mostrar interés", "¡Ah, de verdad! / ¿En serio? / ¡Qué interesante!"),
        ("Para pedir repetir", "¿Podría repetir, por favor? / ¿Cómo se dice...? / No he entendido"),
        ("Para expresar opinión", "Creo que... / Pienso que... / En mi opinión..."),
        ("Para hacer planes", "¿Qué te parece si...? / ¿Te gustaría...? / ¿Podemos...?")
    ]

    for category, expression in expressions:
        pdf.set_font('Arial', 'B', 11)
        pdf.set_text_color(0, 102, 204)
        pdf.cell(50, 6, f"{category}:", 0, 0)
        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(120, 6, preserve_spanish_text(expression))
        pdf.ln(2)

    pdf.output('materials/vocabulario.pdf')
    print("✅ Created vocabulario.pdf with CORRECT Spanish punctuation")

def create_corrected_frases_utiles():
    pdf = SpanishPDF()
    pdf.set_title('Frases Útiles - Curso Intensivo de Español')
    pdf.add_page()
    pdf.title = 'Frases Útiles'

    # Preguntas esenciales para extranjeros
    pdf.chapter_title("Preguntas Esenciales en España")

    essential_questions = [
        ("En el Restaurante", [
            "¿Tienen mesa para dos personas?",
            "¿Qué me recomienda del menú?",
            "¿Está incluida la bebida?",
            "¿Aceptan tarjetas de crédito?",
            "¿Dónde están los servicios?"
        ]),
        ("En Tiendas", [
            "¿Cuánto cuesta esto?",
            "¿Hay rebajas en esta sección?",
            "¿Puedo probármelo?",
            "¿Tienen esta prenda en otro color?",
            "¿Cuál es la política de devolución?"
        ]),
        ("Transporte", [
            "¿Este autobús va al centro?",
            "¿Dónde compro el billete?",
            "¿Cuántas paradas hasta...?",
            "¿A qué hora es el último servicio?",
            "¿Hay conexión con la línea...?"
        ]),
        ("Información Turística", [
            "¿A qué hora abren los museos?",
            "¿Dónde está la oficina de turismo?",
            "¿Cuál es el monumento más importante de la ciudad?",
            "¿Hay tours guiados en inglés?",
            "¿Dónde puedo comprar souvenirs?"
        ])
    ]

    for category, questions in essential_questions:
        pdf.chapter_title(category)
        for question in questions:
            pdf.chapter_body(f"• {question}")
        pdf.ln(3)

    pdf.output('materials/frases-utiles.pdf')
    print("✅ Created frases-utiles.pdf with CORRECT Spanish punctuation")

if __name__ == "__main__":
    print("🇪🇸 Creating PDFs with CORRECT Spanish punctuation...")

    create_corrected_guia_curso()
    create_corrected_vocabulario()
    create_corrected_frases_utiles()

    print("\n✅ PDFs created with proper ¿ and ¡ signs!")
    print("📚 All Spanish punctuation now correctly preserved")