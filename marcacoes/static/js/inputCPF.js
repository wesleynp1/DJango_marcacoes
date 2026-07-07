for ( const form of document.getElementsByClassName("Form-with-input-CPF")){

    const inputs = form.querySelectorAll(".input-CPF");

    form.addEventListener("submit",()=>formatarCampoCpfParaSubmit(inputs));

    for(const input of inputs ){
        input.addEventListener("input", formatarCPF);
        input.dispatchEvent(new Event("input"));
    }
}

function formatarCampoCpfParaSubmit(inputs){
    for(const input of inputs ){
        input.value = input.value.replace(/\D/g, "");
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