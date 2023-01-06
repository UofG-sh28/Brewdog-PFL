window.onload = () => {
    const input = document.getElementById('heatingInput');
    const output = document.getElementById("heatingOutput");
    const sel = document.getElementById("heatingSel");
    const conversion = 0.22;

    const inputHandler = () => {
        const unit = parseFloat(sel.value);
        output.value = parseFloat(input.value) * conversion * unit;
    }

    sel.addEventListener("propertychange", inputHandler);
    sel.addEventListener("input", inputHandler);
    input.addEventListener('input', inputHandler);
    input.addEventListener('propertychange', inputHandler);
}


function applicableCheck(parent){
    const tableRow = this.document.getElementById(parent.id);
    const input = this.document.getElementById(tableRow.id + "Input");
    const sel = this.document.getElementById(tableRow.id + "Sel")
    input.disabled = !input.disabled;
    sel.disabled = !sel.disabled;

}
