#!/usr/bin/env python3
"""
Crear PDFs profesionales mejorados para todos los materiales del curso
Con signos de interrogación correctos y márgenes adecuados
"""

from fpdf import FPDF
import os

def clean_text(text):
    """Limpiar caracteres especiales para PDF manteniendo signos españoles"""
    # Reemplazar emojis con texto equivalente
    replacements = {
        '📘': 'Guia',
        '🎯': 'Objetivos',
        '📚': 'Metodologia',
        '📝': 'Evaluacion',
        '💡': 'Recomendaciones',
        '🌟': 'Expresiones',
        '🗣️': 'Frases',
        '🎭': 'Reacciones',
        '🔢': 'Verbos',
        '✅': 'Soluciones',
        '•': '-',
        '·': '.',
        # Corregir signos si están incorrectos
        '?¿': '¿',
        '!¡': '¡'
    }

    # Asegurar que los signos de apertura estén correctos
    text = text.replace(' ?', ' ¿')
    text = text.replace(' !', ' ¡')
    text = text.replace('(¿', '(¿')
    text = text.replace('(¡', '(¡')

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text

class ImprovedPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=25)
        self.set_margins(20, 30, 20)

    def header(self):
        # Encabezado profesional
        self.set_font('Arial', 'B', 18)
        self.set_text_color(0, 51, 102)
        self.cell(0, 12, self.title, 0, 1, 'C')

        self.set_font('Arial', 'I', 11)
        self.set_text_color(102, 102, 102)
        self.cell(0, 6, 'Curso Intensivo de Español - Nivel 3 CLM (A1.2-A2.1)', 0, 1, 'C')

        self.set_text_color(0, 153, 51)
        self.set_font('Arial', 'B', 12)
        self.cell(0, 8, 'Periodo: 6 - 27 de noviembre de 2025 | Lunes a Jueves 8:30-10:30', 0, 1, 'C')

        self.ln(8)

    def footer(self):
        # Pie de página elegante
        self.set_y(-25)
        self.set_font('Arial', 'I', 9)
        self.set_text_color(128, 128, 128)
        self.cell(0, 6, f'Página {self.page_no()} de {{nb}}', 0, 1, 'C')
        self.cell(0, 6, 'Profesor: Javier Benítez Láinez | Aula: A2', 0, 1, 'C')
        self.cell(0, 6, 'Universidad de Granada - Centro de Lenguas Modernas', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(4)

    def chapter_body(self, text, font_size=11):
        self.set_font('Arial', '', font_size)
        self.set_text_color(0, 0, 0)
        # Usar multi_cell con ancho adecuado para evitar que el texto se salga
        self.multi_cell(170, 6, clean_text(text))
        self.ln(4)

    def vocabulary_section(self, words_dict):
        """Sección especial para vocabulario con formato mejorado"""
        self.chapter_title("Vocabulario Esencial")

        col_width = 80
        for i, (category, words) in enumerate(words_dict.items()):
            if i % 2 == 0:
                self.set_x(20)
            else:
                self.set_x(110)

            self.set_font('Arial', 'B', 11)
            self.set_text_color(0, 102, 204)
            self.multi_cell(col_width, 6, clean_text(category), border=1)
            self.set_font('Arial', '', 10)
            self.set_text_color(0, 0, 0)

            for word in words[:5]:  # Limitar para mejor formato
                self.multi_cell(col_width, 5, f"• {clean_text(word)}", border=1)

            if i % 2 == 1:
                self.ln(5)

        self.ln(10)

def create_improved_guia_curso():
    pdf = ImprovedPDF()
    pdf.set_title('Guía del Curso - Curso Intensivo de Español')
    pdf.set_author('Centro de Lenguas Modernas - Universidad de Granada')
    pdf.add_page()

    # Información del curso
    pdf.chapter_title("📘 Información General del Curso")
    pdf.chapter_body("¡Bienvenidos al Curso Intensivo de Español Nivel 3 CLM!")
    pdf.chapter_body("• Nivel: A1.2-A2.1 (Inicial-Elemental)")
    pdf.chapter_body("• Duración: 4 semanas (40 horas totales)")
    pdf.chapter_body("• Horario: Lunes a Jueves de 8:30 a 10:30")
    pdf.chapter_body("• Profesor: Javier Benítez Láinez")
    pdf.chapter_body("• Aula: A2, Centro de Lenguas Modernas")
    pdf.chapter_body("• Estudiantes: Grupo reducido (9-10 personas)")

    # Objetivos
    pdf.chapter_title("🎯 Objetivos del Curso")
    pdf.chapter_body("Al finalizar este curso, los estudiantes podrán:")
    pdf.chapter_body("• Presentarse y presentar a otras personas")
    pdf.chapter_body("• Pedir y dar información personal básica")
    pdf.chapter_body("• Describir lugares, personas y objetos")
    pdf.chapter_body("• Expresar gustos, preferencias y opiniones")
    pdf.chapter_body("• Realizar compras y transacciones simples")
    pdf.chapter_body("• Pedir direcciones y orientación")
    pdf.chapter_body("• Entender y usar expresiones de tiempo")

    # Metodología
    pdf.chapter_title("📚 Metodología")
    pdf.chapter_body("Nuestro método se basa en:")
    pdf.chapter_body("• Comunicación desde el primer día")
    pdf.chapter_body("• Actividades prácticas y reales")
    pdf.chapter_body("• Trabajo en parejas y grupos pequeños")
    pdf.chapter_body("• Uso de materiales auténticos")
    pdf.chapter_body("• Integración de cultura española")
    pdf.chapter_body("• Retroalimentación constante")

    pdf.add_page()

    # Evaluación
    pdf.chapter_title("📝 Sistema de Evaluación")
    pdf.chapter_body("La evaluación será continua y se basará en:")
    pdf.chapter_body("• Participación en clase (30%)")
    pdf.chapter_body("• Actividades y ejercicios (30%)")
    pdf.chapter_body("• Proyectos y presentaciones (20%)")
    pdf.chapter_body("• Examen final (20%)")

    # Recomendaciones
    pdf.chapter_title("💡 Recomendaciones para el Éxito")
    pdf.chapter_body("Para aprovechar al máximo el curso:")
    pdf.chapter_body("• Asiste puntualmente a todas las clases")
    pdf.chapter_body("• Participa activamente en las actividades")
    pdf.chapter_body("• Estudia 15-20 minutos diariamente")
    pdf.chapter_body("• Practica con compañeros fuera de clase")
    pdf.chapter_body("• No temas cometer errores")
    pdf.chapter_body("• Sumérgete en la cultura local")

    pdf.output('materials/guia-curso.pdf')
    print("✅ Created improved guia-curso.pdf with proper margins and punctuation")

def create_improved_vocabulario():
    pdf = ImprovedPDF()
    pdf.set_title('Vocabulario Esencial - Curso Intensivo de Español')
    pdf.add_page()

    vocabulary_data = {
        "Saludos y Presentaciones": [
            "¡Hola! / ¿Qué tal?",
            "Buenos días/tardes/noches",
            "Me llamo...",
            "¿Cómo te llamas?",
            "Mucho gusto / Encantado/a"
        ],
        "Información Personal": [
            "¿De dónde eres?",
            "Soy de...",
            "¿Cuántos años tienes?",
            "Tengo ... años",
            "¿Qué estudias?"
        ],
        "Familia y Amigos": [
            "Mi familia / mis padres",
            "Hermanos/as",
            "Mi mejor amigo/a",
            "¿Tienes hermanos?",
            "Vivo con..."
        ],
        "Tiempo Libre y Hobbies": [
            "Me gusta...",
            "¿Qué te gusta hacer?",
            "Practicar deportes",
            "Escuchar música",
            "Leer libros"
        ],
        "Comida y Bebidas": [
            "¿Qué quieres comer/beber?",
            "Estoy hambriento/sediento",
            "La comida está deliciosa",
            "¡Buen provecho!",
            "Una mesa para dos, por favor"
        ],
        "Direcciones y Transporte": [
            "¿Dónde está...?",
            "¿Cómo llego a...?",
            "A la derecha/izquierda",
            "Recto todo seguido",
            "Está cerca/lejos"
        ],
        "Compras": [
            "¿Cuánto cuesta?",
            "Estoy buscando...",
            "¿Tienen...?",
            "Voy a pagar con tarjeta",
            "¿Hay descuento?"
        ],
        "Emergencias y Ayuda": [
            "¡Ayuda! / ¡Socorro!",
            "¿Podrías ayudarme?",
            "¿Hablas inglés?",
            "No entiendo",
            "¿Puedes repetir, por favor?"
        ]
    }

    pdf.vocabulary_section(vocabulary_data)

    # Expresiones útiles
    pdf.add_page()
    pdf.chapter_title("🌟 Expresiones Útiles")

    expressions = [
        ("Para pedir ayuda", "¿Podrías ayudarme, por favor? / ¿Me puedes ayudar?"),
        ("Para agradecer", "Muchas gracias / Gracias de verdad / Te lo agradezco"),
        ("Para disculparse", "Lo siento / Perdona / Disculpa"),
        ("Para mostrar interés", "¡Ah, de verdad! / ¡Qué interesante! / No me digas"),
        ("Para pedir repetir", "¿Puedes repetir, por favor? / ¿Cómo se dice...?"),
        ("Para saludar informal", "¿Qué pasa? / ¿Qué hay? / ¿Cómo vamos?"),
        ("Para despedirse", "Hasta luego / Nos vemos / Que tengas un buen día")
    ]

    for category, expression in expressions:
        pdf.set_font('Arial', 'B', 11)
        pdf.set_text_color(0, 102, 204)
        pdf.cell(50, 6, category + ":", 0, 0)
        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(120, 6, clean_text(expression))
        pdf.ln(2)

    pdf.output('materials/vocabulario.pdf')
    print("✅ Created improved vocabulario.pdf with proper margins and punctuation")

def create_improved_frases_utiles():
    pdf = ImprovedPDF()
    pdf.set_title('Frases Útiles - Curso Intensivo de Español')
    pdf.add_page()

    pdf.chapter_title("🗣️ Frases para la Vida Cotidiana")

    daily_phrases = {
        "En el Restaurante": [
            "¡Buenas tardes! ¿Tienen mesa?",
            "¿Qué me recomiendan?",
            "¿Traen menú del día?",
            "La cuenta, por favor",
            "¡Estaba delicioso!"
        ],
        "En la Tienda": [
            "Busco un regalo",
            "¿Cuál es mi talla?",
            "¿Podría probármelo?",
            "Me queda bien/grande/pequeño",
            "Lo voy a pensar"
        ],
        "En el Transporte": [
            "¿Cuánto cuesta el billete?",
            "¿A qué hora sale/llega?",
            "¿Esta parada va a...?",
            "Un billete para..., por favor",
            "¿Tiene que hacer transbordo?"
        ],
        "En el Hotel": [
            "Tengo una reserva",
            "¿Tienen habitaciones disponibles?",
            "¿A qué hora es el desayuno?",
            "¿Hay wifi gratis?",
            "La llave de la habitación 101"
        ]
    }

    for category, phrases in daily_phrases.items():
        pdf.chapter_title(category)
        for phrase in phrases:
            pdf.chapter_body(f"• {clean_text(phrase)}")
        pdf.ln(3)

    pdf.add_page()
    pdf.chapter_title("🎭 Expresiones y Reacciones")

    reactions = [
        "¡Qué fuerte! (¡Qué sorpresa!)",
        "¡Qué lástima! (Qué pena)",
        "¡Menos mal! (Qué alivio)",
        "¡No me digas! (¡No puedo creerlo!)",
        "¡Claro que sí! (Por supuesto)",
        "¡Para nada! (En absoluto)",
        "¡Estoy de acuerdo! (Totalmente de acuerdo)",
        "¡No estoy seguro/a (No sé)"
    ]

    for reaction in reactions:
        pdf.chapter_body(f"• {clean_text(reaction)}")

    pdf.output('materials/frases-utiles.pdf')
    print("✅ Created improved frases-utiles.pdf with proper margins and punctuation")

def create_improved_verbos():
    pdf = ImprovedPDF()
    pdf.set_title('Verbos Irregulares - Curso Intensivo de Español')
    pdf.add_page()

    pdf.chapter_title("🔢 Verbos Irregulares Esenciales")

    irregular_verbs = [
        {
            "infinitivo": "SER (to be)",
            "presente": ["soy", "eres", "es", "somos", "sois", "son"],
            "usos": "Identidad, características, profesión, origen, hora"
        },
        {
            "infinitivo": "ESTAR (to be)",
            "presente": ["estoy", "estás", "está", "estamos", "estáis", "están"],
            "usos": "Ubicación, estado temporal, salud, emociones"
        },
        {
            "infinitivo": "TENER (to have)",
            "presente": ["tengo", "tienes", "tiene", "tenemos", "tenéis", "tienen"],
            "usos": "Posesión, edad, necesidades"
        },
        {
            "infinitivo": "IR (to go)",
            "presente": ["voy", "vas", "va", "vamos", "vais", "van"],
            "usos": "Movimiento, futuro ir + a + infinitivo"
        },
        {
            "infinitivo": "HACER (to do/make)",
            "presente": ["hago", "haces", "hace", "hacemos", "hacéis", "hacen"],
            "usos": "Actividades, tiempo atmosférico"
        },
        {
            "infinitivo": "DECIR (to say/tell)",
            "presente": ["digo", "dices", "dice", "decimos", "decís", "dicen"],
            "usos": "Comunicación, expresión"
        },
        {
            "infinitivo": "VENIR (to come)",
            "presente": ["vengo", "vienes", "viene", "venimos", "venís", "vienen"],
            "usos": "Llegada, procedencia"
        }
    ]

    for verb in irregular_verbs:
        pdf.chapter_title(verb["infinitivo"])
        pdf.chapter_body(f"USO: {clean_text(verb['usos'])}")
        pdf.chapter_body(f"Presente de indicativo:")

        # Tabla de conjugación
        self_cells = ["yo", "tú", "él/ella/usted", "nosotros/as", "vosotros/as", "ellos/ellas/ustedes"]
        conjugations = verb["presente"]

        for i, (pronoun, conj) in enumerate(zip(self_cells, conjugations)):
            text = f"{pronoun}: {conj}"
            if i % 2 == 0:
                pdf.set_x(20)
            else:
                pdf.set_x(110)

            pdf.set_font('Arial', '', 10)
            pdf.cell(80, 6, text, 1)

            if i % 2 == 1:
                pdf.ln(6)

        pdf.ln(8)

    pdf.output('materials/verbos.pdf')
    print("✅ Created improved verbos.pdf with proper margins and punctuation")

def create_improved_ejercicios():
    pdf = ImprovedPDF()
    pdf.set_title('Ejercicios Prácticos - Curso Intensivo de Español')
    pdf.add_page()

    pdf.chapter_title("📝 Ejercicios de Práctica")

    exercises = [
        {
            "title": "Ejercicio 1: Completa con SER o ESTAR",
            "content": """
1. Yo _____ estudiante de español.
2. ¿Cómo _____ usted? ¿Cómo _____?
3. El libro _____ en la mesa.
4. Nosotros _____ muy contentos hoy.
5. La casa _____ muy grande.
6. ¿Dónde _____ las llaves?
7. Mi hermano _____ médico.
8. Yo _____ muy cansado esta mañana.
            """
        },
        {
            "title": "Ejercicio 2: Forma frases con TENER",
            "content": """
Usa las palabras para formar frases correctas:
1. yo / 25 años / tengo
2. ¿cuántos hermanos / tienes / tú?
3. tenemos / mucho trabajo / esta semana
4. ella / hambre / tiene
5. los niños / sueño / tienen
            """
        },
        {
            "title": "Ejercicio 3: Preguntas básicas",
            "content": """
Escribe preguntas para estas respuestas:
1. ___________________________________?
   Me llamo María.
2. ___________________________________?
   Soy de México.
3. ___________________________________?
   Tengo 22 años.
4. ___________________________________?
   Vivo en Granada.
5. ___________________________________?
   Estudio inglés.
            """
        },
        {
            "title": "Ejercicio 4: Descripciones",
            "content": """
Describe estas imágenes usando adjetivos:
1. Un coche nuevo: ___________________________
2. Una persona alta: _________________________
3. Una casa grande: __________________________
4. Un día bonito: ____________________________
5. Un libro interesante: _______________________
            """
        }
    ]

    for i, exercise in enumerate(exercises, 1):
        pdf.chapter_title(exercise["title"])
        pdf.chapter_body(clean_text(exercise["content"]))
        pdf.ln(5)

    pdf.add_page()
    pdf.chapter_title("✅ Soluciones")

    solutions = [
        "Ejercicio 1: soy, está, está, estamos, es, están, es, estoy",
        "Ejercicio 2: 1) Tengo 25 años. 2) ¿Cuántos hermanos tienes? 3) Tenemos mucho trabajo esta semana. 4) Ella tiene hambre. 5) Los niños tienen sueño.",
        "Ejercicio 3: 1) ¿Cómo te llamas? 2) ¿De dónde eres? 3) ¿Cuántos años tienes? 4) ¿Dónde vives? 5) ¿Qué estudias?",
        "Ejercicio 4: (respuestas variadas) El coche es nuevo y moderno. La persona es alta y delgada. La casa es grande y cómoda. Es un día muy bonito y soleado. Es un libro muy interesante."
    ]

    for i, solution in enumerate(solutions, 1):
        pdf.set_font('Arial', 'B', 11)
        pdf.set_text_color(0, 102, 204)
        pdf.cell(0, 6, f"Solución {i}:", 0, 1)
        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(170, 6, clean_text(solution))
        pdf.ln(5)

    pdf.output('materials/ejercicios-practicos.pdf')
    print("✅ Created improved ejercicios-practicos.pdf with proper margins and punctuation")

if __name__ == "__main__":
    print("🔧 Creating improved PDF materials with correct punctuation and margins...")

    # Create improved PDFs
    create_improved_guia_curso()
    create_improved_vocabulario()
    create_improved_frases_utiles()
    create_improved_verbos()
    create_improved_ejercicios()

    print("\n✅ All improved PDFs created successfully!")
    print("📚 Fixed margins, proper Spanish punctuation, and better formatting")