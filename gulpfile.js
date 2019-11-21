'use strict';

const {src, dest, watch, series, parallel} = require('gulp');
const sourcemaps = require('gulp-sourcemaps');
const sass = require('gulp-sass');
const postcss = require('gulp-postcss');
const autoprefixer = require('autoprefixer');
const cssnano = require('cssnano');

const files = {
  scssMainPath: './app/static/scss/main.scss',
  scssPath: './app/static/scss/**/*.scss',
  cssPath: './app/static/css'
};

function scssTaskDebug() {
  return src(files.scssMainPath)
    .pipe(sourcemaps.init())
    .pipe(sass())
    .pipe(sourcemaps.write('.'))
    .pipe(dest(files.cssPath))
}

function scssTask() {
  return src(files.scssMainPath)
    .pipe(sourcemaps.init())
    .pipe(sass())
    .pipe(postcss([autoprefixer(), cssnano()]))
    .pipe(sourcemaps.write('.'))
    .pipe(dest(files.cssPath))
}

function watchTask() {
  watch([files.scssPath], scssTask);
}

exports.scssDebug = scssTaskDebug;

exports.default = series(
  scssTask,
  watchTask
);
