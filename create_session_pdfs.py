#!/usr/bin/env python3
"""
Crear cuadernos de sesiones profesionales
"""

from fpdf import FPDF
import os

def clean_text(text):
    """Limpiar caracteres especiales para PDF"""
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N', 'ü': 'u', 'Ü': 'U',
        '¿': '?', '¡': '!'
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

class SessionPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 18)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, self.title, border=0, align='C')
        self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Pagina {self.page_no()}', border=0, align='C')

sessions = [
    {
        'num': 1,
        'title': 'Sesion 1 - Presentaciones y alfabeto',
        'duracion': '2 horas',
        'objetivos': [
            'Saludos y presentaciones formales e informales',
            'Alfabeto espanol y pronunciacion',
            'Numeros, dias de la semana, meses',
            'Paises y nacionalidades hispanohablantes'
        ],
        'vocab': {
            'Saludos': 'Hola, Buenos dias, Buenas tardes, Buenas noches, Como estas?, Me llamo...',
            'Alfabeto': 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z',
            'Numeros': 'cero, uno, dos, tres, cuatro, cinco, seis, siete, ocho, nueve, diez...'
        },
        'actividades': [
            'Circulo de presentaciones',
            'Pronunciacion del alfabeto',
            'Juego de numeros de telefono',
            'Tarjetas de paises y nacionalidades'
        ],
        'tarea': [
            'Practicar el alfabeto',
            'Memorizar 10 paises y nacionalidades',
            'Preparar una presentacion personal'
        ]
    },
    {
        'num': 2,
        'title': 'Sesion 2 - Numeros y fechas',
        'duracion': '2 horas',
        'objetivos': [
            'Numeros del 0 al 1000',
            'Dias de la semana y meses del ano',
            'Decir y preguntar la fecha',
            'Expresar la hora'
        ],
        'vocab': {
            'Numeros': 'veinte, treinta, cuarenta, cincuenta, sesenta, setenta, ochenta, noventa, cien, mil',
            'Tiempo': 'Que hora es? Son las tres. Que dia es hoy? Hoy es lunes. Cual es la fecha?'
        },
        'actividades': [
            'Practicar numeros con precios',
            'Juego de bingo en espanol',
            'Escribir fechas importantes',
            'Horarios y citas'
        ],
        'tarea': [
            'Escribir 10 fechas importantes en espanol',
            'Practicar decir la hora',
            'Crear un horario semanal'
        ]
    },
    {
        'num': 3,
        'title': 'Sesion 3 - Familia y descripciones',
        'duracion': '2 horas',
        'objetivos': [
            'Vocabulario de familia',
            'Adjetivos para describir personas',
            'Verbos SER y ESTAR',
            'Posesivos: mi, tu, su'
        ],
        'vocab': {
            'Familia': 'padre, madre, hermano, hermana, abuelo, abuela, tio, tia, primo, prima',
            'Descripciones': 'alto, bajo, delgado, gordo, joven, mayor, simpatico, amable, inteligente'
        },
        'actividades': [
            'Presentar tu familia con fotos',
            'Juego: Adivina quien es',
            'Arbol genealogico',
            'Descripciones de companeros'
        ],
        'tarea': [
            'Escribir sobre tu familia (10 frases)',
            'Describir a 3 personas famosas',
            'Estudiar verbos SER y ESTAR'
        ]
    },
    {
        'num': 4,
        'title': 'Sesion 4 - Rutina diaria',
        'duracion': '4 horas',
        'objetivos': [
            'Verbos reflexivos',
            'Expresar rutinas y habitos',
            'Adverbios de frecuencia',
            'La hora en contexto'
        ],
        'vocab': {
            'Verbos reflexivos': 'levantarse, ducharse, vestirse, desayunar, almorzar, cenar, acostarse',
            'Frecuencia': 'siempre, a menudo, a veces, raramente, nunca, todos los dias'
        },
        'actividades': [
            'Describir tu dia tipico',
            'Comparar rutinas',
            'Crear un horario ideal',
            'Entrevista a un companero'
        ],
        'tarea': [
            'Escribir tu rutina diaria completa',
            'Comparar tu rutina con la de un amigo',
            'Practicar verbos reflexivos'
        ]
    },
    {
        'num': 5,
        'title': 'Sesion 5 - Comida y restaurantes',
        'duracion': '2 horas',
        'objetivos': [
            'Vocabulario de comida y bebida',
            'Pedir en un restaurante',
            'Verbo GUSTAR y similares',
            'Expresar gustos y preferencias'
        ],
        'vocab': {
            'Comida': 'desayuno, comida, cena, merienda, carne, pescado, verduras, frutas, postre',
            'Restaurante': 'Que desea tomar? La cuenta, por favor. Quisiera... Me gustaria...'
        },
        'actividades': [
            'Menu del dia',
            'Role-play en el restaurante',
            'Hablar de comidas favoritas',
            'Receta simple en espanol'
        ],
        'tarea': [
            'Escribir tu menu ideal',
            'Lista de 20 comidas en espanol',
            'Practicar: Me gusta / No me gusta'
        ]
    },
    {
        'num': 6,
        'title': 'Sesion 6 - Compras y tiendas',
        'duracion': '2 horas',
        'objetivos': [
            'Vocabulario de ropa y colores',
            'Ir de compras',
            'Adjetivos demostrativos',
            'Tallas y precios'
        ],
        'vocab': {
            'Ropa': 'camisa, pantalon, falda, vestido, zapatos, chaqueta, abrigo',
            'Compras': 'Cuanto cuesta? Donde esta? este, ese, aquel'
        },
        'actividades': [
            'Role-play en una tienda',
            'Describir ropa',
            'Comparar precios',
            'Catalogo de moda'
        ],
        'tarea': [
            'Describir tu ropa favorita',
            'Lista de compras en espanol',
            'Practicar demostrativos'
        ]
    },
    {
        'num': 7,
        'title': 'Sesion 7 - Transporte y direcciones',
        'duracion': '4 horas',
        'objetivos': [
            'Medios de transporte',
            'Dar y pedir direcciones',
            'Preposiciones de lugar',
            'Imperativo para instrucciones'
        ],
        'vocab': {
            'Transporte': 'coche, autobus, metro, tren, avion, taxi, bicicleta, a pie',
            'Direcciones': 'todo recto, a la derecha, a la izquierda, al lado de, enfrente de, detras de'
        },
        'actividades': [
            'Mapa de la ciudad',
            'Dar direcciones',
            'Role-play: turista perdido',
            'Describir rutas'
        ],
        'tarea': [
            'Escribir como llegar a tu casa',
            'Describir tu barrio',
            'Practicar imperativos'
        ]
    },
    {
        'num': 8,
        'title': 'Sesion 8 - Ocio y aficiones',
        'duracion': '2 horas',
        'objetivos': [
            'Actividades de tiempo libre',
            'Deportes y hobbies',
            'Expresar habilidades',
            'Verbos irregulares: poder, querer, preferir'
        ],
        'vocab': {
            'Ocio': 'leer, ver peliculas, escuchar musica, bailar, cantar, viajar, hacer deporte',
            'Deportes': 'futbol, baloncesto, tenis, natacion, correr, caminar, yoga'
        },
        'actividades': [
            'Hablar de hobbies',
            'Planear actividades de fin de semana',
            'Entrevista sobre deportes',
            'Comparar pasatiempos'
        ],
        'tarea': [
            'Escribir sobre tus aficiones',
            'Describir tu fin de semana ideal',
            'Practicar verbos irregulares'
        ]
    },
    {
        'num': 9,
        'title': 'Sesion 9 - Proyecto de fotos',
        'duracion': '2 horas',
        'objetivos': [
            'Describir fotos y lugares',
            'Narrar experiencias pasadas',
            'Preterito perfecto simple',
            'Conectores temporales'
        ],
        'vocab': {
            'Descripcion': 'bonito, feo, grande, pequeno, antiguo, moderno, tipico, interesante',
            'Pasado': 'ayer, la semana pasada, el ano pasado, primero, despues, luego, finalmente'
        },
        'actividades': [
            'Presentar fotos personales',
            'Describir lugares visitados',
            'Contar anecdotas',
            'Album de recuerdos'
        ],
        'tarea': [
            'Traer 5 fotos para presentar',
            'Escribir sobre un viaje memorable',
            'Practicar preterito'
        ]
    },
    {
        'num': 10,
        'title': 'Sesion 10 - Taller de cocina',
        'duracion': '4 horas',
        'objetivos': [
            'Vocabulario de cocina',
            'Imperativo en recetas',
            'Ingredientes y cantidades',
            'Cultura gastronomica espanola'
        ],
        'vocab': {
            'Cocina': 'cocinar, cortar, mezclar, anadir, hornear, freir, hervir, sal, azucar, aceite',
            'Cantidades': 'un poco, mucho, bastante, una taza, una cucharada, un kilo, un litro'
        },
        'actividades': [
            'Leer recetas espanolas',
            'Preparar tapas simples',
            'Explicar como hacer un plato',
            'Video de cocina'
        ],
        'tarea': [
            'Escribir tu receta favorita en espanol',
            'Lista de ingredientes comunes',
            'Investigar un plato espanol'
        ]
    },
    {
        'num': 11,
        'title': 'Sesion 11 - Repaso general',
        'duracion': '2 horas',
        'objetivos': [
            'Revisar todos los temas',
            'Practicar conversacion',
            'Resolver dudas',
            'Preparar examen final'
        ],
        'vocab': {
            'Repaso': 'Presentaciones, descripciones, rutinas, comida, compras, transporte, ocio'
        },
        'actividades': [
            'Juegos de repaso',
            'Conversaciones libres',
            'Simulacros de examen',
            'Preguntas y respuestas'
        ],
        'tarea': [
            'Repasar todo el material',
            'Preparar preguntas para el profesor',
            'Practicar examen oral'
        ]
    },
    {
        'num': 12,
        'title': 'Sesion 12 - Evaluacion final',
        'duracion': '4 horas',
        'objetivos': [
            'Examen escrito (comprension y expresion)',
            'Examen oral (conversacion y entrevista)',
            'Evaluacion del curso',
            'Certificados y despedida'
        ],
        'vocab': {
            'Evaluacion': 'Examen escrito: 90 minutos. Examen oral: 15 minutos por estudiante'
        },
        'actividades': [
            'Examen escrito de comprension lectora',
            'Examen escrito de expresion escrita',
            'Entrevistas orales individuales',
            'Conversacion en grupos',
            'Ceremonia de clausura'
        ],
        'tarea': [
            'Seguir practicando espanol',
            'Continuar con nivel B1',
            'Mantener contacto con companeros'
        ]
    }
]

def create_session_pdf(session):
    pdf = SessionPDF()
    pdf.title = session['title']
    pdf.add_page()

    # Info box
    pdf.set_fill_color(240, 248, 255)
    pdf.set_draw_color(100, 149, 237)
    pdf.rect(10, pdf.get_y(), 190, 30, 'FD')

    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 7, 'Curso Intensivo de Espanol - Nivel 3 CLM', border=0, align='L')
    pdf.ln()

    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(51, 51, 51)
    pdf.cell(0, 6, 'Periodo: 6 - 27 de noviembre de 2025', border=0)
    pdf.ln()
    pdf.cell(0, 6, 'Profesor: Javier Benitez Lainez | Aula: A2', border=0)
    pdf.ln()
    pdf.cell(0, 6, f'Duracion: {session["duracion"]}', border=0)
    pdf.ln(12)

    # Objetivos
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(51, 102, 153)
    pdf.cell(0, 8, 'OBJETIVOS DE LA SESION:', border=0)
    pdf.ln()

    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(0, 0, 0)
    for obj in session['objetivos']:
        pdf.cell(0, 6, '- ' + clean_text(obj), border=0)
        pdf.ln()
    pdf.ln(3)

    # Vocabulario
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(51, 102, 153)
    pdf.cell(0, 8, 'VOCABULARIO CLAVE:', border=0)
    pdf.ln()

    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(0, 0, 0)
    for key, value in session['vocab'].items():
        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(0, 6, clean_text(key + ':'), border=0)
        pdf.ln()
        pdf.set_font('Helvetica', '', 10)
        pdf.multi_cell(0, 5, clean_text(value))
        pdf.ln(2)

    # Actividades
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(51, 102, 153)
    pdf.cell(0, 8, 'ACTIVIDADES DE CLASE:', border=0)
    pdf.ln()

    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(0, 0, 0)
    for i, act in enumerate(session['actividades'], 1):
        pdf.cell(0, 6, f'{i}. {clean_text(act)}', border=0)
        pdf.ln()
    pdf.ln(3)

    # Tarea
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(51, 102, 153)
    pdf.cell(0, 8, 'TAREA PARA CASA:', border=0)
    pdf.ln()

    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(0, 0, 0)
    for tarea in session['tarea']:
        pdf.cell(0, 6, '- ' + clean_text(tarea), border=0)
        pdf.ln()

    # Footer
    pdf.ln(10)
    pdf.set_draw_color(100, 149, 237)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    pdf.set_font('Helvetica', 'I', 9)
    pdf.set_text_color(102, 102, 102)
    pdf.cell(0, 4, 'Universidad de Granada - Centro de Lenguas Modernas', border=0, align='C')

    # Save
    os.makedirs('materials/cuadernos', exist_ok=True)
    filename = f'materials/cuadernos/S{session["num"]}_Espanol_Intensivo.pdf'
    pdf.output(filename)
    print(f"✅ Created {filename}")

# Generate all sessions
print("📚 Creating session notebooks...")
for session in sessions:
    create_session_pdf(session)

print("\n🎉 All session notebooks created successfully!")
print("✨ Check materials/cuadernos/ for the new PDFs")
