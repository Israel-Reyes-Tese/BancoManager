// JS_HOME.js

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
    var ctx = document.getElementById(canvasId).getContext('2d');
    var chart = new Chart(ctx, {
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

// Función para cargar datos de ingresos
function cargarDatosIngresos() {
    cargaIngresos.mostrar(); // Mostrar el cuadro de carga
    $.ajax({
        url: '/api/informacion_ingresos/',
        type: 'GET',
        success: function(data) {
            console.log('Datos de ingresos cargados: ', data);

            // Actualizar el total de ingresos
            $('#total-ingresos').text('$' + data.total_ingresos);
            // Verifica si existen ingresos recientes
            if (data.ingresos_recientes.length > 0) {
                data.ingresos_recientes.forEach(function(ingreso) {
                    $('#lista_ingresos_recientes').append('<li class="list-group-item">' + ingreso.descripcion + ': $' + ingreso.cantidad + ' - ' + ingreso.fecha + '</li>');
                });
            } else {
                $('#no_data_message').show();  // Mostrar mensaje de sin datos
            }

            var mes_lista = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
            
            // Configura la gráfica de ingresos
            configurarGrafica({
                canvasId: 'comparativaMensual',
                tipoGrafica: 'bar',
                etiquetas: mes_lista,
                datos: data.ingresos_graficables,
                label: 'Ingresos por Mes',
                backgroundColor: 'rgba(75, 192, 192, 0.5)'
            });
            // Configura la gráfica de ingresos por categoría
            configurarGrafica({
                canvasId: 'ingresosPorCategoria',
                tipoGrafica: 'doughnut',
                etiquetas: data.ingresos_por_categoria_graficables.map(ingreso => ingreso.fuente),
                datos: data.ingresos_por_categoria_graficables.map(ingreso => ingreso.total),
                label: 'Ingresos por Categoría',
                backgroundColor: data.ingresos_por_categoria_graficables.map(ingreso => ingreso.color)
            });

            // Limpiar la tabla antes de llenarla
            $('#tablaIngresos').DataTable().clear().destroy();
            // Llenar la tabla con los datos de ingresos
            data.todos_ingresos.forEach(function(ingreso) {
                $('#tablaIngresos tbody').append(
                    '<tr>' +
                    '<td>' + ingreso.descripcion + '</td>' +
                    '<td>' + ingreso.cantidad + '</td>' +
                    '<td>' + ingreso.fecha + '</td>' +
                    '<td>' + ingreso.fuente + '</td>' +
                    '<td>' + ingreso.cuenta + '</td>' +
                    '<td> <button class="btn btn-warning btn-sm" onclick="editDebt' + ingreso.id + '">Editar</button>' +
                    '<button class="btn btn-danger btn-sm" onclick="deleteDebt' + ingreso.id + '">Eliminar</button> </td>' +
                    '</tr>'
                );
            });

            // Inicializar DataTables
            $('#tablaIngresos').DataTable({
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
            console.error('Error cargando datos: ', error);
            alert('Ocurrió un error al cargar los datos de ingresos.');
        },
        complete: function() {
            cargaIngresos.ocultar(); // Ocultar el cuadro de carga
        }
    });
}

// Función para buscar y filtrar ingresos
function buscarIngresos() {
    var query = $('#buscarIngreso').val();
    var fechaDesde = $('#rangoFechaDesde').val();
    var fechaHasta = $('#rangoFechaHasta').val();

    cargaIngresos.mostrar(); // Mostrar el cuadro de carga
    $.ajax({
        url: '/api/buscar_dinamica_ingresos/',
        method: 'GET',
        data: {
            query: query,
            fecha_desde: fechaDesde,
            fecha_hasta: fechaHasta
        },
        success: function(data) {
            console.log('Ingresos filtrados: ', data);

            $('#tablaIngresos').DataTable().clear().destroy();
            if (data.ingreso.length > 0) {
                data.ingreso.forEach(function(ingreso) {
                    $('#tablaIngresos tbody').append(
                        '<tr>' +
                        '<td>' + ingreso.descripcion + '</td>' +
                        '<td>' + ingreso.cantidad + '</td>' +
                        '<td>' + ingreso.fecha + '</td>' +
                        '<td>' + ingreso.fuente + '</td>' +
                        '<td>' + ingreso.cuenta__nombre + '</td>' +
                        '<td> <button class="btn btn-warning btn-sm" onclick="editDebt' + ingreso.id + '">Editar</button>' +
                        '<button class="btn btn-danger btn-sm" onclick="deleteDebt' + ingreso.id + '">Eliminar</button> </td>' +
                        '</tr>'
                    );
                });
            } else {
                $('#tablaIngresos tbody').append('<tr><td colspan="5">No se encontraron ingresos.</td></tr>');
            }

            // Inicializar DataTables
            $('#tablaIngresos').DataTable({
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
            console.error('Error buscando ingresos: ', error);
            alert('Ocurrió un error al buscar los ingresos.');
        },
        complete: function() {
            cargaIngresos.ocultar(); // Ocultar el cuadro de carga
        }
    });
}

// Función para manejar la carga del formulario
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
                console.log('Formulario cargado exitosamente', response);
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
// Función para editar un ingreso
window.editarIngreso = function(id) {
    handleFormLoad(null, '/api/editar_ingreso/' + id + '/', '#insert-form-editar-ingreso', '#modalEditarIngreso');
}
// Inicializar el cuadro de carga
const cargaIngresos = cuadroCarga('#cuadroCarga');

// Obtener el token CSRF desde la meta etiqueta
var csrfToken = $('meta[name="csrf-token"]').attr('content');

// Configurar jQuery para incluir el token CSRF en todas las solicitudes AJAX
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
        }
    }
});

// Evento para el botón de filtrar
$('#filtrar').on('click', function() {
    buscarIngresos();
});

// Autocompletado para el campo de búsqueda
$('#buscarIngreso').autocomplete({
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

// Validar el modelo principal y cargar formularios adicionales si es necesario
var modelo_principal = $("#modelo_principal").val();
if (modelo_principal == "Ingreso") {
    handleFormLoad('#btnAgregarIngreso', '/crear_ingreso/', '#insert-form-agregar-ingreso', '#modalAgregarIngreso');
}

// Llamar a la función para cargar datos de ingresos
cargarDatosIngresos();