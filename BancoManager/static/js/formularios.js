$(document).ready(function() {
    // Manejar el envío del formulario
    function handleFormSubmit(formSelector, url) {
        $(formSelector).on('submit', function(e) {
            e.preventDefault(); // Prevenir comportamiento por defecto
            console.log('Formulario enviado', e);

            // Recolectar datos del formulario
            var formData = $(this).serialize();
            $.ajax({
                url: url,  // URL para agregar ingresos
                method: "POST",
                data: formData,
                success: function(response) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Ingreso agregado exitosamente',
                        showConfirmButton: false,
                        timer: 1500
                    });
                    // Limpiar el formulario
                    $(formSelector).trigger('reset');
                },
                error: function(xhr) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error al agregar ingreso',
                        text: xhr.responseText
                    });
                }
            });
        });
    }

    // Manejar la búsqueda de cuentas de manera dinámica
    function handleAccountSearch(inputSelector, resultSelector, searchUrl) {
        var debounceTimer;  // Variable para debounce

        $(inputSelector).on('input', function() {
            var query = $(this).val().trim();
            clearTimeout(debounceTimer);  // Limpiar el timer anterior

            if (query.length > 1) {
                debounceTimer = setTimeout(function() {
                    $.ajax({
                        url: searchUrl,  // Ruta que vas a usar para obtener cuentas
                        method: "GET",
                        data: { q: query },  // Envío de la consulta
                        success: function(data) {
                            showResults(data, resultSelector);
                        },
                        error: function(xhr) {
                            console.error("Error al obtener cuentas: ", xhr.responseText);
                        }
                    });
                }, 300);  // Delay de 300ms
            } else {
                $(resultSelector).hide();  // Ocultar la lista si el input está vacío
            }
        });
    }

    // Mostrar los resultados de la búsqueda
    function showResults(data, resultSelector) {
        var $resultList = $(resultSelector);
        $resultList.empty();  // Limpiar la lista anterior
        if (data.length > 0) {
            data.forEach(function(cuenta) {
                $resultList.append('<li class="list-group-item cuenta-item" data-id="' + cuenta.id + '">' + cuenta.nombre + '</li>');
            });
            $resultList.show();  // Mostrar la lista
        } else {
            $resultList.hide();  // Si no hay resultados oculta la lista
        }
    }

    // Manejar el clic en una cuenta de la lista
    function handleAccountSelection(resultSelector, inputSelector, hiddenInputSelector) {
        $(document).on('click', '.cuenta-item', function() {
            var cuentaNombre = $(this).text();
            var cuentaId = $(this).data('id');
            $(inputSelector).val(cuentaNombre);  // Establecer el nombre de la cuenta en el input visible
            $(hiddenInputSelector).val(cuentaId);  // Establecer el ID de la cuenta en el input oculto
            $(resultSelector).hide();  // Ocultar la lista
        });

        // Cerrar la lista si se hace clic fuera de ella
        $(document).on('click', function(e) {
            if (!$(e.target).closest(resultSelector).length && !$(e.target).is(inputSelector)) {
                $(resultSelector).hide();
            }
        });
    }

    // Manejar el clic en el botón "Ver todas las cuentas"
    function handleViewAllAccounts(buttonSelector, modalSelector, tableSelector, apiUrl) {
        $(buttonSelector).on('click', function() {
            $.ajax({
                url: apiUrl,  // URL para obtener todas las cuentas
                method: "GET",
                success: function(data) {
                    console.log("Informacion cuenta", data);

                    var table = $(tableSelector).DataTable();
                    // Mostrar
                    table.clear();
                    data.cuentas.forEach(function(cuenta) {
                        table.row.add([
                            cuenta.id,
                            cuenta.nombre,
                            cuenta.banco,
                            cuenta.numeroCuenta,
                            cuenta.tipoCuenta
                        ]).draw();
                    });
                    // Mostrar la ventana modal
                    $(modalSelector).modal('show');
                },
                error: function(xhr) {
                    console.error("Error al obtener cuentas: ", xhr.responseText);
                }
            });
        });
    }

    // Validando que funciones se van a a utilizar 
    var modelo_principal = $("#modelo_principal").val();


    if (modelo_principal == "Ingreso"){
        // Inicializar funciones - Formulario ingreso
             // Manejar el envío del formulario
        handleFormSubmit('#form-agregar-ingreso', '/crear_ingreso/');
            // Manejar la búsqueda de cuentas de manera dinámica
        handleAccountSearch('#cuenta', '#lista-cuentas', '/api/buscar_dinamica_cuentas/');
            // Manejar el clic en una cuenta de la lista
        handleAccountSelection('#lista-cuentas', '#cuenta', '#cuenta_id');
            // Manejar el clic en el botón "Ver todas las cuentas"
        handleViewAllAccounts('#ver-todas-cuentas', '#modalCuentas', '#tabla-cuentas', '/api/cuentas/');
    }else if(modelo_principal == "Egreso"){
        // Inicializar funciones - Formulario egreso
        // Manejar el envío del formulario
        handleFormSubmit('#form-agregar-egreso', '/crear_egreso/');
        // Manejar la búsqueda de cuentas de manera dinámica
        handleAccountSearch('#cuenta', '#lista-cuentas', '/api/buscar_dinamica_cuentas/');
        // Manejar el clic en una cuenta de la lista
        handleAccountSelection('#lista-cuentas', '#cuenta', '#cuenta_id');
        // Manejar el clic en el botón "Ver todas las cuentas"
        handleViewAllAccounts('#ver-todas-cuentas', '#modalCuentas', '#tabla-cuentas', '/api/cuentas/');
    }
});