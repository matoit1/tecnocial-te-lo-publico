"use strict";
module.exports = function( grunt ) {

    grunt.loadNpmTasks( "grunt-contrib-compass" );
    grunt.loadNpmTasks( "grunt-contrib-coffee" );
    grunt.loadNpmTasks( "grunt-contrib-watch" );
    grunt.loadNpmTasks( "grunt-concurrent" );
    grunt.loadNpmTasks( "grunt-newer" );
    grunt.loadNpmTasks( "grunt-exec" );

    grunt.initConfig( {

        exec: {

            startServer: {
                cmd: function() {
                    return ". venv/bin/activate\npython app/App.py"
                }
            },

            redis: {
                cmd: function() {
                    return "~/www/redis/src/redis-server"
                }
            }

        },

        concurrent: {
            devServer: {
                tasks: ["exec:startServer", "exec:redis", "watch"],
                options: {
                    logConcurrentOutput: true
                }
            }
        },

        compass: {
            dev: {
                options: {
                    basePath: "app",
                    sassDir: "static/styles/sass",
                    cssDir: "static/styles/css",
                    environment: "development",
                    imagesDir: "static/images",
                    outputStyle: "expanded",
                    noLineComments: true,
                    relativeAssets: true,
                    force: true
                }
            }
        },

        coffee: {
        default: {
            options: {
                sourceMap: true
            },
            expand: true,
            cwd: "app/static/scripts/coffee/",
            src: "**/**.coffee",
            dest: "app/static/scripts/js",
            ext: ".js"
        }
        },
        watch: {
            compass: {
                files: [ "app/static/styles/sass/**/*.{scss,sass}" ],
                tasks: "compass:dev",
                options: {
                    debounceDelay: 200
                }
            },
            coffee: {
                files: [ "app/static/scripts/coffee/**/*.coffee" ],
                tasks: "newer:coffee",
                options: {
                    debounceDelay: 200
                }
            }
        }

    } );

    // Run compass, coffee, and start it all up
    grunt.registerTask( "start", [
        "compass:dev",
        "coffee",
        "concurrent:devServer"
    ]);

    grunt.registerTask( "default", [ "start" ] );

};
