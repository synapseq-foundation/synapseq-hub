<script lang="ts">
	import { defaultArtwork } from '$lib/player/constants';
	import type { AudioEntry } from '$lib/player/types';

	type Props = {
		entry: AudioEntry;
		context?: 'row' | 'player';
	};

	let { entry, context = 'row' }: Props = $props();

	let artworkClass = $derived(
		context === 'player'
			? 'h-[50px] w-[50px] rounded-2xl border border-[var(--line)] bg-[var(--accent-soft)] object-cover'
			: 'h-[58px] w-[58px] rounded-[18px] border border-[var(--line)] bg-[var(--accent-soft)] object-cover'
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
	<img src={artworkFor(entry.id)} alt="" class={artworkClass} onerror={useFallback} />
	<div class="grid min-w-0 gap-0.5">
		<strong class="overflow-hidden text-base tracking-[-0.02em] text-ellipsis whitespace-nowrap">
			{entry.name}
		</strong>
		<span class="overflow-hidden text-sm text-ellipsis whitespace-nowrap text-[var(--muted)]">
			{entry.category}
		</span>
	</div>
</div>
