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
	};

	let {
		entries,
		selectedEntry,
		isFavorite,
		onSelectEntry,
		onToggleFavorite,
		categoryBgSubtleClass = '',
		categoryBorderClass = ''
	}: Props = $props();
</script>

<div class="grid gap-2.5 p-3.5 sm:p-[18px]" aria-label="Available audio entries">
	{#each entries as entry (entry.id)}
		{@const favorite = isFavorite(entry.id)}
		<article
			class={[
				'grid grid-cols-[1fr_auto] items-center gap-3 rounded-3xl border bg-[var(--panel-strong)] transition-colors duration-300 ease-in-out',
				selectedEntry?.id === entry.id
					? 'border-[var(--accent)] shadow-[0_0_0_4px_var(--accent-soft)]'
					: 'border-[var(--line)]',
				categoryBgSubtleClass ? [categoryBgSubtleClass, 'bg-[var(--panel-strong)]'] : [],
				categoryBorderClass ? [categoryBorderClass] : []
			]}
		>
			<button
				type="button"
				class="min-w-0 cursor-pointer border-0 bg-transparent p-3 text-left text-inherit"
				onclick={() => onSelectEntry(entry)}
			>
				<AudioDetails {entry} context="row" />
			</button>
			<button
				type="button"
				class={[
					'mr-3 inline-flex h-11 w-11 cursor-pointer items-center justify-center rounded-full border transition duration-150 hover:-translate-y-px hover:border-[var(--line-strong)] hover:bg-[var(--accent-soft)]',
					favorite
						? 'border-transparent bg-[var(--accent-soft)] text-[var(--accent-strong)]'
						: 'border-[var(--line)] bg-[var(--panel-strong)] text-[var(--text)]'
				]}
				onclick={() => onToggleFavorite(entry)}
				aria-label={favorite ? `Unfavorite ${entry.name}` : `Favorite ${entry.name}`}
				aria-pressed={favorite}
			>
				<Heart size={21} fill={favorite ? 'currentColor' : 'none'} />
			</button>
		</article>
	{/each}
</div>
