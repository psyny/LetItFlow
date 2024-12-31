export function BuildTrayGenericVlisted(width) {
    const main_dom = document.createElement('div');
    main_dom.classList.add('tray-generic-vlisted');
    main_dom.style = "width: " + width + "px;";
    return main_dom;
}