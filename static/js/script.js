function funcaoLimpar() {
    document.getElementById("grafico").style.display = "none"; //esconde o gráfico na página. Ver discussão sobre JS para esconder/revelar tags em https://stackoverflow.com/questions/6242976/javascript-hide-show-element
    document.getElementById("frase").innerHTML = "";
    document.getElementById("aporte_inicial").value = "";
    document.getElementById("aporte_mensal").value = "";
    document.getElementById("rentabilidade").value = "";
    document.getElementById("periodos").value = "";
};

function funcaoGrafico() {
    if (document.getElementById("aporte_inicial").value == "" ||
        document.getElementById("aporte_mensal").value == "" ||
        document.getElementById("rentabilidade").value == "" ||
        document.getElementById("periodos").value == "") {
        alert('Preencha corretamente os inputs')
    } else {
        document.getElementById("grafico").style.display = "block"; //revela o gráfico na página
    }
}