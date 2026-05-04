<script lang="ts">
	let { text = "" }: { text?: string } = $props()
</script>

<div class="custom-scroll overflow-y-auto max-h-[120px] pr-2">
	<p class="leading-relaxed whitespace-pre-wrap" style="font-size: 1rem; color: var(--text);">
		{text}
	</p>
</div>

<style>
	.custom-scroll::-webkit-scrollbar {
		width: 6px;
	}

	.custom-scroll::-webkit-scrollbar-track {
		background: var(--panel);
		border-radius: 3px;
	}

	.custom-scroll::-webkit-scrollbar-thumb {
		background: var(--line-strong);
		border-radius: 3px;
	}

	.custom-scroll::-webkit-scrollbar-thumb:hover {
		background: var(--muted);
	}
</style>
