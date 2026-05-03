<script lang="ts">
	import { Moon, Sun } from '@lucide/svelte';
	import { defaultArtwork } from '$lib/player/constants';
	import type { Theme } from '$lib/player/types';

	type Props = {
		theme: Theme;
		onToggleTheme: () => void;
	};

	let { theme, onToggleTheme }: Props = $props();
</script>

<header
	class="grid grid-cols-[auto_1fr_auto] items-center gap-3.5 rounded-3xl border-b border-[var(--line)] bg-white/90 p-3.5 sm:p-[18px] backdrop-blur-sm dark:bg-black/90"
>
	<img
		src={defaultArtwork}
		alt="SynapSeq"
		class="h-[46px] w-[46px] rounded-2xl border border-[var(--line-strong)] object-cover"
	/>
	<h1 id="player-title" class="m-0 text-[clamp(1.35rem,5vw,2.1rem)] font-[760] tracking-[-0.04em]">
		Hub Player
	</h1>
	<button
		class="inline-flex h-11 w-11 cursor-pointer items-center justify-center rounded-full border border-[var(--line)] bg-[var(--panel-strong)] text-[var(--text)] transition duration-150 hover:-translate-y-px hover:border-[var(--line-strong)] hover:bg-[var(--accent-soft)]"
		type="button"
		onclick={onToggleTheme}
		aria-label="Toggle theme"
	>
		{#if theme === 'dark'}
			<Sun size={20} />
		{:else}
			<Moon size={20} />
		{/if}
	</button>
</header>
