export function BuildInputGeneralLarge(label, typeData = null) {
    if (typeData===null) {
        typeData = {
            "type": "text",
            "placeholder": " ",
        }
    }
    
    const main_dom = document.createElement('div');
    main_dom.classList.add('input-general-large');

    const input_field_dom = document.createElement('input');
    input_field_dom.classList.add('input-field');
    input_field_dom.placeholder = " ";
    
    input_field_dom.type = typeData.type;
    switch( typeData.type ) {
        case "text":
        case "password":
        case "email":
        case "tel":
        case "url":
        case "search":
            input_field_dom.placeholder = typeData.placeholder ?? " ";
            break;

        case "number":
        case "range":
            input_field_dom.min = typeData.min ?? 1;
            input_field_dom.max = typeData.max ?? 20;
            break;
    }
    main_dom.appendChild(input_field_dom);

    const input_label_dom = document.createElement('div');
    input_label_dom.classList.add('input-label');
    input_label_dom.innerHTML = label;
    main_dom.appendChild(input_label_dom);

    const input_styling1_dom = document.createElement('div');
    input_styling1_dom.classList.add('input-styling');
    main_dom.appendChild(input_styling1_dom);

    return [main_dom, input_field_dom];
}