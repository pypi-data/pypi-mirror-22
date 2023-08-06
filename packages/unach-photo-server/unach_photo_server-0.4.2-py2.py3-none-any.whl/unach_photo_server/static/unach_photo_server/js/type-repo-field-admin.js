/**
 * Created by javier on 25-04-17.
 */
(function($) {
    $(function() {

        var fieldsFileSystem = [
          $('#id_user_id'),
          $('#id_password'),
          $('#id_client_machine_name'),
          $('#id_server_name'),
          $('#id_domain'),
          $('#id_server_ip'),
          $('#id_service_name'),
          $('#id_path')
        ];

        var fieldsDatabase = [
          $('#id_engine'),
          $('#id_database_name'),
          $('#id_database_user'),
          $('#id_database_password'),
          $('#id_database_host'),
          $('#id_database_port'),
          $('#id_database_column_search'),
          $('#id_database_table_search'),
          $('#id_database_column_filter'),
          $('#id_is_blob')
        ];

        var repo_type = $('#id_repo_type');

        function hideShowFields(fields, show){
            for (var i = 0; i< fields.length; i++){
                    if(show === true) {
                        $(".field-" + fields[i].attr('name')).show();
                    }else{
                        $(".field-" + fields[i].attr('name')).hide();
                    }
                }
        }

        function toggleFields(value) {
            if(value === 'file_system') {
                hideShowFields(fieldsDatabase, false);
                hideShowFields(fieldsFileSystem, true);
            }else if(value === 'database') {
                hideShowFields(fieldsFileSystem, false);
                hideShowFields(fieldsDatabase, true);

            }else{
                hideShowFields(fieldsFileSystem, false);
                hideShowFields(fieldsDatabase, false);
            }
        }
        // set onInit
        toggleFields(repo_type.val());

        // show/hide on change
        repo_type.change(function() {
            toggleFields($(this).val());
        });

    });
})(django.jQuery);
