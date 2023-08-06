
var hot = null;
var csrftoken = null;

function replaceTag(tag) {
	var tagsToReplace = {
		'&': '&amp;',
		'<': '&lt;',
		'>': '&gt;'
	};
	console.log('replaceTag',tag);
	return tagsToReplace[tag] || tag;
}
function safe_tags_replace(str) {
	//console.log('safe_tags_replace',str);
	return str.replace(/[&<>]/g, replaceTag);
}
function customRenderer (instance, td, row, col, prop, value, cellProperties) {
	//console.log('customRenderer');
	//console.log('  value      ',value);
	//console.log('  value type ',typeof value);

	var v = null;

	if(typeof value == 'string') {
		console.log('renderer got string value');
		console.log(value);
		v = value;

		//console.log('error!');
		//alert('error!');
		
		//var j = JSON.parse(value);
		//var j = value;

		//console.log('  object     ',j);
		//var escaped = Handsontable.helper.stringify(j[1]);
		//var escaped = escape(j[1]);
		//var escaped = j[1];
		//var escaped = safe_tags_replace(j[1]);
		//console.log('  escaped    ',escaped);
		//v = escaped;
     	} else if(value == null) {
		//console.log('renderer: value is null');
		// encountered when dragging to create new rows
		v = '';
	} else if(typeof value == 'object') {
		v = value[1];
	} else {
		console.log('error!');
		console.log('value:', value);
	}

	td.innerHTML = v;

	//console.log('display');
	//console.log(v);

	//Handsontable.renderers.TextRenderer.apply(this, arguments);
}

function apply_data(data_new) {
	//console.log(data_new.cells);

	data_hot.splice(0, data_hot.length);

	data_new.cells.forEach(function(c) {
		var c_new = c.map(function(e) {
			return JSON.parse(e);
		});
		data_hot.push(c_new);
	});
	
	hot.render();
}
function apply_sheet_data(data_new) {
	console.log('apply_sheet_data', data_new);
        apply_data(data_new);
        $("#script_pre").val(data_new.script_pre);
        $("#script_pre_output").val(data_new.script_pre_output);
        $("#script_post").val(data_new.script_post);
        $("#script_post_output").val(data_new.script_post_output);
}
function apply_script_post_output(data_new) {
        $("#script_post_output").val(data_new.script_post_output);
}
function get_sheet_data() {
        var post_data = {
		'csrfmiddlewaretoken':csrftoken,
		'sheet_id': sheet_id,
	};
	var jqxhr = $.post(url_get_sheet_data, post_data, apply_sheet_data).fail(function() {
		console.log("get sheet data ajax post fail");
	});
}
function sheet_page_load() {

	csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

	var container = document.getElementById('tablediv');

	var hooks = Handsontable.hooks.getRegistered();

	console.log(hooks);

	hot = new Handsontable(container, {
		data: data_hot,
		rowHeaders: true,
		colHeaders: true,
		cells: function (row, col, prop) {
			this.renderer = customRenderer;
		}
		//columns: [{renderer:customRenderer}]
	});

	hooks.forEach(function(h) {
		var ignore = [
			"beforeOnCellMouseOver",
			"afterOnCellMouseOver",
			"beforeOnCellMouseOut",
			"afterOnCellMouseOut",
			"beforeOnCellMouseDown",
			"afterOnCellMouseDown",
			"beforeDrawBorders",
			"modifyColWidth",
			"modifyRowHeaderWidth",
			"afterGetRowHeaderRenderers",
			"afterGetColumnHeaderRenderers",
			"afterDocumentKeyDown",
			"beforeKeyDown",
		];

		//if(ignore.indexOf(h) > -1) return;
		return
		
		hot.addHook(h, function() {
			console.log(h);
		});
	});

	hot.addHook('beforeCopy', function(data, coords) {
		console.log('beforeCopy');
		console.log(data);
		console.log(coords);
		/*
		var d = arguments[0].map(function(r){
			return r.map(function(c){
				return c[0];
			});
		});*/
		var data_new = data.map(function(c){
			return c.map(function(v){
				console.log(v);
				return v[0];
			})
		});

		console.log(data_new);

		data.splice(0,data.length);
	
		data_new.forEach(function(c) {
			data.push(c);
		});

	});

	hot.addHook('afterCopy', function(data, coords) {
		console.log('afterCopy');
		console.log(data);
	});

	hot.addHook('modifyData', function() {
		if(arguments[3] == 'set') {
			console.log('modifyData -----------------------');
			console.log(arguments);
			//var o = arguments[2];
			//o.value = JSON.stringify([o.value,'']);
		}
	});

	hot.addHook('afterSetDataAtCell', function() {
		console.log('afterSetDataAtCell -----------------------');
		console.log(arguments);
	});

	hot.addHook('beforeValidate', function() {
		console.log('beforeValidate -----------------------');
	});

	hot.addHook('afterValidate', function() {
		console.log('afterValidate -----------------------');
	});

	hot.addHook('afterBeginEditing', function() {
	});

	get_sheet_data();
	
	$("#button_ws_connect").click(function () {
		console.log("button_ws_connect");
		// Create WebSocket connection.
		ws = new WebSocket(ws_url);

		ws.onclose = function (event) {
			console.log('closed', event);
		};

		ws.onerror = function (event) {
			console.log('error', event);
		};

		// Connection opened
		ws.onopen = function (event) {
			console.log('open');
		};
		$("#button_ws_send").click(function () {
			console.log('readyState', ws.readyState);
			ws.send('hello');
		});
	});

	// Create WebSocket connection.
	const socket = new WebSocket(ws_url);

	socket.onclose = function (event) {
		console.log('closed', event);
	};

	socket.onerror = function (event) {
		console.log('error', event);
	};

	// Connection opened
	socket.onopen = function (event) {
		console.log('open. readyState=',socket.readyState);

		data = {
			'type': 'get_sheet_data',
			'book_id': book_id,
			'sheet_id':sheet_id
		};
		
		console.log('send', data);
		
		socket.send(JSON.stringify(data));
	};

	// Listen for messages
	socket.addEventListener('message', function (event) {
		console.log('Message from server', event.data);
		data = JSON.parse(event.data);

		if(data.type == 'response_sheet_data')
		{
			apply_sheet_data(data);
		}
	});
	
	// define button callbacks
	$("#button_add_col").click(function () {
		socket.send(JSON.stringify({
			'type':'add_col',
			'book_id':book_id,
			'sheet_id':sheet_id,
			'i':null
		}));
	});
	
	$("#button_add_row").click(function () {
		socket.send(JSON.stringify({
			'type':'add_row',
			'book_id':book_id,
			'sheet_id':sheet_id,
			'i':null
		}));
	});

	$("#button_script_pre").click(function () {
		var text = $("#script_pre").val();
		var data = {
			'type':'set_script_pre',
			'csrfmiddlewaretoken':csrftoken,
			'book_id':book_id,
			'sheet_id': sheet_id,
			'text':text 
		};
		socket.send(JSON.stringify(data));
	});

	$("#button_script_post").click(function () {
		var text = $("#script_post").val();
		var data = {
			'type':'set_script_post',
			'csrfmiddlewaretoken':csrftoken,
			'book_id':book_id,
			"sheet_id": sheet_id,
			'text': text 
		};
		socket.send(JSON.stringify(data));
	});

	hot.addHook('afterChange', function() {
		console.log('afterChange');

		arguments[0].forEach(function(args) {
			console.log(args);
			var data = {
				'type':'set_cell',
				'book_id':book_id,
				"sheet_id": sheet_id,
				'csrfmiddlewaretoken': csrftoken,
				'r': args[0],
				'c': args[1],
				's': args[3]
			};
			socket.send(JSON.stringify(data));
		});
	});
}



