<script lang="ts">
	import { defaultArtwork } from '$lib/player/constants';
	import type { AudioEntry } from '$lib/player/types';

	type Props = {
		entry: AudioEntry;
		context?: 'row' | 'player';
		selected?: boolean;
	};

	let { entry, context = 'row', selected = false }: Props = $props();

	let artworkSize = $derived(context === 'player' ? 'h-[46px] w-[46px]' : 'h-[52px] w-[52px]');
	let artworkClass = $derived(
		`${artworkSize} rounded-xl border object-cover transition-all duration-200 sm:rounded-[14px] ${
			selected
				? 'border-[var(--accent-soft)] shadow-[0_0_0_2px_var(--accent-soft)]'
				: 'border-[var(--line)] bg-[var(--accent-soft)]'
		}`
	);

	function artworkFor(id: string) {
		return `/artwork/${id}.webp`;
	}

	function useFallback(event: Event) {
		const image = event.currentTarget as HTMLImageElement;
		if (image.src.endsWith(defaultArtwork)) return;
		image.src = defaultArtwork;
	}
</script>

<div
	class={[
		'grid min-w-0 grid-cols-[auto_minmax(0,1fr)] items-center gap-3',
		context === 'player' && 'flex-1'
	]}
>
	<div class="relative shrink-0">
		{#if selected && context === 'row'}
			<div class="absolute inset-0 rounded-xl bg-[var(--accent-soft)] blur-[8px] opacity-70"></div>
		{/if}
		<img src={artworkFor(entry.id)} alt="" class={artworkClass} onerror={useFallback} />
	</div>

	<div class="grid min-w-0 gap-0.5">
		<strong
			class={[
				'overflow-hidden text-[0.9rem] font-[660] leading-snug tracking-[-0.02em] text-ellipsis whitespace-nowrap transition-colors duration-200 sm:text-base',
				selected ? 'text-[var(--accent)]' : 'text-[var(--text)]'
			]}
		>
			{entry.name}
		</strong>
		<span class="overflow-hidden text-[0.74rem] font-[480] text-ellipsis whitespace-nowrap text-[var(--muted)] sm:text-sm">
			{entry.category}
		</span>
	</div>
</div>
