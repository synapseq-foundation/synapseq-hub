<script lang="ts">
	import { onMount } from 'svelte';
	import AudioList from '$lib/components/player/AudioList.svelte';
	import AudioPlayerBar from '$lib/components/player/AudioPlayerBar.svelte';
	import CategoryBadges from '$lib/components/player/CategoryBadges.svelte';
	import PlayerHeader from '$lib/components/player/PlayerHeader.svelte';
	import StatePanel from '$lib/components/player/StatePanel.svelte';
	import { favoritesStorageKey, maxFavorites, themeStorageKey } from '$lib/player/constants';
	import { getCategoryTheme, type Category } from '$lib/category-themes';
	import type { AudioEntry, FavoriteRecord, Manifest, Theme } from '$lib/player/types';

	let entries = $state.raw<AudioEntry[]>([]);
	let selectedCategory = $state('All');
	let selectedAudioId = $state<string | null>(null);
	let favorites = $state.raw<FavoriteRecord[]>([]);
	let theme = $state<Theme>('light');
	let isLoading = $state(true);
	let errorMessage = $state('');
	let favoriteMessage = $state('');
	let playMessage = $state('');

	let favoriteMap = $derived.by(() => new Map(favorites.map((favorite) => [favorite.id, favorite])));
	let categories = $derived.by(() => [
		'All',
		...Array.from(new Set(entries.map((entry) => entry.category))).sort((a, b) => a.localeCompare(b))
	]);
	let sortedEntries = $derived.by(() =>
		[...entries].sort((a, b) => {
			const favoriteA = favoriteMap.get(a.id)?.favoritedAt ?? 0;
			const favoriteB = favoriteMap.get(b.id)?.favoritedAt ?? 0;

			if (favoriteA || favoriteB) return favoriteB - favoriteA;

			return a.name.localeCompare(b.name);
		})
	);
	let visibleEntries = $derived.by(() =>
		selectedCategory === 'All'
			? sortedEntries
			: sortedEntries.filter((entry) => entry.category === selectedCategory)
	);
	let selectedEntry = $derived.by(() =>
		entries.find((entry) => entry.id === selectedAudioId) ?? sortedEntries[0] ?? null
	);
	let categoryTheme = $derived.by(() => getCategoryTheme(selectedCategory as Category));
	let categoryBgClass = $derived.by(() => categoryTheme?.bgClass ?? '');
	let categoryBgSubtleClass = $derived.by(() => categoryTheme?.bgSubtleClass ?? '');
	let categoryBorderClass = $derived.by(() => categoryTheme?.borderClass ?? '');

	onMount(() => {
		restoreTheme();
		void loadManifest();
	});

	async function loadManifest() {
		try {
			isLoading = true;
			errorMessage = '';

			const response = await fetch('/manifest.json');
			if (!response.ok) throw new Error(`Manifest request failed with ${response.status}`);

			const manifest = (await response.json()) as Manifest;
			entries = Array.isArray(manifest.entries) ? manifest.entries : [];
			favorites = restoreFavorites(entries);
			selectedAudioId = entries[0]?.id ?? null;
		} catch {
			errorMessage = 'Could not load the audio catalog.';
			entries = [];
			favorites = [];
			selectedAudioId = null;
		} finally {
			isLoading = false;
		}
	}

	function restoreTheme() {
		const storedTheme = readStorage(themeStorageKey);
		if (storedTheme === 'dark' || storedTheme === 'light') theme = storedTheme;

		applyTheme(theme);
	}

	function toggleTheme() {
		theme = theme === 'dark' ? 'light' : 'dark';
		applyTheme(theme);
		writeStorage(themeStorageKey, theme);
	}

	function applyTheme(nextTheme: Theme) {
		document.documentElement.dataset.theme = nextTheme;
	}

	function restoreFavorites(audioEntries: AudioEntry[]) {
		const storedFavorites = readStorage(favoritesStorageKey);
		const validIds = new Set(audioEntries.map((entry) => entry.id));

		try {
			const parsed = JSON.parse(storedFavorites ?? '[]') as unknown;

			if (!Array.isArray(parsed)) return [];

			return parsed
				.filter(isFavoriteRecord)
				.filter((favorite) => validIds.has(favorite.id))
				.sort((a, b) => b.favoritedAt - a.favoritedAt)
				.slice(0, maxFavorites);
		} catch {
			return [];
		}
	}

	function isFavoriteRecord(value: unknown): value is FavoriteRecord {
		return (
			typeof value === 'object' &&
			value !== null &&
			typeof (value as FavoriteRecord).id === 'string' &&
			typeof (value as FavoriteRecord).favoritedAt === 'number'
		);
	}

	function toggleFavorite(entry: AudioEntry) {
		favoriteMessage = '';

		if (isFavorite(entry.id)) {
			favorites = favorites.filter((favorite) => favorite.id !== entry.id);
			writeFavorites();
			return;
		}

		if (favorites.length >= maxFavorites) {
			favoriteMessage = `You can keep up to ${maxFavorites} favorites.`;
			return;
		}

		favorites = [{ id: entry.id, favoritedAt: Date.now() }, ...favorites];
		writeFavorites();
	}

	function writeFavorites() {
		writeStorage(favoritesStorageKey, JSON.stringify(favorites));
	}

	function isFavorite(id: string) {
		return favoriteMap.has(id);
	}

	function selectEntry(entry: AudioEntry) {
		selectedAudioId = entry.id;
		playMessage = '';
	}

	function selectCategory(category: string) {
		selectedCategory = category;
	}

	function playSelected() {
		if (!selectedEntry) return;

		playMessage = `${selectedEntry.name} is selected.`;
	}

	function readStorage(key: string) {
		try {
			return localStorage.getItem(key);
		} catch {
			return null;
		}
	}

	function writeStorage(key: string, value: string) {
		try {
			localStorage.setItem(key, value);
		} catch {
			// Local persistence is optional; the in-memory player still works.
		}
	}
</script>

<svelte:head>
	<title>Hub Player | SynapSeq</title>
	<meta
		name="description"
		content="Browse and play SynapSeq audio packages from the hub catalog."
	/>
</svelte:head>

<main class="overflow-hidden px-2.5 pt-3 pb-32 sm:px-4 sm:pt-[22px] sm:pb-[136px]" aria-labelledby="player-title">
	<PlayerHeader {theme} onToggleTheme={toggleTheme} />

	{#if isLoading}
		<StatePanel message="Loading audio catalog..." />
	{:else if errorMessage}
		<StatePanel message={errorMessage} role="alert" />
	{:else if entries.length === 0}
		<StatePanel message="No audio entries are available yet." />
	{:else}
		<CategoryBadges {categories} {selectedCategory} onSelectCategory={selectCategory} />

		{#if favoriteMessage}
			<p class="mt-1 mr-[18px] mb-0 ml-[18px] text-sm text-[var(--warn)]" role="status">
				{favoriteMessage}
			</p>
		{/if}

		<AudioList
			entries={visibleEntries}
			{selectedEntry}
			{isFavorite}
			onSelectEntry={selectEntry}
			onToggleFavorite={toggleFavorite}
			categoryBgSubtleClass={categoryBgSubtleClass}
			categoryBorderClass={categoryBorderClass}
		/>
	{/if}
</main>

<AudioPlayerBar {selectedEntry} {playMessage} onPlay={playSelected} categoryBgClass={categoryBgClass} />

<style>
	:global(body) {
		min-width: 320px;
		min-height: 100vh;
		margin: 0;
		background:
			radial-gradient(circle at top left, rgba(15, 118, 110, 0.18), transparent 24%),
			radial-gradient(circle at top right, rgba(180, 83, 9, 0.16), transparent 20%),
			linear-gradient(180deg, #fbf6eb 0%, var(--bg) 100%);
		color: var(--text);
		font-family:
			Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
	}

	:global(html[data-theme='dark'] body) {
		background:
			radial-gradient(circle at top left, rgba(15, 118, 110, 0.14), transparent 26%),
			radial-gradient(circle at top right, rgba(180, 83, 9, 0.14), transparent 22%),
			linear-gradient(180deg, #1c1714 0%, var(--bg) 100%);
	}

	:global(button) {
		font: inherit;
	}
</style>
