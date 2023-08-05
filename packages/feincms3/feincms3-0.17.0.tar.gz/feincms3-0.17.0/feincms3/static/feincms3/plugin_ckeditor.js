/* global django, CKEDITOR */
(function($) {
    // Activate and deactivate the CKEDITOR because it does not like
    // getting dragged or its underlying ID changed
    // 'processed'-property is (un)set for compatibility with ckeditor-django
    $(document).on(
        'content-editor:activate',
        function(event, $row, formsetName) {
            $row.find('textarea[data-type=ckeditortype]').each(function() {
                if($(this).data('processed') == "0"){
                    $(this).data('processed',"1");
                    $($(this).data('external-plugin-resources')).each(function(){
                        CKEDITOR.plugins.addExternal(this[0], this[1], this[2]);
                    });
                    CKEDITOR.replace(this.id, $(this).data('config'));
                }
            });
        }
    ).on(
        'content-editor:deactivate',
        function(event, $row, formsetName) {
            $row.find('textarea[data-type=ckeditortype]').each(function() {
                try {
                    CKEDITOR.instances[this.id] && CKEDITOR.instances[this.id].destroy();
                    $(this).data('processed',"0");
                } catch(err) {}
            });
        }
    );
})(django.jQuery);
