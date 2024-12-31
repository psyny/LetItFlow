export function BuildSpacerBox(width, height) {
    const main_dom = document.createElement('div');
    main_dom.classList.add('spacer-box');
    main_dom.style.width = width + "px";
    main_dom.style.height = height + "px";
    return main_dom;
}

export function BuildSpacerVline(height) {
    const main_dom = document.createElement('div');
    main_dom.classList.add('spacer-v-line');
    main_dom.style.height = height + "px";
    return main_dom;
}