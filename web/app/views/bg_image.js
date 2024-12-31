export class ViewBgImage {
    static AreRequirementsMet() {
        return true
    }

    static GetPageId() {
        return "bg_image"
    }

    static Build(imageFileName) {
        const reqs = ViewBgImage.AreRequirementsMet();

        if (reqs === false) {
            return null;
        }

        if (!imageFileName) {
            imageFileName = "bg1.webp";
        }

        // Build page dom
        const main_dom = document.createElement('div');
        main_dom.classList.add('positioner-center-vh');
        
        const img_container = document.createElement('div');
        img_container.classList.add('image-fill');
        main_dom.appendChild(img_container);

        const img_ele = document.createElement('img');
        img_ele.src = 'media/images/' + imageFileName;
        img_container.appendChild(img_ele);

        return main_dom
    }

    static Destroy() {
        return true;
    }
}