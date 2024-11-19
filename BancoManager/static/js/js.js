// Librería: AJAX, jQuery

// Objeto global para almacenar las gráficas
var charts = {};
function cargarDatosinicio() {
    // Cargar grafica cuentas
    $.ajax({
        url: '/api/obtener_datos_graficables_ingreso_egreso/',
        method: 'GET',
        success: function(response) {
            console.log("Respuesta de obtener-datos-graficables-ingreso-egreso: ", response);
            // Configurar gráfica de ingresos
            configurarGrafica({
                canvasId: 'grafica-ingresos',
                tipoGrafica: 'bar',
                etiquetas: response.etiquetas_meses,
                datos: response.ingreso_data_graficable,
                label: 'Ingresos',
                backgroundColor: 'rgba(75, 192, 192, 0.5)',
                opciones: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
            // Configurar gráfica de egresos
            configurarGrafica({
                canvasId: 'grafica-egresos',
                tipoGrafica: 'bar',
                etiquetas: response.etiquetas_meses,
                datos: response.egreso_data_graficable,
                label: 'Egresos',
                backgroundColor: 'rgba(255, 99, 132, 0.5)',
                opciones: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }
    });
    // Cargar el listado de cuentas
    $.ajax({
        url: '/api/informacion_cuenta_bancaria/',
        method: 'GET',
        success: function(response) {
            console.log("Respuesta de informacion-cuenta-bancaria: ", response);
            insertarCuentas(response.cuentas, 'lista-cuentas');
        }
    });    
    // Refresh tables on page load
    refrescarTablas();
    // Esperar hasta que obtenga las categorías de transacciones
    UtilidadesDropdownmenu('#dropdownMenuButton', '.dropdown-menu', '#refrescar-transacciones');
    // Insert accounts on page load
    obtenerCategoriaTransacciones('/api/obtener_categoria_ingreso_egreso/', 'categoriaDropdown', 'select');

}
// Función para limpiar el HTML de un elemento
function limpiarHTML(target, destroy = false) {
    // Validar si existe el target
    if ($(target).length) {
        $(target).empty();
        if (destroy) {
            $(target).remove();
        }
    }
}
// Función para configurar las tablas
function configurarTabla({ tablaId, modelo, opciones = {}, data={}, campos={}, categoria_filter='', numeroData=10, totalesdraw=''} ) {
    // Función para actualizar los totales
    function actualizarTotales(table) {
        var totalEgresos = 0;
        var totalIngresos = 0;
        table.rows({ search: 'applied' }).every(function(rowIdx, tableLoop, rowLoop) {
            var data = this.data();
            var cantidad = parseFloat(data[1]); // Asumiendo que la columna 2 es "cantidad"
            var tipo = data[4]; // Asumiendo que la columna 1 es "tipo" (egreso/ingreso)
            if (tipo.toLowerCase() === 'egreso') {
                totalEgresos += cantidad;
            } else if (tipo.toLowerCase() === 'ingreso') {
                totalIngresos += cantidad;
            }
        });
        $('#totalEgresos').text('Total Egresos: ' + totalEgresos.toFixed(2));
        $('#totalIngresos').text('Total Ingresos: ' + totalIngresos.toFixed(2));
    }
    // Eliminar los widgets de buscar y filtrar
    limpiarHTML(`#${tablaId}_length`, true);
    limpiarHTML(`#${tablaId}_filter`, true);
    limpiarHTML(`#${tablaId}_info`, true);
    limpiarHTML(`#${tablaId}_paginate`, true);
    // Limpiar la tabla antes de llenarla
    $(`#${tablaId}`).DataTable().clear().destroy();
    // Llenar la tabla con los datos
    data.forEach(function(item) {
        var fila = '<tr>';
        campos.forEach(function(campo) {
            fila += `<td>${item[campo]}</td>`;
        });
        fila += `<td> <button class="btn btn-warning btn-sm editbutton" id="btnEditar${modelo}" data-id="${item.id}">Editar</button>` +
            `<button class="btn btn-danger btn-sm deletebutton" id="btnEliminar${modelo}" data-id="${item.id}">Eliminar</button> </td></tr>`;
        $(`#${tablaId} tbody`).append(fila);
    });
    // Inicializar DataTables
    $(`#${tablaId}`).DataTable(Object.assign({
        order: [[2, 'desc']],
        paging: true,
        searching: true,
        lengthChange: true,
        pageLength: 10,
    }, opciones));
    var table_filter = $(`#${tablaId}`).DataTable();
    // Categoria filter
    if (categoria_filter !== '') {
        // Filtrar por categoría
        $('#categoriaDropdown').on('change', function() {
            // Remplazar los espacios en blanco al final y al inicio
            var selectedCategory = $(this).val().trim();
            if (selectedCategory) {
                var escapedCategory = selectedCategory.replace(/[()]/g, '\\$&');
                console.log("Selected category: ", escapedCategory);
                table_filter.column(3).search('^' + escapedCategory + '$', true, false).draw();
            } else {
                console.log("No category selected");
                table_filter.column(3).search('').draw();
            }
            actualizarTotales(table_filter);
        });
    } 
    // Actualizar totales al dibujar la tabla
    table_filter.on('draw', function () {
        actualizarTotales(table_filter);
    });
    // Inicializar los totales al cargar la tabla
    actualizarTotales(table_filter);
}    
// Función para configurar las gráficas
function configurarGrafica({ canvasId, tipoGrafica = 'bar', etiquetas, datos, label, backgroundColor = 'rgba(75, 192, 192, 0.5)', opciones = {} }) {
    // Destruir la gráfica si ya existe
    if (charts[canvasId]) {
        charts[canvasId].destroy();
    }

    var ctx = document.getElementById(canvasId).getContext('2d');
    charts[canvasId] = new Chart(ctx, {
        type: tipoGrafica,
        data: {
            labels: etiquetas,
            datasets: [{
                label: label,
                data: datos,
                backgroundColor: backgroundColor
            }]
        },
        options: Object.assign({
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }, opciones)
    });
}
// Function to insert accounts into the container
function insertarCuentas(cuentas, containerId) {
    try {
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
                            <div class="card-front" style="background-color: ${cuenta.colorIdentificacion}; ${cuenta.colorIdentificacion === '#000000' ? 'color: white;' : 'color: black;'}">   
                                <div class="card-body">
                                    <h5 class="card-title">${cuenta.nombre} - ${cuenta.tipoCuenta}</h5> 
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
    } catch (error) {
        console.error("Error in insertarCuentas: ", error);
    }
}
// Function to insert transaction sources into the container
function insertarFuentesTransacciones(fuentes, containerId) {
    try {
        console.log(fuentes);
        const container = document.getElementById(containerId);
        if (!container) return;

        if (fuentes.length === 0) {
            container.innerHTML = `<li>No hay fuentes disponibles.</li>`;
            return;
        }

        fuentes.forEach(function(elemento) {
            container.innerHTML += `<li> ${elemento.fuente} - (${elemento.count})</li>`;
        });
    } catch (error) {
        console.error("Error in insertarFuentesTransacciones: ", error);
    }
}
// Function to create income row
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
// Function to create expense row
function crearFilasEgresoingreso(data) {
    return `<tr>
                <td>${data.fecha}</td>
                <td>${data.descripcion}</td>
                <td>${data.cantidad}</td>
                <td>${data.proposito}</td>
                ${data.tipo === 'Egreso' ? `<td><span class="badge badge-danger">${data.tipo}</span></td>` : ''}
                ${data.tipo === 'Ingreso' ? `<td><span class="badge badge-success">${data.tipo}</span></td>` : ''}
                <td>
                    <button class="btn btn-warning btn-sm" onclick="editTransaction(${data.id})">Editar</button>
                    <button class="btn btn-danger btn-sm" onclick="deleteTransaction(${data.id})">Eliminar</button>
                </td>
            </tr>`;
}
// Function to create account row
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
// Function to update account table
function actualizarTablaCuentas(data) {
    try {
        $('#tabla-cuentas tbody').empty();
        data.cuentas.forEach(function(cuenta) {
            $('#tabla-cuentas tbody').append(crearFilaCuenta(cuenta));
        });
    } catch (error) {
        console.error("Error in actualizarTablaCuentas: ", error);
    }
}
// Function to update transaction table
function actualizarTabla(data, target) {
    try {
        $(`#${target} tbody`).empty();
        data.forEach(function(elemento) {
            $(`#${target}  tbody`).append(crearFilasEgresoingreso(elemento));
        });
    } catch (error) {
        console.error("Error in actualizarTabla: ", error);
    }
}
// Function to refresh tables
function refrescarTablas() {
    try {
        $.ajax({
            url: "/api/refrescar_tablas_transacciones/",
            method: "GET",
            success: function(response) {
                console.log("Respuesta de transacciones: refrescarTablas", response);
            // Llenar la lista de cuentas
            configurarTabla({
                tablaId: `tablatransacciones`,
                modelo: '',            
                data: response,
                campos: ['descripcion', 'cantidad', 'fecha', 'proposito','tipo'],
                categoria_filter: 'categoriaDropdown',
                numeroData: 20
            });

            },
            error: function(xhr) {
                console.error("Error al refrescar las tablas: ", xhr.responseText);
            }
        });
    } catch (error) {
        console.error("Error in refrescarTablas: ", error);
    }
}

function filtrarTransacciones(url, target, categoria) {
    try {
        $.ajax({
            url: url,
            method: "GET",
            data: { categoria: categoria },
            success: function(response) {
                console.log("Respuesta de filtrar-transacciones: ", response);
                actualizarTabla(response, "tabla-transacciones");
            },
            error: function(xhr) {
                console.error("Error al filtrar transacciones: ", xhr.responseText);
            }
        });
    } catch (error) {
        console.error("Error in filtrar-transacciones: ", error);
    }
}

function obtenerCategoriaTransacciones(url, target, tipo="drownmenu") {
    try {
        $.ajax({
            url: url,
            method: "GET",
            success: function(response) {
                console.log("Respuesta de obtener-Categoria-Transacciones: ", response);
                $('#' + target).empty();
                if (tipo === "drownmenu") {
                    response.categorias.forEach(function(categoria) {
                        $('#' + target).append(`<li><a class="dropdown-item dropdown-item-transacciones" href="#" data-categoria="${categoria}">${categoria}</a></li>`);
                    });
                } else if (tipo === "select") {
                    $('#' + target).append(`<option value="">Selecciona una categoría</option>`);
                    response.categorias.forEach(function(categoria) {
                        $('#' + target).append(`<option value="${categoria}">${categoria}</option>`);
                    });
                }
            },
            error: function(xhr) {
                console.error("Error al obtener categoría de transacciones: ", xhr.responseText);
            }
        });
    } catch (error) {
        console.error("Error in obtenerCategoriaTransacciones: ", error);
    }

    // Filter transactions


}

function obtenerIngreEgresossosmes(url, targetIngresos) {
    try {
        $.ajax({
            url: url,
            method: "GET",
            success: function(response) {
                console.log("Obteniendo registros:", response);
                $('#lista-ingresos').empty();
                $('#total-ingresos').text('Total Ingresos: ' + response.total_ingresos);
                response.ingresos.forEach(function(ingreso) {
                    $('#lista-ingresos').append(crearFilaIngreso(ingreso));
                });
            },
            error: function(xhr) {
                console.error("Error al obtener ingresos - egreso: ", xhr.responseText);
            }
        });
    } catch (error) {
        console.error("Error in refrescar-transacciones: ", error);
    }
}

// F
function obtenerTransaccionesmes(url, targetIngresos, targetEgresos, origen="") {
    try {
        $.ajax({
            url: url,
            method: "GET",
            success: function(response) {
                console.log("Respuesta de transacciones FUCTION: " + origen, response);
                $('#lista-transacciones').empty();
                $('#top_fuentes_ingresos').empty();
                $('#top_fuentes_egresos').empty();
                $('#total-ingresos').text('Total Ingresos: ' + response.total_ingresos);
                $('#total-egresos').text('Total Egresos: ' + response.total_egresos);
                insertarFuentesTransacciones(response.top_fuentes_ingresos, targetIngresos);
                insertarFuentesTransacciones(response.top_propositos_egresos, targetEgresos);
            },
            error: function(xhr) {
                console.error("Error al obtener transacciones: ", xhr.responseText);
            }
        });
    } catch (error) {
        console.error("Error in refrescar-transacciones: ", error);
    }
}

function UtilidadesDropdownmenu(targetDropwmenu, uldropdownMenu, refreshTable="",  buttonDropmenu="", dropdownmenu="",  apiUrl="", dataKey="", updateFunction="") {
    console.log("Utilidades-Drop-downmenu");
    // Hide dropdown menu when clicking outside
    $(document).click(function (e) {
        if (!$(e.target).closest('.dropdown').length) {
            $(uldropdownMenu).removeClass('show');
        }
    });
    // Toggle dropdown menu
    $(targetDropwmenu).on('click', function (e) {
        e.stopPropagation();
        $(this).next(uldropdownMenu).toggleClass('show');
    });


}
    // Dropdown menu
    // Function to handle dropdown menu
// Document ready functions
$(document).ready(function () {
    cargarDatosinicio() // Load data on page load
    // Refresh transactions
    $('#refrescar-tablas').on('click', function(e) {
        console.log("Refrescar transacciones");
        e.preventDefault();
        obtenerTransaccionesmes('api/transacciones_mes/', 'top_fuentes_ingresos', 'top_fuentes_egresos', "Resfresh");
    });

});
