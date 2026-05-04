<script lang="ts">
	import { onMount } from 'svelte';
	import AudioList from '$lib/components/player/AudioList.svelte';
	import AudioPlayerBar from '$lib/components/player/AudioPlayerBar.svelte';
	import AudioPlaybackModal from '$lib/components/AudioPlaybackModal.svelte';
	import ConfirmSheet from '$lib/components/ConfirmSheet.svelte';
	import CategoryBadges from '$lib/components/player/CategoryBadges.svelte';
	import PlayerHeader from '$lib/components/player/PlayerHeader.svelte';
	import LoadingScreen from '$lib/components/player/LoadingScreen.svelte';
	import StatePanel from '$lib/components/player/StatePanel.svelte';
	import {
		themeStorageKey,
		categoryStorageKey,
		currentAudioStorageKey
	} from '$lib/player/constants';
	import { favoritesStore, addFavorite, removeFavorite, getFavorites, clearFavorites } from '$lib/player/favorites';
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
	let scrollY = $state(0);
	let compactHeader = $derived(scrollY > 60);
	let isPlaying = $state(false);
	let isPaused = $state(false);
	// List is locked for the entire session (playing OR paused).
	// It only unlocks when the audio ends naturally or the user hits Stop.
	let playerLocked = $derived(isPlaying || isPaused);
	let playbackProgress = $state(0);
	let audioElement: HTMLAudioElement | null = null;
	let wakeLock: WakeLockSentinel | null = null;

	async function acquireWakeLock() {
		if (!('wakeLock' in navigator)) return;
		try {
			wakeLock = await navigator.wakeLock.request('screen');
		} catch {
			// WakeLock may be denied (e.g. battery saver mode) — playback continues normally.
		}
	}

	async function releaseWakeLock() {
		if (!wakeLock) return;
		try {
			await wakeLock.release();
		} finally {
			wakeLock = null;
		}
	}

	function artworkFor(id: string) {
		return `/artwork/${id}.webp`;
	}

	let categories = $derived.by(() => [
		'All',
		'Favorites',
		...Array.from(new Set(entries.map((entry) => entry.category))).sort((a, b) =>
			a.localeCompare(b)
		)
	]);
	let visibleEntries = $derived.by(() => {
		if (selectedCategory === 'All')
			return [...entries].sort((a, b) => a.name.localeCompare(b.name));
		if (selectedCategory === 'Favorites') {
			const favIds = new Set(favorites);
			return entries.filter((entry) => favIds.has(entry.id));
		}
		return entries
			.filter((entry) => entry.category === selectedCategory)
			.sort((a, b) => a.name.localeCompare(b.name));
	});
	let selectedEntry = $derived.by(
		() => entries.find((entry) => entry.id === selectedAudioId) ?? visibleEntries[0] ?? null
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

	let confirmClearShow = $state(false);

	function handleClearFavorites() {
		confirmClearShow = true;
	}

	function executeClearFavorites() {
		clearFavorites();
		confirmClearShow = false;
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

		if (
			storedCategory &&
			(storedCategory === 'All' ||
				storedCategory === 'Favorites' ||
				entries.some((e) => e.category === storedCategory))
		) {
			selectedCategory = storedCategory;
		}

		if (storedAudioId && entries.some((e) => e.id === storedAudioId)) {
			selectedAudioId = storedAudioId;
		}
	}

	function startPlayback() {
		if (!selectedEntry || isPlaying) return;

		// If resuming from pause, just unpause the existing element.
		if (isPaused && audioElement) {
			resumePlayback();
			return;
		}

		const audio = new Audio(`https://audio.synapseq.org/hub/${selectedEntry.id}.mp3`);
		audio.addEventListener('timeupdate', () => {
			if (audio.duration) {
				playbackProgress = (audio.currentTime / audio.duration) * 100;
			}
		});
		audio.addEventListener('ended', () => {
			destroyPlayback();
		});
		audio.play();
		audioElement = audio;
		isPlaying = true;
		isPaused = false;
		void acquireWakeLock();

		if ('mediaSession' in navigator) {
			navigator.mediaSession.metadata = new MediaMetadata({
				title: selectedEntry.name,
				artist: selectedEntry.author,
				album: 'SynapSeq Hub',
				artwork: [
					{ src: `/artwork/${selectedEntry.id}.webp`, sizes: '512x512', type: 'image/webp' }
				]
			});
			navigator.mediaSession.playbackState = 'playing';
			navigator.mediaSession.setActionHandler('play', () => resumePlayback());
			navigator.mediaSession.setActionHandler('pause', () => pausePlayback());
			navigator.mediaSession.setActionHandler('stop', () => destroyPlayback());
		}
	}

	function pausePlayback() {
		if (!audioElement || !isPlaying) return;
		audioElement.pause();
		isPlaying = false;
		isPaused = true;
		void releaseWakeLock();

		if ('mediaSession' in navigator) {
			navigator.mediaSession.playbackState = 'paused';
		}
	}

	function resumePlayback() {
		if (!audioElement || !isPaused) return;
		audioElement.play();
		isPlaying = true;
		isPaused = false;
		void acquireWakeLock();

		if ('mediaSession' in navigator) {
			navigator.mediaSession.playbackState = 'playing';
		}
	}

	function destroyPlayback() {
		if (!audioElement) return;
		audioElement.pause();
		// Explicitly clear the src and call load() before discarding the element.
		// This forces WebKit/Safari to fully release the media resource and
		// relinquish NowPlaying ownership — without this, the browser may keep the
		// audio element registered as the active NowPlaying source even after the
		// JS reference is dropped, leaving the OS play button functional with no
		// corresponding app state to update.
		audioElement.src = '';
		audioElement.load();
		audioElement = null;
		isPlaying = false;
		isPaused = false;
		playbackProgress = 0;
		void releaseWakeLock();

		if ('mediaSession' in navigator) {
			navigator.mediaSession.setActionHandler('play', null);
			navigator.mediaSession.setActionHandler('pause', null);
			navigator.mediaSession.setActionHandler('stop', null);
			navigator.mediaSession.metadata = null;
			navigator.mediaSession.playbackState = 'none';
		}
	}

	function togglePlayPause() {
		if (isPlaying) {
			pausePlayback();
		} else if (isPaused) {
			resumePlayback();
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

<svelte:window bind:scrollY />

<svelte:head>
	<title>Hub Player | SynapSeq</title>
	<meta
		name="description"
		content="Browse and play SynapSeq audio packages from the hub catalog."
	/>
</svelte:head>

<PlayerHeader
	{theme}
	compact={compactHeader}
	onToggleTheme={toggleTheme}
	categoryBorderClass={categoryHeaderBorderClass}
	categoryBgGradientClass={categoryHeaderBgGradientClass}
/>

<main
	class="px-2.5 pb-32 sm:px-4 sm:pb-36"
	style="padding-top: calc(5rem + env(safe-area-inset-top, 0px))"
	aria-labelledby="player-title"
>
	{#if isLoading}
		<LoadingScreen />
	{:else if errorMessage}
		<StatePanel message={errorMessage} role="alert" />
	{:else if entries.length === 0}
		<StatePanel message="No audio entries are available yet." />
	{:else}
		<CategoryBadges
			{categories}
			{selectedCategory}
			hasFavorites={favorites.length > 0}
			onSelectCategory={selectCategory}
			onClearFavorites={handleClearFavorites}
		/>

		{#if selectedCategory === 'Favorites' && visibleEntries.length === 0}
			<StatePanel message="You haven't favorited any audio yet." />
		{:else}
			<AudioList
				entries={visibleEntries}
				{selectedEntry}
				{isFavorite}
				onSelectEntry={selectEntry}
				onToggleFavorite={toggleFavorite}
				{categoryBgSubtleClass}
				{categoryBorderClass}
				locked={playerLocked}
			/>
		{/if}
	{/if}
</main>

<AudioPlayerBar
	{selectedEntry}
	{playMessage}
	{isPlaying}
	{isPaused}
	progress={playbackProgress}
	locked={playerLocked}
	onPlayPause={togglePlayPause}
	onStop={destroyPlayback}
	{playerBgClass}
/>

<AudioPlaybackModal show={modalShow} audio={modalAudio} onclose={closeModal} />

<ConfirmSheet
	show={confirmClearShow}
	title="Clear all favorites?"
	description="This will remove all favorited audio from your device. This action cannot be undone."
	confirmLabel="Clear favorites"
	cancelLabel="Cancel"
	onconfirm={executeClearFavorites}
	oncancel={() => (confirmClearShow = false)}
/>

<style>
	:global(body) {
		min-width: 320px;
		min-height: 100vh;
		margin: 0;
		background:
			radial-gradient(ellipse 80% 40% at 10% 0%, rgba(15, 118, 110, 0.22), transparent),
			radial-gradient(ellipse 70% 35% at 90% 0%, rgba(180, 83, 9, 0.2), transparent),
			radial-gradient(ellipse 60% 50% at 50% 100%, rgba(177, 77, 42, 0.08), transparent),
			linear-gradient(180deg, #f8f2e4 0%, var(--bg) 60%);
		color: var(--text);
		font-family:
			'Plus Jakarta Sans',
			ui-sans-serif,
			system-ui,
			-apple-system,
			sans-serif;
	}

	:global(.dark body) {
		background:
			radial-gradient(ellipse 80% 40% at 10% 0%, rgba(15, 118, 110, 0.18), transparent),
			radial-gradient(ellipse 70% 35% at 90% 0%, rgba(180, 83, 9, 0.18), transparent),
			radial-gradient(ellipse 60% 50% at 50% 100%, rgba(177, 77, 42, 0.06), transparent),
			linear-gradient(180deg, #1a1512 0%, var(--bg) 60%);
	}

	:global(button) {
		font: inherit;
	}
</style>
