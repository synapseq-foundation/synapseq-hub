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

<div class="flex items-center gap-2 px-3.5 pb-2 pt-3 sm:gap-2.5 sm:px-5 sm:pt-4">
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

	<!-- Clear favorites button — only when Favorites is selected and has items -->
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
