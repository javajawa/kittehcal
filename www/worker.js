const codeFiles = [
	'https://tea-cats.co.uk/calendar/',
	'https://tea-cats.co.uk/calendar/calendar.js',
	'https://tea-cats.co.uk/calendar/config.js',
	'https://tea-cats.co.uk/calendar/dates.js',
	'https://tea-cats.co.uk/calendar/events.js',
	'https://tea-cats.co.uk/calendar/index.html',
	'https://tea-cats.co.uk/calendar/manifest.json',
	'https://tea-cats.co.uk/calendar/style.css',
	'https://tea-cats.co.uk/calendar/icon.png',
	'https://static.harcourtprogramming.co.uk/shared/2018.css',
	'https://static.harcourtprogramming.co.uk/shared/2018-print.css',
	'https://javajawa.github.io/elems.js/elems.js'
];

const dataFiles = [
	'https://tea-cats.co.uk/calendar/data.json'
];

const cacheName = 'calendar-v1';

self.addEventListener( 'install', e =>
{
	console.log( 'Worker install' );

	e.waitUntil(
		codeFiles.forEach( url => {
			console.log( 'Caching file ' + url );
			fetch( url, { cache: "no-cache" } ).then( r => cacheResponse( url, r ) );
		} )
	);

	e.waitUntil(
		dataFiles.forEach( url => {
			console.log( 'Caching file ' + url );
			fetch( url, { cache: "no-cache" } ).then( r => cacheResponse( url, r ) );
		} )
	);
} );

self.addEventListener( 'activate', e => {
	console.log( 'Worker activate' );
	e.waitUntil(
		caches.keys().then( names => names.forEach(
			name => ( name !== cacheName ) && caches.delete( name )
		) )
	);

	return self.clients.claim();
} );

self.addEventListener( 'fetch', e =>
{
	// Fetch logic:
	//
	//  - Always see if we have a cached copy
	//  - If we do not, perform a normal fetch, caching the result
	//  - It we do, and this is marked as a `codeFile`, return the cached copy,
	//    and schedule a background update.
	//  - Otherwise, this is data. Attempt to fetch it in 1.5 seconds, else
	//    return the cached version.

	const url  = e.request.url;

	e.respondWith(
		caches.open( cacheName )
		.then( cache => cache.match( e.request ) )
		.then( cached =>
		{
			console.log( cached ? 'Cache Available' : 'Not Cached', url );

			if ( ! ( cached instanceof Response ) )
			{
				console.log( 'Long-Fetching', url );

				return fetch( e.request, { cache: "no-cache" } ).then( rsp => cacheResponse( e.request, rsp ) )
			}

			if ( codeFiles.includes( url ) )
			{
				console.log( 'Using cache for', url );

				fetch( url, { cache: "no-cache" } )
					.then( r => cacheResponse( url, r ) )
					.catch( console.error );

				return cached;
			}

			console.log( 'Short-Fetching', url );

			return _fetch( e.request )
				.then( rsp => { console.log( 'Fetched and caching ', url ); return rsp; } )
				.then( rsp => cacheResponse( e.request, rsp ) )
				.catch( () => { console.log( 'Short fetch failed, falling back to cache', url ); return cached; } )
		}
	) )
} );

const cacheResponse = ( req, rsp ) => caches.open( cacheName )
	.then( cache => cache.put( req, rsp.clone() ) )
	.then( () => rsp );

const _fetch = url => timeout( fetch( url, { mode: 'cors', credentials: 'omit', cache: "no-cache" } ), 1500 );

const timeout =	( promise, ms ) => new Promise( ( accept, reject ) => {
	setTimeout( () => reject( new Error( `timed out after ${ms}ms` ) ), ms );
	promise.then( accept, reject );
} );
