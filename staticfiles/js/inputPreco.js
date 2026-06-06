for ( const form of document.getElementsByClassName("Form-with-input-BRL")){
    const inputs = form.querySelectorAll(".input-BRL");
    form.addEventListener("submit",()=>formatarCampoPrecoParaSubmit(inputs));
    for(const input of inputs ){
        input.addEventListener("input",formatarDinheiro);
        input.dispatchEvent(new Event("input"))
    }
}

function formatarDinheiro(){
    let numero = parseInt(this.value.replace(/[^0-9]/g, ''));
    let numeroEmTexto = isNaN(numero) ? "0" : numero.toString();

    if(numeroEmTexto.length>5){
        //Separa centavos de reais
        let centavos = numeroEmTexto.slice(-2);
        let reais = numeroEmTexto.slice(0,-2);

        //Adiciona o ponto de milhar nos reais
        for(let i=reais.length-3;i>0;i-=3){
            reais = reais.slice(0,i)+"."+reais.slice(i);
        }

        this.value = "R$ "+reais+","+centavos;
    }else{
        //Completa zeros à esquerda
        while(numeroEmTexto.length<3){
            numeroEmTexto = "0"+numeroEmTexto;
        }
        this.value = "R$ "+numeroEmTexto.slice(0,-2)+","+numeroEmTexto.slice(-2);
    }
}

/**
 * @param inputs : NodeListOf<Element>
 * */
function formatarCampoPrecoParaSubmit(inputs){
    for(const input of inputs) {
        input.value = input.value.replace(".","").replace(",", ".").replace("R$ ", "");
    }
}