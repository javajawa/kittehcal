'use strict';

import { SCALE, SLOTS, SLOTKEYS } from './config.js';
import { getWeek } from './dates.js';

class DateStamp
{
	constructor( dateStr )
	{
		this.original = dateStr;

		const parts = dateStr.split( '-' );

		if ( parts.length !== 4 )
		{
			throw `Invalid Date: ${dateStr}`;
		}

		this.date = new Date( parts[0], parseInt( parts[1] ) - 1, parts[2] );
		this.week = getWeek( this.date );
		this.slot = SLOTKEYS.indexOf( parts[3] );
	}

	dow()
	{
		if ( this.date.getDay() == 0 )
		{
			return 6;
		}
		return this.date.getDay() - 1;
	}

	getLeft()
	{
		return SCALE * ( SLOTS * this.dow() + this.slot );
	}

	getRight()
	{
		return SCALE * ( SLOTS * this.dow() + this.slot + 1 );
	}
}

export class Event
{
	constructor( data )
	{
		this.id    = data.id;
		this.title = data.title;
		this.start = new DateStamp( data.start );
		this.end   = new DateStamp( data.end );
		this.class = data.class;
	}
}


