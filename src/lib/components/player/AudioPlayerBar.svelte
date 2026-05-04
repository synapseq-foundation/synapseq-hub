<script lang="ts">
	import AudioDetails from './AudioDetails.svelte';
	import PlayerControls from './PlayerControls.svelte';
	import type { AudioEntry } from '$lib/player/types';

	type Props = {
		selectedEntry: AudioEntry | null;
		playMessage: string;
		isPlaying: boolean;
		isPaused: boolean;
		progress: number;
		locked: boolean;
		onPlayPause: () => void;
		onStop: () => void;
		playerBgClass?: string;
	};

	let { selectedEntry, playMessage, isPlaying, isPaused, progress, locked, onPlayPause, onStop, playerBgClass = '' }: Props = $props();
</script>

<footer
	class={[
		'fixed left-3 right-3 mx-auto flex w-[min(calc(100%-24px),920px)] items-center gap-3 overflow-hidden rounded-[24px] border border-[var(--line-strong)] bg-[var(--panel-strong)] shadow-[0_8px_32px_rgba(0,0,0,0.14),0_2px_8px_rgba(0,0,0,0.08)] backdrop-blur-3xl transition-all duration-300 sm:rounded-[28px]',
		isPlaying ? 'p-2.5 pr-3 sm:p-3 sm:pr-4' : ['p-2.5 pr-3 sm:p-3 sm:pr-4', playerBgClass]
	]}
	style="bottom: calc(0.75rem + env(safe-area-inset-bottom, 0px))"
	aria-label="Audio player"
>
	<!-- Progress fill -->
	{#if isPlaying}
		<div
			class={['absolute top-0 left-0 h-full transition-[width] duration-300 ease-linear opacity-90', playerBgClass]}
			style="width: {progress}%"
		></div>
		<!-- Subtle shimmer at progress edge -->
		<div
			class="absolute top-0 h-full w-6 bg-gradient-to-r from-transparent to-white/10 transition-[left] duration-300 ease-linear"
			style="left: calc({progress}% - 24px)"
		></div>
	{/if}

	{#if selectedEntry}
		<div class="relative z-10 flex w-full items-center gap-2.5 sm:gap-3">
			<AudioDetails entry={selectedEntry} context="player" />

			<div class="ml-auto flex shrink-0 items-center gap-2 sm:gap-2.5">
				{#if playMessage && !isPlaying && !isPaused}
					<span class="hidden max-w-[160px] overflow-hidden text-ellipsis whitespace-nowrap text-[0.8rem] text-[var(--muted)] sm:block">
						{playMessage}
					</span>
				{/if}

				<PlayerControls {isPlaying} {isPaused} {onPlayPause} {onStop} />
			</div>
		</div>
	{:else}
		<p class="relative z-10 m-0 text-sm text-[var(--muted)]">Select an audio to start.</p>
	{/if}
</footer>
