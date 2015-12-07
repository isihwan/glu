from git import Repo
from pydispatch import dispatcher
from enum import Enum
import datetime
import fnmatch, re
import logging

logging.basicConfig(level=logging.WARNING)

MESSAGE = "message"
DIFF = "diff"
END = "end"

class Scope(Enum):
	Week = 7
	Month = 30
	Year = 365


def make_after_date(before):
	now = datetime.datetime.now()
	after = now - datetime.timedelta(before)
	return '{0}-{1}-{2}'.format(after.year, after.month, after.day)


class Git:
	def __init__(self, repositorySrc):
		self.repo = Repo(repositorySrc)

	def make_query(self, src):
		query_glob = fnmatch.translate("*" + src + "*");
		return re.compile(query_glob)

	def doQuery(self, query, message_h, diff_h=None, end_h=None, s_scope=Scope.Week, author=""):
		dispatcher.connect(message_h, signal=MESSAGE, sender=dispatcher.Any)
		query_regex = self.make_query(query)
		if (diff_h == None): dispatcher.connect(message_h, signal=DIFF)
		else: dispatcher.connect(diff_h, signal=DIFF)
		if (end_h == None): dispatcher.connect(message_h, signal=END);
		else: dispatcher.connect(end_h, signal=END)

		scan_commits = []
		kwargs = {}
		kwargs['after'] = make_after_date(s_scope);
		if author != "": kwargs['author'] = author
		logging.info("kwargs : %s", kwargs.__str__())
		for commit in self.repo.iter_commits(**kwargs):
			scan_commits.append(commit)
		# check in head
		for commit in scan_commits:
			logging.debug("scaned %s", commit.message)
			m = query_regex.match(commit.message)
			if m:
				dispatcher.send(signal=MESSAGE, sender={'signal': MESSAGE})
		for commit in scan_commits:
			pass
		dispatcher.send(signal=END, sender={'signal': END})
