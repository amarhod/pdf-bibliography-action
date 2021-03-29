const core = require('@actions/core')
const github = require('@actions/github')

try {
  console.log('Simple test')
}catch(e) {
    core.setFailed(e.message)
}