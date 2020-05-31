export const hamburgerToggle = () => {
   const hamburger = document.querySelector('.hamburger');
   const sideMenu = document.querySelector('.side-menu');
   hamburger.addEventListener('click', ()=> {
      hamburger.classList.toggle('open');
      sideMenu.classList.toggle('open');
   });
}
