// Librería: AJAX, jQuery

function insertarCuentas(cuentas, containerId) {
    console.log(cuentas);

    const container = document.getElementById(containerId);
    if (!container) return;

    if (cuentas.length === 0) {
        container.innerHTML = `
            <div class="col-md-12">
                <div class="alert alert-warning" role="alert">
                    No tienes cuentas registradas.
                </div>
            </div>
        `;
        return;
    }

    let html = '<div class="row">';
    cuentas.forEach(function(cuenta) {
        html += `
            <div class="col-md-4 mb-4">
                <div class="card account-card">
                    <div class="card-inner">
                        <div class="card-front" style="background-color: ${cuenta.colorIdentificacion}; color: black;">
                            <div class="card-body">
                                <h5 class="card-title">${cuenta.banco}</h5>
                                <h6 class="card-subtitle mb-2">Cuenta: ${cuenta.numeroCuenta}</h6>
                                <p class="card-text">Saldo: <strong>$${cuenta.saldoActual}</strong></p>
                                <p class="card-text">Últimos 4 dígitos: <strong>${cuenta.numeroCuenta.slice(-4)}</strong></p>
                            </div>
                            <br>
                            <div class="card-icon mb-3">
                                ${cuenta.afilacion === 'Visa' ? '<img src="static/img/Afilaciones_bancos/visa.png" alt="Visa" class="card-logo">' : ''}
                                ${cuenta.afilacion === 'MasterCard' ? '<img src="static/img/Afilaciones_bancos/mastercard.png" alt="MasterCard" class="card-logo">' : ''}
                                ${cuenta.afilacion === 'American Express' ? '<img src="static/img/Afilaciones_bancos/mastercard.png" alt="American Express" class="card-logo">' : ''}
                                ${!['Visa', 'MasterCard', 'American Express'].includes(cuenta.afilacion) ? '<i class="fas fa-credit-card fa-2x"></i>' : ''}
                            </div>
                        </div>
                        <div class="card-back" style="background-color: ${cuenta.colorIdentificacion}; color: black;">
                            <div class="card-body">
                                <h5 class="card-title">Detalles Adicionales</h5>
                                <p class="card-text">CVC: <strong>${cuenta.cvc}</strong></p>
                                <p class="card-text">Fecha Vencimiento: <strong>${new Date(cuenta.fechaVencimiento).toLocaleDateString('es-ES', { year: 'numeric', month: 'long' })}</strong></p>
                                <p class="card-text">Banco: <strong>${cuenta.banco}</strong></p>
                                <div class="card-icon">
                                    <i class="fas fa-lock fa-2x"></i>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });
    html += '</div><a class="text-center mb-4" id="ver-todas-cuentas">Actualizar</a>';
    container.innerHTML = html;
}

function insertarFuentesTransacciones(fuentes, containerId) {
    console.log(fuentes);

    const container = document.getElementById(containerId);
    if (!container) return;

    if (fuentes.length === 0) {
        container.innerHTML = `
        <li>No hay fuentes disponibles.</li>
        `;
        return;
    }

    fuentes.forEach(function(elemento) {
        container.innerHTML += `
            <li> ${elemento.fuente} - (${elemento.count})</li>
        `;  
    });
}


// Función para generar el HTML de ingresos
// Crear fila para ingreso
function crearFilaIngreso(ingreso) {
    return `<tr>
                <td>${ingreso.fecha}</td>
                <td>${ingreso.descripcion}</td>
                <td>${ingreso.cantidad}</td>
                <td>${ingreso.fuente}</td>
                <td><span class="badge badge-success">${ingreso.tipo}</span></td>
                <td>
                    <button class="btn btn-warning btn-sm" onclick="editTransaction(${ingreso.id})">Editar</button>
                    <button class="btn btn-danger btn-sm" onclick="deleteTransaction(${ingreso.id})">Eliminar</button>
                </td>
            </tr>`;
}
// Función para generar el HTML de egresos
// Crear fila para egreso
function crearFilasEgresoingreso(data) {
    return `<tr>
                <td>${data.fecha}</td>
                <td>${data.descripcion}</td>
                <td>${data.cantidad}</td>
                <td>${data.proposito}</td>


                $${data.tipo === 'Egreso' ? `<td><span class="badge badge-danger">${data.tipo}</span></td>` : ``}
                $${data.tipo === 'Ingreso' ? `<td><span class="badge badge-success">${data.tipo}</span></td>` : ``}

                <td>
                    <button class="btn btn-warning btn-sm" onclick="editTransaction(${data.id})">Editar</button>
                    <button class="btn btn-danger btn-sm" onclick="deleteTransaction(${data.id})">Eliminar</button>
                </td>
            </tr>`;
}

function crearFilaCuenta(cuenta) {
    return `<tr>
                <td>${cuenta.descripcion}</td>
                <td>$${cuenta.cantidad}</td>
                <td>${cuenta.fechaVencimiento}</td>
                <td>${cuenta.tipo}</td>
                <td>
                    <button class="btn btn-warning btn-sm" onclick="editAccount(${cuenta.id})">Editar</button>
                    <button class="btn btn-danger btn-sm" onclick="deleteAccount(${cuenta.id})">Eliminar</button>
                </td>
            </tr>`;
}


// Función para mostrar el menú desplegable de usuario

$(document).ready(function () {
    $(document).click(function (e) {
        if (!$(e.target).closest('.dropdown').length) {
            $('.dropdown-menu').removeClass('show'); // Oculta el dropdown si haces clic fuera de él
        }
    });
    $('#dropdownMenuButton').on('click', function (e) {
        e.stopPropagation(); // Evita que se cierre el menú cuando haces clic en el botón
        $(this).next('.dropdown-menu').toggleClass('show');
    });
    // Menu desplegable dropdownMenuCuentas
    $('#dropdownMenuCuentas').on('click', function (e) {
        e.stopPropagation(); // Evita que se cierre el menú cuando haces clic en el botón
        $(this).next('.dropdown-menu-deudas').toggleClass('show');
    });


    
});
// Función para desplegar la lista de cuentas
$(document).ready(function() {
    // Usa delegación de eventos para manejar el clic en el enlace
    $(document).on('click', '#ver-todas-cuentas', function(e) {
        e.preventDefault(); // Evita que el enlace navegue

        // Realiza la petición AJAX
        $.ajax({
            url: "/api/cuentas/",  // URL para la lista de cuentas
            method: "GET",
            success: function(response) {
                // Limpia la lista de cuentas existente
                $('#lista-cuentas').empty();
                
                // Itera sobre las cuentas y las añade al contenedor
                insertarCuentas(response.cuentas, 'lista-cuentas');
            },
            error: function(xhr) {
                console.error("Error al obtener cuentas: ", xhr.responseText);
            }
        });
    });
});

//Función refresh transacciones
$(document).ready(function() {
    $('#refrescar-transacciones').on('click', function(e) {
        e.preventDefault(); // Evita la acción por defecto del botón
        // Realiza la petición AJAX
        $.ajax({
            url: "/api/transacciones_mes/",  // URL para obtener las transacciones
            method: "GET",
            success: function(response) {
                console.log("Respuesta de transacciones: ", response);
                // Limpia la lista de transacciones existente
                $('#lista-transacciones').empty();
                $('#top_fuentes_ingresos').empty();
                $('#top_fuentes_egresos').empty();
                

            
                // Actualiza los datos en las tarjetas
                $('#total-ingresos').text('Total Ingresos: ' + response.total_ingresos);
                $('#total-egresos').text('Total Egresos: ' + response.total_egresos);
                
                // Inserta las fuentes de ingresos y egresos
                insertarFuentesTransacciones(response.top_fuentes_ingresos, 'top_fuentes_ingresos');
                insertarFuentesTransacciones(response.top_propositos_egresos, 'top_fuentes_egresos');
            
            },
            error: function(xhr) {
                console.error("Error al obtener transacciones: ", xhr.responseText);
            }
        });
    });
});

// Función para actualizar la tabla de cuentas
function actualizarTablaCuentas(data) {
    $('#tabla-cuentas tbody').empty();
    data.cuentas.forEach(function(cuenta) {
        $('#tabla-cuentas tbody').append(crearFilaCuenta(cuenta));
    });
}


// Actualizar la lista de transacciones al cargar la página
$(document).ready(function() {
    // Función para refrescar la tabla
    function refrescarTablas() {
        $.ajax({
            url: "/api/refrescar_tablas_transacciones/", // URL para refrescar la tabla
            method: "GET",
            success: function(response) {
                console.log("Respuesta de transacciones: ", response);
                actualizarTabla(response);
            },
            error: function(xhr) {
                console.error("Error al refrescar las tablas: ", xhr.responseText);
            }
        });
    }
    // Función para actualizar las tablas con los datos obtenidos
    function actualizarTabla(data) {
        $('#tabla-transacciones tbody').empty();

        data.forEach(function(elemento) {
            $('#tabla-transacciones tbody').append(crearFilasEgresoingreso(elemento));
        });
    }
    // Evento para refrescar información en la tabla
    $('#refrescar-tablas').on('click', function(e) {
        e.preventDefault();
        refrescarTablas();
    });
    // Evento para filtrar las transacciones
    $('.dropdown-item-transacciones').on('click', function(e) {
        e.preventDefault();
        var categoria = $(this).data('categoria');
        $.ajax({
            url: "/api/filtrar_transacciones/",
            method: "GET",
            data: { categoria: categoria },
            success: function(response) {
                actualizarTabla(response);
            },
            error: function(xhr) {
                console.error("Error al filtrar transacciones: ", xhr.responseText);
            }
        });
    });


    
    // Evento para ordenar las transacciones
    $('.sortable').on('click', function() {
        var key = $(this).find('i').data('key');
        var tipo = $(this).find('i').hasClass('asc') ? 'desc' : 'asc'; // Alternar tipo

        
        $.ajax({
            url: "/api/ordenar_transacciones/",
            method: "GET",
            data: { orden: key, tipo: tipo },
            success: function(response) {
                console.log("Respuesta de ordenar transacciones: ", response);
                actualizarTabla(response);
            },
            error: function(xhr) {
                console.error("Error al ordenar transacciones: ", xhr.responseText);
            }
        });
                // Aplicar la clase para el orden en el icono
                $(this).find('i').toggleClass('asc');
    });
});



// Actualizar la lista de deudas al cargar la página
$(document).ready(function() {

       // Event handler para filtrar cuentas
       $('.dropdown-item-deudas').on('click', function(e) {
        e.preventDefault();  // Evitar el comportamiento por defecto del enlace
        var estado = $(this).data('estado');  // Obtener el valor del estado seleccionado

        $.ajax({
            url: "/api/filtrar_deudas/",  // Ruta para filtrar cuentas
            method: "GET",
            data: { estado: estado },
            success: function(response) {
                actualizarTablaCuentas(response);  // Actualizar la tabla con los datos filtrados
            },
            error: function(xhr) {
                console.error("Error al filtrar cuentas: ", xhr.responseText);
            }
        });
    });

    // Event handler para refrescar cuentas
    $('#refrescar-cuentas').on('click', function(e) {
    e.preventDefault();
    // Realiza una llamada AJAX para refrescar todos los datos.
    $.ajax({
        url: "/api/refrescar_deudas/",  // Ruta para refrescar cuentas
        method: "GET",
        success: function(response) {
            console.log("Respuesta de refrescar cuentas: ", response);

            actualizarTablaCuentas(response);
        },
        error: function(xhr) {
            console.error("Error al refrescar cuentas: ", xhr.responseText);
        }
    });
});

   }
);
