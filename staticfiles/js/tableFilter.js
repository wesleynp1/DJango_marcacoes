for ( const filterInput of document.getElementsByClassName("table-filter")){
    filterInput.addEventListener("input",function(e){
        
        for(row of document.getElementById(filterInput.dataset.target) .tBodies[0].rows){
            if(this.value){
                row.style.display = !row.textContent.toLowerCase().includes(this.value.toLowerCase()) ? "none" : "table-row";
            }else{
                row.style.display = "table-row";
            }
        }
    })
}