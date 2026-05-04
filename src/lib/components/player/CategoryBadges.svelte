<script lang="ts">
	import { Layers, Heart, Zap, Moon, Waves, Trash2 } from '@lucide/svelte';

	type Props = {
		categories: string[];
		selectedCategory: string;
		hasFavorites: boolean;
		onSelectCategory: (category: string) => void;
		onClearFavorites: () => void;
	};

	let { categories, selectedCategory, hasFavorites, onSelectCategory, onClearFavorites }: Props = $props();

	const categoryIcons: Record<string, typeof Layers> = {
		All: Layers,
		Favorites: Heart,
		Focus: Zap,
		Meditation: Moon,
		Relaxation: Waves
	};

	function getIcon(category: string) {
		return categoryIcons[category] ?? Layers;
	}

	let showClear = $derived(selectedCategory === 'Favorites' && hasFavorites);
</script>

<!--
  Mobile: horizontal scrollable strip (unchanged behaviour)
  Desktop (lg+): vertical floating panel — full list stacked
-->

<!-- Mobile layout -->
<div class="flex items-center gap-2 px-3.5 pb-2 pt-3 sm:gap-2.5 sm:px-5 sm:pt-4 lg:hidden">
	<nav
		class="scrollbar-none flex flex-1 gap-2 overflow-x-auto sm:gap-2.5"
		aria-label="Audio categories"
	>
		{#each categories as category (category)}
			{@const Icon = getIcon(category)}
			{@const active = selectedCategory === category}
			<button
				type="button"
				class={[
					'flex flex-none cursor-pointer items-center gap-1.5 rounded-full border px-3.5 py-[8px] text-[0.82rem] font-[560] transition-all duration-200 active:scale-95 sm:px-4 sm:py-[9px] sm:text-[0.85rem]',
					active
						? 'border-transparent bg-[var(--accent)] text-[#fffaf1] shadow-[0_2px_10px_rgba(177,77,42,0.35)]'
						: 'border-[var(--line)] bg-[var(--panel-strong)] text-[var(--muted)] hover:border-[var(--line-strong)] hover:text-[var(--text)]'
				]}
				onclick={() => onSelectCategory(category)}
			>
				<Icon size={13} strokeWidth={active ? 2.5 : 2} />
				{category}
			</button>
		{/each}
	</nav>

	{#if showClear}
		<button
			type="button"
			class="flex shrink-0 cursor-pointer items-center gap-1.5 rounded-full border border-[var(--line)] bg-[var(--panel-strong)] px-3 py-[8px] text-[0.82rem] font-[560] text-[var(--muted)] transition-all duration-200 hover:border-[var(--danger)] hover:bg-[var(--danger)]/10 hover:text-[var(--danger)] active:scale-95 sm:py-[9px] sm:text-[0.85rem]"
			onclick={onClearFavorites}
			aria-label="Clear all favorites"
			title="Clear all favorites"
		>
			<Trash2 size={13} />
			<span class="hidden sm:inline">Clear all</span>
		</button>
	{/if}
</div>

<!-- Desktop sidebar layout -->
<div class="hidden lg:block">
	<div
		class="rounded-2xl border border-[var(--line)] bg-[var(--panel-strong)] px-3 py-3.5 shadow-[0_2px_16px_rgba(0,0,0,0.06)] backdrop-blur-xl"
	>
		<p class="mb-2.5 px-1 text-[0.68rem] font-[640] uppercase tracking-[0.14em] text-[var(--muted)]">
			Categories
		</p>

		<nav class="flex flex-col gap-1" aria-label="Audio categories">
			{#each categories as category (category)}
				{@const Icon = getIcon(category)}
				{@const active = selectedCategory === category}
				<button
					type="button"
					class={[
						'flex w-full cursor-pointer items-center gap-2.5 rounded-xl border px-3 py-2.5 text-[0.83rem] font-[560] transition-all duration-200 active:scale-[0.98] text-left',
						active
							? 'border-transparent bg-[var(--accent)] text-[#fffaf1] shadow-[0_2px_10px_rgba(177,77,42,0.28)]'
							: 'border-transparent bg-transparent text-[var(--muted)] hover:bg-[var(--line)] hover:text-[var(--text)]'
					]}
					onclick={() => onSelectCategory(category)}
				>
					<Icon size={14} strokeWidth={active ? 2.5 : 2} class="shrink-0" />
					{category}
				</button>
			{/each}
		</nav>

		{#if showClear}
			<div class="mt-3 border-t border-[var(--line)] pt-3">
				<button
					type="button"
					class="flex w-full cursor-pointer items-center gap-2.5 rounded-xl border border-transparent px-3 py-2.5 text-[0.83rem] font-[560] text-[var(--muted)] transition-all duration-200 hover:border-[var(--danger)]/30 hover:bg-[var(--danger)]/8 hover:text-[var(--danger)] active:scale-[0.98]"
					onclick={onClearFavorites}
					aria-label="Clear all favorites"
				>
					<Trash2 size={14} class="shrink-0" />
					Clear favorites
				</button>
			</div>
		{/if}
	</div>
</div>
