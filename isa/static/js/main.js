$(function () {
    $( '#campaign_table' ).DataTable();
    
    $( '#campaign_table' ).css( {
        'width' : '1050px',
        'margin-top':'20px'
    } );

    $( 'input[type="search"]' ).css( {
        'float': 'right',
        'width': '800px'
    } );

    $( '#datetimepicker' ).datepicker();
} );