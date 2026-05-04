<script lang="ts">
	let { text = "" }: { text?: string } = $props()

	let expanded = $state(false)
	let textElement: HTMLDivElement | null = $state(null)
	let isLong = $state(false)

	$effect(() => {
		if (textElement) {
			const lineHeight = parseFloat(getComputedStyle(textElement).lineHeight)
			const height = textElement.scrollHeight
			isLong = height > lineHeight * 3
		}
	})
</script>

<div class="relative">
	<div
		bind:this={textElement}
		class="leading-relaxed whitespace-pre-wrap"
		class:line-clamp-3={!expanded && isLong}
		style="font-size: 1rem; color: var(--text);"
	>
		{text}
	</div>
	{#if isLong}
		<button
			class="text-sm mt-1 cursor-pointer"
			style="color: var(--accent);"
			onmouseenter={(e) => e.currentTarget.style.opacity = '0.8'}
			onmouseleave={(e) => e.currentTarget.style.opacity = '1'}
			onclick={() => expanded = !expanded}
		>
			{expanded ? "Collapse" : "Expand"}
		</button>
	{/if}
</div>
