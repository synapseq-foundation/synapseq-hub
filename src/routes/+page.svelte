<script lang="ts">
import { onMount } from 'svelte';
import AudioList from '$lib/components/player/AudioList.svelte';
import AudioPlayerBar from '$lib/components/player/AudioPlayerBar.svelte';
import CategoryBadges from '$lib/components/player/CategoryBadges.svelte';
import PlayerHeader from '$lib/components/player/PlayerHeader.svelte';
import LoadingScreen from '$lib/components/player/LoadingScreen.svelte';
import StatePanel from '$lib/components/player/StatePanel.svelte';
import { themeStorageKey, categoryStorageKey, currentAudioStorageKey } from '$lib/player/constants';
import { favoritesStore, addFavorite, removeFavorite, getFavorites } from '$lib/player/favorites';
import { getCategoryTheme, type Category } from '$lib/category-themes';
import type { AudioEntry, Manifest, Theme } from '$lib/player/types';

let entries = $state.raw<AudioEntry[]>([]);
let selectedCategory = $state('All');
let selectedAudioId = $state<string | null>(null);
let favorites = $derived($favoritesStore);
let theme = $state<Theme>('light');
let isLoading = $state(true);
let errorMessage = $state('');
let playMessage = $state('');

let categories = $derived.by(() => [
	'All',
	'Favorites',
	...Array.from(new Set(entries.map((entry) => entry.category))).sort((a, b) => a.localeCompare(b))
]);
let visibleEntries = $derived.by(() => {
	if (selectedCategory === 'All') return [...entries].sort((a, b) => a.name.localeCompare(b.name));
	if (selectedCategory === 'Favorites') {
		const favIds = new Set(favorites);
		return entries.filter((entry) => favIds.has(entry.id));
	}
	return entries
		.filter((entry) => entry.category === selectedCategory)
		.sort((a, b) => a.name.localeCompare(b.name));
});
let selectedEntry = $derived.by(() =>
	entries.find((entry) => entry.id === selectedAudioId) ?? visibleEntries[0] ?? null
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
			restoreSelectionState();
			if (!selectedAudioId || !entries.some((e) => e.id === selectedAudioId)) {
				selectedAudioId = entries[0]?.id ?? null;
			}
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
		const storedTheme = localStorage.getItem(themeStorageKey);
		if (storedTheme === 'dark' || storedTheme === 'light') theme = storedTheme;

		applyTheme(theme);
	}

	function toggleTheme() {
		theme = theme === 'dark' ? 'light' : 'dark';
		applyTheme(theme);
		writeStorage(themeStorageKey, theme);
	}

	function applyTheme(nextTheme: Theme) {
		document.documentElement.classList.toggle('dark', nextTheme === 'dark');
	}

	function toggleFavorite(entry: AudioEntry) {
		if (favorites.includes(entry.id)) {
			removeFavorite(entry.id);
		} else {
			addFavorite(entry.id);
		}
	}

	function isFavorite(id: string) {
		return favorites.includes(id);
	}

	function selectEntry(entry: AudioEntry) {
		selectedAudioId = entry.id;
		playMessage = '';
		writeStorage(currentAudioStorageKey, entry.id);
	}

	function selectCategory(category: string) {
		selectedCategory = category;
		writeStorage(categoryStorageKey, category);
	}

	function playSelected() {
		if (!selectedEntry) return;

		playMessage = `${selectedEntry.name} is selected.`;
	}

	function writeStorage(key: string, value: string) {
		try {
			localStorage.setItem(key, value);
		} catch {
			// Local persistence is optional; the in-memory player still works.
		}
	}

	function restoreSelectionState() {
		const storedCategory = localStorage.getItem(categoryStorageKey);
		const storedAudioId = localStorage.getItem(currentAudioStorageKey);

		if (storedCategory && (storedCategory === 'All' || storedCategory === 'Favorites' || entries.some((e) => e.category === storedCategory))) {
			selectedCategory = storedCategory;
		}

		if (storedAudioId && entries.some((e) => e.id === storedAudioId)) {
			selectedAudioId = storedAudioId;
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
		<LoadingScreen />
	{:else if errorMessage}
		<StatePanel message={errorMessage} role="alert" />
	{:else if entries.length === 0}
		<StatePanel message="No audio entries are available yet." />
	{:else}
		<CategoryBadges {categories} {selectedCategory} onSelectCategory={selectCategory} />

		{#if selectedCategory === 'Favorites' && visibleEntries.length === 0}
			<StatePanel message="You haven't favorited any audio yet." />
		{:else}
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

	:global(.dark body) {
		background:
			radial-gradient(circle at top left, rgba(15, 118, 110, 0.14), transparent 26%),
			radial-gradient(circle at top right, rgba(180, 83, 9, 0.14), transparent 22%),
			linear-gradient(180deg, #1c1714 0%, var(--bg) 100%);
	}

	:global(button) {
		font: inherit;
	}
</style>
