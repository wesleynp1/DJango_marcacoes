for ( const input of document.getElementsByClassName("only-numbers")){
        input.addEventListener("input", ()=>{ input.value = input.value.replace(/\D/g, ""); });
    }