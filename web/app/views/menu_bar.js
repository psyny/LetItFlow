import { Router } from '../views/router.js';

import { BuildButtonLarge } from '../components/buttons.js';
import { BuildInputGeneralLarge } from '../components/inputs.js';
import { BuildTitle1 } from '../components/titles.js';
import { BuildTrayGenericVlisted } from '../components/trays.js';
import { BuildSpacerBox } from '../components/spacers.js';
import { BuildSpacerVline } from '../components/spacers.js';
import { BuildText1 } from '../components/texts.js';

import { BuildIconStandard1 } from '../components/icons.js';

export class ViewMenuBar {
    static AreRequirementsMet() {
        return true
    }

    static GetPageId() {
        return "login"
    }

    static Build(icons) {
        const reqs = ViewMenuBar.AreRequirementsMet();

        if (reqs === false) {
            return null
        }

        // Main DOMs
        const main_dom = document.createElement('div');
        main_dom.classList.add('menu-bar-content');

        const left_dom = document.createElement('div');
        left_dom.classList.add('menu-bar-content-left');
        main_dom.appendChild(left_dom);

        const right_dom = document.createElement('div');
        right_dom.classList.add('menu-bar-content-right');
        main_dom.appendChild(right_dom);

        // Controllers
        let onLeft = 0;
        let onRight = 0;
        let vSpacer = null;

        // Icon - Settings
        if (icons.settings) {
            if (onLeft>0) {
                vSpacer = BuildSpacerVline(40);
                left_dom.appendChild(vSpacer);
            }
            onLeft++;

            const icon = BuildIconStandard1("gear.svg", true); 
            left_dom.appendChild(icon);
        }

        // Icon - Logout
        if (icons.logout) {
            if (onLeft>0) {
                vSpacer = BuildSpacerVline(40);
                left_dom.appendChild(vSpacer);
            }
            onLeft++;

            const icon = BuildIconStandard1("key.svg", true); 
            left_dom.appendChild(icon);
        }

        // Icon - Refresh
        if (icons.refresh) {
            if (onLeft>0) {
                vSpacer = BuildSpacerVline(40);
                left_dom.appendChild(vSpacer);
            }
            onLeft++;

            const icon = BuildIconStandard1("refresh.svg", true); 
            left_dom.appendChild(icon);
        }





        return main_dom
    }

    static Destroy() {
        return true;
    }
}