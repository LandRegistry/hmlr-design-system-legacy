const path = require('path')

module.exports = (gulp, config) => {
  gulp.task('appImages', () =>
    gulp
      .src(path.join(config.sourcePath, 'images/**'))
      .pipe(gulp.dest(path.join(config.destinationPath, 'images/app')))
  )

  gulp.task('patternLibraryImages', () => {
    const patternLibraryPath = '.'

    return gulp
      .src(path.join(patternLibraryPath, 'hmlr_design_system/components/**/*.{gif,png,jpg,jpeg,svg}'))
      .pipe(gulp.dest(path.join(config.destinationPath, 'images/hmlr-hmlr-design-system')))
  })

  gulp.task('images', gulp.parallel(['appImages', 'patternLibraryImages']))
}
