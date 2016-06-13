'use strict';

const gulp           = require('gulp');
const gutil          = require('gulp-util');
const del            = require('del');
const concat         = require('gulp-concat');
const browserSync    = require('browser-sync').create();
const autoprefixer   = require('autoprefixer');
const postcss        = require('gulp-postcss');
const sass           = require('gulp-sass');
const sourcemaps     = require('gulp-sourcemaps');
const source         = require('vinyl-source-stream');
const buffer         = require('vinyl-buffer');
const browserify     = require('browserify');
const uglify         = require('gulp-uglify');
const cssnano        = require('gulp-cssnano');
const gulpif         = require('gulp-if');
const runSequence    = require('run-sequence');
const path           = require('path');


function bundle(options) {
  options = options || {};
  const bundlerOpts = { entry: true, debug: true };
  let bundler = browserify(
    './pyconguide/static_src/js/pycon-guide.js', bundlerOpts
    )
    .transform('babelify', { presets: ['es2015'] });

  function rebundle() {
    return bundler.bundle()
      .on('error', function(err) {
        gutil.log(gutil.colors.red(err.message));
        this.emit('end');
      })
      .pipe(source('bundle.js'))
      .pipe(buffer())
      .pipe(sourcemaps.init({ loadMaps: true }))
      .pipe(sourcemaps.write())
      .pipe(gulp.dest('./pyconguide/static/js/'));
  }

  if (options.watch) {
    const watchify = require('watchify');
    bundler = watchify(bundler);
    bundler.on('update', () => {
      gutil.log('-> bundling...');
      rebundle();
    });
  }

  return rebundle();
}

gulp.task('browserify', () => {
  return bundle();
});

gulp.task('watchify', () => {
  return bundle({ watch: true });
});

gulp.task('sass', () => {
  return gulp.src('./pyconguide/static_src/scss/**/*.scss')
    .pipe(sourcemaps.init())
    .pipe(sass(
      {
        includePaths: [path.join(path.dirname(require.resolve('foundation-sites')), '../scss')]
      }
    )
    .on('error', sass.logError))
    .pipe(postcss([autoprefixer]))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest('./pyconguide/static/css/'));
});

gulp.task('extras', () => {
  return gulp.src('./pyconguide/static_src/**/*.{txt,json,xml,jpeg,jpg,png,gif,svg,ttf,otf,eot,woff, woff2}')
    .pipe(gulp.dest('./pyconguide/static/'));
});

gulp.task('watch', ['sass', 'extras', 'watchify'], () => {
  browserSync.init({
    proxy: '127.0.0.1:8000'
  });
  gulp.watch('./pyconguide/static_src/scss/**/*.scss', ['sass']);
  gulp.watch('./pyconguide/static_src/**/*.{txt,json,xml,jpeg,jpg,png,gif,svg,ttf,otf,eot,woff, woff2}', ['extras']);
});

gulp.task('banner', ['browserify'], () => {
  return gulp.src(['./public/banner.txt', './pyconguide/static/js/bundle.js'])
    .pipe(concat('bundle.js'))
    .pipe(gulp.dest('./pyconguide/static/js/'));
});

gulp.task('minify', () => {
  return gulp.src(['./pyconguide/static/**/*'],
                  { base: './pyconguide/static/' })
    // Only target the versioned files with the hash
    // Those files have a - and a 10 character string
    .pipe(gulpif(/\.js$/, uglify()))
    .pipe(gulpif(/\.css$/, cssnano()))
    .pipe(gulp.dest('./pyconguide/static/'));
});

gulp.task('clean', () => {
  return del('./pyconguide/static/');
});

gulp.task('build', (done) => {
  runSequence(
    'clean',
    ['browserify', 'sass', 'extras'],
    done
  );
});

gulp.task('build:production', (done) => {
  runSequence(
    'build',
    ['banner', 'minify'],
    done
  );
});

gulp.task('start', (done) => {
  runSequence(
    'build',
    'watch',
    done
  );
});

gulp.task('default', ['build']);
