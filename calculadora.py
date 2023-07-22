from flask import Flask, render_template, request, jsonify
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('agg')  # matplotlib para frontend. Ver discussão em  https://stackoverflow.com/questions/4930524/how-can-i-set-the-matplotlib-backend


class RendaFixa:
    def __init__(self, aporte_inicial, aporte_mensal, rentabilidade, periodos, tipo_rentabilidade, tipo_periodos):
        self.aporte_inicial = aporte_inicial
        self.aporte_mensal = aporte_mensal
        self.rentabilidade = rentabilidade
        self.periodos = periodos
        self.tipo_rentabilidade = tipo_rentabilidade
        self.tipo_periodos = tipo_periodos
    
    def juros_compostos(self):
        y1 = []
        y2 = []
        if self.tipo_periodos == 'Anos':
            periodos = self.periodos * 12
        else:
            periodos = self.periodos
        if self.tipo_rentabilidade == 'Anual':
            taxa_eq = (self.rentabilidade * 0.01 + 1) ** (1/12) -1
        else:
            taxa_eq = self.rentabilidade * 0.01
        for x in range(1, periodos+1):
            if x == 1:
                v0 = self.aporte_inicial
            else:
                v0 = vf
            aporte = self.aporte_mensal
            rendimento = v0 * taxa_eq
            vf = v0 + aporte + rendimento
            y2.append(vf)
            aporte_acumulado = x * aporte + self.aporte_inicial
            y1.append(aporte_acumulado)
        return [y1,y2,vf]

    def moeda(self, x, pos):
        if x < 1000000:
            return 'R${:,.0f}k'.format(x/1000).replace(',', '.')
        else:
            return 'R${:,.1f}M'.format(x/1000000).replace(',', '.')

    def grafico(self):
        if self.tipo_periodos == 'Anos':
            periodos = self.periodos * 12
        else:
            periodos = self.periodos
        plt.clf()
        fig = plt.figure()
        ax = fig.add_subplot()
        x = np.arange(0, periodos)
        plt.plot(x, self.juros_compostos()[0], color='purple', label='Aportes')
        plt.plot(x, self.juros_compostos()[1], color='aqua', label='Aportes + Rentabilidade')
        plt.xlabel('Meses')
        plt.legend()
        plt.fill_between(x, self.juros_compostos()[1], 0, color='purple')
        plt.fill_between(x, self.juros_compostos()[0], self.juros_compostos()[1], color='aqua')
        ax.yaxis.set_major_formatter(self.moeda)
        # Ajuste o tamanho dos ticks verticais
        plt.yticks(fontsize=10)
        plt.savefig('static/grafico.png')

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calcular', methods=['GET', 'POST'])
def calcular():
    lista_requests = [request.args.get('aporte_inicial'), request.args.get('aporte_mensal'), request.args.get('rentabilidade'), request.args.get('periodos')]
    if '' in lista_requests:
        return render_template('index.html')
    else:
        aporte_inicial = float(request.args.get('aporte_inicial'))
        aporte_mensal = float(request.args.get('aporte_mensal'))
        rentabilidade = float(request.args.get('rentabilidade'))
        periodos = int(request.args.get('periodos'))
        tipo_rentabilidade = request.args.get('tipo_rentabilidade').split()[0]
        tipo_periodos = request.args.get('tipo_periodos').split()[0]
        RendaFixa(aporte_inicial=aporte_inicial, aporte_mensal=aporte_mensal, rentabilidade=rentabilidade, periodos=periodos, tipo_rentabilidade=tipo_rentabilidade, tipo_periodos=tipo_periodos).grafico()
        montante = round(RendaFixa(aporte_inicial=aporte_inicial, aporte_mensal=aporte_mensal, rentabilidade=rentabilidade, periodos=periodos, tipo_rentabilidade=tipo_rentabilidade, tipo_periodos=tipo_periodos).juros_compostos()[2],2)
        montante_fmt = 'R${:,.2f}'.format(montante).replace(',','X').replace('.',',').replace('X','.')
        frase = f'Montante ao término do prazo: {montante_fmt}'
        return jsonify({'frase': frase})
        # render_template('index.html')


if __name__ == '__main__':
    # from os import environ
    #, port=environ.get("PORT", 8000)
    app.run(debug=False)
