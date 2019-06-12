const gulp = require('gulp')

const config = require('./gulp/config.js')

require('./gulp/tasks/clean.js')(gulp, config)
require('./gulp/tasks/gov.js')(gulp, config)
require('./gulp/tasks/images.js')(gulp, config)
require('./gulp/tasks/linting.js')(gulp, config)
require('./gulp/tasks/default.js')(gulp, config)
require('./gulp/tasks/watch.js')(gulp, config)
