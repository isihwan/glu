var stdio = require('stdio');
var sys = require('sys');
var gitkit = require('gitkit/gitkit');
var report = require('gitkit/report');

var ops = stdio.getopt({
	'server': {key: 's', description: 'Excute for server-mode'}
});

if (!ops.server && (!ops.args || ops.args.length > 1)) {
	ops.printHelp();
}

if (ops.server) {
	doServer(ops);
}
else {
	var targetQuery = ops.args[0];
	sys.debug("Query = " + ops.args[0]);
	var gitkitInstance = gitkit.createInstance();
	gitkitInstance.q(targetQuery, gitkit.QueryOption.GO_FINISH);
	
	var rep = report.newConsole();
	gitkitInstance.eventer.on('Log', function (answer) {
		sys.debug("IN_LOG : " + answer.head);
		rep.log(answer);
	});
	gitkitInstance.eventer.on('Diff', function (answer) {
		sys.debug("IN_DIFF : " + answer.diff_file);
		rep.diff(answer);
	});
	gitkitInstance.eventer.on('Finish', function () {
		console.log("End.");
	});
}

