'use strict';

import { elemGenerator } from 'https://javajawa.github.io/elems.js/elems.js';

const style = elemGenerator( 'style' );
const UUID  = /^#[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$/;

function getUUIDs()
{
	const raw = localStorage.getItem( 'uuids' );

	if ( ! raw )
	{
		return [];
	}

	return JSON.parse( raw );
}

function addUUID( uuid )
{
	let set = getUUIDs();

	set.push( uuid );
	set = set.filter( (v, i, a) => a.indexOf(v) === i );

	localStorage.setItem( 'uuids', JSON.stringify( set ) )
}

export function addHighlights()
{
	if ( UUID.test( location.hash ) )
	{
		addUUID( location.hash.substring( 1 ) );
	}

	document.head.appendChild(
		style( '.highlight { stroke: #44cc88; stroke-width: 2; }' )
	);

	getUUIDs()
		.forEach( uuid => fetch( `./${uuid}.json` )
		.then( r => r.json() )
		.then( r => r.forEach(
			eventId => document.querySelectorAll( `[data-id="${eventId}"]` ).forEach(
				elem => elem.classList.add( 'highlight' )
			)
		) )
	);
}
