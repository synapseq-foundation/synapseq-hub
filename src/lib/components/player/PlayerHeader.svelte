<script lang="ts">
	import { Moon, Sun } from '@lucide/svelte';
	import { defaultArtwork } from '$lib/player/constants';
	import type { Theme } from '$lib/player/types';

	type Props = {
		theme: Theme;
		onToggleTheme: () => void;
		compact?: boolean;
		categoryBorderClass?: string;
		categoryBgGradientClass?: string;
	};

	let {
		theme,
		onToggleTheme,
		compact = false,
		categoryBorderClass = '',
		categoryBgGradientClass = ''
	}: Props = $props();
</script>

<header
	class={[
		'fixed left-0 right-0 z-50 mx-auto transition-all duration-300 ease-in-out',
		compact
			? 'top-[calc(0.5rem+env(safe-area-inset-top,0px))] w-[min(calc(100%-24px),480px)] px-2.5'
			: 'top-0 w-full px-2.5 pt-[calc(0.75rem+env(safe-area-inset-top,0px))] sm:px-4'
	]}
>
	<div
		class={[
			'grid items-center gap-3 border border-[var(--line)] bg-[var(--panel-strong)] backdrop-blur-xl transition-all duration-300 ease-in-out sm:gap-4',
			compact
				? 'grid-cols-[auto_1fr_auto] rounded-full px-3 py-1.5 shadow-[0_4px_24px_rgba(0,0,0,0.13)]'
				: 'grid-cols-[auto_1fr_auto] rounded-2xl px-3.5 py-2.5 shadow-[0_2px_16px_rgba(0,0,0,0.07)] sm:rounded-3xl sm:px-5 sm:py-3',
			categoryBgGradientClass
		]}
	>
		<!-- Logo -->
		<div class="relative shrink-0">
			<div
				class={[
					'absolute inset-0 bg-[var(--accent-soft)] blur-[6px] transition-all duration-300',
					compact ? 'rounded-full' : 'rounded-xl'
				]}
			></div>
			<img
				src={defaultArtwork}
				alt="SynapSeq"
				class={[
					'relative border border-[var(--line-strong)] object-cover shadow-sm transition-all duration-300',
					compact
						? 'h-[30px] w-[30px] rounded-full'
						: 'h-[42px] w-[42px] rounded-xl sm:h-[46px] sm:w-[46px] sm:rounded-2xl'
				]}
			/>
		</div>

		<!-- Title + subtitle -->
		<div class="grid min-w-0 gap-0">
			<h1
				id="player-title"
				class={[
					'm-0 truncate font-[780] leading-tight tracking-[-0.04em] text-[var(--text)] transition-all duration-300',
					compact ? 'text-[0.95rem]' : 'text-[clamp(1.1rem,4.5vw,1.55rem)]'
				]}
			>
				Hub Player
			</h1>
			<span
				class={[
					'truncate font-[500] uppercase tracking-[0.12em] text-[var(--muted)] transition-all duration-300',
					compact ? 'text-[0.6rem] opacity-0 h-0 overflow-hidden' : 'text-[0.7rem] sm:text-[0.72rem]'
				]}
			>
				SynapSeq
			</span>
		</div>

		<!-- Theme toggle -->
		<button
			class={[
				'inline-flex shrink-0 cursor-pointer items-center justify-center rounded-full border border-[var(--line)] bg-[var(--panel-strong)] text-[var(--text)] shadow-sm transition-all duration-150 hover:-translate-y-px hover:border-[var(--accent-soft)] hover:bg-[var(--accent-soft)] hover:text-[var(--accent)] active:scale-95',
				compact ? 'h-8 w-8' : 'h-10 w-10'
			]}
			type="button"
			onclick={onToggleTheme}
			aria-label="Toggle theme"
		>
			{#if theme === 'dark'}
				<Sun size={compact ? 15 : 18} />
			{:else}
				<Moon size={compact ? 15 : 18} />
			{/if}
		</button>
	</div>
</header>
