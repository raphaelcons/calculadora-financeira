from flask import Flask, render_template, request, redirect
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('agg')


class RendaFixa:
    def __init__(self, aporte_inicial, aporte_mensal, rentabilidade, meses):
        self.aporte_inicial = aporte_inicial
        self.aporte_mensal = aporte_mensal
        self.rentabilidade = rentabilidade
        self.meses = meses
    
    def juros_compostos(self):
        y1 = []
        y2 = []
        for x in range(1, self.meses+1):
            if x == 1:
                v0 = self.aporte_inicial
            else:
                v0 = vf
            i = self.rentabilidade  
            aporte = self.aporte_mensal
            rendimento = v0*((i*0.01+1)**(1/12)-1)
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
        plt.clf()
        fig = plt.figure()
        ax = fig.add_subplot()
        x = np.arange(0, self.meses)
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

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calcular', methods=['POST','GET'])
def calcular():
    lista_requests = [request.args.get('aporte_inicial'), request.args.get('aporte_mensal'), request.args.get('rentabilidade'), request.args.get('meses')]
    if '' in lista_requests:
        return render_template('index.html')
    else:    
        aporte_inicial = float(request.args.get('aporte_inicial'))
        aporte_mensal = float(request.args.get('aporte_mensal'))
        rentabilidade = float(request.args.get('rentabilidade'))
        meses = int(request.args.get('meses'))
        RendaFixa(aporte_inicial=aporte_inicial, aporte_mensal=aporte_mensal, rentabilidade=rentabilidade, meses=meses).grafico()
        montante = round(RendaFixa(aporte_inicial=aporte_inicial, aporte_mensal=aporte_mensal, rentabilidade=rentabilidade, meses=meses).juros_compostos()[2],2)
        montante_fmt = 'R${:,.2f}'.format(montante).replace(',','X').replace('.',',').replace('X','.')
        frase = f'Montante ao término do prazo: {montante_fmt}'
        return render_template('index.html', frase=frase)

app.run(debug=True)
