/**
 * @license Copyright (c) 2003-2021, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see https://ckeditor.com/legal/ckeditor-oss-license
 */

CKEDITOR.editorConfig = function( config ) {

    // allow all content apart from script tags - can be overridden on a case by case basis if required.
    config.allowedContent = {
        $1: {
            elements: CKEDITOR.dtd,
            attributes: true,
            styles: true,
            classes: true
        }
    };
    config.disallowedContent = 'script; *[on*]';
	config.extraPlugins = 'maximize';

    // toolbar
    config.toolbar =
    [
        { name: 'clipboard', items : [ 'Cut','Copy','Paste','PasteText','PasteFromWord','-','Undo','Redo' ] },
        { name: 'editing', items : [ 'SpellChecker', 'Scayt' ] },
        { name: 'links', items : ['Link','Unlink', 'Anchor']},
        { name: 'insert', items : [ 'Image', 'Table', 'HorizontalRule','SpecialChar', 'Maximise', 'Iframe'] },
        { name: 'document', items : [ 'Source', ] },
        '/',
        { name: 'basicstyles', items : [ 'Bold','Italic','Underline', 'Strike', '-', 'RemoveFormat' ] },
        { name: 'paragraph', items : [ 'NumberedList','BulletedList','-','Outdent','Indent','-', 'JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock' ] },
        { name: 'styles', items : [ 'Styles', 'Format', ] },
    ];

    config.skin = 'office2013';

    // set to whatever your file admin url is (if you install file browser)
    // config.filebrowserBrowseUrl = '/admin/cke-file-uploader/';
    // config.filebrowserImageBrowseUrl = '/admin/cke-image-uploader/';

    config.filebrowserWindowWidth= 325;
    config.filebrowserWindowHeight = 400;

    // Se the most common block elements.
    config.format_tags = 'p;h1;h2;h3;pre';

    // Make dialogs simpler.
    config.removeDialogTabs = 'image:advanced;link:advanced';
    config.width = '100%';

};
