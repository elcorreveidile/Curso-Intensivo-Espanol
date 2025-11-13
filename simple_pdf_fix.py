#!/usr/bin/env python3
"""
Crear PDFs profesionales mejorados y seguros para todos los materiales del curso
"""

from fpdf import FPDF
import os

def clean_text(text):
    """Limpiar caracteres especiales para PDF compatible con latin1"""
    # Reemplazos seguros
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N', 'ü': 'u', 'Ü': 'U',
        '¿': '?', '¡': '!',
        '•': '-', '·': '.',
        '📘': 'Guia', '🎯': 'Objetivos', '📚': 'Metodologia',
        '📝': 'Evaluacion', '💡': 'Recomendaciones', '🌟': 'Expresiones',
        '🗣️': 'Frases', '🎭': 'Reacciones', '🔢': 'Verbos', '✅': 'Soluciones'
    }

    # Asegurar signos correctos
    text = text.replace(' ?', ' ¿')
    text = text.replace(' !', ' ¡')

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text.encode('latin1', 'ignore').decode('latin1')

class SafePDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=25)
        self.set_margins(20, 30, 20)

    def header(self):
        # Encabezado profesional
        self.set_font('Arial', 'B', 18)
        self.set_text_color(0, 51, 102)
        self.cell(0, 12, clean_text(self.title), 0, 1, 'C')

        self.set_font('Arial', 'I', 11)
        self.set_text_color(102, 102, 102)
        self.cell(0, 6, 'Curso Intensivo de Espanol - Nivel 3 CLM (A1.2-A2.1)', 0, 1, 'C')

        self.set_text_color(0, 153, 51)
        self.set_font('Arial', 'B', 12)
        self.cell(0, 8, 'Periodo: 6 - 27 de noviembre de 2025 | Lunes a Jueves 8:30-10:30', 0, 1, 'C')

        self.ln(8)

    def footer(self):
        # Pie de página elegante
        self.set_y(-25)
        self.set_font('Arial', 'I', 9)
        self.set_text_color(128, 128, 128)
        self.cell(0, 6, f'Pagina {self.page_no()} de {{nb}}', 0, 1, 'C')
        self.cell(0, 6, 'Profesor: Javier Benitez Lainez | Aula: A2', 0, 1, 'C')
        self.cell(0, 6, 'Universidad de Granada - Centro de Lenguas Modernas', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, clean_text(title), 0, 1, 'L')
        self.ln(4)

    def chapter_body(self, text, font_size=11):
        self.set_font('Arial', '', font_size)
        self.set_text_color(0, 0, 0)
        self.multi_cell(170, 6, clean_text(text))
        self.ln(4)

def create_improved_guia_curso():
    pdf = SafePDF()
    pdf.set_title('Guia del Curso - Curso Intensivo de Espanol')
    pdf.add_page()
    pdf.title = 'Guia del Curso'

    # Información del curso
    pdf.chapter_title("Informacion General del Curso")
    pdf.chapter_body("¡Bienvenidos al Curso Intensivo de Espanol Nivel 3 CLM!")
    pdf.chapter_body("• Nivel: A1.2-A2.1 (Inicial-Elemental)")
    pdf.chapter_body("• Duracion: 4 semanas (40 horas totales)")
    pdf.chapter_body("• Horario: Lunes a Jueves de 8:30 a 10:30")
    pdf.chapter_body("• Profesor: Javier Benitez Lainez")
    pdf.chapter_body("• Aula: A2, Centro de Lenguas Modernas")
    pdf.chapter_body("• Estudiantes: Grupo reducido (9-10 personas)")

    # Objetivos
    pdf.chapter_title("Objetivos del Curso")
    pdf.chapter_body("Al finalizar este curso, los estudiantes podran:")
    pdf.chapter_body("• Presentarse y presentar a otras personas")
    pdf.chapter_body("• Pedir y dar informacion personal basica")
    pdf.chapter_body("• Describir lugares, personas y objetos")
    pdf.chapter_body("• Expresar gustos, preferencias y opiniones")
    pdf.chapter_body("• Realizar compras y transacciones simples")
    pdf.chapter_body("• Pedir direcciones y orientacion")
    pdf.chapter_body("• Entender y usar expresiones de tiempo")

    # Metodología
    pdf.chapter_title("Metodologia")
    pdf.chapter_body("Nuestro metodo se basa en:")
    pdf.chapter_body("• Comunicacion desde el primer dia")
    pdf.chapter_body("• Actividades practicas y reales")
    pdf.chapter_body("• Trabajo en parejas y grupos pequenos")
    pdf.chapter_body("• Uso de materiales autenticos")
    pdf.chapter_body("• Integracion de cultura espanola")
    pdf.chapter_body("• Retroalimentacion constante")

    pdf.add_page()

    # Evaluación
    pdf.chapter_title("Sistema de Evaluacion")
    pdf.chapter_body("La evaluacion sera continua y se basara en:")
    pdf.chapter_body("• Participacion en clase (30%)")
    pdf.chapter_body("• Actividades y ejercicios (30%)")
    pdf.chapter_body("• Proyectos y presentaciones (20%)")
    pdf.chapter_body("• Examen final (20%)")

    # Recomendaciones
    pdf.chapter_title("Recomendaciones para el Exito")
    pdf.chapter_body("Para aprovechar al maximo el curso:")
    pdf.chapter_body("• Asiste puntualmente a todas las clases")
    pdf.chapter_body("• Participa activamente en las actividades")
    pdf.chapter_body("• Estudia 15-20 minutos diariamente")
    pdf.chapter_body("• Practica companeros fuera de clase")
    pdf.chapter_body("• No temas cometer errores")
    pdf.chapter_body("• Sumergete en la cultura local")

    pdf.output('materials/guia-curso.pdf')
    print("✅ Created improved guia-curso.pdf with proper margins and safe encoding")

def create_improved_vocabulario():
    pdf = SafePDF()
    pdf.set_title('Vocabulario Esencial - Curso Intensivo de Espanol')
    pdf.add_page()
    pdf.title = 'Vocabulario Esencial'

    vocabulary_categories = [
        ("Saludos y Presentaciones", [
            "Hola / ¿Que tal?", "Buenos dias/tardes/noches", "Me llamo...",
            "¿Como te llamas?", "Mucho gusto / Encantado/a"
        ]),
        ("Informacion Personal", [
            "¿De donde eres?", "Soy de...", "¿Cuantos años tienes?",
            "Tengo ... años", "¿Que estudias?"
        ]),
        ("Familia y Amigos", [
            "Mi familia / mis padres", "Hermanos/as", "Mi mejor amigo/a",
            "¿Tienes hermanos?", "Vivo con..."
        ]),
        ("Tiempo Libre y Hobbies", [
            "Me gusta...", "¿Que te gusta hacer?", "Practicar deportes",
            "Escuchar musica", "Leer libros"
        ]),
        ("Comida y Bebidas", [
            "¿Que quieres comer/beber?", "Estoy hambriento/sediento",
            "La comida esta deliciosa", "Buen provecho!", "Una mesa para dos"
        ]),
        ("Direcciones y Transporte", [
            "¿Donde esta...?", "¿Como llego a...?", "A la derecha/izquierda",
            "Recto todo seguido", "Esta cerca/lejos"
        ]),
        ("Compras", [
            "¿Cuanto cuesta?", "Estoy buscando...", "¿Tienen...?",
            "Voy a pagar con tarjeta", "¿Hay descuento?"
        ]),
        ("Emergencias y Ayuda", [
            "¡Ayuda! / ¡Socorro!", "¿Podrias ayudarme?", "¿Hablas ingles?",
            "No entiendo", "¿Puedes repetir, por favor?"
        ])
    ]

    for category, words in vocabulary_categories:
        pdf.chapter_title(category)
        for word in words:
            pdf.chapter_body(f"- {word}")
        pdf.ln(2)

    # Expresiones útiles
    pdf.add_page()
    pdf.chapter_title("Expresiones Utiles")

    expressions = [
        ("Para pedir ayuda", "¿Podrias ayudarme, por favor? / ¿Me puedes ayudar?"),
        ("Para agradecer", "Muchas gracias / Gracias de verdad / Te lo agradezco"),
        ("Para disculparse", "Lo siento / Perdona / Disculpa"),
        ("Para mostrar interes", "¡Ah, de verdad! / ¡Que interesante! / No me digas"),
        ("Para pedir repetir", "¿Puedes repetir, por favor? / ¿Como se dice...?"),
        ("Para saludar informal", "¿Que pasa? / ¿Que hay? / ¿Como vamos?"),
        ("Para despedirse", "Hasta luego / Nos vemos / Que tengas un buen dia")
    ]

    for category, expression in expressions:
        pdf.set_font('Arial', 'B', 11)
        pdf.set_text_color(0, 102, 204)
        pdf.cell(50, 6, f"{category}:", 0, 0)
        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(120, 6, clean_text(expression))
        pdf.ln(2)

    pdf.output('materials/vocabulario.pdf')
    print("✅ Created improved vocabulario.pdf with proper margins and safe encoding")

def create_improved_frases_utiles():
    pdf = SafePDF()
    pdf.set_title('Frases Utiles - Curso Intensivo de Espanol')
    pdf.add_page()
    pdf.title = 'Frases Utiles'

    daily_phrases = {
        "En el Restaurante": [
            "¡Buenas tardes! ¿Tienen mesa?",
            "¿Que me recomiendan?",
            "¿Traen menu del dia?",
            "La cuenta, por favor",
            "¡Estaba delicioso!"
        ],
        "En la Tienda": [
            "Busco un regalo",
            "¿Cual es mi talla?",
            "¿Podria probarmelo?",
            "Me queda bien/grande/pequeno",
            "Lo voy a pensar"
        ],
        "En el Transporte": [
            "¿Cuanto cuesta el billete?",
            "¿A que hora sale/llega?",
            "¿Esta parada va a...?",
            "Un billete para..., por favor",
            "¿Tiene que hacer transbordo?"
        ],
        "En el Hotel": [
            "Tengo una reserva",
            "¿Tienen habitaciones disponibles?",
            "¿A que hora es el desayuno?",
            "¿Hay wifi gratis?",
            "La llave de la habitacion 101"
        ]
    }

    for category, phrases in daily_phrases.items():
        pdf.chapter_title(category)
        for phrase in phrases:
            pdf.chapter_body(f"- {phrase}")
        pdf.ln(3)

    pdf.add_page()
    pdf.chapter_title("Expresiones y Reacciones")

    reactions = [
        "¡Que fuerte! (¡Que sorpresa!)",
        "¡Que lastima! (Que pena)",
        "¡Menos mal! (Que alivio)",
        "¡No me digas! (¡No puedo creerlo!)",
        "¡Claro que si! (Por supuesto)",
        "¡Para nada! (En absoluto)",
        "¡Estoy de acuerdo! (Totalmente de acuerdo)",
        "¡No estoy seguro/a (No se)"
    ]

    for reaction in reactions:
        pdf.chapter_body(f"- {reaction}")

    pdf.output('materials/frases-utiles.pdf')
    print("✅ Created improved frases-utiles.pdf with proper margins and safe encoding")

def create_improved_verbos():
    pdf = SafePDF()
    pdf.set_title('Verbos Irregulares - Curso Intensivo de Espanol')
    pdf.add_page()
    pdf.title = 'Verbos Irregulares'

    pdf.chapter_title("Verbos Irregulares Esenciales")

    irregular_verbs = [
        {
            "infinitivo": "SER (to be)",
            "presente": ["soy", "eres", "es", "somos", "sois", "son"],
            "usos": "Identidad, caracteristicas, profesion, origen, hora"
        },
        {
            "infinitivo": "ESTAR (to be)",
            "presente": ["estoy", "estas", "esta", "estamos", "estais", "estan"],
            "usos": "Ubicacion, estado temporal, salud, emociones"
        },
        {
            "infinitivo": "TENER (to have)",
            "presente": ["tengo", "tienes", "tiene", "tenemos", "teneis", "tienen"],
            "usos": "Posesion, edad, necesidades"
        },
        {
            "infinitivo": "IR (to go)",
            "presente": ["voy", "vas", "va", "vamos", "vais", "van"],
            "usos": "Movimiento, futuro ir + a + infinitivo"
        },
        {
            "infinitivo": "HACER (to do/make)",
            "presente": ["hago", "haces", "hace", "hacemos", "haceis", "hacen"],
            "usos": "Actividades, tiempo atmosferico"
        }
    ]

    for verb in irregular_verbs:
        pdf.chapter_title(verb["infinitivo"])
        pdf.chapter_body(f"USO: {verb['usos']}")
        pdf.chapter_body("Presente de indicativo:")

        # Tabla de conjugación
        pronouns = ["yo", "tu", "el/ella/usted", "nosotros/as", "vosotros/as", "ellos/ellas/ustedes"]
        conjugations = verb["presente"]

        for i, (pronoun, conj) in enumerate(zip(pronouns, conjugations)):
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
    print("✅ Created improved verbos.pdf with proper margins and safe encoding")

def create_improved_ejercicios():
    pdf = SafePDF()
    pdf.set_title('Ejercicios Practicos - Curso Intensivo de Espanol')
    pdf.add_page()
    pdf.title = 'Ejercicios Practicos'

    pdf.chapter_title("Ejercicios de Practica")

    exercises = [
        {
            "title": "Ejercicio 1: Completa con SER o ESTAR",
            "content": """
1. Yo _____ estudiante de espanol.
2. ¿Como _____ usted? ¿Como _____?
3. El libro _____ en la mesa.
4. Nosotros _____ muy contentos hoy.
5. La casa _____ muy grande.
6. ¿Donde _____ las llaves?
7. Mi hermano _____ medico.
8. Yo _____ muy cansado esta manana.
            """
        },
        {
            "title": "Ejercicio 2: Forma frases con TENER",
            "content": """
Usa las palabras para formar frases correctas:
1. yo / 25 anos / tengo
2. ¿cuantos hermanos / tienes / tu?
3. tenemos / mucho trabajo / esta semana
4. ella / hambre / tiene
5. los ninos / sueno / tienen
            """
        },
        {
            "title": "Ejercicio 3: Preguntas basicas",
            "content": """
Escribe preguntas para estas respuestas:
1. ___________________________________?
   Me llamo Maria.
2. ___________________________________?
   Soy de Mexico.
3. ___________________________________?
   Tengo 22 anos.
4. ___________________________________?
   Vivo en Granada.
5. ___________________________________?
   Estudio ingles.
            """
        }
    ]

    for i, exercise in enumerate(exercises, 1):
        pdf.chapter_title(exercise["title"])
        pdf.chapter_body(exercise["content"])
        pdf.ln(5)

    pdf.add_page()
    pdf.chapter_title("Soluciones")

    solutions = [
        "Ejercicio 1: soy, esta, esta, estamos, es, estan, es, estoy",
        "Ejercicio 2: 1) Tengo 25 anos. 2) ¿Cuantos hermanos tienes? 3) Tenemos mucho trabajo esta semana. 4) Ella tiene hambre. 5) Los ninos tienen sueno.",
        "Ejercicio 3: 1) ¿Como te llamas? 2) ¿De donde eres? 3) ¿Cuantos anos tienes? 4) ¿Donde vives? 5) ¿Que estudias?"
    ]

    for i, solution in enumerate(solutions, 1):
        pdf.set_font('Arial', 'B', 11)
        pdf.set_text_color(0, 102, 204)
        pdf.cell(0, 6, f"Solucion {i}:", 0, 1)
        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(170, 6, clean_text(solution))
        pdf.ln(5)

    pdf.output('materials/ejercicios-practicos.pdf')
    print("✅ Created improved ejercicios-practicos.pdf with proper margins and safe encoding")

if __name__ == "__main__":
    print("🔧 Creating improved PDF materials with correct punctuation and margins...")

    # Create improved PDFs
    create_improved_guia_curso()
    create_improved_vocabulario()
    create_improved_frases_utiles()
    create_improved_verbos()
    create_improved_ejercicios()

    print("\n✅ All improved PDFs created successfully!")
    print("📚 Fixed margins, proper Spanish punctuation, and safe encoding")