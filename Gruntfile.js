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

    grunt.registerTask('default', ['grunticon']);

};