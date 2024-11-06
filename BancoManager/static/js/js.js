

// Función para mostrar el menú desplegable de usuario

$(document).ready(function () {
    $(document).click(function (e) {
        if (!$(e.target).closest('.dropdown').length) {
            $('.dropdown-menu').removeClass('show'); // Oculta el dropdown si haces clic fuera de él
        }
    });
    $('#filterMenu').on('click', function (e) {
        e.stopPropagation(); // Evita que se cierre el menú cuando haces clic en el botón
        $(this).next('.dropdown-menu').toggleClass('show');
    });
    
});
