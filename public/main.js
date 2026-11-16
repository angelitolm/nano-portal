// ===== HUD: reloj en vivo (la hora del visitante; el resto son datos de ejemplo) ======
var clock = document.querySelector('[data-clock]');
var sec = document.querySelector('[data-sec]');
var date = document.querySelector('[data-date]');
function pad(n) { return (n < 10 ? '0' : '') + n; }
function tick() {
  var d = new Date();
  clock.textContent = pad(d.getHours()) + ':' + pad(d.getMinutes());
  sec.textContent = ':' + pad(d.getSeconds());
  date.textContent = d.toLocaleDateString('es-ES', { weekday: 'long', day: 'numeric', month: 'short' }).replace(',', '').replace('.', '');
}
if (clock) { tick(); setInterval(tick, 1000); }

// ===== HUD: tarjetas que se dan la vuelta (como en la app: vuelven solas a los 15 s) ===
// Son <button aria-pressed>: Enter y Espacio funcionan solos. La cara oculta lleva aria-hidden.
document.querySelectorAll('[data-flip]').forEach(function (card) {
  var timer;
  var front = card.querySelector('.front'), back = card.querySelector('.back');
  function set(on) {
    clearTimeout(timer);
    card.setAttribute('aria-pressed', on);
    front.setAttribute('aria-hidden', on);
    back.setAttribute('aria-hidden', !on);
    if (on) timer = setTimeout(function () { set(false); }, 15000);
  }
  card.addEventListener('click', function () { set(card.getAttribute('aria-pressed') !== 'true'); });
});

// ===== Movimiento ===================================================================
// Sin JS, o con movimiento reducido, todo se ve desde el principio: los estados ocultos del CSS
// cuelgan de html.motion. Solo se anima transform y opacity.
var root = document.documentElement;
var motion = 'IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches;

var parallax = motion ? [].slice.call(document.querySelectorAll('[data-speed]')) : [];
var ticking = false;
function onScroll() {
  if (ticking) return;
  ticking = true;
  requestAnimationFrame(function () {
    var y = window.scrollY;
    root.classList.toggle('scrolled', y > 24);
    // ponytail: parallax solo mientras el hero puede verse.
    if (y < 1200) parallax.forEach(function (el) {
      el.style.transform = 'translate3d(0,' + (y * el.dataset.speed).toFixed(1) + 'px,0)';
    });
    ticking = false;
  });
}
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();

if (motion) {
  root.classList.add('motion');
  if (performance.now() < 1500) root.classList.add('enter');

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      io.unobserve(e.target);
      e.target.classList.add('in');
    });
  }, { rootMargin: '0px 0px -10% 0px', threshold: .12 });

  document.querySelectorAll('[data-stagger]').forEach(function (list) {
    [].forEach.call(list.children, function (c, i) { c.style.setProperty('--d', (i % 3) * 90 + 'ms'); io.observe(c); });
  });
  document.querySelectorAll('.rv, .hud-fig').forEach(function (el) { io.observe(el); });
}
