<script lang="ts">
	import { Layers, Heart, Zap, Moon, Waves } from '@lucide/svelte';

	type Props = {
		categories: string[];
		selectedCategory: string;
		onSelectCategory: (category: string) => void;
	};

	let { categories, selectedCategory, onSelectCategory }: Props = $props();

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
</script>

<nav
	class="scrollbar-none flex gap-2 overflow-x-auto px-3.5 pb-2 pt-3 sm:gap-2.5 sm:px-5 sm:pt-4"
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
