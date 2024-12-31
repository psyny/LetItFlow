export function BuildTitle1(text) {
    const main_dom = document.createElement('div');
    main_dom.classList.add('text-title1');
    main_dom.classList.add('center');
    main_dom.innerHTML = text;
    return main_dom;
}