<script lang="ts">
	import { Play, Pause, Square } from '@lucide/svelte';

	type Props = {
		isPlaying: boolean;
		isPaused: boolean;
		onPlayPause: () => void;
		onStop: () => void;
	};

	let { isPlaying, isPaused, onPlayPause, onStop }: Props = $props();

	let hasSession = $derived(isPlaying || isPaused);
</script>

<div class="flex items-center gap-2">
	<!-- Stop — only active when a session is ongoing -->
	<button
		type="button"
		class={[
			'inline-flex h-10 w-10 shrink-0 cursor-pointer items-center justify-center rounded-full border transition-all duration-150 active:scale-90',
			hasSession
				? 'border-[var(--line-strong)] bg-[var(--panel-strong)] text-[var(--text)] hover:border-[var(--accent-soft)] hover:bg-[var(--accent-soft)] hover:text-[var(--accent)]'
				: 'cursor-not-allowed border-[var(--line)] bg-transparent text-[var(--off)] opacity-40'
		]}
		onclick={onStop}
		disabled={!hasSession}
		aria-label="Stop"
	>
		<Square size={15} fill="currentColor" />
	</button>

	<!-- Play / Pause -->
	<button
		type="button"
		class="relative z-10 inline-flex h-11 w-11 shrink-0 cursor-pointer items-center justify-center gap-2 rounded-full border border-transparent bg-[var(--accent)] text-[#fffaf1] shadow-[0_2px_12px_rgba(177,77,42,0.4)] transition-all duration-150 hover:-translate-y-px hover:bg-[var(--accent-strong)] hover:shadow-[0_4px_16px_rgba(177,77,42,0.5)] active:scale-95 sm:h-12 sm:w-auto sm:min-w-[108px] sm:rounded-full sm:px-5"
		onclick={onPlayPause}
		aria-label={isPlaying ? 'Pause' : isPaused ? 'Resume' : 'Play'}
	>
		{#if isPlaying}
			<Pause size={18} fill="currentColor" />
			<span class="hidden text-[0.85rem] font-[660] sm:block">Pause</span>
		{:else if isPaused}
			<Play size={18} fill="currentColor" />
			<span class="hidden text-[0.85rem] font-[660] sm:block">Resume</span>
		{:else}
			<Play size={18} fill="currentColor" />
			<span class="hidden text-[0.85rem] font-[660] sm:block">Play</span>
		{/if}
	</button>
</div>
