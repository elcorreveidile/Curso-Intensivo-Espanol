#!/usr/bin/env python3
"""
Generador de PDFs profesionales para cada sesión del curso
"""

from fpdf import FPDF
import os

def clean_text(text):
    """Limpiar caracteres especiales para PDF compatible con latin1"""
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N', 'ü': 'u', 'Ü': 'U',
        '¿': '?', '¡': '!',
        '•': '-', '·': '.'
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text.encode('latin1', 'ignore').decode('latin1')

class SessionPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)
        self.set_margins(15, 25, 15)

    def header(self):
        # Encabezado profesional de sesión
        self.set_font('Arial', 'B', 14)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, clean_text(self.title), 0, 1, 'C')

        self.set_font('Arial', 'I', 10)
        self.set_text_color(102, 102, 102)
        self.cell(0, 5, 'Curso Intensivo de Espanol - Nivel 3 CLM (A1.2-A2.1)', 0, 1, 'C')

        self.set_font('Arial', 'B', 9)
        self.set_text_color(0, 153, 51)
        self.cell(0, 5, f'Sesion {self.session_number}: {clean_text(self.session_date)}', 0, 1, 'C')

        self.ln(8)

    def footer(self):
        # Pie de página
        self.set_y(-20)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 5, f'Pagina {self.page_no()}', 0, 1, 'C')
        self.cell(0, 5, 'Profesor: Javier Benitez Lainez | Lunes-Jueves 8:30-10:30', 0, 0, 'C')

    def section_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_text_color(139, 69, 19)
        self.cell(0, 8, clean_text(title), 0, 1, 'L')
        self.ln(3)

    def content_text(self, text):
        self.set_font('Arial', '', 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(180, 5, clean_text(text))
        self.ln(3)

def create_session_1():
    pdf = SessionPDF()
    pdf.title = 'Sesion 1: Presentaciones y Saludos'
    pdf.session_number = 1
    pdf.session_date = 'Lunes 10 de Noviembre'
    pdf.set_title('Sesion 1 - Curso Intensivo de Espanol')
    pdf.add_page()

    pdf.section_title('Objetivos de la Sesion')
    pdf.content_text('• Presentarse y presentar a otras personas')
    pdf.content_text('• Usar expresiones de saludo y despedida')
    pdf.content_text('• Preguntar y dar informacion personal basica')
    pdf.content_text('• Entender y usar el alfabeto espanol')

    pdf.section_title('Contenido Gramatical')
    pdf.content_text('1. El verbo SER en presente:')
    pdf.content_text('   Yo soy, Tu eres, El/ella es, Nosotros somos, Vosotros sois, Ellos son')
    pdf.content_text('')
    pdf.content_text('2. Pronombres personales sujeto')
    pdf.content_text('3. Genero (masculino/femenino) y numero (singular/plural)')
    pdf.content_text('4. Articulos determinados e indeterminados')

    pdf.section_title('Vocabulario Clave')
    pdf.content_text('• Saludos: Hola, Buenos dias/tardes/noches')
    pdf.content_text('• Despedidas: Adios, Hasta luego, Nos vemos')
    pdf.content_text('• Presentaciones: Me llamo..., Soy de..., Tengo...')
    pdf.content_text('• Paises y nacionalidades')
    pdf.content_text('• Profesiones y ocupaciones')

    pdf.section_title('Actividades de Clase')
    pdf.content_text('1. Calentamiento: Juego de presentaciones en circulo')
    pdf.content_text('2. Practica dialogada: Presentaciones formales e informales')
    pdf.content_text('3. Ejercicio: Completar frases con SER')
    pdf.content_text('4. Actividad de listening: Entender presentaciones')
    pdf.content_text('5. Role-play: Conocer a companeros de clase')

    pdf.section_title('Tarea para Casa')
    pdf.content_text('• Escribir un parrafo de presentacion personal (50-60 palabras)')
    pdf.content_text('• Memorizar 10 paises y sus nacionalidades en espanol')
    pdf.content_text('• Practicar el alfabeto frente a un espejo')

    pdf.output('materials/sessions/sesion-1.pdf')
    print("✅ Created professional sesion-1.pdf")

def create_session_2():
    pdf = SessionPDF()
    pdf.title = 'Sesion 2: Tiempo, Fechas y Numeros'
    pdf.session_number = 2
    pdf.session_date = 'Martes 11 de Noviembre'
    pdf.set_title('Sesion 2 - Curso Intensivo de Espanol')
    pdf.add_page()

    pdf.section_title('Objetivos de la Sesion')
    pdf.content_text('• Contar hasta 100')
    pdf.content_text('• Dar y entender la hora')
    pdf.content_text('• Expresar fechas y dias de la semana')
    pdf.content_text('• Hacer preguntas sobre tiempo y duracion')

    pdf.section_title('Contenido Gramatical')
    pdf.content_text('1. Numeros cardinales (0-100)')
    pdf.content_text('2. Expresion de la hora:')
    pdf.content_text('   - Es la una y cuarto/dos/veinte/cuarto')
    pdf.content_text('   - Son las dos, las tres, las cuatro...')
    pdf.content_text('3. Dias de la semana y meses del ano')
    pdf.content_text('4. Preposiciones de tiempo: a, en, de, por')
    pdf.content_text('5. Uso de SER para expresar tiempo')

    pdf.section_title('Vocabulario Clave')
    pdf.content_text('• Numeros: cero, uno, dos, tres... cien')
    pdf.content_text('• Horas: mediodia, medianoche, tarde, manana')
    pdf.content_text('• Dias: lunes, martes, miercoles, jueves, viernes')
    pdf.content_text('• Meses: enero, febrero, marzo...')
    pdf.content_text('• Expresiones temporales: hoy, manana, ayer')

    pdf.section_title('Actividades de Clase')
    pdf.content_text('1. Dictado de numeros')
    pdf.content_text('2. Ejercicio: Que hora es? (con relojes visuales)')
    pdf.content_text('3. Practica: Fechas importantes y cumpleanos')
    pdf.content_text('4. Juego: Bingo con numeros')
    pdf.content_text('5. Role-play: Hacer citas y planes')

    pdf.section_title('Tarea para Casa')
    pdf.content_text('• Practicar la hora con 10 ejemplos diferentes')
    pdf.content_text('• Escribir las fechas de 5 eventos importantes')
    pdf.content_text('• Crear un horario personal en espanol')

    pdf.output('materials/sessions/sesion-2.pdf')
    print("✅ Created professional sesion-2.pdf")

def create_session_3():
    pdf = SessionPDF()
    pdf.title = 'Sesion 3: Familia y Relaciones Personales'
    pdf.session_number = 3
    pdf.session_date = 'Miercoles 12 de Noviembre'
    pdf.set_title('Sesion 3 - Curso Intensivo de Espanol')
    pdf.add_page()

    pdf.section_title('Objetivos de la Sesion')
    pdf.content_text('• Describir la familia')
    pdf.content_text('• Expresar relaciones personales')
    pdf.content_text('• Usar adjetivos posesivos')
    pdf.content_text('• Describir personas fisicamente')

    pdf.section_title('Contenido Gramatical')
    pdf.content_text('1. El verbo TENER en presente:')
    pdf.content_text('   Tengo, tienes, tiene, tenemos, teneis, tienen')
    pdf.content_text('2. Adjetivos posesivos: mi/mis, tu/tus, su/sus...')
    pdf.content_text('3. Adjetivos descriptivos: genero y concordancia')
    pdf.content_text('4. Verbos SER vs ESTAR para descripciones')
    pdf.content_text('5. Contracciones: del, al')

    pdf.section_title('Vocabulario Clave')
    pdf.content_text('• Familia: padre, madre, hermano/a, hijo/a, abuelo/a')
    pdf.content_text('• Relaciones: amigo/a, companero/a, novio/a')
    pdf.content_text('• Adjetivos fisicos: alto/a, bajo/a, joven, viejo/a')
    pdf.content_text('• Caracter: simpatico/a, serio/a, divertido/a')
    pdf.content_text('• Posesiones: mi, tu, su, nuestro/a')

    pdf.section_title('Actividades de Clase')
    pdf.content_text('1. Arbol genealogico: Presentar la familia')
    pdf.content_text('2. Ejercicio: Describir companeros de clase')
    pdf.content_text('3. Juego: Quien es quien? (descripciones)')
    pdf.content_text('4. Practica dialogada: Hablar de relaciones')
    pdf.content_text('5. Actividad de writing: Descripcion personal')

    pdf.section_title('Tarea para Casa')
    pdf.content_text('• Dibujar y describir a tu familia (min. 6 personas)')
    pdf.content_text('• Escribir sobre tu mejor amigo/a')
    pdf.content_text('• Memorizar 10 adjetivos de caracter y sus opuestos')

    pdf.output('materials/sessions/sesion-3.pdf')
    print("✅ Created professional sesion-3.pdf")

def create_session_4():
    pdf = SessionPDF()
    pdf.title = 'Sesion 4: Rutina Diaria y Actividades'
    pdf.session_number = 4
    pdf.session_date = 'Jueves 13 de Noviembre'
    pdf.set_title('Sesion 4 - Curso Intensivo de Espanol')
    pdf.add_page()

    pdf.section_title('Objetivos de la Sesion')
    pdf.content_text('• Describir rutinas diarias')
    pdf.content_text('• Expresar frecuencia y tiempo')
    pdf.content_text('• Usar verbos reflexivos')
    pdf.content_text('• Hablar de hobbies y tiempo libre')

    pdf.section_title('Contenido Gramatical')
    pdf.content_text('1. Verbos reflexivos y pronombres: me, te, se, nos, os')
    pdf.content_text('2. Verbos regulares en presente (AR, ER, IR)')
    pdf.content_text('3. Adverbios de frecuencia:')
    pdf.content_text('   siempre, generalmente, a veces, nunca')
    pdf.content_text('4. Expresiones de tiempo: por la manana, por la tarde')
    pdf.content_text('5. Verbos irregulares comunes: IR, ESTAR, HACER')

    pdf.section_title('Vocabulario Clave')
    pdf.content_text('• Rutina: levantarse, ducharse, desayunar, trabajar...')
    pdf.content_text('• Comidas: desayuno, almuerzo, cena, merienda')
    pdf.content_text('• Tiempo libre: practicar deportes, leer, ver la television')
    pdf.content_text('• Lugares: casa, trabajo, universidad, parque')
    pdf.content_text('• Frecuencia: todos los dias, nunca, a veces')

    pdf.section_title('Actividades de Clase')
    pdf.content_text('1. Organizar un horario diario')
    pdf.content_text('2. Ejercicio: Que haces todos los dias?')
    pdf.content_text('3. Juego: Mimica con acciones diarias')
    pdf.content_text('4. Role-play: Planificar actividades de fin de semana')
    pdf.content_text('5. Listening: Entender rutinas de otras personas')

    pdf.section_title('Tarea para Casa')
    pdf.content_text('• Escribir tu rutina diaria detallada')
    pdf.content_text('• Entrevistar a un companero sobre sus hobbies')
    pdf.content_text('• Preparar una mini-presentacion sobre tu fin de semana ideal')

    pdf.output('materials/sessions/sesion-4.pdf')
    print("✅ Created professional sesion-4.pdf")

def create_all_sessions():
    """Crear todos los PDFs de sesiones"""
    # Crear directorio si no existe
    if not os.path.exists('materials/sessions'):
        os.makedirs('materials/sessions')

    print("📚 Creating professional session PDFs...")
    create_session_1()
    create_session_2()
    create_session_3()
    create_session_4()

    print("\n✅ All session PDFs created successfully!")
    print("📖 Professional formatting with proper structure and educational content")
    print("🎯 Each session includes objectives, grammar, vocabulary, activities and homework")

if __name__ == "__main__":
    create_all_sessions()