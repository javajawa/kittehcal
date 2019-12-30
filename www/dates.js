// Based on https://weeknumber.net/how-to/javascript

"use strict";

export function getWeek( sourceDate )
{
	const date = new Date(sourceDate.getTime());

	// Thursday in current week decides the year.
	// January 4 is always in week 1.
	date.setHours(0, 0, 0, 0);
	date.setDate(date.getDate() + 3 - (date.getDay() + 6) % 7);

	const week1 = new Date(date.getFullYear(), 0, 4);

	// Adjust to Thursday in week 1 and count number of weeks from date to week1.
	// NB: This has been changed to yield 0-52, not the real 1-53 value,
	// and has 53 weeks for each year since 53 counted before it.
	const yearWeeks = ( date.getFullYear() - 2000 ) * 53;
	const weekInYear = Math.round(
		( ( date.getTime() - week1.getTime() ) / 86400000 - 3 +
		( week1.getDay() + 6 ) % 7 ) / 7
	);

	return yearWeeks + weekInYear;
}

export function getStartOfWeek(year, week)
{
	const date   = new Date( Date.UTC( year, 0, 1 + week * 7 ) );
	const dow    = date.getDay();
	const offset = ( dow <= 4 ) ? 1 : 8;

	date.setDate( date.getDate() - dow + offset );

	return date;
}

function pad( num )
{
	return num < 10 ? '0' + num.toString() : num.toString();
}

export function isoDateString( date )
{
	return date.getFullYear() + '-' +
		pad( 1 + date.getMonth() ) + '-' +
		pad( date.getDate() );
}
