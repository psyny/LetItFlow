import { State } from '../services/state.js';

import { ViewBgImage } from '../views/bg_image.js';

import { ViewLogin } from '../views/login.js';
import { ViewGameSelect } from './game_select.js';

const main_page_dom = document.getElementById("mainapp-container");
const background_page_dom = document.getElementById("background-container");
const tool_page_dom = document.getElementById("toolapp-container");
const menu_bar_dom = document.getElementById("menu-bar-container");

export class Router {
    // Destroy methods
    static DestroyMain() {
        const currPageDestroy = State.get("current_main_page_destroy");
        if (currPageDestroy) {
            console.log(currPageDestroy);
            currPageDestroy();
        }
        main_page_dom.innerHTML = '';
    }

    static DestroyBackground() {
        const currPageDestroy = State.get("current_background_page_destroy");
        if (currPageDestroy) {
            currPageDestroy();
        }
        background_page_dom.innerHTML = '';
    }

    static DestroyTool() {
        const currPageDestroy = State.get("current_tool_page_destroy");
        if (currPageDestroy) {
            currPageDestroy();
        }
        tool_page_dom.innerHTML = '';
    }

    static DestroyMenuBar() {
        menu_bar_dom.innerHTML = '';
    }

    // Main Page Mathods
    static MainLogin() {
        const currPage = State.get("current_main_page");
        const pageId = ViewLogin.GetPageId();

        if (currPage === pageId ) {
            return true;
        }

        // Reqs are met?
        const reqsMet = ViewLogin.AreRequirementsMet();
        if (reqsMet===false) {
            return false;
        }

        // Destroy current page
        Router.DestroyMain();
        Router.DestroyTool();
        Router.DestroyMenuBar();

        // Build new page
        const pageDom = ViewLogin.Build();
        if (!pageDom) {
            return false;
        }

        // Register new page
        State.set("current_main_page", pageId);
        State.set("current_main_page_destroy", ViewLogin.Destroy);

        // Attach new page
        main_page_dom.appendChild(pageDom);
    }

    // Background
    static BgImage(imageFileName) {
        const currPage = State.get("current_background_page");
        const pageId = ViewBgImage.GetPageId();

        if (currPage === pageId ) {
            return true;
        }

        // Reqs are met?
        const reqsMet = ViewBgImage.AreRequirementsMet();
        if (reqsMet===false) {
            return false;
        }

        // Destroy current page
        Router.DestroyBackground();

        // Build new page
        const pageDom = ViewBgImage.Build(imageFileName);
        if (!pageDom) {
            return false;
        }

        // Register new page
        State.set("current_background_page", pageId);
        State.set("current_background_page_destroy", ViewBgImage.Destroy);

        // Attach new page
        background_page_dom.appendChild(pageDom);
    }

    // Menu Bar
}