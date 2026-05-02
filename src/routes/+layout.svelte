<script lang="ts">
	import './layout.css';

	import favicon from '$lib/assets/favicon.svg';
	import favicon32 from '$lib/assets/favicon-32.png';
	import favicon48 from '$lib/assets/favicon-48.png';
	import favicon96 from '$lib/assets/favicon-96.png';
	import favicon144 from '$lib/assets/favicon-144-precomposed.png';
	import favicon192 from '$lib/assets/favicon-192.png';
	import faviconIco from '$lib/assets/favicon.ico';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={faviconIco} sizes="any" />
	<link rel="icon" href={favicon} type="image/svg+xml" />
	<link rel="icon" href={favicon32} sizes="32x32" type="image/png" />
	<link rel="icon" href={favicon48} sizes="48x48" type="image/png" />
	<link rel="icon" href={favicon96} sizes="96x96" type="image/png" />
	<link rel="apple-touch-icon" href={favicon144} sizes="144x144" />
	<link rel="apple-touch-icon" href={favicon192} sizes="192x192" />
</svelte:head>
{@render children()}
