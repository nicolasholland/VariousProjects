var canvas = document.getElementById("myCanvas");
var ctx = canvas.getContext("2d");
const width = canvas.width;
const height = canvas.height;

function ty(y) {
  return Math.abs(y - height);
}

function d2r(degrees) {
  var pi = Math.PI;
  return degrees * (pi / 180);
}

function angled_line(x, y, alpha, l) {
    ctx.moveTo(x, ty(y));
    ctx.lineTo(x + l * Math.cos(d2r(alpha)), ty(y + l * Math.sin(d2r(alpha))));
    ctx.stroke();
}

function c2x(c, alpha, l) {
  return c - (l * Math.cos(d2r(alpha))) / 2;
}

function c2y(c, alpha, l) {
  return c - (l * Math.sin(d2r(alpha))) / 2;
}

function module(x, y, alpha, l) {
  angled_line(c2x(x, alpha, l), c2y(y, alpha, l), alpha, l);
}

function table_base(th) {
    ctx.moveTo(width / 2, ty(0));
    ctx.lineTo(200, ty(th));
    ctx.stroke();
}

function get_total_mod_length() {
    var modptab = document.getElementById("t_modpertab").innerText;
    var modlen = document.getElementById("t_modlen").innerText;

    return modptab * modlen;
}

function draw() {
    var alpha = document.getElementById("t_tiltangle").innerText;
    var th = document.getElementById("t_tableheight").innerText;
    var l = get_total_mod_length();

    ctx.clearRect(0, 0, width, height);
    ctx.beginPath();
    table_base(th);
    module(200, th, alpha, l);
    ctx.closePath();
}

// Draw initial default module
ctx.beginPath();
table_base(70);
module(200, 70, 15, 100);
ctx.closePath();


