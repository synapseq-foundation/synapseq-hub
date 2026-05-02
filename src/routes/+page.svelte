<script lang="ts">
	import { onMount } from 'svelte';

	onMount(() => {
		setTimeout(() => {
			window.location.href = 'https://synapseq.org';
		}, 3000);
	});
</script>

<p>Redirecting to <a href="https://synapseq.org">SynapSeq</a>...</p>
