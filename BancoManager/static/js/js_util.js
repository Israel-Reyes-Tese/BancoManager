// js_util.js
export function funcion1() {
    // código de la función
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
export function configurarTabla({ tablaId, modelo, opciones = {}, data={}, campos={}, categoria_filter='', numeroData=10, totalesdraw='', actualizar_totales_validacion =true, agregar_botones_edit=true, total_text_act_ext ='', cantidad_ingresar =''} ) {
    console.log("Actualizando totales" , "tablaId: ",tablaId , "modelo: ", modelo, "opciones: ", opciones, "data: ", data, "campos: ", campos, "categoria_filter: ", categoria_filter, "numeroData: ", numeroData, "totalesdraw: ", totalesdraw, "actualizar_totales: ", actualizar_totales_validacion, "agregar_botones_edit: ", agregar_botones_edit, "total_text_act_ext: ", total_text_act_ext, "cantidad_ingresar: ", cantidad_ingresar);
    if (actualizar_totales_validacion){
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
    }
    if (total_text_act_ext){
        $(`#${total_text_act_ext}`).text('$'+ cantidad_ingresar);
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
        if (agregar_botones_edit){
            fila += `<td> <button class="btn btn-warning btn-sm editbutton" id="btnEditar${modelo}" data-id="${item.id}">Editar</button>` +
            `<button class="btn btn-danger btn-sm deletebutton" id="btnEliminar${modelo}" data-id="${item.id}">Eliminar</button> </td></tr>`;
        }
        $(`#${tablaId} tbody`).append(fila);
    });
    // Inicializar DataTables
    $(`#${tablaId}`).DataTable(Object.assign({
        order: [[0, 'desc']],
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
    if (actualizar_totales_validacion){
        console.log("Actualizando totales");
        // Actualizar totales al dibujar la tabla
        table_filter.on('draw', function () {
            actualizarTotales(table_filter);
        });
        // Inicializar los totales al cargar la tabla
        actualizarTotales(table_filter);
    }
}    

// Manejar el envío del formulario
export function handleFormSubmit(formSelector, url, metodo = "POST", modalSelector=null, serializeArray=false, returnData=false, callback=null) {
    $(formSelector).on('submit', function(e) {
        try {
            e.preventDefault(); // Prevenir comportamiento por defecto
            console.log('Formulario enviado', e);
            // Recolectar datos del formulario
            var formData = $(this).serialize();
            if (serializeArray) {
                var formData = $(this).serializeArray().reduce(function(obj, item) {
                    obj[item.name] = item.value;
                    return obj;
                }, {});
            }
            $.ajax({
                url: url,  // URL para agregar ingresos
                method: metodo,
                data: formData,
                headers: {
                    'X-CSRFToken': csrfToken
                },
                success: function(response) {
                    try {
                        Swal.fire({
                            icon: 'success',
                            title: 'Ingreso agregado exitosamente',
                            showConfirmButton: false,
                            timer: 1500
                        });
                        // Limpiar el formulario
                        $(formSelector).trigger('reset');
                        // Validar si existe un modal
                        if (modalSelector) {
                            // Ocultar el modal
                            console.log('Cerrando modal', $(modalSelector));
                            $(modalSelector).modal('hide');
                        }
                        // Retornar el response si returnData está activado
                        if (returnData) {
                            console.log('Retornando response:', response);
                            callback(response);
                        }

                    } catch (error) {
                        console.error('Error en handleFormSubmit success callback:', error);
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
        } catch (error) {
            console.error('Error en handleFormSubmit:', error);
        }
    });
}




