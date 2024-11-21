// js_util.js

// **************************************************************************************************
// * .----------------. .----------------. .----------------. .----------------. .----------------. *
// *| .--------------. | .--------------. | .--------------. | .--------------. | .--------------. |*
// *| | _____  _____ | | |  _________   | | |     _____    | | |   _____      | | |    _______   | |*
// *| ||_   _||_   _|| | | |  _   _  |  | | |    |_   _|   | | |  |_   _|     | | |   /  ___  |  | |*
// *| |  | |    | |  | | | |_/ | | \_|  | | |      | |     | | |    | |       | | |  |  (__ \_|  | |*
// *| |  | '    ' |  | | |     | |      | | |      | |     | | |    | |   _   | | |   '.___`-.   | |*
// *| |   \ `--' /   | | |    _| |_     | | |     _| |_    | | |   _| |__/ |  | | |  |`\____) |  | |*
// *| |    `.__.'    | | |   |_____|    | | |    |_____|   | | |  |________|  | | |  |_______.'  | |*
// *| |              | | |              | | |              | | |              | | |              | |*
// *| '--------------' | '--------------' | '--------------' | '--------------' | '--------------' |*
// * '----------------' '----------------' '----------------' '----------------' '----------------' *
// **************************************************************************************************


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




function llenarCarruselcardLarge(data, modelo, campos=["descripcion", "monto", "fecha_vencimiento", "estado"]) {
    console.log('Llenando carrusel de deudas: ', data, 'modelo: ', modelo, 'campos: ', campos);
    const carouselInner = document.getElementById(`${modelo.toLowerCase()}CarouselInner`);
    carouselInner.innerHTML = ''; // Limpiar contenido existente
    let itemsPerSlide = 3;
    let totalItems = data.length;
    let slides = Math.ceil(totalItems / itemsPerSlide);

    for (let i = 0; i < slides; i++) {
        const item = document.createElement('div');
        item.className = `carousel-item ${i === 0 ? 'active' : ''}`;
        let itemContent = '<div class="d-flex justify-content-around">';
        for (let j = 0; j < itemsPerSlide; j++) {
            let index = i * itemsPerSlide + j;
            if (index < totalItems) {
                let deuda = data[index];
                itemContent += '<div class="card mx-2" style="width: 30%;">';
                campos.forEach((campo) => {
                    if (campo === "descripcion") {
                        itemContent += `<h5>${deuda[campo]}</h5>`;
                    } else if (campo === "monto") {
                        itemContent += `<p>Monto: $${deuda[campo]}</p>`;
                    } else if (campo === "fecha_vencimiento") {
                        itemContent += `<p>Fecha de Vencimiento: ${deuda[campo]}</p>`;
                    } else if (campo === "estado") {
                        itemContent += `<p>Estado: ${deuda[campo] ? 'Saldada' : 'Pendiente'}</p>`;
                    }
                });
                itemContent += '</div>';
            }
        }
        itemContent += '</div>';
        item.innerHTML = itemContent;
        carouselInner.appendChild(item);
    }

    function prevCarouselItem() {
        $(`#${modelo.toLowerCase()}Carousel`).carousel('prev');
    }

    function nextCarouselItem() {
        $(`#${modelo.toLowerCase()}Carousel`).carousel('next');
    }

    // Attach event listeners to the buttons
    try {
        document.querySelector(`#${modelo.toLowerCase()}Carousel .carousel-control-prev`).addEventListener('click', prevCarouselItem);
        document.querySelector(`#${modelo.toLowerCase()}Carousel .carousel-control-next`).addEventListener('click', nextCarouselItem);
    } catch (error) {
        console.error('Error al adjuntar los eventos de los botones del carrusel:', error);
    }

    // Initialize the carousel
    $(`#${modelo.toLowerCase()}Carousel`).carousel({
        interval: 2000
    });
}





// ***********************************************************************************************************************************************************************************************************************
// * .----------------. .----------------. .----------------. .----------------. .----------------.    .----------------. .----------------. .----------------. .----------------. .----------------. .----------------. *
// *| .--------------. | .--------------. | .--------------. | .--------------. | .--------------. |  | .--------------. | .--------------. | .--------------. | .--------------. | .--------------. | .--------------. |*
// *| |  ________    | | |      __      | | |  _________   | | |     ____     | | |    _______   | |  | | ____    ____ | | |     ____     | | |  ________    | | |  _________   | | |   _____      | | |     ____     | |*
// *| | |_   ___ `.  | | |     /  \     | | | |  _   _  |  | | |   .'    `.   | | |   /  ___  |  | |  | ||_   \  /   _|| | |   .'    `.   | | | |_   ___ `.  | | | |_   ___  |  | | |  |_   _|     | | |   .'    `.   | |*
// *| |   | |   `. \ | | |    / /\ \    | | | |_/ | | \_|  | | |  /  .--.  \  | | |  |  (__ \_|  | |  | |  |   \/   |  | | |  /  .--.  \  | | |   | |   `. \ | | |   | |_  \_|  | | |    | |       | | |  /  .--.  \  | |*
// *| |   | |    | | | | |   / ____ \   | | |     | |      | | |  | |    | |  | | |   '.___`-.   | |  | |  | |\  /| |  | | |  | |    | |  | | |   | |    | | | | |   |  _|  _   | | |    | |   _   | | |  | |    | |  | |*
// *| |  _| |___.' / | | | _/ /    \ \_ | | |    _| |_     | | |  \  `--'  /  | | |  |`\____) |  | |  | | _| |_\/_| |_ | | |  \  `--'  /  | | |  _| |___.' / | | |  _| |___/ |  | | |   _| |__/ |  | | |  \  `--'  /  | |*
// *| | |________.'  | | | ||____|  |____|| | |   |_____|    | | |   `.____.'   | | |  |_______.'  | |  | ||_____||_____|| | |   `.____.'   | | | |________.'  | | | |_________|  | | |  |________|  | | |   `.____.'   | |*
// *| |              | | |              | | |              | | |              | | |              | |  | |              | | |              | | |              | | |              | | |              | | |              | |*
// *| '--------------' | '--------------' | '--------------' | '--------------' | '--------------' |  | '--------------' | '--------------' | '--------------' | '--------------' | '--------------' | '--------------' |*
// * '----------------' '----------------' '----------------' '----------------' '----------------'    '----------------' '----------------' '----------------' '----------------' '----------------' '----------------' *
// ***********************************************************************************************************************************************************************************************************************
export function cargarDatosModelo(modelo) {
    console.log(`Cargando datos de ${modelo}...`);
    const cargaModelo = cuadroCarga(`#cuadroCarga${modelo}`);
    $.ajax({
        url: `/api/informacion_${modelo.toLowerCase()}/`,
        type: 'GET',
        success: function(data) {
            console.log(`Datos de ${modelo} cargados: `, data);
            // Validar que modelo es para cargar los datos
            if (modelo === 'Ingreso' || modelo === 'Egreso') {
                cargarDatosModeloIngresosorEgresos(modelo, data, targetCuenta = `cuenta-${modelo}`);
            } else if (modelo === 'Cuenta_bancaria') {
                console.log('Datos de cuentas bancarias cargados: Funcion' );
                cargarDatosModeloCuentasBancarias(modelo, data);
            } else if (modelo === 'Deuda') {
                cargarDatosDeudas(modelo, data);
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
    // initializeEditButtons(modelo);
    // initializeDeleteButtons(modelo);
}
                                                                                    // *********************************************************
                                                                                    // *8888888b.                         888                  *
                                                                                    // *888  "Y88b                        888                  *
                                                                                    // *888    888                        888                  *
                                                                                    // *888    888  .d88b.  888  888  .d88888  8888b.  .d8888b *
                                                                                    // *888    888 d8P  Y8b 888  888 d88" 888     "88b 88K     *
                                                                                    // *888    888 88888888 888  888 888  888 .d888888 "Y8888b.*
                                                                                    // *888  .d88P Y8b.     Y88b 888 Y88b 888 888  888      X88*
                                                                                    // *8888888P"   "Y8888   "Y88888  "Y88888 "Y888888  88888P'*
                                                                                    // *********************************************************
function cargarDatosDeudas(modelo, data) {
    console.log('Datos de deudas cargados: ', data , 'Funcion lv 2' , 'modelo: ', modelo, "CSRF: ", csrfToken);
    // Actualizar el total
    $(`#total-${modelo.toLowerCase()}`).text('$' + data.total_deuda);
    // Generar el carrusel de deudas
    llenarCarruselcardLarge(data.deudas, modelo, ["descripcion", "monto", "fecha_vencimiento", "estado"]);
    // Generar las tablas :
        // Listado de deudas 
    configurarTabla({
        tablaId: `tabla${modelo}`,
        modelo: modelo,
        data: data.deudas,
        data_totales: {
            "cantidadColIndex": 2,
            "tipoColIndex": undefined,
            "tipoEgreso": undefined,
            "tipoIngreso": undefined,
            "totalEgresosId": undefined,
            "totalIngresosId": undefined,
            "totalTargetId": `totalTabla${modelo}`
        }, 
        campos: ['usuario_deudor', 'descripcion', 'monto', 'fecha_vencimiento', 'estado', 'tipo_deuda'],
        categoria_filter: '',
        numeroData: 10,
        totalesdraw: '',
        actualizar_totales_validacion: true,
        agregar_botones_edit: true,
        total_text_act_ext: `total-${modelo.toLowerCase()}`,
        cantidad_ingresar: data.total_deuda,
        boton_extra: 'Diferir'
    });


    }


                                                                                    // **************************************************************************
                                                                                    // *      .d8888b.                             888                          *
                                                                                    // *     d88P  Y88b                            888                          *
                                                                                    // *     888    888                            888                          *
                                                                                    // *     888        888  888  .d88b.  88888b.  888888  8888b.  .d8888b      *
                                                                                    // *     888        888  888 d8P  Y8b 888 "88b 888        "88b 88K          *
                                                                                    // *     888    888 888  888 88888888 888  888 888    .d888888 "Y8888b.     *
                                                                                    // *     Y88b  d88P Y88b 888 Y8b.     888  888 Y88b.  888  888      X88     *
                                                                                    // *      "Y8888P"   "Y88888  "Y8888  888  888  "Y888 "Y888888  88888P'     *
                                                                                    // **************************************************************************
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
        insertarRegistroRapido(csrfToken, '#insertar_form_ingreso_rapido', 'Ingreso', '', lista_select=['Salario', 'Venta', 'Intereses', 'Otro'], targetCuenta='cuenta');
        // Cargar el formulario de agregar egreso
        insertarRegistroRapido(csrfToken, '#insertar_form_egreso_rapido', 'Egreso', '', lista_select=['Compra', 'Pago', 'Retiro', 'Otro']);
    }




// ***********************************************************************************************************************************************************
// * .----------------. .----------------. .----------------. .----------------. .----------------. .----------------. .----------------. .----------------. *
// *| .--------------. | .--------------. | .--------------. | .--------------. | .--------------. | .--------------. | .--------------. | .--------------. |*
// *| |    ______    | | |  _______     | | |      __      | | |  _________   | | |     _____    | | |     ______   | | |      __      | | |    _______   | |*
// *| |  .' ___  |   | | | |_   __ \    | | |     /  \     | | | |_   ___  |  | | |    |_   _|   | | |   .' ___  |  | | |     /  \     | | |   /  ___  |  | |*
// *| | / .'   \_|   | | |   | |__) |   | | |    / /\ \    | | |   | |_  \_|  | | |      | |     | | |  / .'   \_|  | | |    / /\ \    | | |  |  (__ \_|  | |*
// *| | | |    ____  | | |   |  __ /    | | |   / ____ \   | | |   |  _|      | | |      | |     | | |  | |         | | |   / ____ \   | | |   '.___`-.   | |*
// *| | \ `.___]  _| | | |  _| |  \ \_  | | | _/ /    \ \_ | | |  _| |_       | | |     _| |_    | | |  \ `.___.'\  | | | _/ /    \ \_ | | |  _| |  \ \_  | |*
// *| |  `._____.'   | | | |____| |___| | | ||____|  |____|| | | |_____|      | | |    |_____|   | | |   `._____.'  | | ||____|  |____|| | |  |_______.'  | |*
// *| |              | | |              | | |              | | |              | | |              | | |              | | |              | | |              | |*
// *| '--------------' | '--------------' | '--------------' | '--------------' | '--------------' | '--------------' | '--------------' | '--------------' |*
// * '----------------' '----------------' '----------------' '----------------' '----------------' '----------------' '----------------' '----------------' *
// ***********************************************************************************************************************************************************
// Función para configurar las tablas

// *********************************************************************************************************************
// * .----------------. .----------------. .----------------. .----------------. .----------------. .----------------. *
// *| .--------------. | .--------------. | .--------------. | .--------------. | .--------------. | .--------------. |*
// *| |  _________   | | |      __      | | |   ______     | | |   _____      | | |      __      | | |    _______   | |*
// *| | |  _   _  |  | | |     /  \     | | |  |_   _ \    | | ||_   \  /   _|| | ||_   _||_   _|| | |  |_   _|     | | |     /  \     | | | |_   __ \    | | |    |_   _|   | | |   .'    `.   | | |   /  ___  |  | |*
// *| |_/ | | \_|  | | |    / /\ \    | | |    | |_) |   | | |    | |       | | |    / /\ \    | | |  |  (__ \_|  | |*
// *| |     | |      | | |   / ____ \   | | |    |  __'.   | | |    | |   _   | | |   / ____ \   | | |   '.___`-.   | |*
// *| |    _| |_     | | | _/ /    \ \_ | | |   _| |__) |  | | |   _| |__/ |  | | | _/ /    \ \_ | | |  |`\____) |  | |*
// *| |   |_____|    | | ||____|  |____|| | |  |_______/   | | |  |________|  | | ||____|  |____|| | |  |_______.'  | |*
// *| |              | | |              | | |              | | |              | | |              | | |              | |*
// *| '--------------' | '--------------' | '--------------' | '--------------' | '--------------' | '--------------' |*
// * '----------------' '----------------' '----------------' '----------------' '----------------' '----------------' *
// *********************************************************************************************************************
// Función para actualizar los totales
function actualizarTotales(table, cantidadColIndex, tipoColIndex, tipoEgreso, tipoIngreso, totalEgresosId, totalIngresosId, totalTargetId) {
    console.log('Actualizando totales...', "Table: ", table, "cantidadColIndex: ", cantidadColIndex, "tipoColIndex: ", tipoColIndex, "tipoEgreso: ", tipoEgreso, "tipoIngreso: ", tipoIngreso, "totalEgresosId: ", totalEgresosId, "totalIngresosId: ", totalIngresosId, "totalTargetId: ", totalTargetId);
    
    var totalEgresos = 0;
    var totalIngresos = 0;
    var total = 0;

    table.rows({ search: 'applied' }).every(function(rowIdx, tableLoop, rowLoop) {
        var data = this.data();
        var cantidad = parseFloat(data[cantidadColIndex]); // Columna de "cantidad"
        total += cantidad;

        if (tipoColIndex !== undefined) {
            var tipo = data[tipoColIndex]; // Columna de "tipo" (egreso/ingreso)
            if (tipo.toLowerCase() === tipoEgreso.toLowerCase()) {
                totalEgresos += cantidad;
            } else if (tipo.toLowerCase() === tipoIngreso.toLowerCase()) {
                totalIngresos += cantidad;
            }
        }
    });

    if (tipoColIndex !== undefined) {
        $('#' + totalEgresosId).text('Total Egresos: ' + totalEgresos.toFixed(2));
        $('#' + totalIngresosId).text('Total Ingresos: ' + totalIngresos.toFixed(2));
    }

    $('#' + totalTargetId).text('Total-listado: $' + total.toFixed(2));
}

// Función para configurar las tablas
export function configurarTabla({ tablaId, modelo, opciones = {}, data={}, data_totales={}, campos={}, categoria_filter='', numeroData=10, totalesdraw='', actualizar_totales_validacion =true, agregar_botones_edit=true, total_text_act_ext ='', cantidad_ingresar ='', boton_extra=''} ) {
    console.log("Configurando tabla..." , "tablaId: ",tablaId , "modelo: ", modelo, "opciones: ", opciones, "data: ", data, "campos: ", campos, "categoria_filter: ", categoria_filter, "numeroData: ", numeroData, "totalesdraw: ", totalesdraw, "actualizar_totales: ", actualizar_totales_validacion, "agregar_botones_edit: ", agregar_botones_edit, "total_text_act_ext: ", total_text_act_ext, "cantidad_ingresar: ", cantidad_ingresar);
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
                    `<button class="btn btn-danger btn-sm deletebutton" id="btnEliminar${modelo}" data-id="${item.id}">Eliminar</button> </td> ${boton_extra ? '' : '</tr>'}
                    `;
        }
        if (boton_extra){
            fila += `<td> <button class="btn-neon" aria-label="${boton_extra}" id="btnext${modelo}" data-id="${item.id}"> <i class="fas fa-clock"></i> ${boton_extra} </button> </td></tr>`;
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
            actualizarTotales(table_filter, data_totales.cantidadColIndex, data_totales.tipoColIndex, data_totales.tipoEgreso, data_totales.tipoIngreso, data_totales.totalEgresosId, data_totales.totalIngresosId, data_totales.totalTargetId);
        });
    } 
    if (actualizar_totales_validacion){
        console.log("Actualizando totales");
        // Actualizar totales al dibujar la tabla
        table_filter.on('draw', function () {
            actualizarTotales(table_filter, data_totales.cantidadColIndex, data_totales.tipoColIndex, data_totales.tipoEgreso, data_totales.tipoIngreso, data_totales.totalEgresosId, data_totales.totalIngresosId, data_totales.totalTargetId);
        });
        actualizarTotales(table_filter, data_totales.cantidadColIndex, data_totales.tipoColIndex, data_totales.tipoEgreso, data_totales.tipoIngreso, data_totales.totalEgresosId, data_totales.totalIngresosId, data_totales.totalTargetId);
    }
}    

// ********************************************************************************************************************************************************************************************************************
// * .----------------. .----------------. .----------------. .----------------. .----------------. .----------------. .----------------. .----------------. .----------------. .----------------. .----------------. *
// *| .--------------. | .--------------. | .--------------. | .--------------. | .--------------. | .--------------. | .--------------. | .--------------. | .--------------. | .--------------. | .--------------. |*
// *| |  _________   | | |     ____     | | |  _______     | | | ____    ____ | | | _____  _____ | | |   _____      | | |      __      | | |  _______     | | |     _____    | | |     ____     | | |    _______   | |*
// *| | |_   ___  |  | | |   .'    `.   | | | |_   __ \    | | ||_   \  /   _|| | ||_   _||_   _|| | |  |_   _|     | | |     /  \     | | | |_   __ \    | | |    |_   _|   | | |   .'    `.   | | |   /  ___  |  | |*
// *| |   | |_  \_|  | | |  /  .--.  \  | | |   | |__) |   | | |  |   \/   |  | | |  | |    | |  | | |    | |       | | |    / /\ \    | | |   | |__) |   | | |      | |     | | |  /  .--.  \  | | |  |  (__ \_|  | |*
// *| |   |  _|      | | |  | |    | |  | | |   |  __ /    | | |  | |\  /| |  | | |  | '    ' |  | | |    | |   _   | | |   / ____ \   | | |   |  __ /    | | |      | |     | | |  | |    | |  | | |   '.___`-.   | |*
// *| |  _| |_       | | |  \  `--'  /  | | |  _| |  \ \_  | | | _| |_\/_| |_ | | |   \ `--' /   | | |   _| |__/ |  | | | _/ /    \ \_ | | |  _| |  \ \_  | | |     _| |_    | | |  \  `--'  /  | | |  |`\____) |  | |*
// *| | |_____|      | | |   `.____.'   | | | |____| |___| | | ||_____||_____|| | |    `.__.'    | | |  |________|  | | ||____|  |____|| | | |____| |___| | | |    |_____|   | | |   `.____.'   | | |  |_______.'  | |*
// *| |              | | |              | | |              | | |              | | |              | | |              | | |              | | |              | | |              | | |              | | |              | |*
// *| '--------------' | '--------------' | '--------------' | '--------------' | '--------------' | '--------------' | '--------------' | '--------------' | '--------------' | '--------------' | '--------------' |*
// * '----------------' '----------------' '----------------' '----------------' '----------------' '----------------' '----------------' '----------------' '----------------' '----------------' '----------------' *
// ********************************************************************************************************************************************************************************************************************
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

export function inicializarCarruselDeudas(carouselId) {
    $(carouselId).carousel({
        interval: 2000
    });
}




