<script lang="ts">
	import { Heart } from '@lucide/svelte';
	import AudioDetails from './AudioDetails.svelte';
	import type { AudioEntry } from '$lib/player/types';

	type Props = {
		entries: AudioEntry[];
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
		selectedEntry,
		isFavorite,
		onSelectEntry,
		onToggleFavorite,
		categoryBgSubtleClass = '',
		categoryBorderClass = '',
		locked = false
	}: Props = $props();
</script>

<div class="grid gap-2 p-3.5 pt-2 sm:gap-2.5 sm:p-4 sm:pt-3 lg:grid-cols-2 lg:gap-3 lg:p-0 lg:pt-0" aria-label="Available audio entries">
	{#each entries as entry (entry.id)}
		{@const favorite = isFavorite(entry.id)}
		{@const selected = selectedEntry?.id === entry.id}
		<article
			class={[
				'group relative grid grid-cols-[1fr_auto] items-center overflow-hidden rounded-2xl border transition-all duration-200 ease-in-out sm:rounded-[22px]',
				selected
					? 'border-[var(--accent)] bg-[var(--panel-strong)] shadow-[0_0_0_3px_var(--accent-soft),0_4px_20px_rgba(0,0,0,0.08)]'
					: 'border-[var(--line)] bg-[var(--panel-strong)] hover:border-[var(--line-strong)] hover:shadow-[0_2px_12px_rgba(0,0,0,0.06)]',
				categoryBgSubtleClass,
				categoryBorderClass && !selected ? categoryBorderClass : ''
			]}
		>
			<!-- Left accent bar for selected state -->
			{#if selected}
				<div class="absolute left-0 top-0 h-full w-0.5 rounded-r-full bg-[var(--accent)]"></div>
			{/if}

			<button
				type="button"
				class="relative min-w-0 cursor-pointer border-0 bg-transparent px-3 py-2.5 text-left text-inherit transition-opacity duration-150 active:opacity-70 sm:px-4 sm:py-3 {locked ? 'pointer-events-none' : ''}"
				onclick={() => { if (locked) return; onSelectEntry(entry); }}
			>
				<AudioDetails {entry} context="row" {selected} />
			</button>

			<button
				type="button"
				class={[
					'mr-3 inline-flex h-10 w-10 shrink-0 cursor-pointer items-center justify-center rounded-full border transition-all duration-150 active:scale-90 sm:h-11 sm:w-11',
					favorite
						? 'border-transparent bg-[var(--accent-soft)] text-[var(--accent)]'
						: 'border-[var(--line)] bg-transparent text-[var(--muted)] hover:border-[var(--line-strong)] hover:bg-[var(--accent-soft)] hover:text-[var(--accent)]'
				]}
				onclick={() => onToggleFavorite(entry)}
				aria-label={favorite ? `Unfavorite ${entry.name}` : `Favorite ${entry.name}`}
				aria-pressed={favorite}
			>
				<Heart size={17} fill={favorite ? 'currentColor' : 'none'} strokeWidth={favorite ? 0 : 2} />
			</button>
		</article>
	{/each}
</div>
