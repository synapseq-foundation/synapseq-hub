<script lang="ts">
	import { Heart } from '@lucide/svelte';
	import AudioDetails from './AudioDetails.svelte';
	import type { AudioEntry } from '$lib/player/types';
	import type { CategoryTheme } from '$lib/category-themes';

	type GroupedCategory = {
		category: string;
		theme: CategoryTheme | null;
		entries: AudioEntry[];
	};

	type Props = {
		entries: AudioEntry[];
		groupedEntries?: GroupedCategory[];
		selectedCategory?: string;
		selectedEntry: AudioEntry | null;
		isFavorite: (id: string) => boolean;
		onSelectEntry: (entry: AudioEntry) => void;
		onToggleFavorite: (entry: AudioEntry) => void;
		categoryBgSubtleClass?: string;
		categoryBorderClass?: string;
		locked?: boolean;
	};

	let {
		entries,
		groupedEntries = [],
		selectedCategory = 'All',
		selectedEntry,
		isFavorite,
		onSelectEntry,
		onToggleFavorite,
		categoryBgSubtleClass = '',
		categoryBorderClass = '',
		locked = false
	}: Props = $props();

	let showGrouped = $derived(selectedCategory === 'All');
	let inFavorites = $derived(selectedCategory === 'Favorites');

	// Track which IDs are mid-animation so we can apply classes
	let burstingIds = $state<Set<string>>(new Set());
	let dismissingIds = $state<Set<string>>(new Set());

	function handleToggleFavorite(entry: AudioEntry) {
		const wasFavorite = isFavorite(entry.id);

		if (!wasFavorite) {
			// Favoriting: trigger heart burst animation
			burstingIds = new Set([...burstingIds, entry.id]);
			setTimeout(() => {
				burstingIds = new Set([...burstingIds].filter((id) => id !== entry.id));
			}, 600);
			onToggleFavorite(entry);
		} else if (inFavorites) {
			// Unfavoriting inside Favorites tab: animate card out first
			dismissingIds = new Set([...dismissingIds, entry.id]);
			setTimeout(() => {
				onToggleFavorite(entry);
				dismissingIds = new Set([...dismissingIds].filter((id) => id !== entry.id));
			}, 320);
		} else {
			// Unfavoriting in any other tab: just toggle, no removal animation needed
			onToggleFavorite(entry);
		}
	}
</script>

{#snippet card(entry: AudioEntry, cardBgClass: string, cardBorderClass: string, compact: boolean)}
	{@const favorite = isFavorite(entry.id)}
	{@const selected = selectedEntry?.id === entry.id}
	{@const bursting = burstingIds.has(entry.id)}
	{@const dismissing = dismissingIds.has(entry.id)}
	<article
		class={[
			'group relative grid grid-cols-[1fr_auto] items-center overflow-visible border transition-all duration-200 ease-in-out',
			compact ? 'rounded-xl' : 'rounded-2xl sm:rounded-[22px]',
			selected
				? 'border-[var(--accent)] bg-[var(--panel-strong)] shadow-[0_0_0_2px_var(--accent-soft),0_4px_20px_rgba(0,0,0,0.08)]'
				: [
						'bg-[var(--panel-strong)] hover:border-[var(--line-strong)] hover:shadow-[0_2px_8px_rgba(0,0,0,0.06)]',
						cardBorderClass || 'border-[var(--line)]'
					],
			!selected && cardBgClass,
			dismissing && 'dismissing'
		]}
	>
		{#if selected}
			<div class="absolute left-0 top-0 h-full w-0.5 rounded-r-full bg-[var(--accent)]"></div>
		{/if}
		<button
			type="button"
			class="relative min-w-0 cursor-pointer border-0 bg-transparent px-3 py-2.5 text-left text-inherit transition-opacity duration-150 active:opacity-70 {compact ? '' : 'sm:px-4 sm:py-3'} {locked ? 'pointer-events-none' : ''}"
			onclick={() => { if (locked) return; onSelectEntry(entry); }}
		>
			<AudioDetails {entry} context="row" {selected} />
		</button>

		<!-- Heart button with burst container -->
		<div class="relative {compact ? 'mr-2.5' : 'mr-3'}">
			<button
				type="button"
				class={[
					'heart-btn relative shrink-0 cursor-pointer items-center justify-center rounded-full border transition-all duration-150 active:scale-90',
					compact ? 'inline-flex h-9 w-9' : 'inline-flex h-10 w-10 sm:h-11 sm:w-11',
					favorite
						? 'border-transparent bg-[var(--accent-soft)] text-[var(--accent)]'
						: 'border-[var(--line)] bg-transparent text-[var(--muted)] hover:border-[var(--line-strong)] hover:bg-[var(--accent-soft)] hover:text-[var(--accent)]',
					bursting && 'bursting'
				]}
				onclick={() => handleToggleFavorite(entry)}
				aria-label={favorite ? `Unfavorite ${entry.name}` : `Favorite ${entry.name}`}
				aria-pressed={favorite}
			>
				<Heart size={compact ? 15 : 17} fill={favorite ? 'currentColor' : 'none'} strokeWidth={favorite ? 0 : 2} />
			</button>

			<!-- Burst particles (only rendered during burst) -->
			{#if bursting}
				<div class="burst-ring pointer-events-none absolute inset-0" aria-hidden="true">
					{#each [0, 45, 90, 135, 180, 225, 270, 315] as angle}
						<div class="burst-dot" style="--angle: {angle}deg;"></div>
					{/each}
				</div>
			{/if}
		</div>
	</article>
{/snippet}

<!-- ── MOBILE flat list (hidden on lg) ── -->
<div class="grid gap-2 p-3.5 pt-2 sm:gap-2.5 sm:p-4 sm:pt-3 lg:hidden" aria-label="Available audio entries">
	{#each entries as entry (entry.id)}
		{@render card(entry, categoryBgSubtleClass, categoryBorderClass, false)}
	{/each}
</div>

<!-- ── DESKTOP view (hidden below lg) ── -->
<div class="hidden lg:block" aria-label="Available audio entries">

	{#if showGrouped}
		<div class="flex flex-col gap-6">
			{#each groupedEntries as group (group.category)}
				<section>
					<h2 class="mb-2.5 flex items-center gap-2 text-[0.72rem] font-[660] uppercase tracking-[0.13em] text-[var(--muted)]">
						<span class={['inline-block h-1.5 w-1.5 rounded-full', group.theme?.bgClass ?? 'bg-[var(--muted)]']}></span>
						{group.category}
					</h2>
					<div class="grid grid-cols-2 gap-2.5">
						{#each group.entries as entry (entry.id)}
							{@render card(entry, group.theme?.bgSubtleClass ?? '', group.theme?.borderClass ?? '', true)}
						{/each}
					</div>
				</section>
			{/each}
		</div>

	{:else}
		<div class="grid grid-cols-2 gap-2.5">
			{#each entries as entry (entry.id)}
				{@render card(entry, categoryBgSubtleClass, categoryBorderClass, true)}
			{/each}
		</div>
	{/if}

</div>

<style>
	/* ── Heart burst on favorite ── */
	@keyframes heart-pop {
		0%   { transform: scale(1); }
		30%  { transform: scale(1.5); }
		55%  { transform: scale(0.88); }
		75%  { transform: scale(1.18); }
		100% { transform: scale(1); }
	}

	@keyframes burst-out {
		0%   { transform: rotate(var(--angle)) translateY(0)   scale(1);   opacity: 1; }
		60%  { transform: rotate(var(--angle)) translateY(-18px) scale(0.9); opacity: 0.9; }
		100% { transform: rotate(var(--angle)) translateY(-28px) scale(0);   opacity: 0; }
	}

	.heart-btn.bursting {
		animation: heart-pop 0.55s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
	}

	.burst-ring {
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.burst-dot {
		position: absolute;
		width: 5px;
		height: 5px;
		border-radius: 50%;
		background: var(--accent);
		animation: burst-out 0.55s ease-out forwards;
	}

	/* ── Card dismiss on unfavorite (Favorites tab) ── */
	@keyframes card-dismiss {
		0%   { transform: translateX(0);     opacity: 1;   max-height: 80px; }
		40%  { transform: translateX(-18px); opacity: 0.4; max-height: 80px; }
		100% { transform: translateX(-32px); opacity: 0;   max-height: 0;    margin: 0; padding: 0; }
	}

	:global(article.dismissing) {
		animation: card-dismiss 0.32s cubic-bezier(0.4, 0, 0.6, 1) forwards;
		pointer-events: none;
		overflow: hidden;
	}
</style>
