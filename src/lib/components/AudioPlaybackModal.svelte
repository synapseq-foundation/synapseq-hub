<script lang="ts">
	import type { AudioEntry } from '../player/types.js'
	import CollapsibleText from "./CollapsibleText.svelte"
	import { getAudioDescription } from "../utils/spsq-parser.js"

	let { show = false, audio = null, onclose = null }: { show: boolean, audio: (AudioEntry & { artwork: string }) | null, onclose: (() => void) | null } = $props()

	let description = $state<string[]>([])
	let loading = $state(false)

	$effect(() => {
		if (show && audio?.path) {
			loading = true
			console.log('Fetching description for path:', audio.path)
			getAudioDescription(audio.path)
				.then((lines) => {
					console.log('Description lines:', lines)
					description = lines
					loading = false
				})
				.catch((err) => {
					console.error('Error fetching description:', err)
					description = []
					loading = false
				})
		} else {
			description = []
		}
	})

	function handleClose() {
		show = false
		if (onclose) onclose()
	}

	function handlePlay() {
		show = false
		if (onclose) onclose()
	}

	function handleOverlayClick(e: MouseEvent) {
		if (e.target === e.currentTarget) handleClose()
	}

	function handleOverlayKeydown(e: KeyboardEvent) {
		if (e.key === 'Escape') handleClose()
	}
</script>

{#if show && audio}
	<div class="fixed inset-0 z-50 flex items-center justify-center bg-[rgba(0,0,0,0.5)]" role="dialog" aria-modal="true" tabindex="-1" onclick={handleOverlayClick} onkeydown={handleOverlayKeydown}>
		<div class="relative rounded-2xl max-w-md w-full mx-4 p-6 max-h-[90vh] overflow-y-auto" style="background: var(--panel-strong); box-shadow: var(--shadow);">
			<button
				class="absolute top-4 left-4 hover:opacity-80 cursor-pointer"
				style="color: var(--muted);"
				onclick={handleClose}
				aria-label="Close modal"
			>
				<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
				</svg>
			</button>

			<div class="flex flex-col items-center mt-8">
				{#if audio.artwork}
					<img
						src={audio.artwork}
						alt="Audio artwork"
						class="w-48 h-48 rounded-lg object-cover mb-4"
					/>
				{/if}

				{#if audio.author}
					<p class="text-sm mb-3" style="color: var(--muted);">created by {audio.author}</p>
				{/if}

				{#if loading}
					<p class="text-sm" style="color: var(--muted);">Loading description...</p>
				{:else if description.length > 0}
					<div class="w-full mb-4">
						<CollapsibleText text={description.join("\n")} />
					</div>
				{/if}

				<div class="w-full rounded-lg p-4 mb-6" style="background: var(--panel);">
					<p class="text-sm mb-2" style="color: var(--text);">Listen in a calm environment without interruptions.</p>
					<p class="text-sm mb-2" style="color: var(--text);">Focus on your breathing and try not to think about random things.</p>
					<p class="text-sm" style="color: var(--text);">Enjoy the experience!</p>
				</div>
			</div>

			<div class="flex gap-3">
				<button
					class="flex-1 py-3 px-4 rounded-lg cursor-pointer"
					style="background: var(--panel); color: var(--text); border: 1px solid var(--line);"
					onmouseenter={(e) => e.currentTarget.style.background = 'var(--panel-strong)'}
					onmouseleave={(e) => e.currentTarget.style.background = 'var(--panel)'}
					onclick={handleClose}
				>
					Cancel
				</button>
				<button
					class="flex-1 py-3 px-4 rounded-lg font-semibold cursor-pointer"
					style="background: var(--accent); color: white;"
					onmouseenter={(e) => e.currentTarget.style.background = 'var(--accent-strong)'}
					onmouseleave={(e) => e.currentTarget.style.background = 'var(--accent)'}
					onclick={handlePlay}
				>
					PLAY!
				</button>
			</div>
		</div>
	</div>
{/if}
