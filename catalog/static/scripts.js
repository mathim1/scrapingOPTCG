document.addEventListener("DOMContentLoaded", function () {
    setupSearch();
    setupProductHoverEffect();
});

function setupSearch() {
    var searchBar = document.querySelector('.search-bar-container input');
    searchBar.addEventListener('input', function () {
        var searchTerm = searchBar.value.toLowerCase();
        filterCards(searchTerm);
    });
}

function filterCards(searchTerm) {
    var cards = document.querySelectorAll('.producto-card');

    cards.forEach(function (card) {
        var cardName = card.querySelector('.card-title').innerText.toLowerCase();
        card.style.display = cardName.includes(searchTerm) ? 'block' : 'none';
    });
}

function setupProductHoverEffect() {
    var productos = document.querySelectorAll('.tarjeta-con-efecto');

    productos.forEach(function (producto) {
        var cardBody = producto.querySelector('.card-body');
        var cardImage = producto.querySelector('.card-img-top');

        producto.addEventListener('mouseenter', function () {
            cardBody.classList.add('bg-darker'); // Añade la clase para el fondo más oscuro al card-body
            cardImage.classList.add('bg-light'); // Añade la clase para el fondo más claro al card-image
        });

        producto.addEventListener('mouseleave', function () {
            cardBody.classList.remove('bg-darker');
            cardImage.classList.remove('bg-light');
        });
    });
}

