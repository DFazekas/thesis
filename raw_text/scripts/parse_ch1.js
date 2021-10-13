const Promise = require('bluebird')
const fs = Promise.promisifyAll(require('fs'))

function transcribeToLatex({ inputPath, outputPath }) {
  fs.readFileAsync(inputPath)
    .then((data) => {
      // Match the replace tags.
      const fromPattern = /^# ([\w\s]+)\n/

      // Transform data Buffer to string.
      let fileContents = data.toString()
      let matches = fileContents.match(fromPattern)
      matches = matches.slice(1)
      console.log('matches:\n')
      console.log(matches)

      return [fileContents, matches]
    })
    .spread((fileContent, matches) => {
      console.dir(matches)
      // Set string template to replace.
      const toPattern = `\\chapter{${matches[0]}}`
      return fs.writeFileAsync(
        outputPath,
        fileContent.replace(matches[0], toPattern)
      )
    })
    .then(() => {
      console.log(`Overwrote file: ${outputPath}`)
    })
    .catch((err) => {
      throw err
    })
}

transcribeToLatex({
  inputPath:
    '/Users/tribalscale/Documents/thesis/thesis/raw_text/chap2_Literature_Review.txt',
  outputPath:
    '/Users/tribalscale/Documents/thesis/thesis/texStudio/chap2_Literature_Review.tex'
})
