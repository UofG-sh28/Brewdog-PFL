
function getDecimalLength(r){
    if(Math.floor(r) === r) return 0;
    try{
        return r.toString().split(".")[1].length || 0;
    }catch (TypeError){
        return 0;
    }
}


window.onload = () => {

    const inputHandler = (e) => {
        const tableRow = this.document.getElementById(e.target.parentNode.parentNode.id)
        const input = this.document.getElementById(tableRow.id + 'Input');
        const output = this.document.getElementById(tableRow.id + "Output");
        const conversion = this.document.getElementById(tableRow.id + "Conv");
        let value = parseFloat(input.value) * parseFloat(conversion.innerText);
        const decimalLength = getDecimalLength(parseFloat(input.value));
        if(value <= 0) value = "";
        output.value = isNaN(value) ? "" : value.toFixed(Math.max(2, decimalLength));
    }

    const outputValidation = (e) => {
        const output = this.document.querySelector('input:invalid')
        const tableRowId = output.parentNode.parentNode.id;
        const input = this.document.getElementById(tableRowId + "Input");
        input.value = "";
        input.select();
        input.focus();
    }

    const tables = this.document.getElementsByClassName("table");
    for(let j=0; j < tables.length; j++) {
        for (let i = 0; i < tables[j].rows.length; i++) {
            const row = tables[j].rows[i];
            if (row.id === "headers") continue;

            const input = this.document.getElementById(row.id + "Input");
            const output = this.document.getElementById(row.id + "Output");
            const check = this.document.getElementById(row.id + "Checkbox")
            if (input === undefined || output === undefined
                || check===undefined) continue;

            if(!check.checked) applicableCheck(check);

            input.addEventListener('invalid', outputValidation);
            output.addEventListener('invalid', (e) => e.preventDefault());
            input.addEventListener('input', inputHandler);
            input.addEventListener('propertychange', inputHandler);
        }
    }
}



function applicableCheck(current){
    const tableRow = this.document.getElementById(current.parentNode.parentNode.id);
    const input = this.document.getElementById(tableRow.id + "Input");
    const output = this.document.getElementById(tableRow.id + "Output");
    const name = this.document.getElementById(tableRow.id + "Name");
    const conv = this.document.getElementById(tableRow.id + "Conv");
    const check = this.document.getElementById(tableRow.id + "Check");
    const info = this.document.getElementById(tableRow.id + "Info");
    const span = this.document.getElementById(tableRow.id + "Span");


    input.style.border = "0.15em solid " + (input.disabled ? "black" : "grey");
    output.style.border = "0.15em solid " + (input.disabled ? "black" : "grey");
    const value = input.disabled ? "1" : "0.5"
    name.style.opacity = value;
    conv.style.opacity = value;
    check.style.opacity = value;
    info.style.opacity = value;
    span.hidden = !span.hidden;



    input.disabled = !input.disabled;
    input.required = !input.required;
    input.value = "";
    output.value = " ";

}
