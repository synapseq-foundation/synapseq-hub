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
</script>

{#snippet card(entry: AudioEntry, cardBgClass: string, cardBorderClass: string, compact: boolean)}
	{@const favorite = isFavorite(entry.id)}
	{@const selected = selectedEntry?.id === entry.id}
	<article
		class={[
			'group relative grid grid-cols-[1fr_auto] items-center overflow-hidden border transition-all duration-200 ease-in-out',
			compact ? 'rounded-xl' : 'rounded-2xl sm:rounded-[22px]',
			selected
				? 'border-[var(--accent)] bg-[var(--panel-strong)] shadow-[0_0_0_2px_var(--accent-soft),0_4px_20px_rgba(0,0,0,0.08)]'
				: [
						'bg-[var(--panel-strong)] hover:border-[var(--line-strong)] hover:shadow-[0_2px_8px_rgba(0,0,0,0.06)]',
						cardBorderClass || 'border-[var(--line)]'
					],
			!selected && cardBgClass
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
		<button
			type="button"
			class={[
				'shrink-0 cursor-pointer items-center justify-center rounded-full border transition-all duration-150 active:scale-90',
				compact ? 'mr-2.5 inline-flex h-9 w-9' : 'mr-3 inline-flex h-10 w-10 sm:h-11 sm:w-11',
				favorite
					? 'border-transparent bg-[var(--accent-soft)] text-[var(--accent)]'
					: 'border-[var(--line)] bg-transparent text-[var(--muted)] hover:border-[var(--line-strong)] hover:bg-[var(--accent-soft)] hover:text-[var(--accent)]'
			]}
			onclick={() => onToggleFavorite(entry)}
			aria-label={favorite ? `Unfavorite ${entry.name}` : `Favorite ${entry.name}`}
			aria-pressed={favorite}
		>
			<Heart size={compact ? 15 : 17} fill={favorite ? 'currentColor' : 'none'} strokeWidth={favorite ? 0 : 2} />
		</button>
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
		<!-- "All" mode: sections per category, cards carry the category colour -->
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
		<!-- Single category mode: flat 2-col grid, cards carry the category colour -->
		<div class="grid grid-cols-2 gap-2.5">
			{#each entries as entry (entry.id)}
				{@render card(entry, categoryBgSubtleClass, categoryBorderClass, true)}
			{/each}
		</div>
	{/if}

</div>
