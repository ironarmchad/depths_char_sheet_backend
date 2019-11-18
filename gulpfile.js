'use strict';

const gulp = require('gulp');
const sass = require('gulp-sass');

sass.compiler = require('node-sass');

gulp.task('sass', function() {
    return gulp.src('./app/static/scss/main.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest('./app/static/css'))
});

gulp.task('sass:watch', function() {
    gulp.watch('./app/static/scss/**/*.scss', ['sass']);
});
