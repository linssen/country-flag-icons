module.exports = function (grunt) {
    'use strict';

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        grunticon: {
            dist: {
                options: {
                    src: 'images/svg',
                    dest: 'images/css',
                    pngfolder: '../png'
                }
            }
        }

    });

    grunt.loadNpmTasks('grunt-grunticon');

    grunt.registerTask('default', ['grunticon', 'preview']);
    grunt.registerTask('preview', 'Creates a preview of all flags', function () {
        var countries, preview;
        countries = JSON.parse(grunt.file.read('countries.json'));
        preview = grunt.template.process(
            grunt.file.read('preview.tpl'),
            {data: {countries: countries}}
        );
        grunt.file.write('preview.html', preview);
        grunt.log.writeln('Preview of flags built');
    });

};