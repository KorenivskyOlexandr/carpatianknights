// Plugins
import {hamburgerToggle} from "./custom/toggle-menu";
import { CountUp } from 'countup.js/dist/countUp';
import "bootstrap/dist/js/bootstrap.bundle";
import "waypoints/lib/noframework.waypoints"


document.addEventListener("DOMContentLoaded", () => {
    hamburgerToggle();
    let counter = new CountUp("counter1", 0, 15000, 0, 5, {
        useEasing: true,
        useGrouping: true,
        separator: ',',
        decimal: '.'
    });
    counter.start()
});


console.log("hello");

alert('hello');

import '../sass/main.scss';
// const waypoint = new Waypoint({
//     element: document.getElementById('waypoint1'),
//     handler: function (direction) {
//
//         if (direction === "up") {
//             counter.reset();
//         } else {
//             counter.start();
//         }
//
//     },
//     offset: '50%'
// });
