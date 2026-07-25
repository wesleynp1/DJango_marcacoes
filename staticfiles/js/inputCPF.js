for ( const form of document.getElementsByClassName("Form-with-input-CPF")){

    const inputs = form.querySelectorAll(".input-CPF");

    form.addEventListener("submit",e => formatarCampoCpfParaSubmit(inputs, e));

    for(const input of inputs ){
        input.addEventListener("input", formatarCPF);
        input.dispatchEvent(new Event("input"));
    }
}

function formatarCampoCpfParaSubmit(inputs, evento){
    for(const input of inputs ){

        let cpf = input.value.replace(/\D/g, "");

        if(validarCPF(cpf)){
            input.value = cpf
        }else{
            input.classList.add("is-invalid")
            evento.preventDefault()
        }

    }
}

function formatarCPF(event){
    let valor = event.target.value;
    let posicao_do_cursor = event.target.selectionStart;
    valor = valor.replace(/\D/g, "");

    if (valor.length >= 4 && valor.length < 7) {
        valor = valor.replace(/(\d{3})(\d+)/, '$1.$2');

    } else if (valor.length >= 7 && valor.length < 10) {
        valor = valor.replace(/(\d{3})(\d{3})(\d+)/, '$1.$2.$3');

    } else if (valor.length >= 10) {
        valor = valor.replace(/(\d{3})(\d{3})(\d{3})(\d+)/, '$1.$2.$3-$4');
    }

    if (posicao_do_cursor === 4)posicao_do_cursor++;
    if (posicao_do_cursor === 8)posicao_do_cursor++;
    if (posicao_do_cursor === 12)posicao_do_cursor++;

    event.target.value = valor;
    console.log(posicao_do_cursor)

    try {
        event.target.setSelectionRange(posicao_do_cursor, posicao_do_cursor);
    }catch (error) {
        console.error(error);
    }
}

function validarCPF(cpf){
    //Retorna true se for válido ou false senão
    if (cpf.length !== 11 || !!cpf.match(/(\d)\1{10}/)) return false;

    cpf = cpf.split('').map(el => +el);

    const rest = (count) => (
    cpf
        .slice(0, count - 12)
        .reduce((soma, el, index) => soma + el * (count - index), 0) * 10
    ) % 11 % 10;

return rest(10) === cpf[9] && rest(11) === cpf[10];
}