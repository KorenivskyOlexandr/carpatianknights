const bodyScrollLock = require('body-scroll-lock');
export const hamburgerToggle = () => {
    const hamburger = document.querySelector('.hamburger');
    const sideMenu = document.querySelector('.side-menu');
    const mainBlock = document.querySelector('.main');
    const headers_container = document.querySelector('.headers-container');

    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('open');
        sideMenu.classList.toggle('open');
        mainBlock.classList.toggle('main-rotate');
        document.body.classList.toggle('open-menu');

        ((sideMenu.classList.contains("open"))
            ? bodyScrollLock.disableBodyScroll(sideMenu)
            : bodyScrollLock.enableBodyScroll(sideMenu))
        try {
            headers_container.classList.toggle('close');
        } catch (e) {
        }

    });
}
