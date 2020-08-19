$(document).ready(function() {
    //Cuando no se tiene validacion
    var table = $('#matrixGeneral').removeAttr('width').DataTable( {
        lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "All"]],
        //lengthMenu: [ 10, 25, 50, 75, 100 ],
        deferRender:    true,
        scrollY:        "300px",
        scrollX:        true,
        scrollCollapse: true,
        //paging:         false,
        columnDefs: [
          { 
            //width: 150, targets: [2,3],
            width: 600, targets: [2, 6, 17, 18, 19, 27, 29],
            //  width: 700, targets: [8,21,22,35,37,38,39,49]
          }
         ],
        //fixedColumns: true,
        fixedColumns:   {leftColumns: 1}
        //"lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]]
        //"pageLength": 50
    } );
    //Para validacion - admin y riskAnalyst
    var table = $('#matrixValidation').removeAttr('width').DataTable( {
        lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "All"]],
        deferRender:    true,
        scrollY:        "500px",
        scrollX:        true,
        scrollCollapse: true,
        //paging:         false,
        columnDefs: [
          {
            //width: 600, targets: [12,17,26,29,30,31,43,47,49,54,55,56,57,58],
            width: 600, targets: [37],
            //width: 500, targets: [13,17,27,30,31,32,44,48,49,50,59]
            //width: 750, targets: [8,22,23,35,39,40,41,50]
          }
        ],
        //fixedColumns: true,
        //"lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]]
        //"pageLength": 50
        fixedColumns:   {leftColumns: 1}
    } );
    //Para validacion - processOwner y controlResp
    var table = $('#matrixValidation2').removeAttr('width').DataTable( {
        lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "All"]],
        deferRender:    true,
        scrollY:        "500px",
        scrollX:        true,
        scrollCollapse: true,
        //paging:         false,
        columnDefs: [
          {
            //width: 600, targets: [9,18,21,22,23,35,39,41,46,47,48,49,50],
            width: 600, targets: [3,7,18,19,20,28,30],
            //width: 500, targets: [13,17,27,30,31,32,44,48,49,50,59]
            //width: 750, targets: [8,22,23,35,39,40,41,50]
          }
        ],
        //fixedColumns: true,
        //"lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]]
        //"pageLength": 50
        fixedColumns:   {leftColumns: 1}
    } );

    var table = $('#matrixTesting').removeAttr('width').DataTable( {
        lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "All"]],
        deferRender:    true,
        scrollY:        "500px",
        scrollX:        true,
        scrollCollapse: true,
        //paging:         false,
        columnDefs: [
          {
            width: 600, targets: [26, 27, 28, 40],
          }
        ],
        fixedColumns:   {leftColumns: 2}
    } );

    var table = $('#matrixSummary').removeAttr('width').DataTable( {
        lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "All"]],
        deferRender:    true,
        scrollY:        "500px",
        scrollX:        true,
        scrollCollapse: true
    } );

    var table = $('#exampleActionPlan').removeAttr('width').DataTable( {
        lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "All"]],
        deferRender:    true,
        scrollY:        "500px",
        scrollX:        true,
        scrollCollapse: true,
        //paging:         false,
    } );

   
} );


$(document).ready(function() {
    $('#exampleItRisk').dataTable( {
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
        //"scrollY":        '300px',
        //"scrollX":        true,
        //scrollCollapse: true,
        paging:         true,
        bDestroy: true,
        deferRender:    true,
        scrollY:        "300px",
        scrollX:        true,
        scrollCollapse: true,
    } );
} );
