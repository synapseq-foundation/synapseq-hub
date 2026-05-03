<script lang="ts">
	import { Play } from '@lucide/svelte';
	import AudioDetails from './AudioDetails.svelte';
	import type { AudioEntry } from '$lib/player/types';

	type Props = {
		selectedEntry: AudioEntry | null;
		playMessage: string;
		onPlay: () => void;
	};

	let { selectedEntry, playMessage, onPlay }: Props = $props();
</script>

<footer
	class="fixed right-3 bottom-3 left-3 mx-auto flex w-[min(calc(100%_-_24px),920px)] items-center gap-3 rounded-[26px] border border-[var(--line-strong)] bg-[var(--panel-strong)] p-3 shadow-[var(--shadow)] backdrop-blur-3xl max-[620px]:items-stretch max-[620px]:gap-2.5 max-[620px]:rounded-[22px]"
	aria-label="Audio player"
>
	{#if selectedEntry}
		<AudioDetails entry={selectedEntry} context="player" />
		<div class="ml-auto flex items-center gap-2.5 max-[620px]:flex-col max-[620px]:items-end max-[620px]:gap-1.5">
			{#if playMessage}
				<span class="max-w-[180px] overflow-hidden text-ellipsis whitespace-nowrap text-[0.85rem] text-[var(--muted)] max-[620px]:hidden">
					{playMessage}
				</span>
			{/if}
			<button
				class="inline-flex min-h-[46px] cursor-pointer items-center justify-center gap-2 rounded-full border border-transparent bg-[var(--accent)] px-[18px] font-[760] text-[#fffaf1] transition duration-150 hover:-translate-y-px hover:bg-[var(--accent-strong)] max-[620px]:w-12 max-[620px]:px-0"
				type="button"
				onclick={onPlay}
			>
				<Play size={20} fill="currentColor" />
				<span class="max-[620px]:hidden">Play</span>
			</button>
		</div>
	{:else}
		<p class="m-0 text-[var(--muted)]">Select an audio to start.</p>
	{/if}
</footer>
