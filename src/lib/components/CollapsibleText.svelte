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
		class="text-gray-300 text-sm leading-relaxed whitespace-pre-wrap"
		class:line-clamp-3={!expanded && isLong}
	>
		{text}
	</div>
	{#if isLong}
		<button
			class="text-blue-400 hover:text-blue-300 text-sm mt-1 cursor-pointer"
			onclick={() => expanded = !expanded}
		>
			{expanded ? "Collapse" : "Expand"}
		</button>
	{/if}
</div>
