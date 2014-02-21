module.exports = function(grunt) {
    // Config
    grunt.initConfig({
        less: {
            development: {
                options: {
                    paths: ["./assets/less/*", "./assets/less/preboot"],
                    yuicompress: true
                },
                files: {
                    "./assets/css/main.css": "./assets/less/main.less",
                    "./assets/css/flat-ui.css": "./assets/less/flat-ui/flat-ui.less"
                }
            }
        },
        // running `grunt watch` will watch for changes
        watch: {
            files: ["./assets/less/*.less", "./assets/less/layout/*.less"],
            tasks: ["less"]
        }
    });

    // Loading tasks
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-watch');

    // Custom tasks
    grunt.registerTask('dev-default', ['watch']);
};
