'use strict';

import { SLOTS, SCALE, HALFSCALE, QUARTSCALE, DAYS } from './config.js';
import { elemGenerator } from 'https://javajawa.github.io/elems.js/elems.js';
import { Event } from './events.js';
import { getWeek, getStartOfWeek, isoDateString } from './dates.js';
import { addHighlights } from './highlight.js';

const svg   = elemGenerator( 'svg', 'http://www.w3.org/2000/svg' );
const path  = elemGenerator( 'path', 'http://www.w3.org/2000/svg' );
const text  = elemGenerator( 'text', 'http://www.w3.org/2000/svg' );

function dayOfWeekHeader(n, i)
{
	return text(
		{
			x: ( SCALE * SLOTS * i + HALFSCALE * SLOTS ),
			y: -2,
			'text-anchor': 'middle'
		},
		n
	);
}

function dayDivider( i, height )
{
	return path( { d: `M${SCALE*SLOTS*i}-${SCALE}v${height}` } );
}

function weekHeader( n, i )
{
	const week = n % 53;
	const year = 2000 + Math.floor( n / 53 );

	return text(
		{
			x: -4,
			y: SCALE * i + 12,
			'text-anchor': 'end',
			title: ''
		},
		isoDateString( getStartOfWeek( year, week ) )
	);
}

function weekBackground( i, width, background )
{
	background = background || 'rgba( 80, 80, 80, 0.4 )';

	return path( {
		d: `M${-4*SCALE},${i * SCALE}v${SCALE}h${width}v${-SCALE}z`,
		style: `fill: ${background}; stroke: none;`
	} );
}

function eventPath( event, ...points )
{
	return path(
		{
			'data-id': event.id,
			class: event.class,
			title: event.title || '',
			'd': points.join('')
		}
	);
}

function makeEvent( e, firstWeek )
{
	const startWeek = e.start.week - firstWeek;
	const endWeek   = e.end.week   - firstWeek;

	if ( endWeek < 0 )
	{
		return [];
	}

	let midline = startWeek * SCALE + HALFSCALE;
	let left    = e.start.getLeft();
	let right   = e.end.getRight();
	let bar;

	if ( startWeek === endWeek )
	{
		bar = right - left - HALFSCALE;

		return eventPath(
			e,
			`M${left},${midline}`,
			`l${QUARTSCALE},${QUARTSCALE}`,
			`h${bar}`,
			`l${QUARTSCALE},${-QUARTSCALE}`,
			`l${-QUARTSCALE},${-QUARTSCALE}`,
			`h${-bar}z`
		);
	}

	let paths = [];

	bar = SCALE * SLOTS * DAYS.length - left - QUARTSCALE;

	paths.push(
		eventPath(
			e,
			`M${left},${midline}`,
			`l${QUARTSCALE},${QUARTSCALE}`,
			`h${bar}`,
			`v${-HALFSCALE}`,
			`h${-bar}z`
		)
	);

	right  -= QUARTSCALE;
	midline = endWeek * SCALE + QUARTSCALE;

	paths.push(
		eventPath(
			e,
			`M0,${midline}`,
			`h${right}`,
			`l${QUARTSCALE},${QUARTSCALE}`,
			`l${-QUARTSCALE},${QUARTSCALE}`,
			`h${-right}z`
		)
	);

	bar = DAYS.length * SCALE * SLOTS;

	for ( let i = startWeek + 1; i < endWeek; ++i )
	{
		midline = i * SCALE + QUARTSCALE;

		paths.push(
			eventPath(
				e,
				`M0,${midline}`,
				`h${bar}`,
				`v${HALFSCALE}`,
				`h${-bar}z`
			)
		);
	}

	return paths;
}

function range( start, end )
{
	return Array( end - start + 1 ).fill(0).map( (v, k) => v + k + start );
}

function makeTable( data )
{
	const thisWeek = getWeek( new Date() );
	const firstWeek = Math.max(
		thisWeek - 2,
		data.reduce( ( acc, event ) => Math.min( acc, event.start.week ), thisWeek )
	);
	const lastWeek = Math.min(
		thisWeek + 13,
		data.reduce( ( acc, event ) => Math.max( acc, event.end.week ), thisWeek )
	);

	const weeks = lastWeek - firstWeek + 1;

	const width = (SLOTS * DAYS.length + 4) * SCALE + 1;
	const height = SCALE * ( weeks + 1 );

	document.body.appendChild(
		svg(
			// viewBox attribute of the SVG
			{ viewBox: `${-4*SCALE} ${-SCALE} ${width} ${height}` },

			// Background stripes (including current week)
			range( 0, weeks ).map( i => i % 2 ? [] : weekBackground( i, width ) ),
			weekBackground( thisWeek - firstWeek, width, 'rgba(0,128,255,0.3)' ),

			// The day of week and start of week headers
			DAYS.map( dayOfWeekHeader ),
			range( firstWeek, lastWeek ).map( weekHeader ),

			// Add the dividing lines between the days of the week
			DAYS.map( ( _, i) => dayDivider( i, height ) ),
			dayDivider( DAYS.length, height ),

			// Add all the actual events
			data.map( e => makeEvent( e, firstWeek ) )
		)
	);
}

fetch( 'data.json' )
	.then( r => r.json() )
	.then( r => r.map( data => new Event( data ) ) )
	.then( makeTable )
	.then( addHighlights )
	/*.catch( e => document.body.appendChild( document.createTextNode( e.toString() ) ) )*/;
