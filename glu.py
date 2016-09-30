#!python

# for GHEdit comment
import sys, getopt, os
from pydispatch import dispatcher
import gluserver
import glugit

def usage():
	print 'Usage : glu [<options>]... [<query>] [<repository>]'
	print '\t-h, --help\t\tPrint this message.'
	print '\t-s, --server\t\tExcute with server-mode.'
	print '\t-q\t\t\tQuery string'
	pass


def vers_major():
	return 0


def vers_minor():
	return 1


def vers_release():
	return "a"

def query_handle(sender):
	if (sender['signal'] == glugit.MESSAGE):
		print "event {0} - {2}\n\t{1}".format(sender['signal'], sender['message'], sender['commit'])
	elif sender['signal'] == glugit.DIFF:
		print "event ({0})".format(sender['signal'])
	elif sender['signal'] == glugit.END:
		print "event End..."

def main(argv):
	query = ''
	isServer = False
	repositorySrc = ''
	try:
		opts, args = getopt.getopt(argv, "hs:", ["help", "server"])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit(2)
		elif opt in ("-s", "--server"):
			isServer = True
	if (len(args) > 0):
		if len(args) == 1:
			query = args[0]
		if len(args) == 2:
			query, repositorySrc = args[0:2]

	print 'GLU (v{0}.{1}{2}) start...'.format(vers_major(), vers_minor(), vers_release());

	if repositorySrc == '':
		repositorySrc = os.path.abspath(".")
	else:
		repositorySrc = os.path.abspath(repositorySrc)
	if isServer:
		gluserver.doServer(repositorySrc)
	else:
		if query == '':
			usage()
			sys.exit(2)
		mygit = glugit.Git(repositorySrc)
		mygit.doQuery(query, query_handle, s_scope=glugit.Scope.Month)


if __name__ == "__main__":
	main(sys.argv[1:])
