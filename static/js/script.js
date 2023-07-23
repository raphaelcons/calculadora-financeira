function funcaoLimpar() {
    document.getElementById("chart").style.display = "none"; //esconde o gráfico na página. Ver discussão sobre JS para esconder/revelar tags em https://stackoverflow.com/questions/6242976/javascript-hide-show-element
    document.getElementById("frase").innerHTML = "";
    document.getElementById("aporte_inicial").value = "";
    document.getElementById("aporte_mensal").value = "";
    document.getElementById("rentabilidade").value = "";
    document.getElementById("periodos").value = "";
};

function funcaoChart() {
    if (document.getElementById("aporte_inicial").value === "" ||
        document.getElementById("aporte_mensal").value === "" ||
        document.getElementById("rentabilidade").value === "" ||
        document.getElementById("periodos").value === "") {
        alert('Preencha corretamente os inputs')
    } else {
        document.getElementById("chart").style.display = "block"; //revela o gráfico na página
        var tipo_rentabilidade = document.getElementById('tipo_rentabilidade').value;
        var tipo_periodos = document.getElementById('tipo_periodos').value;
        var aporte_inicial = parseFloat(document.getElementById('aporte_inicial').value);
        var aporte_mensal = parseFloat(document.getElementById('aporte_mensal').value);
        var rentabilidade = parseFloat(document.getElementById('rentabilidade').value);
        var periodos = parseInt(document.getElementById('periodos').value);
        const y1 = [];
        const y2 = [];
        let vf = 0;

        let meses;
        if (tipo_periodos === '1') { // Anos
            meses = periodos * 12;
        } else {
            meses = periodos;
        }
        let taxa_eq;
        if (tipo_rentabilidade === '1') { // Anual
            taxa_eq = Math.pow((rentabilidade * 0.01 + 1), (1 / 12)) - 1;
        } else {
            taxa_eq = rentabilidade * 0.01;
        }
        console.log(taxa_eq);
        for (let x = 1; x <= meses; x++) {
            let v0;
            if (x === 1) {
                v0 = aporte_inicial;
            } else {
                v0 = vf;
            }
            const aporte = aporte_mensal;
            const rendimento = v0 * taxa_eq;
            vf = v0 + aporte + rendimento;
            y2.push(vf);
            const aporte_acumulado = x * aporte + aporte_inicial;
            y1.push(aporte_acumulado);
        }
        // return [y1, y2, vf];
        var N = meses;
        const numbersArray = [];
        for (let i = 1; i <= N; i++) {
            numbersArray.push(i.toString());
        }
        var ctx = document.getElementById('chart');
        //Type, Data e Options
        var chartExist = Chart.getChart("chart"); // <canvas> id
        if (chartExist != undefined)
            chartExist.destroy(); // O gráfico anteriro precisa ser destruído antes de atualizar o gráfico. Ver https://stackoverflow.com/questions/72193719/chart-js-error-in-angular-canvas-is-already-in-use-chart-with-id-0-must-be-d
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: numbersArray,
                datasets: [{
                        label: 'Aportes + Rendimento',
                        data: y2,
                        borderWidth: 4,
                        borderColor: '#31fd22',
                        backgroundColor: 'transparent',
                    },
                    {
                        label: 'Aportes',
                        data: y1,
                        borderWidth: 4,
                        borderColor: '#066699',
                        backgroundColor: 'transparent',
                    },
                ]
            },
            options: {
                plugins: {
                    title: {
                        display: true,
                        text: 'RELATÓRIO',
                        color: '#000000d3',
                        font: {
                            size: 40,
                            family: 'Roboto',
                        },
                    },
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Meses',
                            color: '#000000d3',
                            font: {
                                size: 30,
                                family: 'Roboto',
                            },
                        },
                    },
                    y: {
                        ticks: {
                            // Inclua um cifrão na frente dos ticks no eixo y. Ver https://stackoverflow.com/questions/47836842/dollar-sign-on-y-axis-with-chartjs
                            callback: function(value, index, values) {
                                return value.toLocaleString('pt-BR', { minimumFractionDigits: 2, style: 'currency', currency: 'BRL' });
                            }
                        }
                    }
                }
            }
        });
    }
}