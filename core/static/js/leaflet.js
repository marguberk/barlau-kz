/* Leaflet Simplified - just enough to show map */
(function (global, factory) {
	typeof exports === 'object' && typeof module !== 'undefined' ? factory(exports) :
	typeof define === 'function' && define.amd ? define(['exports'], factory) :
	(factory((global.L = {})));
}(this, (function (exports) { 'use strict';

var version = "1.7.1";

/*
 * @namespace Util
 */
var Util = {
	// extend an object with properties of one or more other objects
	extend: function (dest) {
		var i, j, len, src;

		for (j = 1, len = arguments.length; j < len; j++) {
			src = arguments[j];
			for (i in src) {
				dest[i] = src[i];
			}
		}
		return dest;
	},

	create: Object.create || (function () {
		function F() {}
		return function (proto) {
			F.prototype = proto;
			return new F();
		};
	})(),

	bind: function (fn, obj) {
		var slice = Array.prototype.slice;

		if (fn.bind) {
			return fn.bind.apply(fn, slice.call(arguments, 1));
		}

		var args = slice.call(arguments, 2);

		return function () {
			return fn.apply(obj, args.length ? args.concat(slice.call(arguments)) : arguments);
		};
	}
};

// Simplified map implementation
function Map(id, options) {
	this._container = typeof id === 'string' ? document.getElementById(id) : id;
	this._options = options || {};
	this._layers = [];
	this._zoom = options.zoom || 10;
	this._center = options.center || [0, 0];
	
	this._initContainer();
	this._initEvents();
	
	console.log("Leaflet map created with mock implementation");
	
	return this;
}

Map.prototype = {
	setView: function(center, zoom) {
		this._center = center;
		this._zoom = zoom;
		return this;
	},
	
	addLayer: function(layer) {
		this._layers.push(layer);
		if (layer.onAdd) {
			layer.onAdd(this);
		}
		return this;
	},
	
	removeLayer: function(layer) {
		var idx = this._layers.indexOf(layer);
		if (idx !== -1) {
			this._layers.splice(idx, 1);
			if (layer.onRemove) {
				layer.onRemove(this);
			}
		}
		return this;
	},
	
	_initContainer: function() {
		var container = this._container;
		container.classList.add('leaflet-container');
		var mapDiv = document.createElement('div');
		mapDiv.style.width = '100%';
		mapDiv.style.height = '100%';
		mapDiv.style.backgroundColor = '#f2f2f2';
		mapDiv.innerHTML = '<div style="padding: 20px; text-align: center; color: #333;">' +
			'<h3>Карта Алматы</h3>' +
			'<p>Координаты центра: ' + this._center[0].toFixed(4) + ', ' + this._center[1].toFixed(4) + '</p>' +
			'<p>Масштаб: ' + this._zoom + '</p>' +
			'<p style="color: #666; margin-top: 15px;">Это упрощенная версия карты для демонстрации</p>' +
		'</div>';
		container.appendChild(mapDiv);
		this._mapDiv = mapDiv;
	},
	
	_initEvents: function() {
		// Simplified event handling
	},
	
	invalidateSize: function() {
		// Recalculate size if needed
		return this;
	}
};

// TileLayer class
function TileLayer(urlTemplate, options) {
	this._url = urlTemplate;
	this._options = options || {};
}

TileLayer.prototype = {
	onAdd: function(map) {
		this._map = map;
		// In a real implementation, this would add tiles to the map
		console.log("TileLayer added to map:", this._url);
	},
	
	onRemove: function(map) {
		this._map = null;
	}
};

// Marker class
function Marker(latlng, options) {
	this._latlng = latlng;
	this._options = options || {};
}

Marker.prototype = {
	addTo: function(map) {
		map.addLayer(this);
		return this;
	},
	
	onAdd: function(map) {
		this._map = map;
		// In a real implementation, this would add a marker to the map
		console.log("Marker added at:", this._latlng);
	},
	
	onRemove: function(map) {
		this._map = null;
	},
	
	setLatLng: function(latlng) {
		this._latlng = latlng;
		return this;
	},
	
	bindPopup: function(content) {
		this._popupContent = content;
		return this;
	},
	
	openPopup: function() {
		// Open the popup in a real implementation
		return this;
	}
};

// Circle class
function Circle(latlng, options) {
	this._latlng = latlng;
	this._options = options || {};
	this._radius = options.radius || 10;
}

Circle.prototype = {
	addTo: function(map) {
		map.addLayer(this);
		return this;
	},
	
	onAdd: function(map) {
		this._map = map;
		// In a real implementation, this would add a circle to the map
		console.log("Circle added at:", this._latlng, "with radius:", this._radius);
	},
	
	onRemove: function(map) {
		this._map = null;
	}
};

// Icon class
function Icon(options) {
	this._options = options || {};
}

// DivIcon class
function DivIcon(options) {
	this._options = options || {};
}

// Expose the classes
exports.Map = Map;
exports.map = function(id, options) {
	return new Map(id, options);
};

exports.TileLayer = TileLayer;
exports.tileLayer = function(urlTemplate, options) {
	return new TileLayer(urlTemplate, options);
};

exports.Marker = Marker;
exports.marker = function(latlng, options) {
	return new Marker(latlng, options);
};

exports.Circle = Circle;
exports.circle = function(latlng, options) {
	return new Circle(latlng, options);
};

exports.Icon = Icon;
exports.icon = function(options) {
	return new Icon(options);
};

exports.DivIcon = DivIcon;
exports.divIcon = function(options) {
	return new DivIcon(options);
};

exports.version = version;
exports.noConflict = function() { return this; };

Object.defineProperty(exports, '__esModule', { value: true });

}))); 