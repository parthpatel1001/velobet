/* 
Paste this scrip in chrome console on the page where you pick players
*/
var category = 'Wildcard Rider';
$('button[title="'+category+'"]').siblings('div').children('ul').children('li').each(function (i) {
	var row = $(this);
	if (row.attr('rel') != 0 ) {
		var pieces = $.map(row.text().split('|'), $.trim).join(",");
		var row = category + "," + pieces;

		console.log(row)	
	}
	
});