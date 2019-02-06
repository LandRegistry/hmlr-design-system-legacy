module.exports = (gulp, config) => {
  gulp.task('copy', gulp.parallel([
    'copyGov',
    'jquery',
    'images'
  ]))

  gulp.task('compile', gulp.parallel([
    'sass',
    'js',
    'js-vendor'
  ]))

  gulp.task('build', gulp.series([
    'clean',
    gulp.parallel([
      'copy',
      'compile'
    ])
  ]))

  gulp.task('default', gulp.series([
    'build'
  ]))
}
