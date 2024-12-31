export function BuildButtonLarge(label) {
    const main_dom = document.createElement('div');
    main_dom.classList.add('button-large');

    const bg_dom = document.createElement('div');
    bg_dom.classList.add('button-bg');
    main_dom.appendChild(bg_dom);

    const label_dom = document.createElement('div');
    label_dom.classList.add('button-label');
    label_dom.innerHTML = label;
    main_dom.appendChild(label_dom);

    return [main_dom, bg_dom];
}