module.exports = (gulp, config) => {
  gulp.task('copy', gulp.parallel([
    'copyGov',
    'images'
  ]))

  gulp.task('build', gulp.series([
    'clean',
    'copy'
  ]))

  gulp.task('default', gulp.series([
    'build'
  ]))
}
