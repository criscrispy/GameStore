# Load all required libraries.
gulp    = require('gulp')
sass    = require('gulp-sass')
plumber = require('gulp-plumber')
clean   = require('gulp-clean')
rename  = require('gulp-rename')
cssmin  = require('gulp-clean-css')
concat  = require('gulp-concat')
cssurls = require('gulp-modify-css-urls')

# -----
# Tasks
# -----

gulp.task "sass", ->
  gulp.src "./gamestore/sass/main.{scss,sass}"
    .pipe sass()
    .pipe cssmin()
    .pipe rename({extname: ".min.css"})
    .pipe gulp.dest("./gamestore/static/css")


defaultTasks = [ 'sass'];
gulp.task('default', defaultTasks);
