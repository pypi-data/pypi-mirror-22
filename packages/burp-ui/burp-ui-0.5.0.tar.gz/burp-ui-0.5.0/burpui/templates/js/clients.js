
/***
 * Here is the 'clients' part
 * It is available on the global clients view
 */

/***
 * First we map some burp status with some style
 */
var __status = {
	"{{ _('client crashed') }}": 'danger',
	"{{ _('server crashed') }}": 'danger',
	"{{ _('running') }}": 'info',
	"{{ _('idle') }}": 'idle',  // hack to manage translation
};

/***
 * Show the row as warning if there are no backups
 */
var __date = {
	"{{ _('never') }}": 'warning',
	"{{ _('now') }}": 'now',  // hack to manage translation
};

/***
 * _clients: function that retrieve up-to-date informations from the burp server
 * JSON format:
 * [
 *   {
 *     "last": "2014-05-12 19:40:02",
 *     "name": "client1",
 *     "state": "idle",
 *     "phase": "phase1",
 *     "percent": 12,
 *   },
 *   {
 *     "last": "never",
 *     "name": "client2",
 *     "state": "idle",
 *     "phase": "phase2",
 *     "percent": 42,
 *   }
 * ]
 *  The JSON is then parsed into a table
 */
{% import 'macros.html' as macros %}

{{ macros.timestamp_filter() }}

var _clients_table = $('#table-clients').dataTable( {
	{{ macros.translate_datatable() }}
	{{ macros.get_page_length() }}
	responsive: true,
	ajax: {
		url: '{{ url_for("api.clients_stats", server=server) }}',
		dataSrc: function (data) {
			return data;
		},
		error: myFail,
		headers: { 'X-From-UI': true },
	},
	order: [[2, 'desc']],
	destroy: true,
	rowCallback: function( row, data ) {
		if (__status[data.state] != undefined) {
			row.className += ' '+__status[data.state];
		}
		if (__date[data.last] != undefined) {
			row.className += ' '+__date[data.last];
		}
		row.className += ' clickable';
	},
	columns: [
		{
			data: null,
			render: function ( data, type, row ) {
				return '<a href="{{ url_for("view.client", server=server) }}?name='+data.name+'" style="color: inherit; text-decoration: inherit;">'+data.name+'</a>';
			}
		},
		{
			data: null,
			render: function ( data, type, row ) {
				if ('phase' in data && data.phase) {
					return data.state+' - '+data.phase+' ('+data.percent+'%)';
				}
				return data.state;
			}
		},
		{ 
			data: null,
			type: 'timestamp',
			render: function (data, type, row ) {
				if (!(data.last in __status || data.last in __date))
					return '<span data-toggle="tooltip" title="'+data.last+'">'+moment(data.last, moment.ISO_8601).format({{ g.date_format|tojson }})+'</span>';
				return data.last
			}
		},
		{
			data: null,
			render: function (data, type, row ) {
				var cls = '';
				var link_start = '';
				var link_end = '';
				var label = '';
				if (__date[data.last] == 'now' && __status[data.state] != 'idle') {
					cls = 'blink';
					link_start = '<a href="{{ url_for("view.live_monitor", server=server) }}/'+data.name+'">';
					link_end = '</a>';
					label = '&nbsp;{{ _("view") }}';
				}
				return link_start + '<span class="fa-stack" style="color: #000; text-align: center;"><i class="fa fa-square fa-stack-2x"></i><i class="fa fa-terminal fa-stack-1x fa-inverse ' + cls + '"></i></span>' + label + link_end;
			}
		}
	]
});
var first = true;

var _clients = function() {
	if (first) {
		first = false;
	} else {
		_clients_table.api().ajax.reload( null, false );
	}
};

{{ macros.page_length('#table-clients') }}

_clients_table.on('draw.dt', function() {
	$('[data-toggle="tooltip"]').tooltip();
});
