/* -*- coding: utf-8 -*-
* ----------------------------------------------------------------------------
* Copyright (c) 2017 - Chris Kirby
*
* Distributed under the terms of the Modified BSD License.
*
* An IPython notebook extension to drag inputs and prompts for presentation.
* -----------------------------------------------------------------------------
*/

define([
'jquery',
'notebook/js/celltoolbar'
], 
function ($, celltoolbar){
	"use strict";

	var ctb = celltoolbar.CellToolbar;

	$('#notebook-container').sortable({
		// connectWith: ".cell"
	});

	function getter(cell){
		var cb = cell.metadata.corkboard;
		adjust(cell);
		return (cb == undefined)? undefined: cb.width
	}

	function setter(cell, value){
		if (cell.metadata.corkboard == undefined){cell.metadata.corkboard = {}}
		cell.metadata.corkboard.width = value;
		adjust(cell);
		// console.log(value);
	}

	function adjust(cell){
		var cb = cell.metadata.corkboard;
		if(cb && cb.width){
			$(cell.element).css('width', cb.width);
			$(cell.element).css('float', 'left' );
		}
	}

	var sizes = [['100%', '100%'], ['50%', '50%']]

	var select = ctb.utils.select_ui_generator(sizes, setter, getter);

	function load_ipython_extension(){
		ctb.register_callback('corkboard.select', select);
		ctb.register_preset('Corkboard', ['corkboard.select']);

		$.each(Jupyter.notebook.get_cells(), function(index, cell){
	    	adjust(cell);
	    });

		console.log('Corkboard setup complete.');
	}

	return { load_ipython_extension: load_ipython_extension }
});

