from fpdf import FPDF
import random

class PDF(FPDF):
    def header(self):
        self.set_top_margin(30)
        self.image('diseñosenmadera2.png', 235, 8, 50)
        # font
        self.set_font('helvetica', 'BU', 24)
        # Padding
        # self.cell(40, 25)
        # Title
        self.cell(0, 35, 'Presupuesto', ln=True, align='C')
        # line break
        self.ln(20)


pedido = {'Fecha': '2-05-2023', 'Cliente': 'Johannes Perez',
          'Contacto': '2645045779', 'Total': 40000, 'Observaciones': 'A entregar pasado mañana por la tarde'
                                                                     ''}
new = {'Silla Eco Tapiz': [4, 40000]}

def generate_pdf(dic1, dic2):
    pdf = PDF('L', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 17)
    pdf.cell(100, 23, f'Fecha: {dic1["Fecha"]}')
    pdf.cell(105, 23, f'Cliente: {dic1["Cliente"]}')
    pdf.cell(20, 23, f'Contacto: {dic1["Contacto"]}')
    pdf.ln()
    pdf.set_font('helvetica', 'BU', 15)
    if len(dic1['Observaciones']) > 1:
        pdf.cell(43, 10, 'Observaciones:')
        pdf.set_font('helvetica', '', 15)
        pdf.multi_cell(200, 10, txt=f'{dic1["Observaciones"]}')
        pdf.ln()
    pdf.set_font('helvetica', 'BU', 15)
    pdf.cell(40, 20, 'Detalle:')
    pdf.ln()
    pdf.set_font('helvetica', '', 15)
    for k, v in dic2.items():
        pdf.cell(100, 10, f'{k} ')
        pdf.cell(100, 10, f'x{v[0]}')
        pdf.cell(70, 10, f'{v[1]}')
        pdf.ln()
    pdf.set_font('helvetica', 'B', 15)
    pdf.cell(200, 30, 'Total')
    pdf.cell(20, 30, f'{dic1["Total"]}')
    rn = random.randint(5, 100)
    pdf.output(f'{dic1["Fecha"]}-{dic1["Cliente"]}-{rn}.pdf')


if __name__ == '__main__':
    generate_pdf(pedido, new)
