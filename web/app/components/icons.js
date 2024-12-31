import { ColorTools } from "../utils/color.js";

export function BuildIconGeneric1(iconFileName, color1, color2, width, height, clickable, color3, color4) {
    const img_path = 'media/icons/' + iconFileName;
    const url_string = "url('" + img_path + "') no-repeat center";

    const main_dom = document.createElement('div');
    main_dom.style.width = width + "px";
    main_dom.style.height = height + "px";
    main_dom.classList.add('icon-container');

    const idle_dom = document.createElement('div');
    idle_dom.style.background = "linear-gradient(to bottom, " + color1 + ", " + color2 + ")";
    idle_dom.style.mask = url_string;
    idle_dom.style["-webkit-mask"] = url_string;
    idle_dom.style["mask-size"] = width + "px " + height + "px";
    idle_dom.style["-webkit-mask-size"] = width + "px " + height + "px";
    idle_dom.classList.add('idle');
    main_dom.appendChild(idle_dom);

    if (clickable) {
        main_dom.style.cursor = "pointer";
        const over_dom = document.createElement('div');
        over_dom.style.background = "linear-gradient(to bottom, " + color3 + ", " + color4 + ")";
        over_dom.style.mask = url_string;
        over_dom.style["-webkit-mask"] = url_string;
        over_dom.style["mask-size"] = width + "px " + height + "px";
        over_dom.style["-webkit-mask-size"] = width + "px " + height + "px";
        over_dom.classList.add('over');
        main_dom.appendChild(over_dom);
    }


    return main_dom;
}

export function BuildIconStandard1(iconFileName, clickable, width, height) {
    if (!width) {
        width = 40;
    }
    if (!height) {
        height = 40;
    }

    const docStyle = getComputedStyle(document.documentElement);

    const color1 = docStyle.getPropertyValue('--button-bg-passive');
    const color2 = docStyle.getPropertyValue('--button-bg-passive');

    const color3 = docStyle.getPropertyValue('--button-bg-hover');
    const color4 = docStyle.getPropertyValue('--button-bg-hover');

    return BuildIconGeneric1(iconFileName, color1, color2, width, height, clickable, color3, color4);
}