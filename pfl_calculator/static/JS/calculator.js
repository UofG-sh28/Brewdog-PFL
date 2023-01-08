window.onload = () => {

    const inputHandler = (e) => {
        const tableRow = this.document.getElementById(e.target.parentNode.parentNode.id)
        const input = this.document.getElementById(tableRow.id + 'Input');
        const output = this.document.getElementById(tableRow.id + "Output");
        const conversion = this.document.getElementById(tableRow.id + "Conv");
        const value = parseFloat(input.value) * parseFloat(conversion.innerText);
        output.value = isNaN(value) ? "" : value;
    }

    const table = this.document.getElementById("table");
    for(let i=0; i < table.rows.length; i++){
        const row = table.rows[i];
        if (row.id === "headers") continue;

        const input = this.document.getElementById(row.id + "Input");
        if (input === undefined) continue;

        input.addEventListener('input', inputHandler);
        input.addEventListener('propertychange', inputHandler);
    }

}

function applicableCheck(parent){
    const tableRow = this.document.getElementById(parent.parentNode.parentNode.id);
    const input = this.document.getElementById(tableRow.id + "Input");
    const output = this.document.getElementById(tableRow.id + "Output");
    input.disabled = !input.disabled;
    output.required = !output.required;
    input.value = "";
    output.value = "";

}
