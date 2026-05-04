<script lang="ts">
	import { Moon, Sun } from '@lucide/svelte';
	import { defaultArtwork } from '$lib/player/constants';
	import type { Theme } from '$lib/player/types';

	type Props = {
		theme: Theme;
		onToggleTheme: () => void;
		categoryBorderClass?: string;
		categoryBgGradientClass?: string;
	};

	let {
		theme,
		onToggleTheme,
		categoryBorderClass = '',
		categoryBgGradientClass = ''
	}: Props = $props();
</script>

<header
	class="sticky top-0 z-50 grid grid-cols-[auto_1fr_auto] items-center gap-3 rounded-2xl border border-[var(--line)] bg-[var(--panel-strong)] px-3.5 py-2.5 shadow-[0_2px_16px_rgba(0,0,0,0.07)] backdrop-blur-xl transition-colors duration-300 ease-in-out sm:gap-4 sm:rounded-3xl sm:px-5 sm:py-3 {categoryBgGradientClass}"
>
	<!-- Logo -->
	<div class="relative">
		<div class="absolute inset-0 rounded-xl bg-[var(--accent-soft)] blur-[6px]"></div>
		<img
			src={defaultArtwork}
			alt="SynapSeq"
			class="relative h-[42px] w-[42px] rounded-xl border border-[var(--line-strong)] object-cover shadow-sm sm:h-[46px] sm:w-[46px] sm:rounded-2xl"
		/>
	</div>

	<!-- Title + subtitle -->
	<div class="grid min-w-0 gap-0">
		<h1
			id="player-title"
			class="m-0 truncate text-[clamp(1.1rem,4.5vw,1.55rem)] font-[780] leading-tight tracking-[-0.04em] text-[var(--text)]"
		>
			Hub Player
		</h1>
		<span class="truncate text-[0.7rem] font-[500] uppercase tracking-[0.12em] text-[var(--muted)] sm:text-[0.72rem]">
			SynapSeq
		</span>
	</div>

	<!-- Theme toggle -->
	<button
		class="inline-flex h-10 w-10 cursor-pointer items-center justify-center rounded-full border border-[var(--line)] bg-[var(--panel-strong)] text-[var(--text)] shadow-sm transition-all duration-150 hover:-translate-y-px hover:border-[var(--accent-soft)] hover:bg-[var(--accent-soft)] hover:text-[var(--accent)] active:scale-95"
		type="button"
		onclick={onToggleTheme}
		aria-label="Toggle theme"
	>
		{#if theme === 'dark'}
			<Sun size={18} />
		{:else}
			<Moon size={18} />
		{/if}
	</button>
</header>
