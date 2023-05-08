import random
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import white, gray
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import PIL


x = {'Fecha': '2-05-2023', 'Cliente': 'Johannes Perez',
          'Contacto': '2645045779', 'Total': 85234, 'Observaciones': 'A entregar pasado mañana por la tarde',
          'Articulos': ['Silla Eco Tapiz', 'Silla Eco Tapiz','Silla Eco Tapiz', 'Silla Eco Tapiz'
                        'Mesa Octogonal', 'Mesa Octogonal'], 'Precios': [10000, 10000, 10000, 10000,
                                                                         22617, 22617]
                                                                     }
new = {'Silla Eco Tapiz': [4, 40000], 'Mesa Octogonal': [2, 45234]}


def generate(dic1, dic2):
    datos = ['Diseños en Maderas', 'Av. España 1445 Sur', '2645305811 / 2617149952']
    rn = random.randint(1, 100)
    name = f'{dic1["Fecha"]}-{dic1["Cliente"]}-{rn}.pdf'
    canvas = Canvas(name)
    width, length = A4

    # Set font
    pdfmetrics.registerFont(TTFont('Calibri', 'calibri-font-family/calibri-regular.ttf'))
    pdfmetrics.registerFont(TTFont('Calibri Bold', 'calibri-font-family/calibri-bold.ttf'))
    canvas.setFont('Calibri Bold', 18)
    # (distance from left edge of canvas, distance from bottom edge)
    # measured in points (point == 1/72 inches; 72 == 1 inch)
    image = 'diseñosenmadera2.png'
    canvas.drawString(50, length - 115, 'Presupuesto')
    # canvas.setTitle('Presupuesto')
    canvas.drawImage(image, x=width-120, y=length-120, width=90, height=90, mask=None)
    canvas.setFont('Calibri Bold', 15)
    canvas.drawString(50, length-160, 'Datos Cliente')
    canvas.drawString(width / 2, length-160, 'Fecha:')
    # text1.setFont('Calibri Bold', 14)

    # Text 1
    text1 = canvas.beginText(50, length - 190)
    text1.setFont('Calibri', 12)
    text1.textLine(f'Nombre: {dic1["Cliente"]}')
    text1.textLine(f'Contacto: {dic1["Contacto"]}')
    text1.textLine(f'Dirección: ')

    # Text 2
    text2 = canvas.beginText(width / 2, length-190)
    text2.setFont('Calibri Bold', 14)
    text2.textLine(f'{dic1["Fecha"]}')

    # Text 3
    text3 = canvas.beginText(width-118, length-160)
    text3.setFont('Calibri', 10)
    text3.textLine(datos[0])
    text3.textLine(datos[1])
    text3.textLine(datos[2])

    # Tabla
    # Text4
    text4 = canvas.beginText(50, length - 300)
    text4.setFont('Calibri Bold', 14)
    text4.textLine('Concepto')
    text4.setFont('Calibri', 12)
    for k in dic2.keys():
        text4.textLine()
        text4.textLine(k)
        text4.textLine()
    # Text 5
    text5 = canvas.beginText(width/2, length - 300)
    text5.setFont('Calibri Bold', 14)
    text5.textLine('Cantidad')
    text5.setFont('Calibri', 12)
    for v in dic2.values():
        text5.textLine()
        text5.textLine(f'{v[0]}')
        text5.textLine()

    # Text 6
    text6 = canvas.beginText(width/2 + 70, length-300)
    text6.setFont('Calibri Bold', 14)
    text6.textLine('Precio Unidad')
    text6.setFont('Calibri', 12)
    for v in dic2.values():
        text6.textLine()
        text6.textLine(f'{v[1] / v[0]}')
        text6.textLine()
    # text6.textLine('Total:')
    # Text 7
    text7 = canvas.beginText(width-70, length-300)
    text7.setFont('Calibri Bold', 14)
    text7.textLine('Total')
    text7.setFont('Calibri', 12)
    for v in dic2.values():
        text7.textLine()
        text7.textLine(f'{v[1]}')
        text7.textLine()
    text7.setFont('Calibri Bold', 12)
    text7.textLine(f'{dic1["Total"]}')

    # End text
    endtext = canvas.beginText(50, 160)
    endtext.setFont('Calibri Bold', 14)
    endtext.textLine('Método de pago:')
    endtext.textLine('Fecha de entrega:')
    endtext.textLine()
    endtext.textLine(f'Comentarios: {dic1["Observaciones"]}')

    # Total

    # Draw Text
    canvas.drawText(text1)
    canvas.drawText(text2)
    canvas.drawText(text3)
    canvas.drawText(text4)
    canvas.drawText(text5)
    canvas.drawText(text6)
    canvas.drawText(text7)
    canvas.drawText(endtext)
    canvas.save()
