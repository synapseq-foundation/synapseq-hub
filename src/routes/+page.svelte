<script lang="ts">
	import { onMount } from 'svelte';
	import { Heart, Moon, Play, Sun } from '@lucide/svelte';

	type Theme = 'light' | 'dark';

	type AudioEntry = {
		id: string;
		name: string;
		author: string;
		path: string;
		category: string;
		download_url: string;
		updated_at: string;
		dependencies: string[];
	};

	type Manifest = {
		version: string;
		lastUpdated: string;
		entries: AudioEntry[];
	};

	type FavoriteRecord = {
		id: string;
		favoritedAt: number;
	};

	const defaultArtwork = '/artwork/default.webp';
	const favoritesStorageKey = 'synapseq-hub:favorites';
	const themeStorageKey = 'synapseq-hub:theme';
	const maxFavorites = 5;

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

	function artworkFor(id: string) {
		return `/artwork/${id}.webp`;
	}

	function useFallback(event: Event) {
		const image = event.currentTarget as HTMLImageElement;

		if (image.src.endsWith(defaultArtwork)) return;

		image.src = defaultArtwork;
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

{#snippet audioDetails(entry: AudioEntry, context: 'row' | 'player')}
	<div class="audio-details" data-context={context}>
		<img src={artworkFor(entry.id)} alt="" class="artwork" onerror={useFallback} />
		<div class="track-copy">
			<strong>{entry.name}</strong>
			<span>{entry.author}</span>
		</div>
	</div>
{/snippet}

<main class="hub-shell">
	<section class="player-card" aria-labelledby="player-title">
		<header class="hub-header">
			<img src={defaultArtwork} alt="SynapSeq" class="logo" />
			<h1 id="player-title">Hub Player</h1>
			<button class="icon-button" type="button" onclick={toggleTheme} aria-label="Toggle theme">
				{#if theme === 'dark'}
					<Sun size={20} />
				{:else}
					<Moon size={20} />
				{/if}
			</button>
		</header>

		{#if isLoading}
			<div class="state-panel">Loading audio catalog...</div>
		{:else if errorMessage}
			<div class="state-panel" role="alert">{errorMessage}</div>
		{:else if entries.length === 0}
			<div class="state-panel">No audio entries are available yet.</div>
		{:else}
			<nav class="categories" aria-label="Audio categories">
				{#each categories as category (category)}
					<button
						type="button"
						class={selectedCategory === category ? 'category-badge active' : 'category-badge'}
						onclick={() => selectCategory(category)}
					>
						{category}
					</button>
				{/each}
			</nav>

			{#if favoriteMessage}
				<p class="notice" role="status">{favoriteMessage}</p>
			{/if}

			<div class="audio-list" aria-label="Available audio entries">
				{#each visibleEntries as entry (entry.id)}
					<article class={selectedEntry?.id === entry.id ? 'audio-row selected' : 'audio-row'}>
						<button type="button" class="details-button" onclick={() => selectEntry(entry)}>
							{@render audioDetails(entry, 'row')}
						</button>
						<button
							type="button"
							class={isFavorite(entry.id) ? 'favorite-button active' : 'favorite-button'}
							onclick={() => toggleFavorite(entry)}
							aria-label={isFavorite(entry.id) ? `Unfavorite ${entry.name}` : `Favorite ${entry.name}`}
							aria-pressed={isFavorite(entry.id)}
						>
							<Heart size={21} fill={isFavorite(entry.id) ? 'currentColor' : 'none'} />
						</button>
					</article>
				{/each}
			</div>
		{/if}
	</section>
</main>

<footer class="fixed-player" aria-label="Audio player">
	{#if selectedEntry}
		{@render audioDetails(selectedEntry, 'player')}
		<div class="player-actions">
			{#if playMessage}
				<span class="play-message">{playMessage}</span>
			{/if}
			<button class="play-button" type="button" onclick={playSelected}>
				<Play size={20} fill="currentColor" />
				<span>Play</span>
			</button>
		</div>
	{:else}
		<p class="empty-player">Select an audio to start.</p>
	{/if}
</footer>

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

	.hub-shell {
		width: min(100%, 920px);
		min-height: 100vh;
		margin: 0 auto;
		padding: 22px 16px 136px;
	}

	.player-card {
		border: 1px solid var(--line);
		border-radius: 32px;
		background: var(--panel);
		box-shadow: var(--shadow);
		backdrop-filter: blur(20px);
		overflow: hidden;
	}

	.hub-header {
		display: grid;
		grid-template-columns: auto 1fr auto;
		align-items: center;
		gap: 14px;
		padding: 18px;
		border-bottom: 1px solid var(--line);
	}

	.logo {
		width: 46px;
		height: 46px;
		border: 1px solid var(--line-strong);
		border-radius: 16px;
		object-fit: cover;
	}

	h1 {
		margin: 0;
		font-size: clamp(1.35rem, 5vw, 2.1rem);
		font-weight: 760;
		letter-spacing: -0.04em;
	}

	.icon-button,
	.favorite-button,
	.play-button {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		border: 1px solid var(--line);
		color: var(--text);
		background: var(--panel-strong);
		cursor: pointer;
		transition:
			transform 160ms ease,
			border-color 160ms ease,
			background 160ms ease;
	}

	.icon-button:hover,
	.favorite-button:hover,
	.play-button:hover {
		transform: translateY(-1px);
		border-color: var(--line-strong);
		background: var(--accent-soft);
	}

	.icon-button {
		width: 44px;
		height: 44px;
		border-radius: 999px;
	}

	.state-panel {
		margin: 18px;
		padding: 24px;
		border: 1px solid var(--line);
		border-radius: 24px;
		background: var(--panel-strong);
		color: var(--muted);
		text-align: center;
	}

	.categories {
		display: flex;
		gap: 10px;
		overflow-x: auto;
		padding: 18px 18px 8px;
		scrollbar-width: none;
	}

	.categories::-webkit-scrollbar {
		display: none;
	}

	.category-badge {
		flex: 0 0 auto;
		border: 1px solid var(--line);
		border-radius: 999px;
		padding: 9px 15px;
		color: var(--muted);
		background: var(--panel-strong);
		cursor: pointer;
	}

	.category-badge.active {
		border-color: transparent;
		color: var(--accent-strong);
		background: var(--accent-soft);
		font-weight: 700;
	}

	.notice {
		margin: 4px 18px 0;
		color: var(--warn);
		font-size: 0.9rem;
	}

	.audio-list {
		display: grid;
		gap: 10px;
		padding: 18px;
	}

	.audio-row {
		display: grid;
		grid-template-columns: 1fr auto;
		align-items: center;
		gap: 12px;
		border: 1px solid var(--line);
		border-radius: 24px;
		background: var(--panel-strong);
	}

	.audio-row.selected {
		border-color: var(--accent);
		box-shadow: 0 0 0 4px var(--accent-soft);
	}

	.details-button {
		min-width: 0;
		border: 0;
		padding: 12px;
		color: inherit;
		background: transparent;
		cursor: pointer;
		text-align: left;
	}

	.audio-details {
		display: grid;
		grid-template-columns: auto minmax(0, 1fr);
		align-items: center;
		gap: 12px;
		min-width: 0;
	}

	.audio-details[data-context='player'] {
		flex: 1;
	}

	.artwork {
		width: 58px;
		height: 58px;
		border: 1px solid var(--line);
		border-radius: 18px;
		object-fit: cover;
		background: var(--accent-soft);
	}

	.audio-details[data-context='player'] .artwork {
		width: 50px;
		height: 50px;
		border-radius: 16px;
	}

	.track-copy {
		display: grid;
		gap: 2px;
		min-width: 0;
	}

	.track-copy strong,
	.track-copy span {
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.track-copy strong {
		font-size: 1rem;
		letter-spacing: -0.02em;
	}

	.track-copy span {
		color: var(--muted);
		font-size: 0.9rem;
	}

	.favorite-button {
		width: 44px;
		height: 44px;
		margin-right: 12px;
		border-radius: 999px;
	}

	.favorite-button.active {
		border-color: transparent;
		color: var(--accent-strong);
		background: var(--accent-soft);
	}

	.fixed-player {
		position: fixed;
		right: 12px;
		bottom: 12px;
		left: 12px;
		display: flex;
		align-items: center;
		gap: 12px;
		width: min(calc(100% - 24px), 920px);
		margin: 0 auto;
		padding: 12px;
		border: 1px solid var(--line-strong);
		border-radius: 26px;
		background: var(--panel-strong);
		box-shadow: var(--shadow);
		backdrop-filter: blur(24px);
	}

	.player-actions {
		display: flex;
		align-items: center;
		gap: 10px;
		margin-left: auto;
	}

	.play-message {
		max-width: 180px;
		overflow: hidden;
		color: var(--muted);
		font-size: 0.85rem;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.play-button {
		gap: 8px;
		min-height: 46px;
		border-color: transparent;
		border-radius: 999px;
		padding: 0 18px;
		color: #fffaf1;
		background: var(--accent);
		font-weight: 760;
	}

	.play-button:hover {
		background: var(--accent-strong);
	}

	.empty-player {
		margin: 0;
		color: var(--muted);
	}

	@media (max-width: 620px) {
		.hub-shell {
			padding: 12px 10px 128px;
		}

		.player-card {
			border-radius: 26px;
		}

		.hub-header,
		.audio-list {
			padding: 14px;
		}

		.categories {
			padding: 14px 14px 8px;
		}

		.fixed-player {
			align-items: stretch;
			gap: 10px;
			border-radius: 22px;
		}

		.player-actions {
			flex-direction: column;
			align-items: flex-end;
			gap: 6px;
		}

		.play-message {
			display: none;
		}

		.play-button span {
			display: none;
		}

		.play-button {
			width: 48px;
			padding: 0;
		}
	}
</style>
