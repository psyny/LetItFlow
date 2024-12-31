export function BuildText1(text) {
    const main_dom = document.createElement('div');
    main_dom.classList.add('text-body1');
    main_dom.innerHTML = text;
    return main_dom;
}