import { Router } from '../views/router.js';

import { BuildButtonLarge } from '../components/buttons.js';
import { BuildInputGeneralLarge } from '../components/inputs.js';
import { BuildTitle1 } from '../components/titles.js';
import { BuildTrayGenericVlisted } from '../components/trays.js';
import { BuildSpacerBox } from '../components/spacers.js';
import { BuildText1 } from '../components/texts.js';

import { ViewMenuBar } from './menu_bar.js';

import { API } from '../services/api.js';

export class ViewLogin {
    static AreRequirementsMet() {
        return true
    }

    static GetPageId() {
        return "login"
    }

    static Build() {
        const reqs = ViewLogin.AreRequirementsMet();

        if (reqs === false) {
            return null
        }

        // Main DOM
        const main_dom = document.createElement('div');
        main_dom.classList.add('positioner-center-vh');

        // Tray DOM
        const main_tray_dom = BuildTrayGenericVlisted(500);
        main_dom.appendChild(main_tray_dom);

        // Title
        const title_dom = BuildTitle1("Let It Flow");
        main_tray_dom.appendChild(title_dom);

        // Input 1 - Username
        const [input_user_dom, input_user_dom_input] = BuildInputGeneralLarge("Username", {"type": "text"})
        main_tray_dom.appendChild(input_user_dom);

        // Input 2 - Password
        const [input_pass_dom, input_pass_dom_input] = BuildInputGeneralLarge("Password", {"type": "password"})
        main_tray_dom.appendChild(input_pass_dom);

        // Spacer 1
        const spacer1_dom = BuildSpacerBox(100, 20);
        main_tray_dom.appendChild(spacer1_dom);

        // Button 1 - login
        const [btn_login_dom, btn_login_dom_bg] = BuildButtonLarge("login");
        main_tray_dom.appendChild(btn_login_dom);

        // Spacer 2
        const spacer2_dom = BuildSpacerBox(20, 20);
        main_tray_dom.appendChild(spacer2_dom);

        // Text - Or
        const text1_dom = BuildText1("OR");
        main_tray_dom.appendChild(text1_dom);

        // Spacer 3
        const spacer3_dom = BuildSpacerBox(100, 20);
        main_tray_dom.appendChild(spacer3_dom);

        // Button 1 - Spectator
        const [btn_spectator_dom, btn_spectator_dom_bg] = BuildButtonLarge("join as spectator");
        main_tray_dom.appendChild(btn_spectator_dom);

        // Set Actions
        btn_login_dom.onclick = function () {
            API.Login("admin", "admin", "actor");
        };

        // Activate BG
        Router.BgImage("bg1.webp");

        // Menu Bar 
        const menu_bar_dom = document.getElementById("menu-bar-container");
        const menuIcons = {
            settings: true,
            logout: true,
            refresh: true,
        }
        const menu_bar_content = ViewMenuBar.Build(menuIcons);
        menu_bar_dom.appendChild(menu_bar_content);

        return main_dom;
    }

    static Destroy() {
        return true;
    }
}