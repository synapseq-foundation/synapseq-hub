<script lang="ts">
	type Props = {
		categories: string[];
		selectedCategory: string;
		onSelectCategory: (category: string) => void;
	};

	let { categories, selectedCategory, onSelectCategory }: Props = $props();
</script>

<nav class="scrollbar-none flex gap-2.5 overflow-x-auto px-3.5 pt-3.5 pb-2 sm:px-[18px] sm:pt-[18px]" aria-label="Audio categories">
	{#each categories as category (category)}
		<button
			type="button"
			class={[
				'flex-none cursor-pointer rounded-full border px-[15px] py-[9px]',
				selectedCategory === category
					? 'border-transparent bg-[var(--accent-soft)] font-bold text-[var(--accent-strong)]'
					: 'border-[var(--line)] bg-[var(--panel-strong)] text-[var(--muted)]'
			]}
			onclick={() => onSelectCategory(category)}
		>
			{category}
		</button>
	{/each}
</nav>
