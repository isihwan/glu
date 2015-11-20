var stdio = require('stdio');
var ops = stdio.getopt({
	'server': {key: 's', description: 'Excute for server-mode'}
});

if (!ops.args || ops.args.length > 1) {
	ops.printHelp();
}

var targetGitPath = ops.args[0];
