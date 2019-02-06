const path = require('path')
const fs = require('fs')
const es = require('event-stream')
const filter = require('gulp-filter')

module.exports = (gulp, config) => {
  const govukTemplatePath = path.dirname(require.resolve('govuk-frontend/README.md'))

  const templateFilter = filter([
    '**',
    '!**/components/**/template.njk' // We want everything *except* the templates (i.e. just the macros)
  ])

  gulp.task('copyGovTemplates', () => {
    return gulp
      .src(path.join(govukTemplatePath, '**/*.njk'))
      .pipe(templateFilter)
      .pipe(es.map(function (file, cb) {
        var contents = file.contents.toString()

        // "Unwrap" the include directly inside the macro since it causes problems in Jinja,
        // and the only reason it's done this way is for the govuk design system's demo code
        const matches = contents.match(/(?:{%-? include ['"](.*)["'] -?%})/)

        if (matches) {
          const includePath = path.join(path.dirname(file.path), matches[1])
          const templateContents = fs.readFileSync(includePath)
          contents = contents.replace(matches[0], templateContents)
        }

        // Rename file
        file.path = file.path.replace('.njk', '.html')

        // Simple conversions from nunjucks/js to jinja/python
        contents = contents.replace(/true/g, 'True')
        contents = contents.replace(/false/g, 'False')
        contents = contents.replace(/\.njk/g, '.html')

        // Quoting dict keys, because nunjucks doesn't require them but jinja does
        contents = contents.replace(/^([ ]*)([^ '"#\r\n:]+?)\s*:/gm, "$1'$2':")

        // Gov template uses .items, which is a reserved word in python
        contents = contents.replace(/\.items/g, "['items']")

        // No such thing as elseif - it's elif in Python
        contents = contents.replace(/elseif/g, 'elif')

        // Python doesn't like inline ifs that don't have elses
        // See phase banner for example
        contents = contents.replace(/\b(.+) if \1(?! else)/g, "$1 if $1 else ''")

        // Concatenating loop index onto strings doesn't work implicitly in Python
        // Jinja has a specific operator for doing this
        contents = contents.replace(/\+ loop.index/g, '~ loop.index')

        // Remove all indentation and trimming which causes problems in jinja whereby the
        // indent filter fails to mark stuff as safe, and instead escapes the html special characters
        // In addition, this kind of formatting is not necessary in production code and is an unnecessary overhead
        contents = contents.replace(/\s?\|\s?trim/g, '', contents)
        contents = contents.replace(/\s?\|\s?indent(?:[(\d)]*)/g, '', contents)

        // Additional code needed for looping over dicts in python
        // Adds in the .items() suffix, but also guards against iterating over empty dicts which is something
        // that you can "get away with" in JS but not Python
        contents = contents.replace(/in (.*).attributes %}/g, 'in ($1.attributes.items() if $1.attributes else {}.items()) %}', contents)

        // Resolve paths to the templates as jinja does not support relative paths as nunjucks does
        contents = contents.replace(/\.\.\//g, 'app/vendor/.govuk-frontend/' + path.relative(govukTemplatePath, path.dirname(path.resolve(file.path, '..'))) + '/')
        contents = contents.replace(/\.\//g, 'app/vendor/.govuk-frontend/' + path.relative(govukTemplatePath, path.dirname(file.path)) + '/')

        // Hardcoded replacements for deeply nested dict access, which requires
        // more protection in Python than it does in JS
        // Not perfect to have to keep this hardcoded here, but at the time of writing, there's only a handful of examples
        const replacements = {
          'if params.formGroup.classes': 'if params.formGroup and params.formGroup.classes',
          'params.hint.classes': '(params.hint.classes if params.hint and params.hint.classes)',
          'item.hint.text': '(item.hint.text if item.hint and item.hint.text)',
          'item.hint.html': '(item.hint.html if item.hint and item.hint.html)',
          'item.label.attributes': '(item.label.attributes if item.label and item.label.attributes)',
          "(' ' + item.label.classes if item.label.classes else '')": "(' ' + item.label.classes if item.classes and item.label.classes else '')",
          "' govuk-textarea--error' if params.errorMessage": "' govuk-textarea--error' if params.errorMessage else ''"
        }

        for (const key in replacements) {
          contents = contents.replace(key, replacements[key])
        }

        file.contents = Buffer.from(contents, 'utf8')
        cb(null, file)
      }))

      .pipe(gulp.dest(path.join(config.applicationPath, 'templates/vendor/.govuk-frontend')))
  })

  gulp.task('copyGovAssets', () =>
    gulp
      .src(path.join(govukTemplatePath, 'assets/**/*.*'))
      .pipe(gulp.dest(path.join(config.destinationPath, '.govuk-frontend')))
  )

  gulp.task(
    'copyGov',
    gulp.parallel([
      'copyGovTemplates',
      'copyGovAssets'
    ])
  )
}
