<script lang="ts">
import { onMount } from 'svelte';
import AudioList from '$lib/components/player/AudioList.svelte';
import AudioPlayerBar from '$lib/components/player/AudioPlayerBar.svelte';
import AudioPlaybackModal from '$lib/components/AudioPlaybackModal.svelte';
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
let isPlaying = $state(false);
let playerLocked = $state(false);
let playbackProgress = $state(0);
let audioElement: Audio | null = null;

	function artworkFor(id: string) {
		return `/artwork/${id}.webp`;
	}

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

let modalShow = $state(false);
let modalAudio = $state<(AudioEntry & { artwork: string }) | null>(null);

function openModal(entry: AudioEntry) {
	modalAudio = { ...entry, artwork: artworkFor(entry.id) };
	modalShow = true;
}

function closeModal() {
	modalShow = false;
	modalAudio = null;
}

	let categoryTheme = $derived.by(() => getCategoryTheme(selectedCategory as Category));
	let categoryBgSubtleClass = $derived.by(() => categoryTheme?.bgSubtleClass ?? '');
	let categoryBorderClass = $derived.by(() => categoryTheme?.borderClass ?? '');
	let categoryHeaderBorderClass = $derived.by(() => categoryTheme?.headerBorderClass ?? '');
	let categoryHeaderBgGradientClass = $derived.by(() => categoryTheme?.headerBgGradientClass ?? '');

	let playerTheme = $derived.by(() => {
		if (!selectedEntry) return null;
		return getCategoryTheme(selectedEntry.category as Category);
	});
	let playerBgClass = $derived.by(() => playerTheme?.bgClass ?? '');

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

	function selectCategory(category: string) {
		selectedCategory = category;
		writeStorage(categoryStorageKey, category);
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

	function startPlayback() {
		if (!selectedEntry || isPlaying) return;

		const audio = new Audio(`https://audio.synapseq.org/hub/${selectedEntry.id}.mp3`);
		audio.addEventListener('timeupdate', () => {
			if (audio.duration) {
				playbackProgress = (audio.currentTime / audio.duration) * 100;
			}
		});
		audio.addEventListener('ended', () => {
			stopPlayback();
		});
		audio.play();
		audioElement = audio;
		isPlaying = true;
		playerLocked = true;

		if ('mediaSession' in navigator) {
			navigator.mediaSession.metadata = new MediaMetadata({
				title: selectedEntry.name,
				artist: selectedEntry.author,
				album: 'SynapSeq Hub',
				artwork: [
					{ src: `/artwork/${selectedEntry.id}.webp`, sizes: '512x512', type: 'image/webp' }
				]
			});
			navigator.mediaSession.setActionHandler('play', () => startPlayback());
			navigator.mediaSession.setActionHandler('pause', () => stopPlayback());
			navigator.mediaSession.setActionHandler('stop', () => stopPlayback());
		}
	}

	function stopPlayback() {
		if (!audioElement) return;
		audioElement.pause();
		audioElement.currentTime = 0;
		audioElement = null;
		isPlaying = false;
		playerLocked = false;
		playbackProgress = 0;

		if ('mediaSession' in navigator) {
			navigator.mediaSession.metadata = null;
			navigator.mediaSession.setActionHandler('play', null);
			navigator.mediaSession.setActionHandler('pause', null);
			navigator.mediaSession.setActionHandler('stop', null);
		}
	}

	function togglePlayback() {
		if (isPlaying) {
			stopPlayback();
		} else {
			startPlayback();
		}
	}

	function selectEntry(entry: AudioEntry) {
		selectedAudioId = entry.id;
		playMessage = '';
		writeStorage(currentAudioStorageKey, entry.id);
		openModal(entry);
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
	<PlayerHeader
		{theme}
		onToggleTheme={toggleTheme}
		categoryBorderClass={categoryHeaderBorderClass}
		categoryBgGradientClass={categoryHeaderBgGradientClass}
	/>

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
				locked={playerLocked}
			/>
		{/if}
	{/if}
</main>

<AudioPlayerBar {selectedEntry} {playMessage} {isPlaying} progress={playbackProgress} locked={playerLocked} onToggle={togglePlayback} playerBgClass={playerBgClass} />

<AudioPlaybackModal show={modalShow} audio={modalAudio} onclose={closeModal} />

<!-- AudioPlaybackModal removed - playback now handled directly in AudioPlayerBar -->

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
