var request = require('request');

$(function() {
	function IndexViewModel() {
		this.searchTerm = ko.observable();
		this.results = ko.observableArray();
		
		this.search = function() {
			var vm = this;
			
		}
	}
	ko.applyBindings(new IndexViewModel());
});
