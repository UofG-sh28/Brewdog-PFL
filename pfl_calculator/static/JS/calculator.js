window.onload = () => {

    const inputHandler = (e) => {
        const tableRow = this.document.getElementById(e.target.parentNode.parentNode.id)
        const input = this.document.getElementById(tableRow.id + 'Input');
        const output = this.document.getElementById(tableRow.id + "Output");
        const conversion = this.document.getElementById(tableRow.id + "Conv");
        output.value = parseFloat(input.value) * parseFloat(conversion.innerText);
    }

    const input = this.document.getElementById("goodDelInput");
    input.addEventListener('input', inputHandler);
    input.addEventListener('propertychange', inputHandler);
}


function applicableCheck(parent){
    const tableRow = this.document.getElementById(parent.parentNode.parentNode.id);
    const input = this.document.getElementById(tableRow.id + "Input");
    input.disabled = !input.disabled;
}
