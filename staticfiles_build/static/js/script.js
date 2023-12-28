const mainElement = document.querySelector("main");
const navItems = document.querySelector("#navItems");
const chev1 = document.querySelector("#chev-1");
const chev2 = document.querySelector("#chev-2");
const sideBar = document.querySelector("#sideBar");
const toTop = document.querySelector("#toTop");

mainElement.addEventListener("click", function (event) {
  if (!navItems.contains(event.target)) {
    navItems.classList.remove("move-left");
    navItems.classList.add("move-right");
  }
});

document.querySelector("#hamburger").addEventListener("click", function () {
  navItems.classList.toggle("move-left");
  navItems.classList.toggle("move-right");
});

window.addEventListener("scroll", function () {
  if (window.scrollY > 100) {
    toTop.classList.add("active");
  } else {
    toTop.classList.remove("active");
  }
});

function closeSideBar() {
  chev1.classList.toggle("rotator-initial-1");
  chev2.classList.toggle("rotator-initial-2");
  chev1.classList.toggle("rotator-1");
  chev2.classList.toggle("rotator-2");
  sideBar.classList.toggle("close-navbar");
  sideBar.classList.toggle("open-navbar");
}

function barcodePayment() {
  document.querySelector("#barcode-payment").classList.add("active");
  document.querySelector("#payment-slider").classList.add("active");
}
