// JS_HOME.js
// Objeto global para almacenar las gráficas
var charts = {};
// Inicializar el cuadro de carga
const cargaIngresos = cuadroCarga('#cuadroCargaIngresos');
// Obtener el token CSRF desde del input oculto en el HTML body 
// <input type="hidden" name="csrfmiddlewaretoken" value="p07Eb4EnxPEdHIlgSAUwpSOTh1rVfyGkxQPeNk3wBJPNdAyqKyqLnopRWd0bAyNJ">
var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
// Configurar jQuery para incluir el token CSRF en todas las solicitudes AJAX
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
        }
    }
});
// Función para editar un modelo
window.editarModelo = function(modelo, id) {
    handleFormLoad(null, `/api/editar_${modelo.toLowerCase()}/` + id + '/', `#insert-form-editar-${modelo.toLowerCase()}`, `#modalEditar${modelo}`);
}

// Función para crear el cuadro de carga
function cuadroCarga(divID) {
    const cuadroCarga = ` 
    <div class="loader">
        <div class="bill">
            <div class="bill-border"></div>
            <div class="dollar-sign">$</div>
        </div>
        <p class="loading-text">Cargando...</p>
    </div>`;
    $(divID).html(cuadroCarga);

    const loadingText = $(divID).find('.loading-text');
    const text = "Cargando...";
    let index = 0;

    function showText() {
        if (index < text.length) {
            loadingText.text(text.substring(0, index + 1));
            index++;
            setTimeout(showText, 500); // Tiempo entre cada letra
        }
    }

    function iniciarAnimacionTexto() {
        index = 0;
        loadingText.text('');
        showText();
    }

    function finalizarAnimacionTexto() {
        loadingText.text('¡Listo!');
    }

    function mostrarCuadroCarga() {
        $(divID).find('.loader').fadeIn();
        iniciarAnimacionTexto();
    }

    function ocultarCuadroCarga() {
        $(divID).find('.loader').fadeOut();
        finalizarAnimacionTexto();
    }

    return {
        mostrar: mostrarCuadroCarga,
        ocultar: ocultarCuadroCarga
    };
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

function configurarTabla({ tablaId, modelo, opciones = {}, data={}, campos={} } ) {
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
}
            

function limpiarHTML(target, destroy = false) {
    // Validar si existe el target
    if ($(target).length) {
        $(target).empty();
        if (destroy) {
            $(target).remove();
        }
    }
}

function generarListadocuentas(url, targetSelector) {
    $.ajax({
        url: url,
        method: 'GET',
        success: function(data) {
            // Seleccionar el elemento objetivo
            const targetElement = document.querySelector(targetSelector);
            if (!targetElement) {
                console.error('Elemento objetivo no encontrado:', targetSelector);
                return;
            }
            const cuentaSelect = $('#cuenta');
            cuentaSelect.empty(); // Limpiar las opciones existentes
            cuentaSelect.append('<option selected>Selecciona una cuenta...</option>');
            data.cuentas.forEach(function(cuenta) {
                cuentaSelect.append(`<option value="${cuenta.id}">${cuenta.nombre}</option>`);
            });
        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
        }
    });
}

function insertarRegistroRapido(csrfToken, targetSelector, modelo, cantidad = '', fuente =  ['Salario', 'Venta', 'Préstamo', 'Otro'], cuenta = '') {
    // Validar eliminar todo el contenido que exista en el targetSelector
    limpiarHTML(targetSelector);
    // Seleccionar el elemento objetivo
    const targetElement = document.querySelector(targetSelector);
    if (!targetElement) {
        console.error('Elemento objetivo no encontrado:', targetSelector);
        return;
    }
    // Crear el div row
    const div_row = document.createElement('div');
    div_row.className = 'row';
    targetElement.appendChild(div_row);
    // Crear el div col
    const div_col = document.createElement('div');
    div_col.className = 'col';
    div_row.appendChild(div_col);
    // Crear el h2 con el titulo
    const h2 = document.createElement('h2');
    h2.textContent = `Agregar ${modelo} Rápido`;
    div_col.appendChild(h2);
    // Crear el formulario
    const form = document.createElement('form');
    form.id = `formAgregarRapido${modelo}`;
    div_col.appendChild(form);
    // Generar el token CSRF y añadirlo al formulario
    const csrf = document.createElement('input');
    csrf.type = 'hidden';
    csrf.name = 'csrfmiddlewaretoken';
    csrf.value = csrfToken;
    form.appendChild(csrf);
    // Crear el div form-group
    const div_form_group = document.createElement('div');
    div_form_group.className = 'input-group mb-3';
    form.appendChild(div_form_group);
    // Crear el label para cantidad
    const label_cantidad = document.createElement('input');
    label_cantidad.htmlFor = 'cantidad';
    label_cantidad.textContent = 'Cantidad:';
    label_cantidad.className = 'form-control';
    label_cantidad.id = 'cantidad';
    label_cantidad.name = 'cantidad';
    label_cantidad.type = 'number';
    label_cantidad.value = cantidad;
    label_cantidad.required = true;
    div_form_group.appendChild(label_cantidad);
    // Crear el select de fuente
    const fuenteSelect = document.createElement('select');
    fuenteSelect.className = 'custom-select';
    fuenteSelect.id = 'fuente';
    fuenteSelect.name = 'fuente';
    fuenteSelect.required = true;
    const fuentes = fuente;
    fuentes.forEach(fuenteOption => {
        const option = document.createElement('option');
        option.value = fuenteOption;
        option.text = fuenteOption;
        if (fuenteOption === fuente) {
            option.selected = true;
        }
        fuenteSelect.appendChild(option);
    });
    div_form_group.appendChild(fuenteSelect);
    // Crear el select de cuenta
    const cuentaSelect = document.createElement('select');
    cuentaSelect.className = 'custom-select';
    cuentaSelect.id = 'cuenta';
    cuentaSelect.name = 'cuenta';
    cuentaSelect.required = true;
    div_form_group.appendChild(cuentaSelect);
    // El div # input-group-append
    const div_input_group_append = document.createElement('div');
    div_input_group_append.className = 'input-group-append';
    div_form_group.appendChild(div_input_group_append);

    // Crear el botón de submit
    const submitButton = document.createElement('button');
    submitButton.className = 'btn btn-success';
    submitButton.type = 'submit';
    submitButton.textContent = 'Agregar';
    div_input_group_append.appendChild(submitButton);
    // Funciones de ayuda
    generarListadocuentas(`/api/informacion_${modelo.toLowerCase()}/`, '#cuenta');
    // Enviar el formulario
    handleFormSubmit(`#formAgregarRapido${modelo}`, `/api/crear_rapido_${modelo.toLowerCase()}/`, 'POST', modelo);
}
function cargarDatosModeloIngresosorEgresos(modelo, data) {
    // Actualizar el total
    $(`#total-${modelo.toLowerCase()}`).text('$' + data[`total_${modelo.toLowerCase()}`]);
    // Verifica si existen datos recientes
    if (data[`${modelo.toLowerCase()}_recientes`].length > 0) {
        data[`${modelo.toLowerCase()}_recientes`].forEach(function(item) {
            $(`#lista_${modelo.toLowerCase()}_recientes`).append('<li class="list-group-item">' + item.descripcion + ': $' + item.cantidad + ' - ' + item.fecha + '</li>');
        });
    } else {
        $('#no_data_message').show();  // Mostrar mensaje de sin datos
    }

    // Generar el listado de opciones cuentas
    const cuentaSelect = $('#cuenta');
    cuentaSelect.empty(); // Limpiar las opciones existentes
    cuentaSelect.append('<option selected>Selecciona una cuenta...</option>');
    data.cuentas.forEach(function(cuenta) {
        cuentaSelect.append(`<option value="${cuenta.id}">${cuenta.nombre}</option>`);
    });

    var mes_lista = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
    
    // Configura la gráfica de datos
    configurarGrafica({
        canvasId: `comparativaMensual`,
        tipoGrafica: 'bar',
        etiquetas: mes_lista,
        datos: data[`${modelo.toLowerCase()}_graficables`],
        label: `${modelo} por Mes`,
        backgroundColor: 'rgba(75, 192, 192, 0.5)'
    });
    // Configura la gráfica de datos por categoría
    configurarGrafica({
        canvasId: `${modelo.toLowerCase()}PorCategoria`,
        tipoGrafica: 'doughnut',
        etiquetas: data[`${modelo.toLowerCase()}_por_categoria_graficables`].map(item => item.fuente),
        datos: data[`${modelo.toLowerCase()}_por_categoria_graficables`].map(item => item.total),
        label: `${modelo} por Categoría`,
        backgroundColor: data[`${modelo.toLowerCase()}_por_categoria_graficables`].map(item => item.color)
    });
    // Eliminar los widgets de buscar y filtrar         charts[canvasId].destroy();
    limpiarHTML(`#tabla${modelo}_length`, true);
    limpiarHTML(`#tabla${modelo}_filter`, true);            
    limpiarHTML(`#tabla${modelo}_info`, true);
    limpiarHTML(`#tabla${modelo}_paginate`, true);

    // Limpiar la tabla antes de llenarla
    $(`#tabla${modelo}`).DataTable().clear().destroy();
    // Llenar la tabla con los datos
    data[`todos_${modelo.toLowerCase()}`].forEach(function(item) {
        $(`#tabla${modelo} tbody`).append(
            '<tr>' +
            '<td>' + item.descripcion + '</td>' +
            '<td>' + item.cantidad + '</td>' +
            '<td>' + item.fecha + '</td>' +
            '<td>' + item.fuente + '</td>' +
            '<td>' + item.cuenta + '</td>' +
            '<td> <button class="btn btn-warning btn-sm editbutton" id="btnEditar' + modelo + '" data-id="'+item.id+'">Editar</button>' +
            '<button class="btn btn-danger btn-sm deletebutton" id="btnEliminar' + modelo + '" data-id="'+item.id+'">Eliminar</button> </td>' +
            '</tr>'
        );
    });

    // Inicializar DataTables
    $(`#tabla${modelo}`).DataTable({
        order: [[2, 'desc']],
        paging: true,
        searching: true,
        lengthChange: true,
        pageLength: 10,
        language: {
            "url": "/static/js/i18n/es-ES.json"
        }
    });
}

function cargarDatosModeloCuentasBancarias(modelo, data) {
    console.log('Datos de cuentas bancarias cargados: Funcion lv 2' );
    console.log('Datos de cuentas bancarias cargados: ', data.total_cuenta_bancaria);
    // Obtener el csrfToken
    console.log('csrfToken: ', csrfToken);
    // Actualizar el total
    $(`#total-cuenta_bancaria`).text('$' + data.total_cuenta_bancaria);
    // Verifica si existen datos recientes
    if (data[`${modelo.toLowerCase()}_recientes`].length > 0) {
        data[`${modelo.toLowerCase()}_recientes`].forEach(function(item) {
            $(`#lista_${modelo.toLowerCase()}_recientes`).append('<li class="list-group-item">' + item.descripcion + ': $' + item.cantidad + ' - ' + item.fecha + '</li>');
        });
    } else {
        $('#no_data_message').show();  // Mostrar mensaje de sin datos
    }
    // Actualizar el resumen rápido
    $('#resumen-rapido').text(`${data.cuentas.length} cuentas, ${data.tarjetas_credito.length} tarjeta(s) de crédito, ${data.prestamos.length} préstamo(s) activos.`);
    // Llenar la lista de cuentas
    configurarTabla({
        tablaId: `tabla${modelo}`,
        modelo: modelo,            
        data: data.cuentas,
        campos: ['nombre', 'saldoActual', 'banco', 'tipoCuenta']
    });
    var mes_lista = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
    // Configurar la gráfica comparativa
    configurarGrafica({
        canvasId: 'graficaTipoCuenta',
        tipoGrafica: 'pie',
        etiquetas: data.cuentas.map(cuenta => cuenta.banco),
        datos: data.cuentas.map(cuenta => cuenta.saldoActual),
        label: 'Distribución de Saldos por Tipo de Cuenta',
        backgroundColor: data.cuentas.map(cuenta => cuenta.colorIdentificacion)
    });    
    // Configura la gráfica de datos
    configurarGrafica({
        canvasId: `comparativaMensual`,
        tipoGrafica: 'bar',
        etiquetas: mes_lista,
        datos: data[`${modelo.toLowerCase()}_graficables`],
        label: `${modelo} por Mes`,
        backgroundColor: 'rgba(75, 192, 192, 0.5)'
    });
    // Configura la gráfica distribución de tipos de cuenta
    configurarGrafica({
        canvasId: 'distribucionTipos',
        tipoGrafica: 'doughnut',
        etiquetas: data.cuentas.map(cuenta => cuenta.banco),
        datos: data.cuentas.map(cuenta => cuenta.saldoActual),
        label: 'Distribución de Saldos por Tipo de Cuenta',
        backgroundColor: data.cuentas.map(cuenta => cuenta.colorIdentificacion)
    });
    // Cargar el formulario de agregar ingreso
    insertarRegistroRapido(csrfToken, '#insertar_form_ingreso_rapido', 'Ingreso');
    

}
// Función para cargar datos de un modelo
function cargarDatosModelo(modelo) {
    const cargaModelo = cuadroCarga(`#cuadroCarga${modelo}`);
    $.ajax({
        url: `/api/informacion_${modelo.toLowerCase()}/`,
        type: 'GET',
        success: function(data) {
            console.log(`Datos de ${modelo} cargados: `, data);
            // Validar que modelo es para cargar los datos
            if (modelo === 'Ingreso' || modelo === 'Egreso') {
                cargarDatosModeloIngresosorEgresos(modelo, data);
            } else if (modelo === 'Cuenta_bancaria') {
                console.log('Datos de cuentas bancarias cargados: Funcion' );
                cargarDatosModeloCuentasBancarias(modelo, data);
            }
        },
        error: function(xhr, status, error) {
            console.error(`Error cargando datos de ${modelo}: `, error);
            alert(`Ocurrió un error al cargar los datos de ${modelo}.`);
        },
        complete: function() {
            cargaModelo.ocultar(); // Ocultar el cuadro de carga
        }
    });
    initializeEditButtons(modelo);
    initializeDeleteButtons(modelo);
}
// Función para buscar y filtrar datos de un modelo
function buscarModelo(modelo) {
    var query = $(`#buscar${modelo}`).val();
    var fechaDesde = $(`#rangoFechaDesde${modelo}`).val();
    var fechaHasta = $(`#rangoFechaHasta${modelo}`).val();

    const cargaModelo = cuadroCarga(`#cuadroCarga${modelo}`);
    $.ajax({
        url: `/api/buscar_dinamica_${modelo.toLowerCase()}/`,
        method: 'GET',
        data: {
            query: query,
            fecha_desde: fechaDesde,
            fecha_hasta: fechaHasta
        },
        success: function(data) {
            console.log(`${modelo} filtrados: `, data);

            $(`#tabla${modelo}`).DataTable().clear().destroy();
            if (data[modelo.toLowerCase()].length > 0) {
                data[modelo.toLowerCase()].forEach(function(item) {
                    $(`#tabla${modelo} tbody`).append(
                        '<tr>' +
                        '<td>' + item.descripcion + '</td>' +
                        '<td>' + item.cantidad + '</td>' +
                        '<td>' + item.fecha + '</td>' +
                        '<td>' + item.fuente + '</td>' +
                        '<td>' + item.cuenta__nombre + '</td>' +
                        '<td> <button class="btn btn-warning btn-sm editbutton" id="btnEditar' + modelo + '" data-id="'+item.id+'">Editar</button>' +
                        '<button class="btn btn-danger btn-sm deletebutton" id="btnEliminar' + modelo + '" data-id="'+item.id+'">Eliminar</button> </td>' +
                        '</tr>'
                    );
                });
            } else {
                $(`#tabla${modelo} tbody`).append('<tr><td colspan="5">No se encontraron ' + modelo.toLowerCase() + '.</td></tr>');
            }

            // Inicializar DataTables
            $(`#tabla${modelo}`).DataTable({
                order: [[2, 'desc']],
                paging: true,
                searching: true,
                lengthChange: true,
                pageLength: 10,
                language: {
                    url: '//cdn.datatables.net/plug-ins/1.11.5/i18n/es-ES.json'
                }
            });
        },
        error: function(xhr, status, error) {
            console.error(`Error buscando ${modelo}: `, error);
            alert(`Ocurrió un error al buscar los ${modelo.toLowerCase()}.`);
        },
        complete: function() {
            cargaModelo.ocultar(); // Ocultar el cuadro de carga
        }
    });
}
// Función para manejar la carga del formulario con botón
function handleFormLoad(buttonSelector, url, targetSelector, modalSelector) {
    $(buttonSelector).on('click', function(e) {
        e.preventDefault(); // Prevenir comportamiento por defecto
        console.log('Cargando formulario desde', url);
        $.ajax({
            url: url,
            method: "GET",
            success: function(response) {
                response = response.replace(/<header>[\s\S]*<\/header>/, '');
                response = response.replace(/<footer class="bg-light text-dark text-center py-4">[\s\S]*<\/footer>/, '');
                $(targetSelector).html(response);
                $(modalSelector).removeAttr('aria-hidden').modal('show');
            },
            error: function(xhr) {
                Swal.fire({
                    icon: 'error',
                    title: 'Error al cargar el formulario',
                    text: xhr.responseText
                });
            }
        });
    });
}
// Función para manejar la carga del formulario sin botón
function handleFormLoadNoButton(url, targetSelector, modalSelector) {
    console.log('Cargando formulario desde', url);
    $.ajax({
        url: url,
        method: "GET",
        success: function(response) {
            response = response.replace(/<header>[\s\S]*<\/header>/, '');
            response = response.replace(/<footer class="bg-light text-dark text-center py-4">[\s\S]*<\/footer>/, '');
            $(targetSelector).html(response);
            $(modalSelector).removeAttr('aria-hidden').modal('show');
        },
        error: function(xhr) {
            Swal.fire({
                icon: 'error',
                title: 'Error al cargar el formulario',
                text: xhr.responseText
            });
        }
    });
}
// Función para manejar el envio rapido de formularios
// Manejar el envío del formulario
function handleFormsubmitFast(formSelector, url, metodo = "POST", modalSelector=null, actualizar_informacion = true) {
    $(formSelector).on('submit', function(e) {
        e.preventDefault(); // Prevenir comportamiento por defecto
        console.log('Formulario enviado', e);
        // Recolectar datos del formulario
        var formData = $(this).serialize();
        $.ajax({
            url: url,  // URL para agregar ingresos
            method: metodo,
            data: formData,
            headers: {
                'X-CSRFToken': csrfToken
            },
            success: function(response) {
                Swal.fire({
                    icon: 'success',
                    title: 'Ingreso agregado exitosamente',
                    showConfirmButton: false,
                    timer: 1500
                });
                // Limpiar el formulario
                $(formSelector).trigger('reset');
                // Actualizar los datos 
                if (actualizar_informacion) {
                    cargarDatosModelo(modelo_principal);
                }

                // Validar si existe un modal
                if (modalSelector) {
                    // Ocultar el modal
                    console.log('Cerrando modal', $(modalSelector));
                    $(modalSelector).modal('hide');
                }
            },
            error: function(xhr) {
                Swal.fire({
                    icon: 'error',
                    title: 'Error al agregar',
                    text: xhr.responseText
                });
            }
        });
    });
}
function handleFormDelete(url) {
    console.log('Cargando formulario desde', url);
    // Confirmar la acción
    Swal.fire({
        title: '¿Estás seguro?',
        text: "Esta acción no se puede deshacer.",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                url: url,
                method: "GET",
                success: function(response) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Ingreso eliminado',
                        text: response.message
                    });
                },
                error: function(xhr) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error al eliminar el ingreso',
                        text: xhr.responseText
                    });
                }
            });
        }
    });
}

// Manejar el envío del formulario
function handleFormSubmit(formSelector, url, metodo = "POST", modelo,  modalSelector=null, actualizar_informacion = true) {
    $(formSelector).on('submit', function(e) {
        e.preventDefault(); // Prevenir comportamiento por defecto
        console.log('Formulario enviado', e);
        // Recolectar datos del formulario
        var formData = $(this).serialize();
        console.log('Datos del formulario', formData);
        $.ajax({
            url: url,  // URL para agregar ingresos
            method: metodo,
            data: formData,
            headers: {
                'X-CSRFToken': csrfToken
            },
            success: function(response) {
                Swal.fire({
                    icon: 'success',
                    title:  `${modelo} agregado exitosamente `,
                    showConfirmButton: false,
                    timer: 1500
                });
                // Limpiar el formulario
                $(formSelector).trigger('reset');
                if (actualizar_informacion) {
                    cargarDatosModelo(modelo_principal);
                }
                // Validar si existe un modal
                if (modalSelector) {
                    // Ocultar el modal
                    console.log('Cerrando modal', $(modalSelector));
                    $(modalSelector).modal('hide');
                }
            },
            error: function(xhr) {
                Swal.fire({
                    icon: 'error',
                    title: 'Error al agregar',
                    text: xhr.responseText
                });
            }
        });
    });
}

// Evento para el botón de filtrar
$('#filtrarIngresos').on('click', function() {
    buscarModelo('Ingresos');
});
// Autocompletado para el campo de búsqueda
$('#buscarIngresos').autocomplete({
    source: function(request, response) {
        $.ajax({
            url: '/api/buscar_dinamica_ingresos/',
            method: 'GET',
            data: {
                query: request.term
            },
            success: function(data) {
                response(data.ingreso.map(function(ingreso) {
                    return {
                        label: ingreso.descripcion + ' - $' + ingreso.cantidad + ' - ' + ingreso.fecha + ' - ' + ingreso.fuente,
                        value: ingreso.descripcion
                    };
                }));
            },
            error: function(xhr, status, error) {
                console.error('Error en autocompletado: ', error);
            }
        });
    },
    minLength: 2
});
// Function to handle the click event on the Edit button
function initializeEditButtons(modelo) {
    $(`#tabla${modelo}`).on('click', '.editbutton', function() {
        var id = $(this).data('id');
        console.log('Edit button clicked', id);
        handleFormLoadNoButton(`/api/editar_${modelo.toLowerCase()}/` + id + '/', `#insert-form-editar-${modelo.toLowerCase()}`, `#modalEditar${modelo}`);
    });
}
// Function to handle the click event on the Delete button
function initializeDeleteButtons(modelo) {
    $(`#tabla${modelo}`).on('click', '.deletebutton', function() {
        var id = $(this).data('id');
        console.log('Delete button clicked', id);
        handleFormDelete(`/api/eliminar_${modelo.toLowerCase()}/` + id + '/');
    });
}
// Validar el modelo principal y cargar formularios adicionales si es necesario
var modelo_principal = $("#modelo_principal").val();
if (modelo_principal) {
    // AGREGAR MODELO
    handleFormLoad(`#btnAgregar${modelo_principal}`, `/crear_${modelo_principal.toLowerCase()}/`, `#insert-form-agregar-${modelo_principal.toLowerCase()}`, `#modalAgregar${modelo_principal}`);
    // AGREGAR RÁPIDO
    handleFormSubmit(`#formAgregarRapido${modelo_principal}`, `/api/crear_rapido_${modelo_principal.toLowerCase()}/`, 'POST', modelo_principal );
}



function buscarBotoneditar() {
    var botones = document.querySelectorAll('.editbutton');
    console.log("Los botones son: ", botones);
    botones.forEach(function(boton) {
        boton.addEventListener('click', function() {
            var id = this.getAttribute('data-id');
            editarIngreso(id);
        });
    });
}

function buscarBotonEliminar() {
    var botones = document.querySelectorAll('.deletebutton');
    console.log("Los botones son: ", botones);
    botones.forEach(function(boton) {
        boton.addEventListener('click', function() {
            var id = this.getAttribute('data-id');
            eliminarIngreso(id);
        });
    });
}



// Llamar a la función para cargar datos del modelo principal
cargarDatosModelo(modelo_principal);

// Boton actualizar
$(`#btnActualizar${modelo_principal}`).on('click', function() {
    cargarDatosModelo(modelo_principal);
});

